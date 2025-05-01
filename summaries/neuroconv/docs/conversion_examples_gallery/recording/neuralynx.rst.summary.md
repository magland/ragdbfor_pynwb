# Neuralynx Data Conversion with PyNWB

## Installation
Install NeuroConv with Neuralynx dependencies:
```bash
pip install "neuroconv[neuralynx]"
```

## Converting Neuralynx Data to NWB Format

The following example demonstrates how to convert Neuralynx data to NWB format using the `NeuralynxRecordingInterface`:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import NeuralynxRecordingInterface

# Specify the folder containing Neuralynx data
folder_path = f"{ECEPHY_DATA_PATH}/neuralynx/Cheetah_v5.7.4/original_data"
interface = NeuralynxRecordingInterface(folder_path=folder_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Handle session_start_time (required for conversion)
# Set timezone if needed
session_start_time = metadata["NWBFile"]["session_start_time"]
session_start_time = session_start_time.replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"]["session_start_time"] = session_start_time

# Choose save path and run conversion
nwbfile_path = f"{path_to_save_nwbfile}"  # e.g., "./saved_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

For Neuralynx NVT files, refer to the separate neuralynx_nvt_conversion documentation.