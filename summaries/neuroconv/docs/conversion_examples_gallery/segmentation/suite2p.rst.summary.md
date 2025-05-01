# Suite2p Conversion to NWB

## Installation

Install NeuroConv with suite2p support:

```bash
pip install "neuroconv[suite2p]"
```

## Basic Conversion

Convert suite2p segmentation data to NWB using the `Suite2pSegmentationInterface`:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import Suite2pSegmentationInterface

folder_path = OPHYS_DATA_PATH / "segmentation_datasets" / "suite2p"
interface = Suite2pSegmentationInterface(folder_path=folder_path, verbose=False)

metadata = interface.get_metadata()
# Add time zone information for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run the conversion
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

## Key Parameters

- `plane_name`: Specifies which plane to convert (use `Suite2pSegmentationInterface.get_available_planes(folder_path)` to view options)
- `channel_name`: For multichannel recordings (use `Suite2pSegmentationInterface.get_channel_names(folder_path)` to view options)
- `plane_segmentation_name`: Name for the resulting `PlaneSegmentation` (should be unique for each plane/channel combination)

## Multi-Plane Conversion

For datasets with multiple planes:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv import ConverterPipe
from neuroconv.datainterfaces import Suite2pSegmentationInterface

folder_path = OPHYS_DATA_PATH / "segmentation_datasets" / "suite2p"
interface_first_plane = Suite2pSegmentationInterface(folder_path=folder_path, plane_name="plane0", verbose=False)
interface_second_plane = Suite2pSegmentationInterface(folder_path=folder_path, plane_name="plane1", verbose=False)

converter = ConverterPipe(data_interfaces=[interface_first_plane, interface_second_plane], verbose=False)
metadata = converter.get_metadata()
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

nwbfile_path = f"{output_folder}/file2.nwb"
converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```