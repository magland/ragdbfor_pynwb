## Editing NWB files

This document describes how to edit NWB files in-place.

**Warning:** Manually editing an existing NWB file can make the file invalid. It is highly recommended to make a copy before editing and validating the file after editing.

### Editing datasets

When reading an HDF5 NWB file, PyNWB exposes `h5py.Dataset` objects that can be edited in-place, by opening the file in read/write mode ("r+" or "a").

**Example:** Editing the values of a dataset.

```python
from pynwb import NWBHDF5IO, NWBFile, TimeSeries
from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np

# creates a sample nwb file
nwbfile = NWBFile(
    session_description="my first synthetic recording",
    identifier="EXAMPLE_ID",
    session_start_time=datetime.now(tzlocal()),
    session_id="LONELYMTN",
)

nwbfile.add_acquisition(
    TimeSeries(
        name="synthetic_timeseries",
        description="Random values",
        data=np.random.randn(100, 100),
        unit="m",
        rate=10e3,
    )
)

with NWBHDF5IO("test_edit.nwb", "w") as io:
    io.write(nwbfile)

# edits the file
with NWBHDF5IO("test_edit.nwb", "r+") as io:
    nwbfile = io.read()
    nwbfile.acquisition["synthetic_timeseries"].data[:10] = 0.0
```

**Example:** Editing the attributes of a dataset.

```python
with NWBHDF5IO("test_edit.nwb", "r+") as io:
    nwbfile = io.read()
    nwbfile.acquisition["synthetic_timeseries"].data.attrs["unit"] = "volts"
```

#### Changing the shape of a dataset

Whether it is possible to change the shape of a dataset depends on how the dataset was created. If the dataset was created with a flexible shape (using the `maxshape` argument of the `H5DataIO` class constructor), then it is possible to change it in-place.  Using a `None` value for a component of the `maxshape` tuple allows the size of the corresponding dimension to grow. Chunking is required for datasets with flexible shapes.

**Example:** Creating an NWB file with a dataset with a flexible shape.

```python
from hdmf.backends.hdf5.h5_utils import H5DataIO

nwbfile = NWBFile(
    session_description="my first synthetic recording",
    identifier="EXAMPLE_ID",
    session_start_time=datetime.now(tzlocal()),
    session_id="LONELYMTN",
)

data_io = H5DataIO(data=np.random.randn(100, 100), maxshape=(None, 100))

nwbfile.add_acquisition(
    TimeSeries(
        name="synthetic_timeseries",
        description="Random values",
        data=data_io,
        unit="m",
        rate=10e3,
    )
)

with NWBHDF5IO("test_edit2.nwb", "w") as io:
    io.write(nwbfile)
```

**Example:** Resizing the dataset when the first dimension is unlimited.

```python
with NWBHDF5IO("test_edit2.nwb", "r+") as io:
    nwbfile = io.read()
    nwbfile.acquisition["synthetic_timeseries"].data.resize((200, 100))
```

**Note:** Dataset edits that cannot be done in-place: changing the shape of a dataset with a fixed shape, or changing the datatype, compression, chunking, max-shape, or fill-value of a dataset. For any of these, use the :py:class:`pynwb.NWBHDF5IO.export` method to export the data to a new file.

### Editing groups

Editing of groups is not yet directly supported in PyNWB. To edit the attributes of a group, use `h5py`.

**Example:** Editing the attributes of a group using `h5py`.

```python
import h5py

with h5py.File("test_edit.nwb", "r+") as f:
    f["acquisition"]["synthetic_timeseries"].attrs["description"] = "Random values in volts"
```

**Warning:** Be careful not to edit values that will bring the file out of compliance with the NWB specification.

#### Renaming groups and datasets

Rename groups and datasets in-place using the :py:meth:`~h5py.Group.move` method.

**Example:** Renaming a group.

```python
import h5py

with h5py.File("test_edit.nwb", "r+") as f:
    f["acquisition"].move("synthetic_timeseries", "synthetic_timeseries_renamed")
```

**Example:** Moving a group to a different location in the file.

```python
with h5py.File("test_edit.nwb", "r+") as f:
    f["acquisition"].move(
        "synthetic_timeseries_renamed",
        "/analysis/synthetic_timeseries_renamed",
    )
```

### Adding datasets to existing groups

You can add new datasets to existing groups using PyNWB by calling `set_modified()`.

**Example:** Adding a genotype to a Subject.

```python
from pynwb import NWBFile, NWBHDF5IO
from pynwb.file import Subject
from datetime import datetime
from dateutil.tz import tzlocal

# Create a file with a Subject that is missing the genotype
nwbfile = NWBFile(
    session_description="example file with subject",
    identifier="EXAMPLE_ID",
    session_start_time=datetime.now(tzlocal()),
    session_id="LONELYMTN",
    subject=Subject(
        subject_id="mouse001",
        species="Mus musculus",
        age="P30D",
    )
)

with NWBHDF5IO("test_edit3.nwb", "w") as io:
    io.write(nwbfile)

# Add the genotype using PyNWB and set_modified()
with NWBHDF5IO("test_edit3.nwb", "a") as io:
    nwbfile = io.read()
    nwbfile.subject.genotype = "Sst-IRES-Cre"
    nwbfile.subject.set_modified()  # Required to mark the container as modified
    io.write(nwbfile)

# Verify the dataset was added
with NWBHDF5IO("test_edit3.nwb", "r") as io:
    nwbfile = io.read()
    print(f"Subject genotype: {nwbfile.subject.genotype}")
```
