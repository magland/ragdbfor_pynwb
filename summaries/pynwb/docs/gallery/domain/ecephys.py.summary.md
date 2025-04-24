This document describes how to store extracellular electrophysiology data in NWB files using pynwb.

**1. Creating an NWBFile:**

First, create an `NWBFile` object. This requires metadata such as session description, identifier, and session start time.

```python
from datetime import datetime
from uuid import uuid4
from dateutil.tz import tzlocal
from pynwb import NWBHDF5IO, NWBFile

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

**2. Electrodes Table:**

Extracellular electrode information is stored in the `electrodes` table, a `DynamicTable`.  An `ElectrodeGroup` is required for each electrode. Creating an `ElectrodeGroup` requires a `Device`.

```python
device = nwbfile.create_device(
    name="array",
    description="A 12-channel array with 4 shanks and 3 channels per shank",
    manufacturer="Array Technologies",
    model_number="PRB_1_4_0480_123",
    model_name="Neurovoxels 0.99",
    serial_number="1234567890",
)

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

nwbfile.electrodes.to_dataframe() # convert to a pandas DataFrame to view it

```

**3. Extracellular Recordings (ElectricalSeries):**

Raw voltage traces and LFP data are stored as `ElectricalSeries` objects, subclasses of `TimeSeries`. You need to reference rows in the "electrodes" table using a `DynamicTableRegion`.

```python
all_table_region = nwbfile.create_electrode_table_region(
    region=list(range(electrode_counter)),  # reference row indices 0 to N-1
    description="all electrodes",
)

raw_data = np.random.randn(50, 12)
raw_electrical_series = ElectricalSeries(
    name="ElectricalSeries",
    description="Raw acquisition traces",
    data=raw_data,
    electrodes=all_table_region,
    starting_time=0.0,  # timestamp of the first sample in seconds relative to the session start time
    rate=20000.0,  # in Hz
)

nwbfile.add_acquisition(raw_electrical_series) #Add raw data to the acquisition group
```

**4. LFP Data:**

LFP data is also stored as an `ElectricalSeries`, usually placed inside an `LFP` object for organization.

```python
from pynwb.ecephys import LFP

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
ecephys_module.add(lfp) # Add LFP object to ecephys processing module
```

**5. FilteredEphys Data:**

Data filtered for frequency ranges other than LFP (e.g., Gamma or Theta) should be stored in an `ElectricalSeries` and encapsulated within a `FilteredEphys` object.

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

**6. DecompositionSeries:**

Further processed LFP data, like spectral decompositions, are stored using `DecompositionSeries`.

```python
from pynwb.misc import DecompositionSeries

bands = dict(theta=(4.0, 12.0),
             beta=(12.0, 30.0),
             gamma=(30.0, 80.0))  # in Hz
phase_data = np.random.randn(50, 12, len(bands))  # 50 samples, 12 channels, 3 frequency bands

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

**7. Sorted spike times (Units Table):**

Spike times are stored in the `Units` table, a subclass of `DynamicTable`.  Add custom columns for sorting quality using `nwbfile.add_unit_column`. Add spike data with `nwbfile.add_unit`.

```python
nwbfile.add_unit_column(name="quality", description="sorting quality")

firing_rate = 20
n_units = 10
res = 1000
duration = 20
for n_units_per_shank in range(n_units):
    spike_times = np.where(np.random.rand((res * duration)) < (firing_rate / res))[0] / res
    nwbfile.add_unit(spike_times=spike_times, quality="good")

nwbfile.units.to_dataframe()  # convert to a DataFrame to inspect
```

**8. Unsorted Spike Times:**

Unsorted spiking activity can be stored using `SpikeEventSeries` objects.

```python
from pynwb.ecephys import SpikeEventSeries

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

**9. EventDetection and FeatureExtraction:**

Use `EventDetection` to identify spike events in raw traces and `FeatureExtraction` to store spike features (e.g., principal components).

```python
from pynwb.ecephys import EventDetection, FeatureExtraction

event_detection = EventDetection(
    name="threshold_events",
    detection_method="thresholding, 1.5 * std",
    source_electricalseries=raw_electrical_series,
    source_idx=[1000, 2000, 3000],
    times=[.033, .066, .099],
)
ecephys_module.add(event_detection)

feature_extraction = FeatureExtraction(
    name="PCA_features",
    electrodes=all_table_region,
    description=["PC1", "PC2", "PC3", "PC4"],
    times=[.033, .066, .099],
    features=np.random.rand(3, 12, 4),  # time, channel, feature
)
ecephys_module.add(feature_extraction)
```

**10. Writing the NWB File:**

Use `NWBHDF5IO` to write the file.

```python
from pynwb import NWBHDF5IO

with NWBHDF5IO("ecephys_tutorial.nwb", "w") as io:
    io.write(nwbfile)
```

**11. Reading the NWB File:**

Use `NWBHDF5IO` to read the file.  Access data through `nwbfile.acquisition` and `nwbfile.processing`.

```python
with NWBHDF5IO("ecephys_tutorial.nwb", "r") as io:
    read_nwbfile = io.read()
    print(read_nwbfile.acquisition["ElectricalSeries"])
    print(read_nwbfile.processing["ecephys"])
    print(read_nwbfile.processing["ecephys"]["LFP"])
    print(read_nwbfile.processing["ecephys"]["LFP"]["ElectricalSeries"])

    print("section of LFP:")
    print(read_nwbfile.processing["ecephys"]["LFP"]["ElectricalSeries"].data[:10, :3])
    print("")
    print("spike times from 0th unit:")
    print(read_nwbfile.units["spike_times"][0])
```

Data is passively read, calling `.data` on a `TimeSeries` returns an `h5py.Dataset` object. Use indexing (e.g. `[:]`) to read data into memory.
