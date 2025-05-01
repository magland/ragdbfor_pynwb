# NWB File Basics

## Basic Concepts
- Each experiment session is represented by an `NWBFile` object
- `NWBFile` provides functionality for creating and retrieving:
  - TimeSeries datasets (time series data)
  - Processing Modules (for storing analyses)
  - Experiment metadata and data provenance

## TimeSeries
- Base class for all time series data in NWB
- Follows object-oriented inheritance pattern (specialized subtypes for different kinds of data)
- Main subtypes include:
  - Extracellular electrophysiology: `ElectricalSeries`, `SpikeEventSeries`
  - Intracellular electrophysiology: `PatchClampSeries` and its variants
  - Optical physiology/imaging: `ImageSeries` and its variants
  - Others: `OptogeneticSeries`, `SpatialSeries`, etc.

## Processing Modules
- Group common analyses done during data processing
- Hold data of different processing/analysis types
- Main analysis data types:
  - Behavior: `BehavioralEpochs`, `Position`, etc.
  - Electrophysiology: `EventDetection`, `LFP`, etc.
  - Optical physiology: `DfOverF`, `Fluorescence`, etc.

## NWBFile Usage

### Creating an NWBFile
```python
nwbfile = NWBFile(
    session_description="Mouse exploring an open field",  # required
    identifier=str(uuid4()),  # required
    session_start_time=session_start_time,  # required
    session_id="session_1234",  # optional
    experimenter=["Baggins, Bilbo"],  # optional
    lab="Bag End Laboratory"  # optional
    # other optional metadata
)
```

### Adding Subject Information
```python
subject = Subject(
    subject_id="001",
    age="P90D",  # ISO 8601 Duration format
    description="mouse 5",
    species="Mus musculus",
    sex="M"
)
nwbfile.subject = subject
```

### Working with TimeSeries
```python
# Creating a TimeSeries with regular sampling rate
ts_with_rate = TimeSeries(
    name="test_timeseries",
    description="an example time series",
    data=data,
    unit="m",
    starting_time=0.0,
    rate=1.0,
)

# Creating a TimeSeries with irregular sampling
ts_with_timestamps = TimeSeries(
    name="test_timeseries",
    description="an example time series",
    data=data,
    unit="m",
    timestamps=timestamps,
)

# Adding to NWBFile
nwbfile.add_acquisition(time_series_with_timestamps)

# Accessing the TimeSeries
nwbfile.acquisition["test_timeseries"]
# or
nwbfile.get_acquisition("test_timeseries")
```

### Specialized TimeSeries: AnnotationSeries
```python
annotations = AnnotationSeries(
    name='airpuffs',
    data=['Left Airpuff', 'Right Airpuff', 'Right Airpuff'],
    description='Airpuff events delivered to the animal',
    timestamps=[1.0, 3.0, 8.0],
)
nwbfile.add_stimulus(annotations)
```

### SpatialSeries and Position
```python
# Create SpatialSeries
spatial_series_obj = SpatialSeries(
    name="SpatialSeries",
    description="(x,y) position in open field",
    data=position_data,
    timestamps=position_timestamps,
    reference_frame="(0,0) is bottom left corner",
)

# Create Position object to contain the SpatialSeries
position_obj = Position(spatial_series=spatial_series_obj)
```

### Processing Modules
```python
# Create a processing module for behavioral data
behavior_module = nwbfile.create_processing_module(
    name="behavior", description="processed behavioral data"
)
# Add position data to the module
behavior_module.add(position_obj)

# Access the module
nwbfile.processing["behavior"]
```

### Time Intervals and Trials
```python
# Add custom column to trials table
nwbfile.add_trial_column(
    name="correct",
    description="whether the trial was correct",
)
# Add trial data
nwbfile.add_trial(start_time=1.0, stop_time=5.0, correct=True)
nwbfile.add_trial(start_time=6.0, stop_time=10.0, correct=False)

# Convert to pandas DataFrame
nwbfile.trials.to_dataframe()
```

### Writing NWB Files
```python
# Method 1
io = NWBHDF5IO("file.nwb", mode="w")
io.write(nwbfile)
io.close()

# Method 2 (context manager)
with NWBHDF5IO("file.nwb", "w") as io:
    io.write(nwbfile)
```

### Reading NWB Files
```python
with NWBHDF5IO("file.nwb", "r") as io:
    read_nwbfile = io.read()
    # Read entire dataset
    data = read_nwbfile.acquisition["test_timeseries"].data[:]
    # Read partial data
    partial_data = read_nwbfile.acquisition["test_timeseries"].data[:2]
    
    # Access data through object hierarchy
    behavior_data = read_nwbfile.processing["behavior"]["Position"]["SpatialSeries"]
```

### Appending to NWB Files
```python
# Open in append mode
io = NWBHDF5IO("file.nwb", mode="a")
nwbfile = io.read()

# Add new data
new_time_series = TimeSeries(
    name="new_time_series",
    description="a new time series",
    data=data,
    timestamps=timestamps,
    unit="n.a.",
)
nwbfile.add_acquisition(new_time_series)

# Write changes and close
io.write(nwbfile)
io.close()
```

Note: NWB only supports adding to files; removal and modification of existing data is not allowed.