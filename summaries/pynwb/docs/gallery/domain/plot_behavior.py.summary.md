# Behavior Data in PyNWB

## Overview
This document explains how to use the `pynwb.behavior` module to store and access behavioral data in an NWBFile. The workflow for adding behavior data follows these general steps:

1. Create a data object (TimeSeries, SpatialSeries, IntervalSeries, or TimeIntervals)
2. Store that object in an appropriate behavior interface object
3. Add the behavior interface to a behavior processing module in the NWBFile

## Basic Usage

```python
from pynwb import NWBFile, TimeSeries, NWBHDF5IO
from pynwb.behavior import (
    SpatialSeries, Position, CompassDirection, BehavioralTimeSeries,
    BehavioralEvents, BehavioralEpochs, PupilTracking, EyeTracking
)
from pynwb.misc import IntervalSeries
from pynwb.epoch import TimeIntervals
import numpy as np
```

### Create NWBFile
```python
nwbfile = NWBFile(
    session_description="my first synthetic recording",
    identifier=str(uuid4()),
    session_start_time=datetime.now(tzlocal()),
    experimenter=["Baggins, Bilbo"],
    lab="Bag End Laboratory"
)
```

### Adding Position Data

```python
# Create position data (x, y) over time
position_data = np.array([np.linspace(0, 10, 50), np.linspace(0, 8, 50)]).T
timestamps = np.linspace(0, 50) / 200

# Create SpatialSeries
position_spatial_series = SpatialSeries(
    name="SpatialSeries",
    description="Position (x, y) in an open field.",
    data=position_data,
    timestamps=timestamps,
    reference_frame="(0,0) is bottom left corner",
)

# Create Position interface
position = Position(spatial_series=position_spatial_series)

# Create behavior module and add position
behavior_module = nwbfile.create_processing_module(
    name="behavior", description="Processed behavioral data"
)
behavior_module.add(position)
```

### Adding Direction Data

```python
view_angle_data = np.linspace(0, 4, 50)
direction_spatial_series = SpatialSeries(
    name="SpatialSeries",
    description="View angle of the subject measured in radians.",
    data=view_angle_data,
    timestamps=timestamps,
    reference_frame="straight ahead",
    unit="radians",
)

direction = CompassDirection(
    spatial_series=direction_spatial_series, name="CompassDirection"
)
behavior_module.add(direction)
```

### Adding Continuous Behavior Data

```python
speed_data = np.linspace(0, 0.4, 50)
speed_time_series = TimeSeries(
    name="speed",
    data=speed_data,
    timestamps=timestamps,
    description="The speed of the subject measured over time.",
    unit="m/s",
)

behavioral_time_series = BehavioralTimeSeries(
    time_series=speed_time_series,
    name="BehavioralTimeSeries",
)
behavior_module.add(behavioral_time_series)
```

### Adding Behavioral Events

```python
reward_amount = [1.0, 1.5, 1.0, 1.5]
events_timestamps = [1.0, 2.0, 5.0, 6.0]

time_series = TimeSeries(
    name="lever_presses",
    data=reward_amount,
    timestamps=events_timestamps,
    description="The water amount the subject received as a reward.",
    unit="ml",
)

behavioral_events = BehavioralEvents(time_series=time_series, name="BehavioralEvents")
behavior_module.add(behavioral_events)
```

### Adding Behavioral Epochs/Intervals

```python
# Using IntervalSeries
run_intervals = IntervalSeries(
    name="running",
    description="Intervals when the animal was running.",
    data=[1, -1, 1, -1, 1, -1],  # 1 marks start, -1 marks end
    timestamps=[0.5, 1.5, 3.5, 4.0, 7.0, 7.3],
)

behavioral_epochs = BehavioralEpochs(name="BehavioralEpochs")
behavioral_epochs.add_interval_series(run_intervals)
behavior_module.add(behavioral_epochs)

# Using TimeIntervals (preferred)
sleep_intervals = TimeIntervals(
    name="sleep_intervals",
    description="Intervals when the animal was sleeping.",
)
sleep_intervals.add_column(name="stage", description="The stage of sleep.")
sleep_intervals.add_row(start_time=0.3, stop_time=0.35, stage=1)
sleep_intervals.add_row(start_time=0.7, stop_time=0.9, stage=2)
nwbfile.add_time_intervals(sleep_intervals)
```

### Adding Eye Tracking Data

```python
# Pupil size tracking
pupil_diameter = TimeSeries(
    name="pupil_diameter",
    description="Pupil diameter extracted from the video of the right eye.",
    data=np.linspace(0.001, 0.002, 50),
    timestamps=timestamps,
    unit="meters",
)
pupil_tracking = PupilTracking(time_series=pupil_diameter, name="PupilTracking")
behavior_module.add(pupil_tracking)

# Gaze direction
right_eye_positions = SpatialSeries(
    name="right_eye_position",
    description="The position of the right eye measured in degrees.",
    data=np.linspace(-20, 30, 50),
    timestamps=timestamps,
    reference_frame="bottom left",
    unit="degrees",
)
eye_tracking = EyeTracking(name="EyeTracking", spatial_series=right_eye_positions)
behavior_module.add(eye_tracking)
```

## Writing and Reading NWB Files

### Write the file
```python
with NWBHDF5IO("behavioral_tutorial.nwb", "w") as io:
    io.write(nwbfile)
```

### Read the file
```python
with NWBHDF5IO("behavioral_tutorial.nwb", "r") as io:
    read_nwbfile = io.read()
    behavior_module = read_nwbfile.processing["behavior"]
    
    # Access data
    position_data = read_nwbfile.processing["behavior"]["Position"]["SpatialSeries"].data[:]
    
    # Access specific slices
    first_two_positions = read_nwbfile.processing["behavior"]["Position"]["SpatialSeries"].data[:2]
```