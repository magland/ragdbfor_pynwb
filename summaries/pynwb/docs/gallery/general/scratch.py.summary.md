# Exploratory Data Analysis with NWB

This document demonstrates how to use PyNWB for exploratory data analysis, particularly focusing on:

1. Using scratch space for non-standardized data
2. Copying NWBFiles
3. Adding processed data to an NWBFile

## Scratch Space

- Scratch space is explicitly for non-standardized data not intended for reuse by others
- Published data should not include scratch data
- Users should be able to ignore scratch data to use a file

## Key Operations

### Creating Raw Data File

```python
from datetime import datetime
import numpy as np
from dateutil.tz import tzlocal
from pynwb import NWBHDF5IO, NWBFile, TimeSeries

# Create NWBFile
nwb = NWBFile(
    session_description="demonstrate NWBFile scratch",
    identifier="NWB456",
    session_start_time=datetime(2019, 4, 3, 11, tzinfo=tzlocal()),
    file_create_date=datetime(2019, 4, 15, 12, tzinfo=tzlocal())
)

# Create and add TimeSeries data
timestamps = np.linspace(0, 100, 1024)
data = np.sin(0.333 * timestamps) + np.cos(0.1 * timestamps) + np.random.randn(len(timestamps))
test_ts = TimeSeries(name="raw_timeseries", data=data, unit="m", timestamps=timestamps)
nwb.add_acquisition(test_ts)

# Write to file
with NWBHDF5IO("raw_data.nwb", mode="w") as io:
    io.write(nwb)
```

### Copying an NWB File and Adding Processed Data

```python
# Read original file
raw_io = NWBHDF5IO("raw_data.nwb", "r")
nwb_in = raw_io.read()

# Create a shallow copy
nwb_proc = nwb_in.copy()

# Process data and add to a processing module
import scipy.signal as sps
mod = nwb_proc.create_processing_module("filtering_module", "a module to store filtering results")

ts1 = nwb_in.acquisition["raw_timeseries"]
filt_data = sps.correlate(ts1.data, np.ones(128), mode="same") / 128
ts2 = TimeSeries(name="filtered_timeseries", data=filt_data, unit="m", timestamps=ts1)
mod.add_container(ts2)

# Write the copy with processed data
with NWBHDF5IO("processed_data.nwb", mode="w", manager=raw_io.manager) as io:
    io.write(nwb_proc)
```

### Adding and Retrieving Scratch Data

```python
# Read processed data
proc_io = NWBHDF5IO("processed_data.nwb", "r")
nwb_proc_in = proc_io.read()

# Make a copy for scratch data
nwb_scratch = nwb_proc_in.copy()

# Add scratch data
filt_ts = nwb_scratch.processing["filtering_module"]["filtered_timeseries"]
fft = np.fft.fft(filt_ts.data)
nwb_scratch.add_scratch(
    fft,
    name="dft_filtered",
    description="discrete Fourier transform from filtered data"
)

# Write file with scratch data
with NWBHDF5IO("scratch_analysis.nwb", "w", manager=proc_io.manager) as io:
    io.write(nwb_scratch)

# Retrieve scratch data
scratch_io = NWBHDF5IO("scratch_analysis.nwb", "r")
nwb_scratch_in = scratch_io.read()

# Two ways to access scratch data:
fft_in = nwb_scratch_in.scratch["dft_filtered"]
# or
fft_in = nwb_scratch_in.get_scratch("dft_filtered")
```

## Important Notes

- When reusing timestamps, you can link to the original TimeSeries
- The copied file contains external links to data in the original file, avoiding duplication
- Scratch space only exists if you add scratch data
- It's recommended to write scratch data into copies of files for easier isolation