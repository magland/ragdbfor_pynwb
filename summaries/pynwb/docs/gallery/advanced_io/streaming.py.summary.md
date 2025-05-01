# Streaming NWB Files

## Overview
This document explains how to stream data from remote NWB files, which is useful for reading parts of large NWB files without downloading them entirely. Three methods are presented:

## Getting File Location on DANDI
```python
from dandi.dandiapi import DandiAPIClient

dandiset_id = '000006'
filepath = 'sub-anm372795/sub-anm372795_ses-20170718.nwb'
with DandiAPIClient() as client:
    asset = client.get_dandiset(dandiset_id, 'draft').get_asset_by_path(filepath)
    s3_url = asset.get_content_url(follow_redirects=1, strip_query=True)
```

## Method 1: Using remfile
This is a simple, fast library optimized for streaming HDF5 files from S3.

```python
import h5py
from pynwb import NWBHDF5IO
import remfile

# Create optional disk cache
cache_dirname = '/tmp/remfile_cache'
disk_cache = remfile.DiskCache(cache_dirname)

# Open file
rem_file = remfile.File(s3_url, disk_cache=disk_cache)
h5py_file = h5py.File(rem_file, "r")
io = NWBHDF5IO(file=h5py_file)
nwbfile = io.read()

# Access data
streamed_data = nwbfile.acquisition["lick_times"].time_series["lick_left_times"].data[:]

# Close file
io.close()
h5py_file.close()
rem_file.close()
```

Using context managers:
```python
rem_file = remfile.File(s3_url, disk_cache=disk_cache)
with h5py.File(rem_file, "r") as h5py_file:
    with NWBHDF5IO(file=h5py_file, load_namespaces=True) as io:
        nwbfile = io.read()
        streamed_data = nwbfile.acquisition["lick_times"].time_series["lick_left_times"].data[:]
```

## Method 2: Using fsspec
A flexible library creating virtual filesystems for various remote stores.

```python
import fsspec
import pynwb
import h5py
from fsspec.implementations.cached import CachingFileSystem

# Create filesystem
fs = fsspec.filesystem("http")

# Optional cache
fs = CachingFileSystem(
    fs=fs,
    cache_storage="nwb-cache",
)

# Open file
f = fs.open(s3_url, "rb")
file = h5py.File(f)
io = pynwb.NWBHDF5IO(file=file)
nwbfile = io.read()

# Access data
streamed_data = nwbfile.acquisition['lick_times'].time_series['lick_left_times'].data[:]

# Close file
io.close()
file.close()
f.close()
```

Using context managers:
```python
with fs.open(s3_url, "rb") as f:
    with h5py.File(f) as file:
        with pynwb.NWBHDF5IO(file=file) as io:
            nwbfile = io.read()
            data = nwbfile.acquisition['lick_times'].time_series['lick_left_times'].data[:]
```

## Method 3: Using ROS3 (Read-Only S3)
Direct HDF5 driver for S3 access. Requires HDF5 built with ROS3 support.

```python
from pynwb import NWBHDF5IO

# With context manager
with NWBHDF5IO(s3_url, mode='r', driver='ros3') as io:
    nwbfile = io.read()
    streamed_data = nwbfile.acquisition['lick_times'].time_series['lick_left_times'].data[:]

# Manually
io = NWBHDF5IO(s3_url, mode='r', driver='ros3')
nwbfile = io.read()
streamed_data = nwbfile.acquisition['lick_times'].time_series['lick_left_times'].data[:]
io.close()
```

Note: For ROS3, install h5py with conda: `conda install h5py` as PyPI versions don't include S3 support.