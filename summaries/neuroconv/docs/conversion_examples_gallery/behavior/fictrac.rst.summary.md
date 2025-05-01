# FicTrac Data Conversion with NeuroConv

## Installation

Install NeuroConv with FicTrac support:

```bash
pip install "neuroconv[fictrac]"
```

## Converting FicTrac Data to NWB

FicTrac spherical motion and fictive animal path data can be converted to NWB using the `FicTracDataInterface`:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import FicTracDataInterface

# Path to your FicTrac .dat file
file_path = BEHAVIOR_DATA_PATH / "FicTrac" / "sample" / "sample-20230724_113055.dat"

# If you have the radius of the ball (in meters), pass it to get data in meters
radius = 0.035
interface = FicTracDataInterface(file_path=file_path, radius=radius, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add timezone information for data provenance
session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run the conversion to create an NWB file
interface.run_conversion(nwbfile_path=path_to_save_nwbfile, metadata=metadata)
```

This converts FicTrac `.dat` file data into an NWB file with proper metadata and units.