# CaImAn Integration with PyNWB

## Installation

Install NeuroConv with CaImAn support:

```bash
pip install "neuroconv[caiman]"
```

## Converting CaImAn Data to NWB

Use the `CaimanSegmentationInterface` class to convert CaImAn segmentation data to NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import CaimanSegmentationInterface

# Path to CaImAn analysis file
file_path = OPHYS_DATA_PATH / "segmentation_datasets" / "caiman" / "caiman_analysis.hdf5"

# Create interface
interface = CaimanSegmentationInterface(file_path=file_path, verbose=False)

# Get metadata and add session start time for data provenance
metadata = interface.get_metadata()
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run conversion
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```