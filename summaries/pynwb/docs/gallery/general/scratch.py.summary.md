**Exploratory Data Analysis with NWB**

This document demonstrates using pynwb for exploratory data analysis, including storing intermediate analyses and one-off analyses. It focuses on linking and the scratch space for non-standardized data.

**Raw Data**

Example of setting up an `NWBFile` with some acquired data:

```python
from datetime import datetime
import numpy as np
from dateutil.tz import tzlocal
from pynwb import NWBHDF5IO, NWBFile, TimeSeries

# set up the NWBFile
start_time = datetime(2019, 4, 3, 11, tzinfo=tzlocal())
create_date = datetime(2019, 4, 15, 12, tzinfo=tzlocal())

nwb = NWBFile(
    session_description="demonstrate NWBFile scratch",  # required
    identifier="NWB456",  # required
    session_start_time=start_time,  # required
    file_create_date=create_date,
)  # optional

# make some fake data
timestamps = np.linspace(0, 100, 1024)
data = (
    np.sin(0.333 * timestamps)
    + np.cos(0.1 * timestamps)
    + np.random.randn(len(timestamps))
)
test_ts = TimeSeries(name="raw_timeseries", data=data, unit="m", timestamps=timestamps)

# add it to the NWBFile
nwb.add_acquisition(test_ts)

with NWBHDF5IO("raw_data.nwb", mode="w") as io:
    io.write(nwb)
```

**Copying an NWB file**

Demonstrates copying an NWB file using the `copy` method:

```python
from pynwb import NWBHDF5IO
# read the file:
raw_io = NWBHDF5IO("raw_data.nwb", "r")
nwb_in = raw_io.read()

# create a shallow copy of the file:
nwb_proc = nwb_in.copy()
```

Next, it shows how to add a `ProcessingModule`:

```python
import scipy.signal as sps
from pynwb import NWBHDF5IO, TimeSeries

# create a processing module
mod = nwb_proc.create_processing_module(
    "filtering_module", "a module to store filtering results"
)

# create and add a TimeSeries to the processing module
ts1 = nwb_in.acquisition["raw_timeseries"]
filt_data = sps.correlate(ts1.data, np.ones(128), mode="same") / 128
ts2 = TimeSeries(name="filtered_timeseries", data=filt_data, unit="m", timestamps=ts1)

mod.add_container(ts2)

# write the copy, which contains the processed data
with NWBHDF5IO("processed_data.nwb", mode="w", manager=raw_io.manager) as io:
    io.write(nwb_proc)
raw_io.close() #close io object
```

Note: The processed file contains external links to the original raw data.

**Adding scratch data**

Shows how to store results from a one-off analysis using the scratch space:

```python
import numpy as np
from pynwb import NWBHDF5IO

# read the processed data:
proc_io = NWBHDF5IO("processed_data.nwb", "r")
nwb_proc_in = proc_io.read()

# create a copy to put our scratch data into:
nwb_scratch = nwb_proc_in.copy()

# perform analysis; discrete Fourier transform
filt_ts = nwb_scratch.processing["filtering_module"]["filtered_timeseries"]
fft = np.fft.fft(filt_ts.data)

# add to scratch with a name and description:
nwb_scratch.add_scratch(
    fft,
    name="dft_filtered",
    description="discrete Fourier transform from filtered data",
)

# write the results:
with NWBHDF5IO("scratch_analysis.nwb", "w", manager=proc_io.manager) as io:
    io.write(nwb_scratch)
proc_io.close() #close io object

#To retrieve the scratch data:
scratch_io = NWBHDF5IO("scratch_analysis.nwb", "r")
nwb_scratch_in = scratch_io.read()

fft_in = nwb_scratch_in.scratch["dft_filtered"] # access by name

fft_in = nwb_scratch_in.get_scratch("dft_filtered") # alternative access by name

scratch_io.close() #close io object
```

Important: It is recommended to write scratch data into copies of files to isolate and discard it easily. Use `nwb_scratch_in.scratch["name"]` or `nwb_scratch_in.get_scratch("name")` to access scratch data.
