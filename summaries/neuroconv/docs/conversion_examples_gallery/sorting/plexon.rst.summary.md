# Plexon Sorting Data Conversion to NWB

## Installation
Install NeuroConv with Plexon support:
```bash
pip install "neuroconv[plexon]"
```

## Converting Plexon Data to NWB
Convert Plexon spiking data (.plx) to NWB using `PlexonSortingInterface`:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import PlexonSortingInterface

# Set path to Plexon file
file_path = f"{ECEPHY_DATA_PATH}/plexon/File_plexon_2.plx"
# Initialize interface
interface = PlexonSortingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add timezone information for data provenance
tzinfo = ZoneInfo("US/Pacific")
session_start_time = metadata["NWBFile"]["session_start_time"]
metadata["NWBFile"].update(session_start_time=session_start_time.replace(tzinfo=tzinfo))

# Choose output path and run conversion
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```