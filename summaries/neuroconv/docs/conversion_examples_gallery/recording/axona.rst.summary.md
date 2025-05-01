# Axona Data Conversion to NWB Format

## Installation

Install NeuroConv with Axona-specific dependencies:

```bash
pip install "neuroconv[axona]"
```

## Converting Axona Data to NWB

Use the `AxonaRecordingInterface` to convert Axona data files to NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import AxonaRecordingInterface

# Specify the location of the .bin file
file_path = f"{ECEPHY_DATA_PATH}/axona/axona_raw.bin"
interface = AxonaRecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add timezone information for data provenance
tzinfo = ZoneInfo("US/Pacific")
session_start_time = metadata["NWBFile"]["session_start_time"]
metadata["NWBFile"].update(session_start_time=session_start_time.replace(tzinfo=tzinfo))

# Run the conversion and save the NWB file
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```