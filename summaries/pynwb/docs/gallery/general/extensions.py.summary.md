# Extending NWB

The NWB format can be extended through Neurodata Extensions (NDX).

## Defining extensions
Extensions should be defined separately from the code that uses them.
PyNWB provides functionality for creating and exporting such extensions.

The following example demonstrates how to create a new namespace and add a new `neurodata_type` to it, saving the extensions to disk for later use.

```python
from pynwb.spec import NWBAttributeSpec, NWBGroupSpec, NWBNamespaceBuilder

ns_path = "mylab.namespace.yaml"
ext_source = "mylab.extensions.yaml"

ns_builder = NWBNamespaceBuilder(
    "Extension for use in my Lab", "mylab", version="0.1.0"
)
ns_builder.include_namespace("core")

ext = NWBGroupSpec(
    "A custom ElectricalSeries for my lab",
    attributes=[NWBAttributeSpec("trode_id", "the tetrode id", "int")],
    neurodata_type_inc="ElectricalSeries",
    neurodata_type_def="TetrodeSeries",
)

ns_builder.add_spec(ext_source, ext)
ns_builder.export(ns_path)
```

This will generate two YAML files: `mylab.namespace.yaml` (containing namespace specifications) and `mylab.extensions.yaml` (containing details on newly defined types).

## Using extensions

After an extension has been created and the namespace file has been created, it can be used for reading and writing data using `pynwb`.

There are two ways to read and write extension data:
1.  Defining new `NWBContainer` classes that map to the `neurodata_types` in the extension.
2.  Using dynamically created `NWBContainer` subclasses.

The code in the following example defines a new `NWBContainer` class.

```python
from hdmf.utils import docval, get_docval, popargs
from pynwb import load_namespaces, register_class
from pynwb.ecephys import ElectricalSeries

ns_path = "mylab.namespace.yaml"
load_namespaces(ns_path)


@register_class("TetrodeSeries", "mylab")
class TetrodeSeries(ElectricalSeries):
    __nwbfields__ = ("trode_id",)

    @docval(
        *get_docval(ElectricalSeries.__init__)
        + ({"name": "trode_id", "type": int, "doc": "the tetrode id"},)
    )
    def __init__(self, **kwargs):
        trode_id = popargs("trode_id", kwargs)
        super().__init__(**kwargs)
        self.trode_id = trode_id
```

When extending `NWBContainer` subclasses, you should define the class field `__nwbfields__`.

If you do not want to write additional code to read your extensions, PyNWB is able to dynamically create an `NWBContainer` subclass for use within the PyNWB API.

```python
from pynwb import get_class, load_namespaces

ns_path = "mylab.namespace.yaml"
load_namespaces(ns_path)

AutoTetrodeSeries = get_class("TetrodeSeries", "mylab")
```

## Caching extensions to file

Extensions are cached to file by default, so the NWB file can carry the extensions needed to read the file. Here's how to create data using the extension and write the file:

```python
from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile

start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())
create_date = datetime(2017, 4, 15, 12, tzinfo=tzlocal())

nwbfile = NWBFile(
    "demonstrate caching", "NWB456", start_time, file_create_date=create_date
)

device = nwbfile.create_device(name="trodes_rig123")

electrode_name = "tetrode1"
description = "an example tetrode"
location = "somewhere in the hippocampus"

electrode_group = nwbfile.create_electrode_group(
    electrode_name, description=description, location=location, device=device
)
for idx in [1, 2, 3, 4]:
    nwbfile.add_electrode(
        id=idx,
        x=1.0,
        y=2.0,
        z=3.0,
        imp=float(-idx),
        location="CA1",
        filtering="none",
        group=electrode_group,
    )
electrode_table_region = nwbfile.create_electrode_table_region(
    [0, 2], "the first and third electrodes"
)

import numpy as np

rate = 10.0
np.random.seed(1234)
data_len = 1000
data = np.random.rand(data_len * 2).reshape((data_len, 2))
timestamps = np.arange(data_len) / rate

ts = TetrodeSeries(
    "test_ephys_data",
    data,
    electrode_table_region,
    timestamps=timestamps,
    trode_id=1,
    # Alternatively, could specify starting_time and rate as follows
    # starting_time=ephys_timestamps[0],
    # rate=rate,
    resolution=0.001,
    comments="This data was randomly generated with numpy, using 1234 as the seed",
    description="Random numbers generated with numpy.random.rand",
)
nwbfile.add_acquisition(ts)

from pynwb import NWBHDF5IO

io = NWBHDF5IO("cache_spec_example.nwb", mode="w")
io.write(nwbfile)
io.close()
```

You can prevent the caching of the specification by setting cache_spec=False in `io.write()`.

By default, if a namespace is not already loaded, PyNWB loads the namespace cached in the file. To disable this, set `load_namespaces=False` in the `NWBHDF5IO` constructor.

## Creating and using a custom MultiContainerInterface

This example defines a group (`PotatoSack`) that holds multiple objects (`Potato`). First use `pynwb` to define the new data types.

```python
from pynwb.spec import NWBAttributeSpec, NWBGroupSpec, NWBNamespaceBuilder

name = "test_multicontainerinterface"
ns_path = name + ".namespace.yaml"
ext_source = name + ".extensions.yaml"

ns_builder = NWBNamespaceBuilder(name + " extensions", name, version="0.1.0")
ns_builder.include_namespace("core")

potato = NWBGroupSpec(
    neurodata_type_def="Potato",
    neurodata_type_inc="NWBDataInterface",
    doc="A potato",
    quantity="*",
    attributes=[
        NWBAttributeSpec(
            name="weight", doc="weight of potato", dtype="float", required=True
        ),
        NWBAttributeSpec(
            name="age", doc="age of potato", dtype="float", required=False
        ),
    ],
)

potato_sack = NWBGroupSpec(
    neurodata_type_def="PotatoSack",
    neurodata_type_inc="NWBDataInterface",
    name="potato_sack",
    doc="A sack of potatoes",
    quantity="?",
    groups=[potato],
)

ns_builder.add_spec(ext_source, potato_sack)
ns_builder.export(ns_path)
```

Then create Container classes registered to the new data types

```python
from pynwb import load_namespaces, register_class
from pynwb.file import MultiContainerInterface, NWBContainer

load_namespaces(ns_path)


@register_class("Potato", name)
class Potato(NWBContainer):
    __nwbfields__ = ("name", "weight", "age")

    @docval(
        {"name": "name", "type": str, "doc": "who names a potato?"},
        {"name": "weight", "type": float, "doc": "weight of potato in grams"},
        {"name": "age", "type": float, "doc": "age of potato in days"},
    )
    def __init__(self, **kwargs):
        super().__init__(name=kwargs["name"])
        self.weight = kwargs["weight"]
        self.age = kwargs["age"]


@register_class("PotatoSack", name)
class PotatoSack(MultiContainerInterface):
    __clsconf__ = {
        "attr": "potatos",
        "type": Potato,
        "add": "add_potato",
        "get": "get_potato",
        "create": "create_potato",
    }
```

Then use the objects

```python
from datetime import datetime
from dateutil.tz import tzlocal

from pynwb import NWBHDF5IO, NWBFile

potato_sack = PotatoSack(potatos=Potato(name="potato1", age=2.3, weight=3.0))
potato_sack.add_potato(Potato("potato2", 3.0, 4.0))
potato_sack.create_potato("big_potato", 10.0, 20.0)

nwbfile = NWBFile(
    "a file with metadata", "NB123A", datetime(2018, 6, 1, tzinfo=tzlocal())
)

pmod = nwbfile.create_processing_module("module_name", "desc")
pmod.add_container(potato_sack)


with NWBHDF5IO("test_multicontainerinterface.nwb", "w") as io:
    io.write(nwbfile)
```

This is how you read the NWB file

```python
load_namespaces(ns_path)
with NWBHDF5IO("test_multicontainerinterface.nwb", "r") as io:
    nwb = io.read()
    print(nwb.get_processing_module()["potato_sack"].get_potato("big_potato").weight)
```

## Example: Cortical Surface Mesh

This example shows how to create extensions by creating a data class for a cortical surface mesh, which contains `vertices` (an (n, 3) matrix of floats) and `faces` (an (m, 3) matrix of uints).

```python
from pynwb.spec import NWBDatasetSpec, NWBGroupSpec, NWBNamespaceBuilder

name = "ecog"
ns_path = name + ".namespace.yaml"
ext_source = name + ".extensions.yaml"

surface = NWBGroupSpec(
    doc="brain cortical surface",
    datasets=[
        NWBDatasetSpec(
            doc="faces for surface, indexes vertices",
            shape=(None, 3),
            name="faces",
            dtype="uint",
            dims=("face_number", "vertex_index"),
        ),
        NWBDatasetSpec(
            doc="vertices for surface, points in 3D space",
            shape=(None, 3),
            name="vertices",
            dtype="float",
            dims=("vertex_number", "xyz"),
        ),
    ],
    neurodata_type_def="CorticalSurface",
    neurodata_type_inc="NWBDataInterface",
)

ns_builder = NWBNamespaceBuilder(name + " extensions", name, version="0.1.0")
ns_builder.add_spec(ext_source, surface)
ns_builder.export(ns_path)
```

Finally, we should test the new types to make sure they run as expected

```python
from datetime import datetime

import numpy as np

from pynwb import NWBHDF5IO, NWBFile, get_class, load_namespaces

load_namespaces("ecog.namespace.yaml")
CorticalSurface = get_class("CorticalSurface", "ecog")

cortical_surface = CorticalSurface(
    vertices=[
        [0.0, 1.0, 1.0],
        [1.0, 1.0, 2.0],
        [2.0, 2.0, 1.0],
        [2.0, 1.0, 1.0],
        [1.0, 2.0, 1.0],
    ],
    faces=np.array([[0, 1, 2], [1, 2, 3]]).astype("uint"),
    name="cortex",
)

nwbfile = NWBFile("my first synthetic recording", "EXAMPLE_ID", datetime.now())

cortex_module = nwbfile.create_processing_module(
    name="cortex", description="description"
)
cortex_module.add_container(cortical_surface)


with NWBHDF5IO("test_cortical_surface.nwb", "w") as io:
    io.write(nwbfile)
```