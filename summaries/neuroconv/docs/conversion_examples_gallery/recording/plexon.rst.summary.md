# Plexon Recording Conversion to NWB

## Installation
Install NeuroConv with Plexon support:
```
pip install "neuroconv[plexon]"
```

## Converting Plexon (.plx) Files to NWB

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import PlexonRecordingInterface

# Specify the path to your Plexon file
file_path = "/path/to/your/plexon/file.plx"

# Initialize the interface
interface = PlexonRecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from the source files
metadata = interface.get_metadata()

# Add timezone information for data provenance
session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Specify output path and run conversion
nwbfile_path = "/path/to/save/output.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

Note: Currently only .plx file format is supported by the PlexonRecordingInterface.