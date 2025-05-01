# Excel Data Conversion with pynwb and NeuroConv

## Installation

Install NeuroConv with Excel support:

```bash
pip install "neuroconv[excel]"
```

## Converting Excel Data to NWB

Excel files can be converted to NWB format using `ExcelTimeIntervalsInterface`. The Excel file must have a header row containing at least the columns "start_time" and "stop_time". The data will be saved as trials in the NWB file.

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import ExcelTimeIntervalsInterface

file_path = "path/to/trials.xlsx"
interface = ExcelTimeIntervalsInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add session start time with timezone
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"] = dict(session_start_time=session_start_time)

# Run conversion
nwbfile_path = "./saved_file.nwb"
nwbfile = interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This converts the time intervals from Excel into trial data in an NWB file.