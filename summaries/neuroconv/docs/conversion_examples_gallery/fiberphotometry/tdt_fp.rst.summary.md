# TDT Fiber Photometry Data Conversion to NWB

## Installation
Install NeuroConv with TDT Fiber Photometry dependencies:
```bash
pip install "neuroconv[tdt_fp]"
```

## Conversion Process
The conversion of TDT Fiber Photometry data to NWB format involves:

1. Specifying detailed metadata in a YAML file that describes:
   - Optical fibers
   - Excitation sources
   - Photodetectors
   - Optical filters
   - Dichroic mirrors
   - Fluorescent indicators
   - Commanded voltage series
   - FiberPhotometryTable configuration
   - FiberPhotometryResponseSeries specifications

2. Using the `TDTFiberPhotometryInterface` to convert the data:

```python
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from neuroconv.datainterfaces import TDTFiberPhotometryInterface
from neuroconv.utils import dict_deep_update, load_dict_from_file

# Specify data and metadata paths
folder_path = OPHYS_DATA_PATH / "fiber_photometry_datasets" / "TDT" / "Photo_249_391-200721-120136_stubbed"
editable_metadata_path = Path("./fiber_photometry_metadata.yaml")

# Initialize interface and get metadata
interface = TDTFiberPhotometryInterface(folder_path=folder_path, verbose=False)
metadata = interface.get_metadata()

# Set session start time
metadata["NWBFile"]["session_start_time"] = datetime.now(tz=ZoneInfo("US/Pacific"))

# Load and merge custom metadata from YAML file
editable_metadata = load_dict_from_file(editable_metadata_path)
metadata = dict_deep_update(metadata, editable_metadata)

# Run conversion (can specify time window with t1 and t2)
nwbfile_path = "path_to_save_nwbfile.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata, t1=0.0, t2=1.0)
```

The converter handles TDT-specific data streams, mapping them to the appropriate NWB structures including calcium signal and isosbestic control recordings from different brain regions (DMS and DLS).