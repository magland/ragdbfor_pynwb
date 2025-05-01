# PyNWB Extension Tutorial

## Creating Extensions

PyNWB allows for creating Neurodata Extensions (NDX) to extend the NWB format:

```python
from pynwb.spec import NWBAttributeSpec, NWBGroupSpec, NWBNamespaceBuilder

# Create namespace files
ns_path = "mylab.namespace.yaml"
ext_source = "mylab.extensions.yaml"

# Initialize namespace builder
ns_builder = NWBNamespaceBuilder("Extension for use in my Lab", "mylab", version="0.1.0")
ns_builder.include_namespace("core")

# Define a new type that extends ElectricalSeries
ext = NWBGroupSpec(
    "A custom ElectricalSeries for my lab",
    attributes=[NWBAttributeSpec("trode_id", "the tetrode id", "int")],
    neurodata_type_inc="ElectricalSeries",
    neurodata_type_def="TetrodeSeries",
)

# Add spec and export
ns_builder.add_spec(ext_source, ext)
ns_builder.export(ns_path)
```

## Using Extensions

After creating an extension, you can use it in two ways:

### 1. Creating custom container classes

```python
from hdmf.utils import docval, get_docval, popargs
from pynwb import load_namespaces, register_class
from pynwb.ecephys import ElectricalSeries

# Load the namespace
load_namespaces("mylab.namespace.yaml")

# Create and register a class
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

### 2. Using dynamic class generation

```python
from pynwb import get_class, load_namespaces

load_namespaces("mylab.namespace.yaml")
AutoTetrodeSeries = get_class("TetrodeSeries", "mylab")
```

## Creating a MultiContainerInterface Extension

For groups that hold multiple objects of the same type:

```python
# Define specs
potato = NWBGroupSpec(
    neurodata_type_def="Potato",
    neurodata_type_inc="NWBDataInterface",
    doc="A potato",
    quantity="*",
    attributes=[
        NWBAttributeSpec(name="weight", doc="weight of potato", dtype="float", required=True),
        NWBAttributeSpec(name="age", doc="age of potato", dtype="float", required=False),
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

# Create container classes
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

## Example: Cortical Surface Mesh

Creating a more complex extension for a cortical surface mesh:

```python
# Define specs
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

# Usage example
load_namespaces("ecog.namespace.yaml")
CorticalSurface = get_class("CorticalSurface", "ecog")

cortical_surface = CorticalSurface(
    vertices=[[0.0, 1.0, 1.0], [1.0, 1.0, 2.0], [2.0, 2.0, 1.0], [2.0, 1.0, 1.0], [1.0, 2.0, 1.0]],
    faces=np.array([[0, 1, 2], [1, 2, 3]]).astype("uint"),
    name="cortex",
)
```

## Caching Extensions to File

By default, extensions are cached with the NWB file:

```python
# Write an NWB file with custom extensions
io = NWBHDF5IO("example.nwb", mode="w")
io.write(nwbfile)
io.close()

# When reading, PyNWB loads the cached namespace by default
# To disable, set load_namespaces=False in the constructor
with NWBHDF5IO("example.nwb", "r") as io:
    nwb = io.read()
```