Object IDs in NWB are UUID strings assigned to each NWB container object. Access the object ID using the `.object_id` attribute.

Example:

```python
from datetime import datetime
import numpy as np
from dateutil.tz import tzlocal
from pynwb import NWBFile, TimeSeries

# Create an NWBFile
start_time = datetime(2019, 4, 3, 11, tzinfo=tzlocal())
nwbfile = NWBFile(
    session_description="demonstrate NWB object IDs",
    identifier="NWB456",
    session_start_time=start_time,
)

# Create a TimeSeries object
timestamps = np.linspace(0, 100, 1024)
data = np.sin(0.333 * timestamps) + np.cos(0.1 * timestamps) + np.random.randn(len(timestamps))
test_ts = TimeSeries(name="raw_timeseries", data=data, unit="m", timestamps=timestamps)

# Add the TimeSeries to the NWBFile
nwbfile.add_acquisition(test_ts)

# Print the object ID of the NWBFile
print(nwbfile.object_id)

# Print the object ID of the TimeSeries
print(test_ts.object_id)
```

The `NWBFile` class has the `.objects` attribute, which is a dictionary of all neurodata_type objects in the `NWBFile`, indexed by each object's object ID. Iterate or access them like any other python dict.

```python
# Access the objects dictionary
print(nwbfile.objects)

# Iterate through the objects dictionary
for oid in nwbfile.objects:
    print(nwbfile.objects[oid])

for obj in nwbfile.objects.values():
    print('%s: %s "%s"' % (obj.object_id, obj.neurodata_type, obj.name))

# Access an object using its object ID
ts_id = test_ts.object_id
my_ts = nwbfile.objects[ts_id]  # test_ts == my_ts
```

Note: The object ID is NOT a unique hash of the data. If the contents of an NWB container change, the object ID remains the same.
