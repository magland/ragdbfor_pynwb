# NeuroScope Data Conversion to NWB

## Installation
Install NeuroConv with NeuroScope dependencies:
```bash
pip install "neuroconv[neuroscope]"
```

## Converting NeuroScope Data to NWB
The conversion process uses `NeuroScopeRecordingInterface` from the NeuroConv package:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import NeuroScopeRecordingInterface

# Path to the .dat file
file_path = "/path/to/your/neuroscope/file.dat"

# Create interface
interface = NeuroScopeRecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add required session_start_time if not available in the source
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Save as NWB file
nwbfile_path = "./output_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This process extracts available metadata from the NeuroScope files and creates a properly formatted NWB file with the electrophysiology recordings.