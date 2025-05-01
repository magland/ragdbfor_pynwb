# HDF5 Data Conversion with NeuroConv

## Installation

Install NeuroConv with HDF5 support:

```bash
pip install "neuroconv[hdf5]"
```

## Converting HDF5 Imaging Data to NWB

The `Hdf5ImagingInterface` class allows conversion of HDF5 imaging data to NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import Hdf5ImagingInterface

# Define path to HDF5 file
file_path = OPHYS_DATA_PATH / "imaging_datasets" / "hdf5" / "demoMovie.hdf5"

# Initialize the interface
interface = Hdf5ImagingInterface(file_path=file_path, verbose=False)

# Get metadata
metadata = interface.get_metadata()

# Add session start time with timezone for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run conversion
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```