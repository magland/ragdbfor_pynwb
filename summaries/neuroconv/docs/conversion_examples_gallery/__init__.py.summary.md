# PyNWB: NWB Standard API for Python

## Overview
PyNWB provides an API for working with Neurodata Without Borders (NWB) files in Python. NWB is a data standard for neurophysiology, providing a standardized format for storing experimental data and metadata.

## Installation
```
pip install pynwb
```
For development:
```
pip install -e .
```

## Core Concepts

### NWBFile
Core class representing an NWB file with methods to add data.
```python
from datetime import datetime
from pynwb import NWBFile

nwbfile = NWBFile(
    session_description='my first synthetic recording',
    identifier='EXAMPLE_ID',
    session_start_time=datetime.now(),
    experimenter='Dr. Bilbo Baggins',
    lab='Bag End Laboratory',
    institution='University of Middle Earth',
    experiment_description='I went on an adventure with thirteen dwarves to reclaim vast treasures.'
)
```

### Reading/Writing Files
```python
from pynwb import NWBHDF5IO

# Write
with NWBHDF5IO('test_nwb.nwb', 'w') as io:
    io.write(nwbfile)

# Read
with NWBHDF5IO('test_nwb.nwb', 'r') as io:
    nwbfile_in = io.read()
```

### Working with Timeseries Data
TimeSeries is the core class for storing time-series data:
```python
from pynwb.base import TimeSeries
import numpy as np

data = list(range(100, 200, 10))
timestamps = list(range(10))
test_ts = TimeSeries(
    name='test_timeseries',
    data=data,
    unit='m',
    timestamps=timestamps
)
nwbfile.add_acquisition(test_ts)
```

### Subject Information
```python
from pynwb.file import Subject

subject = Subject(
    subject_id='001',
    age='P90D',
    description='mouse 001',
    species='Mus musculus',
    sex='M'
)
nwbfile.subject = subject
```

### Trials
```python
nwbfile.add_trial(start_time=0.0, stop_time=2.0, condition='stim')
nwbfile.add_trial(start_time=3.0, stop_time=5.0, condition='no_stim')
```

### Processing Modules
```python
behavior_module = nwbfile.create_processing_module('behavior', 'Contains behavioral data')

from pynwb.behavior import BehavioralTimeSeries, BehavioralEvents
behavioral_ts = BehavioralTimeSeries(name='behavioral_ts', data=data, timestamps=timestamps, unit='m')
behavioral_events = BehavioralEvents(name='behavioral_events')

behavior_module.add(behavioral_ts)
behavior_module.add(behavioral_events)
```

### Epochs
```python
nwbfile.add_epoch(start_time=0.0, stop_time=6.0, tags=['example_epoch'])
```

### Electrodes and Electrode Groups
```python
from pynwb.ecephys import ElectrodeGroup

device = nwbfile.create_device(name='array')
electrode_group = ElectrodeGroup(
    name='electrode_group',
    description='my electrodes',
    location='brain area',
    device=device
)
nwbfile.add_electrode_group(electrode_group)

nwbfile.add_electrode(
    id=0,
    x=1.0, y=2.0, z=3.0,
    imp=300.,
    location='CA1',
    filtering='none',
    group=electrode_group
)
```

### LFP Data
```python
from pynwb.ecephys import LFP, ElectricalSeries

electrode_table_region = nwbfile.create_electrode_table_region([0], 'the first electrode')
ephys_ts = ElectricalSeries(
    name='test_ephys_data',
    data=[0.1, 0.2, 0.3, 0.4, 0.5],
    electrodes=electrode_table_region,
    timestamps=[0.1, 0.2, 0.3, 0.4, 0.5],
    unit='V'
)
lfp = LFP(electrical_series=ephys_ts)
ecephys_module = nwbfile.create_processing_module('ecephys', 'contains extracellular electrophysiology data')
ecephys_module.add(lfp)
```

### Optical Physiology
```python
from pynwb.ophys import TwoPhotonSeries, OpticalChannel

optical_channel = OpticalChannel('test_optical_channel', 'description', 500.)
imaging_plane = nwbfile.create_imaging_plane(
    name='test_imaging_plane',
    optical_channel=optical_channel,
    device=device,
    excitation_lambda=600.,
    indicator='GFP',
    location='brain',
    grid_spacing=[0.1, 0.1],
    grid_spacing_unit='meters'
)

two_p_series = TwoPhotonSeries(
    name='test_2p_series',
    data=np.ones((5, 10, 10)),
    imaging_plane=imaging_plane,
    rate=1.0,
    unit='normalized amplitude'
)
nwbfile.add_acquisition(two_p_series)
```

### ROIs and Segmentation
```python
from pynwb.ophys import ImageSegmentation, Fluorescence

mod = nwbfile.create_processing_module('ophys', 'contains optical physiology data')
img_seg = ImageSegmentation()
mod.add(img_seg)
ps = img_seg.create_plane_segmentation(
    name='plane_seg',
    description='plane segmentation',
    imaging_plane=imaging_plane
)

ps.add_roi(pixel_mask=np.array([[1, 2, 1.0], [3, 4, 1.0]]))
ps.add_roi(pixel_mask=np.array([[5, 6, 1.0], [7, 8, 1.0]]))

rt_region = ps.create_roi_table_region('all ROIs', region=[0, 1])

fl = Fluorescence()
mod.add(fl)
fl.create_roi_response_series(
    name='my_rrs',
    data=np.array([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]]),
    rois=rt_region,
    rate=1.0,
    unit='lumens'
)
```

## Extensions
PyNWB supports extending the NWB format with custom data types.
```python
from pynwb.spec import NWBNamespaceBuilder, NWBGroupSpec, NWBAttributeSpec

ext_source = 'myext.yaml'
ns_path = 'myext.namespace.yaml'

spec = NWBGroupSpec(
    neurodata_type_def='Extension',
    neurodata_type_inc='NWBDataInterface',
    attributes=[
        NWBAttributeSpec(
            name='my_attribute',
            dtype='text',
            doc='custom attribute'
        ),
    ],
    doc='My custom extension'
)

ns_builder = NWBNamespaceBuilder(
    doc='Extension for use in my lab',
    name='myext',
    version='0.1.0',
    author='Dr. Bilbo Baggins',
    contact='bilbo@bagend.com'
)
ns_builder.add_spec(ext_source, spec)
ns_builder.export(ns_path)
```