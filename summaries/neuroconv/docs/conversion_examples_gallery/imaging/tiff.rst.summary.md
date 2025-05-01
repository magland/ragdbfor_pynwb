# TIFF Data Conversion with PyNWB

## Installation
Install NeuroConv with TIFF support:
```bash
pip install "neuroconv[tiff]"
```

## Converting TIFF Imaging Data to NWB

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import TiffImagingInterface

# Path to the TIFF file
file_path = OPHYS_DATA_PATH / "imaging_datasets" / "Tif" / "demoMovie.tif"

# Initialize the interface with the file path and sampling frequency
interface = TiffImagingInterface(file_path=file_path, sampling_frequency=15.0, verbose=False)

# Get metadata from the interface
metadata = interface.get_metadata()

# Add timestamp information for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Set output path and run conversion
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

**Note:** TiffImagingInterface is only suitable for multi-page TIFF files containing all frames, not for data spread across multiple files (e.g., from Bruker acquisition software).