# Spike2 Data Conversion to NWB

## Installation
Install NeuroConv with Spike2 support:
```bash
pip install "neuroconv[spike2]"
```

## Converting Spike2 Data to NWB
Use the `Spike2RecordingInterface` class from NeuroConv:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import Spike2RecordingInterface

# Specify path to Spike2 file
file_path = "/path/to/your/file.smrx"

# Create interface
interface = Spike2RecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add session start time with timezone info for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run conversion and save NWB file
nwbfile_path = "/path/to/save/output.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This converts Spike2 electrophysiology data to the NWB format while preserving metadata and timing information.