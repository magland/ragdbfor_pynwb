# Scanbox Data Conversion with NeuroConv

## Installation

Install NeuroConv with the Scanbox-specific dependencies:

```bash
pip install"neuroconv[scanbox]"
```

## Converting Scanbox Imaging Data to NWB

The `SbxImagingInterface` class is used to convert Scanbox files to the NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import SbxImagingInterface

# Path to the Scanbox .sbx file
file_path = OPHYS_DATA_PATH / "imaging_datasets" / "Scanbox" / "sample.sbx"

# Create the interface
interface = SbxImagingInterface(file_path=file_path, verbose=False)

# Get metadata from the file
metadata = interface.get_metadata()

# Add session start time with timezone for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run the conversion and save the NWB file
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This code extracts metadata from the Scanbox file, adds necessary timing information, and converts the data to the NWB format.