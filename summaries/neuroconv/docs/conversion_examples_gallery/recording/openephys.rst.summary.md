# OpenEphys Data Conversion to NWB

This guide demonstrates how to convert OpenEphys data to NWB format using the NeuroConv package.

## Installation

Install NeuroConv with OpenEphys support:

```bash
pip install "neuroconv[openephys]"
```

## Conversion Process

The conversion uses the `OpenEphysRecordingInterface` class:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

from neuroconv.datainterfaces import OpenEphysRecordingInterface

# Path to OpenEphys data folder
folder_path = "/path/to/openephysbinary/data"

# Initialize the interface
interface = OpenEphysRecordingInterface(folder_path=folder_path)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add required session start time if not available in source files
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Set output path and run conversion
nwbfile_path = "./output.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This creates an NWB file containing the converted OpenEphys electrophysiology data with appropriate metadata.