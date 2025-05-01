# DeepLabCut Data Conversion to NWB

## Installation

Install NeuroConv with DeepLabCut dependencies:

```bash
pip install "neuroconv[deeplabcut]"
```

## Using DeepLabCutInterface

DeepLabCutInterface supports converting both .h5 and .csv output files from DeepLabCut to NWB format.

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import DeepLabCutInterface

# Define file paths
file_path = "/path/to/m3v1mp4DLC_resnet50_openfieldAug20shuffle1_30000.h5"
config_file_path = "/path/to/config.yaml"

# Create interface instance
interface = DeepLabCutInterface(
    file_path=file_path, 
    config_file_path=config_file_path, 
    subject_name="ind1", 
    verbose=False
)

# Get metadata and add session time information
metadata = interface.get_metadata()
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run the conversion
interface.run_conversion(nwbfile_path="/path/to/save/nwbfile.nwb", metadata=metadata)
```

The interface extracts pose estimation data from DeepLabCut and properly structures it in the NWB file according to the standard.