# ExtractSegmentationInterface for NWB Conversion

This interface enables conversion of EXTRACT segmentation data to NWB format.

## Installation
Install NeuroConv with EXTRACT dependencies:
```bash
pip install "neuroconv[extract]"
```

## Usage Example
Convert EXTRACT segmentation data to NWB:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import ExtractSegmentationInterface

# Setup the interface
file_path = OPHYS_DATA_PATH / "segmentation_datasets" / "extract"/ "2014_04_01_p203_m19_check01_extractAnalysis.mat"
sampling_frequency = 20.0  # Hz
interface = ExtractSegmentationInterface(
    file_path=file_path, 
    sampling_frequency=sampling_frequency, 
    verbose=False
)

# Get and update metadata
metadata = interface.get_metadata()
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run conversion
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

The interface handles EXTRACT-format ophys segmentation data and converts it to the NWB standard format.