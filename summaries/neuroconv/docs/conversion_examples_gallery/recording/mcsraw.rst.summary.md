# MCSRaw Conversion with NeuroConv

## Installation
Install NeuroConv with MCSRaw support:
```bash
pip install "neuroconv[mcsraw]"
```

## Converting MCSRaw to NWB
Use the `MCSRawRecordingInterface` class to convert MCSRaw data to NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import MCSRawRecordingInterface

# Set path to your MCSRaw file
file_path = "path/to/your/raw_mcs_file.raw"

# Initialize interface
interface = MCSRawRecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add session start time with timezone for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Set output path and run conversion
nwbfile_path = "path/to/save/output.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This process extracts available metadata from the MCSRaw file and creates an NWB file with properly formatted electrophysiology data.