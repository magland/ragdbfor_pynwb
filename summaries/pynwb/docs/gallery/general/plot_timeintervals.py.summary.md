# Annotating Time Intervals in NWB

## TimeIntervals Overview

`TimeIntervals` is a `DynamicTable`-based type in PyNWB used to annotate time ranges in neuroscience data. It has the following key columns:

- `start_time` and `stop_time`: Floating point values in seconds
- `tags`: Optional indexed column for user-defined string tags (0+ tags per interval)
- `timeseries`: Optional indexed column to map intervals to ranges in `TimeSeries` objects
- Custom columns can be added via `add_column()`

## Pre-defined TimeIntervals in NWBFile

NWBFile provides three built-in TimeIntervals tables:

1. **Trials**: Access via `nwbfile.trials`
2. **Epochs**: Access via `nwbfile.epochs`
3. **Invalid Times**: Access via `nwbfile.invalid_times`

## Working with Trials

```python
# Add a custom column to trials
nwbfile.add_trial_column(name="stim", description="the visual stimuli during the trial")

# Add a trial with tags and timeseries references
nwbfile.add_trial(
    start_time=0.0,
    stop_time=2.0,
    stim="dog",
    tags=["animal"],
    timeseries=[test_ts, rate_ts],
)
```

## Creating Custom TimeIntervals

```python
from pynwb.epoch import TimeIntervals

# Create a custom TimeIntervals table
sleep_stages = TimeIntervals(
    name="sleep_stages",
    description="intervals for each sleep stage as determined by EEG",
)

# Add custom columns
sleep_stages.add_column(name="stage", description="stage of sleep")
sleep_stages.add_column(name="confidence", description="confidence in stage (0-1)")

# Add rows
sleep_stages.add_row(start_time=0.3, stop_time=0.5, stage=1, confidence=0.5)

# Add to NWBFile
nwbfile.add_time_intervals(sleep_stages)
```

## Accessing TimeIntervals Data

```python
# Access pre-defined tables
trials = nwbfile.trials
epochs = nwbfile.epochs

# Access custom tables
sleep_data = nwbfile.get_time_intervals("sleep_stages")

# Convert to pandas DataFrame for analysis
trials_df = nwbfile.trials.to_dataframe()

# Query the data
filtered_trials = trials_df.query("(start_time > 2.0) & (stop_time < 9.0)")
```

## Working with TimeSeries References

TimeIntervals can reference specific ranges of TimeSeries data:

```python
# Get a TimeSeriesReference from the trials table
tsr = nwbfile.trials["timeseries"][0][0]

# Access the data values for the referenced time range
data = tsr.data

# Access the timestamps
timestamps = tsr.timestamps

# Check if the reference is valid
is_valid = tsr.isvalid()
```

## Reading/Writing to File

```python
from pynwb import NWBHDF5IO

# Write to file
with NWBHDF5IO("example_file.nwb", "w") as io:
    io.write(nwbfile)

# Read from file
with NWBHDF5IO("example_file.nwb", "r") as io:
    nwbfile_in = io.read()
    sleep_data = nwbfile_in.get_time_intervals("sleep_stages").to_dataframe()
```