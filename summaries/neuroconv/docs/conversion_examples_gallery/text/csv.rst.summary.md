# Converting CSV Data to NWB Format

## Installation

```bash
pip install neuroconv
```

No additional dependencies are required for reading CSV files.

## Using CsvTimeIntervalsInterface

This interface converts CSV data to NWB trials:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import CsvTimeIntervalsInterface

# Set path to your CSV file
file_path = "path/to/trials.csv"

# Initialize the interface
interface = CsvTimeIntervalsInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add session start time with timezone information
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"] = dict(session_start_time=session_start_time)

# Convert and save to NWB file
nwbfile_path = "path/to/save/file.nwb"
nwbfile = interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

## Requirements

The CSV file must contain a header row with at least these column names:
- "start_time"
- "stop_time"

The CSV data will be saved in the trials table of the NWB file.