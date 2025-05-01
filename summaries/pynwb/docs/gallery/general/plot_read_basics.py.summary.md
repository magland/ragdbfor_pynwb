# Reading and Exploring an NWB File

This tutorial demonstrates how to read, explore, and visualize data within an NWB (Neurodata Without Borders) file using PyNWB.

## Getting NWB Data

NWB files can be accessed from the DANDI archive by:
1. Downloading via web interface
2. Using the `dandi` Python module:
   ```python
   from dandi.download import download
   download("https://api.dandiarchive.org/api/assets/0f57f0b0-f021-42bb-8eaa-56cd482e2a29/download/", ".")
   ```
3. Streaming data without full download (see streaming documentation)

## Opening NWB Files

PyNWB provides two main methods for reading NWB files:

### Simple Method with `read_nwb()`
```python
from pynwb import read_nwb
nwbfile = read_nwb("sub-P11HMH_ses-20061101_ecephys+image.nwb")
```

### Using NWBHDF5IO with Context Manager
```python
from pynwb import NWBHDF5IO
with NWBHDF5IO(filepath, mode="r") as io:
    nwbfile = io.read()
    # Work with data here
# File is automatically closed outside the context
```

## Accessing Stimulus Data

Stimulus data is stored in the `stimulus` attribute:
```python
nwbfile.stimulus  # Returns a dictionary of stimulus objects
stimulus_presentation = nwbfile.stimulus["StimulusPresentation"]
```

## Lazy Loading and Data Slicing

NWB uses lazy loading to efficiently handle large datasets:
```python
# This doesn't load data yet, just provides access to it
stimulus_presentation.data  

# Load entire dataset into memory
all_stimulus_data = stimulus_presentation.data[:]

# Access specific frames
image = stimulus_presentation.data[31]
```

## Working with Single Unit Data

Single unit (neuronal) data is stored in the `units` attribute:
```python
units = nwbfile.units

# Convert to pandas DataFrame for easy viewing
units_df = units.to_dataframe()

# Access spike times for a specific unit
spike_times = units["spike_times"][0]
```

## Accessing Trial Data

Trials are stored in `trials` as a TimeIntervals object (a subclass of DynamicTable):
```python
# Convert to pandas DataFrame
trials_df = nwbfile.trials.to_dataframe()

# Access specific trial categories
landscape_trials = trials_df[trials_df.category_name == "landscapes"]
```

## Working with Timestamps

Get timestamps for time series data:
```python
# Get all timestamps (works with both explicit timestamps and calculated ones)
stim_on_times = stimulus_presentation.get_timestamps()
```

## Visualization Examples

The tutorial includes examples of:
- Displaying stimulus images
- Creating spike raster plots aligned to stimulus onset
- Generating histograms of neural activity

## Closing Files

Always close NWB files when finished:
```python
nwbfile.get_read_io().close()
```