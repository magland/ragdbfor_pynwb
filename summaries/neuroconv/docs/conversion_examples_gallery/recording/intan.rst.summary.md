# Intan Data Conversion to NWB

## Installation

Install NeuroConv with Intan-specific dependencies:

```bash
pip install "neuroconv[intan]"
```

## Converting Intan Data to NWB

Use `IntanRecordingInterface` to convert Intan data files (`.rhd` or `.rhs`) to NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import IntanRecordingInterface

# Path to the Intan data file (.rhd or .rhs)
file_path = "/path/to/intan_file.rhd"

# Create the interface
interface = IntanRecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Set required session start time if not automatically inferred
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run the conversion
nwbfile_path = "/path/to/save/file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

The conversion process automatically extracts available metadata and creates an NWB file with the electrophysiology data properly formatted.