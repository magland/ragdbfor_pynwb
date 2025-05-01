# Extracellular Electrophysiology Data in PyNWB

This document provides a tutorial on storing extracellular electrophysiology data in NWB using PyNWB. The process involves four main steps:

1. Creating the electrodes table
2. Adding acquired raw voltage data
3. Adding LFP data
4. Adding spike data

## Creating NWB Files

First, initialize an NWB file:

```python
from datetime import datetime
from uuid import uuid4
import numpy as np
from dateutil.tz import tzlocal
from pynwb import NWBHDF5IO, NWBFile
from pynwb.ecephys import LFP, ElectricalSeries, SpikeEventSeries
from pynwb.misc import DecompositionSeries

nwbfile = NWBFile(
    session_description="my first synthetic recording",
    identifier=str(uuid4()),
    session_start_time=datetime.now(tzlocal()),
    experimenter=["Baggins, Bilbo"],
    lab="Bag End Laboratory",
    institution="University of Middle Earth at the Shire",
    experiment_description="I went on an adventure to reclaim vast treasures.",
    keywords=["ecephys", "exploration", "wanderlust"],
    related_publications="doi:10.1016/j.neuron.2016.12.011",
)
```

## Electrodes Table

1. First, define a device:

```python
device = nwbfile.create_device(
    name="array",
    description="A 12-channel array with 4 shanks and 3 channels per shank",
    manufacturer="Array Technologies",
    model_number="PRB_1_4_0480_123",
    model_name="Neurovoxels 0.99",
    serial_number="1234567890",
)
```

2. Create electrode groups and add electrodes to the table:

```python
nwbfile.add_electrode_column(name="label", description="label of electrode")

nshanks = 4
nchannels_per_shank = 3
electrode_counter = 0

for ishank in range(nshanks):
    electrode_group = nwbfile.create_electrode_group(
        name="shank{}".format(ishank),
        description="electrode group for shank {}".format(ishank),
        device=device,
        location="brain area",
    )
    for ielec in range(nchannels_per_shank):
        nwbfile.add_electrode(
            group=electrode_group,
            label="shank{}elec{}".format(ishank, ielec),
            location="brain area",
        )
        electrode_counter += 1
```

3. Create an electrode table region:

```python
all_table_region = nwbfile.create_electrode_table_region(
    region=list(range(electrode_counter)),
    description="all electrodes",
)
```

## Raw Voltage Data

Add raw voltage data using ElectricalSeries:

```python
raw_data = np.random.randn(50, 12)
raw_electrical_series = ElectricalSeries(
    name="ElectricalSeries",
    description="Raw acquisition traces",
    data=raw_data,
    electrodes=all_table_region,
    starting_time=0.0,
    rate=20000.0,  # in Hz
)

nwbfile.add_acquisition(raw_electrical_series)
```

## LFP Data

Add LFP data:

```python
lfp_data = np.random.randn(50, 12)
lfp_electrical_series = ElectricalSeries(
    name="ElectricalSeries",
    description="LFP data",
    data=lfp_data,
    filtering='Low-pass filter at 300 Hz',
    electrodes=all_table_region,
    starting_time=0.0,
    rate=200.0,
)

lfp = LFP(electrical_series=lfp_electrical_series)

ecephys_module = nwbfile.create_processing_module(
    name="ecephys", description="processed extracellular electrophysiology data"
)
ecephys_module.add(lfp)
```

## Filtered Electrophysiology Data

For storing data filtered for specific frequency bands:

```python
from pynwb.ecephys import FilteredEphys

filtered_data = np.random.randn(50, 12)
filtered_electrical_series = ElectricalSeries(
    name="FilteredElectricalSeries",
    description="Filtered data",
    data=filtered_data,
    filtering='Band-pass filtered between 4 and 8 Hz',
    electrodes=all_table_region,
    starting_time=0.0,
    rate=200.0,
)

filtered_ephys = FilteredEphys(electrical_series=filtered_electrical_series)
ecephys_module.add(filtered_ephys)
```

## Spectral Decomposition

Store results from spectral analyses:

```python
bands = dict(theta=(4.0, 12.0), 
             beta=(12.0, 30.0), 
             gamma=(30.0, 80.0))
phase_data = np.random.randn(50, 12, len(bands))

decomp_series = DecompositionSeries(
    name="theta",
    description="phase of bandpass filtered LFP data",
    data=phase_data,
    metric='phase',
    rate=200.0,
    source_channels=all_table_region,
    source_timeseries=lfp_electrical_series,
)

for band_name, band_limits in bands.items():
    decomp_series.add_band(
        band_name=band_name,
        band_limits=band_limits,
    )

ecephys_module.add(decomp_series)
```

## Sorted Spike Times

Add columns and units to the Units table:

```python
nwbfile.add_unit_column(name="quality", description="sorting quality")

firing_rate = 20
n_units = 10
res = 1000
duration = 20
for n_units_per_shank in range(n_units):
    spike_times = np.where(np.random.rand((res * duration)) < (firing_rate / res))[0] / res
    nwbfile.add_unit(spike_times=spike_times, quality="good")
```

## Unsorted Spike Times

Store unsorted spike events:

```python
spike_snippets = np.random.rand(40, 3, 30)  # 40 events, 3 channels, 30 samples per event
shank0 = nwbfile.create_electrode_table_region(
    region=[0, 1, 2],
    description="shank0",
)

spike_events = SpikeEventSeries(
    name='SpikeEvents_Shank0',
    description="events detected with 100uV threshold",
    data=spike_snippets,
    timestamps=np.arange(40).astype(float),
    electrodes=shank0,
)
nwbfile.add_acquisition(spike_events)
```

## Event Detection and Feature Extraction

```python
from pynwb.ecephys import EventDetection

event_detection = EventDetection(
    name="threshold_events",
    detection_method="thresholding, 1.5 * std",
    source_electricalseries=raw_electrical_series,
    source_idx=[1000, 2000, 3000],
    times=[.033, .066, .099],
)
ecephys_module.add(event_detection)

from pynwb.ecephys import FeatureExtraction

feature_extraction = FeatureExtraction(
    name="PCA_features",
    electrodes=all_table_region,
    description=["PC1", "PC2", "PC3", "PC4"],
    times=[.033, .066, .099],
    features=np.random.rand(3, 12, 4),  # time, channel, feature
)
ecephys_module.add(feature_extraction)
```

## Writing and Reading Data

Write the file:

```python
with NWBHDF5IO("ecephys_tutorial.nwb", "w") as io:
    io.write(nwbfile)
```

Read the file:

```python
with NWBHDF5IO("ecephys_tutorial.nwb", "r") as io:
    read_nwbfile = io.read()
    # Access raw data
    raw_data = read_nwbfile.acquisition["ElectricalSeries"]
    # Access LFP data
    lfp_data = read_nwbfile.processing["ecephys"]["LFP"]["ElectricalSeries"]
    
    # Read specific data regions
    lfp_subset = lfp_data.data[:10, :3]
    spike_times = read_nwbfile.units["spike_times"][0]
```

Note: Data arrays are read passively—the `data` attribute returns an h5py.Dataset object that can be indexed to read specific portions of data.