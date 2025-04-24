Zarr is an alternative backend for NWB files, suitable for large datasets and parallel computing. It supports chunked, compressed, N-dimensional arrays. Zarr's native storage is optimized for cloud storage (e.g., S3).

To use Zarr, install the `hdmf-zarr` package.

**Writing to Zarr:**

1.  Create an `NWBFile` using PyNWB.

2.  Configure datasets using `ZarrDataIO` instead of `H5DataIO` to leverage chunking and compression. Specify compressors from the `numcodecs` library.

    ```python
    from numcodecs import Blosc
    from hdmf_zarr import ZarrDataIO
    import numpy as np

    data_with_zarr_data_io = ZarrDataIO(
        data=np.random.randn(100, 100),
        chunks=(10, 10),
        fillvalue=0,
        compressor=Blosc(cname='zstd', clevel=3, shuffle=Blosc.SHUFFLE)
    )
    ```

3.  Add the dataset (e.g., a `TimeSeries`) to the `NWBFile`.

    ```python
    from pynwb import TimeSeries
    nwbfile.add_acquisition(
        TimeSeries(
            name="synthetic_timeseries",
            data=data_with_zarr_data_io,
            unit="m",
            rate=10e3,
        )
    )
    ```

4.  Write the `NWBFile` to a Zarr file using `NWBZarrIO`, replacing `NWBHDF5IO`.

    ```python
    from hdmf_zarr.nwb import NWBZarrIO
    import os

    path = "zarr_tutorial.nwb.zarr"
    absolute_path = os.path.abspath(path)  # Use absolute path for testing
    with NWBZarrIO(path=path, mode="w") as io:
        io.write(nwbfile)
    ```

**Reading from Zarr:**

1.  Read the NWB file from Zarr using `NWBZarrIO`.

    ```python
    from hdmf_zarr.nwb import NWBZarrIO

    with NWBZarrIO(path=absolute_path, mode="r") as io:
        read_nwbfile = io.read()
    ```
