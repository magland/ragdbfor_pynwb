# Video Data Conversion for NWB

## Installation
To handle multimedia data conversion to NWB format, install NeuroConv with video support:

```bash
pip install "neuroconv[video]"
```

## External Video Interface

For natural behavior videos, best practice is to store as external files with links from NWB. Use `ExternalVideoInterface`:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import ExternalVideoInterface
from neuroconv.utils import dict_deep_update

# Setup
video_file_path = "/path/to/video_file.avi"
interface = ExternalVideoInterface(
    file_paths=[video_file_path], 
    verbose=False, 
    video_name="MyExternalVideo"
)

# Generate metadata
metadata = interface.get_metadata()
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Add custom video metadata
video_metadata = {
    "Behavior": {
        "ExternalVideos": {
            "MyExternalVideo": {  # Must match video_name
                "description": "My description of the video data",
                "device": {
                    "name": "MyCamera",
                    "description": "My description of the camera",
                },
            }
        }
    }
}
metadata = dict_deep_update(metadata, video_metadata)

# Run conversion
nwbfile_path = "output_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata, overwrite=True)
```

## Internal Video Interface

For neural data videos where lossy compression should be avoided, use `InternalVideoInterface` to store within the NWB file:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import InternalVideoInterface
from neuroconv.utils import dict_deep_update

# Setup
video_file_path = "/path/to/video_file.avi"
interface = InternalVideoInterface(
    file_path=video_file_path, 
    verbose=False, 
    video_name="MyInternalVideo"
)

# Generate metadata
metadata = interface.get_metadata()
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Add custom video metadata
video_metadata = {
    "Behavior": {
        "InternalVideos": {
            "MyInternalVideo": {  # Must match video_name
                "description": "My description of the video data",
                "device": {
                    "name": "MyCamera",
                    "description": "My description of the camera",
                },
            }
        }
    }
}
metadata = dict_deep_update(metadata, video_metadata)

# Run conversion
nwbfile_path = "output_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata, overwrite=True)
```

## Legacy VideoInterface (pre-0.8)
For older versions of NeuroConv:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import VideoInterface

video_file_path = "/path/to/video_file.avi"
interface = VideoInterface(file_paths=[video_file_path], verbose=False)

metadata = interface.get_metadata()
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

nwbfile_path = "output_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata, overwrite=True)
```

Supported formats include avi, mov, mp4, wmv, flv, and most FFmpeg-supported formats.