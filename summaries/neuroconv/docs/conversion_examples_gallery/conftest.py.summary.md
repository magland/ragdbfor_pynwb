# PyNWB Testing Utilities

This module provides pytest fixtures and utilities specifically for testing the PyNWB package:

## Features

- Provides a fixture `add_data_space` that automatically adds common data paths to the doctest namespace
- Sets up test data paths for different domains:
  - `ECEPHY_DATA_PATH` - Extracellular electrophysiology data
  - `BEHAVIOR_DATA_PATH` - Behavioral data
  - `OPHYS_DATA_PATH` - Optical physiology data
  - `TEXT_DATA_PATH` - Text-based data

- Creates temporary paths for doctests:
  - `path_to_save_nwbfile` - Path for saving test NWB files
  - `output_folder` - General output directory for tests

## Conditional Testing

Includes platform/version-specific hooks to skip certain tests:
- Skips `deeplabcut.rst` doctests on Python 3.9 and macOS
- Conditionally skips tests related to `sleap.rst` and `ecephys_pose_estimation.rst` based on the installed `ndx-pose` version

This utility ensures doctests can run consistently across different environments while accommodating platform-specific limitations.