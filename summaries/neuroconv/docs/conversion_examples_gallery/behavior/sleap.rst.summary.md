# SLEAP Data Conversion to NWB

## Installation
Install NeuroConv with SLEAP support:
```bash
pip install "neuroconv[sleap]"
```

## Conversion Example
Convert SLEAP pose estimation data to NWB using `SLEAPInterface`:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import SLEAPInterface

# Path to the .slp file
file_path = BEHAVIOR_DATA_PATH / "sleap" / "predictions_1.2.7_provenance_and_tracking.slp"
interface = SLEAPInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add required session_start_time if not automatically inferred
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run conversion
nwbfile_path = "path_to_save_nwbfile.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

The example demonstrates the complete workflow for converting SLEAP pose estimation data to NWB format, including setting up the interface, extracting metadata, providing required timestamps, and executing the conversion.