# Plexon2 Recording Conversion to NWB

## Installation

Install NeuroConv with Plexon support:

```bash
pip install neuroconv[plexon]
```

**Note:** When using platforms other than Windows, you need to install [wine](https://www.winehq.org/).

## Converting Plexon2 data to NWB

The following example demonstrates how to convert Plexon2 recording data to NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import Plexon2RecordingInterface

# Set the path to your Plexon file
file_path = "/path/to/your/plexon/4chDemoPL2.pl2"

# Create the interface
interface = Plexon2RecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add timezone information for data provenance
tzinfo = ZoneInfo("US/Pacific")
session_start_time = metadata["NWBFile"]["session_start_time"]
metadata["NWBFile"].update(session_start_time=session_start_time.replace(tzinfo=tzinfo))

# Set output path and run conversion
nwbfile_path = "/path/to/save/output.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

The conversion uses the `Plexon2RecordingInterface` to extract data and metadata from the Plexon files and writes them to a properly formatted NWB file.