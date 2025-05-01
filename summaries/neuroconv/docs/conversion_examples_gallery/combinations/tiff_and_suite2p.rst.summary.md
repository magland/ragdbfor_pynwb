# Processing Tiff Images with Suite2p in PyNWB

## Workflow Overview
This guide shows how to use PyNWB to convert optical physiology data where:
1. Images are recorded with a microscope (Tiff format)
2. A segmentation algorithm (Suite2p) produces regions of interest and fluorescence traces

## Implementation with NeuroConv

The conversion uses two interfaces:
- `TiffImagingInterface`: Handles the raw imaging data
- `Suite2pSegmentationInterface`: Processes the segmentation output

## Code Example

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv import ConverterPipe
from neuroconv.datainterfaces import TiffImagingInterface, Suite2pSegmentationInterface

# Set up the Tiff imaging interface
file_path = OPHYS_DATA_PATH / "imaging_datasets" / "Tif" / "demoMovie.tif"
interface_tiff = TiffImagingInterface(file_path=file_path, sampling_frequency=15.0, verbose=False)

# Set up the Suite2p segmentation interface
folder_path= OPHYS_DATA_PATH / "segmentation_datasets" / "suite2p"
interface_suit2p = Suite2pSegmentationInterface(folder_path=folder_path, verbose=False)

# Combine interfaces in a ConverterPipe for coordinated conversion
converter = ConverterPipe(data_interfaces=[interface_tiff, interface_suit2p], verbose=False)

# Extract metadata from source files
metadata = converter.get_metadata()

# Add session start time with timezone for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run the conversion
nwbfile_path = f"{path_to_save_nwbfile}"
converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```