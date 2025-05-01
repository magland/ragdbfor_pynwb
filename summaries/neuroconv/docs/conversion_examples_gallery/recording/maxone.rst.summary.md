# MaxOne Conversion Guide

## Installation
Install NeuroConv with Maxwell dependencies (Linux systems only):

```bash
pip install "neuroconv[maxwell]"
```

## Converting MaxOne Data to NWB

```python
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import MaxOneRecordingInterface

# Set file path to your MaxOne data
file_path = "/path/to/maxwell/MaxOne_data/Record/000011/data.raw.h5"

# Create interface
interface = MaxOneRecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add session start time with timezone for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run conversion
nwbfile_path = "/path/to/save/output.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

The conversion uses the `MaxOneRecordingInterface` class to read MaxOne electrophysiology data and convert it to NWB format with appropriate metadata.