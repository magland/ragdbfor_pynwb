This document describes how to iteratively write data to NWB files using pynwb, which is useful for handling large datasets, streaming data, and sparse data arrays.

**Key Concepts:**

*   **Iterative Data Write:** Writing data incrementally instead of all at once.
*   **:py:class:`~hdmf.data_utils.DataChunk`:** A data structure representing a subset (chunk) of a larger array, containing the data (`DataChunk.data`) and its location (`DataChunk.selection`).
*   **:py:class:`~hdmf.data_utils.AbstractDataChunkIterator`:** An abstract class for iterating over large data arrays, one chunk at a time.
*   **:py:class:`~hdmf.data_utils.DataChunkIterator`:** A concrete implementation of `AbstractDataChunkIterator` optimized for iterating over the first dimension of an array where the elements are yielded in consecutive order. Can buffer data to improve performance.
*   **:py:class:`~hdmf.data_utils.GenericDataChunkIterator`:** A semi-abstract implementation that automatically handles buffer regions and communication of compatible chunk regions. Useful when users specify chunk and buffer shapes/sizes and the iterator should handle how the data is broken up.
*   **:py:class:`~hdmf.backends.hdf5.h5_utils.H5DataIO`:** Used to configure advanced HDF5 dataset I/O features such as compression, chunking and `fillvalue`.
*   **:py:class:`~pynwb.NWBHDF5IO`:** The standard class for NWB file I/O via hdf5

**Workflow:**

1.  **Create a Data Chunk Iterator:** Wrap your data (e.g., from a generator, stream, or file) in an `AbstractDataChunkIterator` or use `DataChunkIterator` for simple cases or `GenericDataChunkIterator` for semi-abstract chunk management. This iterator yields `DataChunk` objects.
2.  **Write the Data:** Pass the data chunk iterator as the `data` argument when creating a `TimeSeries` or other data object.  PyNWB will then write the data iteratively.

**Examples:**

1.  **Writing Data from a Generator:**

    *   Define a data generator (e.g., `iter_sin` that yields chunks of sine wave samples).
    *   Wrap the generator with `DataChunkIterator(data=your_generator)`.
    *   Create a `TimeSeries` object, passing the `DataChunkIterator` as the `data` argument.
    *   Write the `TimeSeries` to an NWB file using `NWBHDF5IO`.
        ```python
        from hdmf.data_utils import DataChunkIterator
        from pynwb import NWBHDF5IO, NWBFile, TimeSeries
        from datetime import datetime
        from uuid import uuid4
        from dateutil.tz import tzlocal
        import numpy as np
        from math import pi, sin
        from random import random

        def iter_sin(chunk_length=10, max_chunks=100):
            x = 0
            num_chunks = 0
            while x < 0.5 and num_chunks < max_chunks:
                val = np.asarray([sin(random() * 2 * pi) for i in range(chunk_length)])
                x = random()
                num_chunks += 1
                yield val

        data = DataChunkIterator(data=iter_sin(10))

        start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())
        nwbfile = NWBFile(
            session_description="demonstrate iterative write",
            identifier=str(uuid4()),
            session_start_time=start_time,
        )

        # Create our time series
        test_ts = TimeSeries(
            name="synthetic_timeseries",
            data=data,
            unit="n/a",
            rate=1.0,
        )
        nwbfile.add_acquisition(test_ts)

        # Write the data to file
        io = NWBHDF5IO("basic_iterwrite_example.nwb", "w")
        io.write(nwbfile)
        io.close()
        ```
2.  **Optimizing Sparse Data Array I/O and Storage:**

    *   Create a custom `AbstractDataChunkIterator` (e.g., `SparseMatrixIterator`) that generates chunks of data at random locations, mimicking a sparse matrix. The example explicitly sets the data type, full array shape, and recommends a chunk shape.
    *   Optionally, wrap the `SparseMatrixIterator` with `H5DataIO` to enable compression, customized chunking, and `fillvalue`.
    *   Write the data as usual, by creating an NWBFile and TimeSeries with the iterator in the `data` field for timeseries and writing the file using the io.write command.
        ```python
        from hdmf.data_utils import AbstractDataChunkIterator, DataChunk

        class SparseMatrixIterator(AbstractDataChunkIterator):
            def __init__(self, shape, num_chunks, chunk_shape):
                self.shape, self.num_chunks, self.chunk_shape = shape, num_chunks, chunk_shape
                self.__chunks_created = 0

            def __iter__(self):
                return self

            def __next__(self):
                if self.__chunks_created < self.num_chunks:
                    data = np.random.rand(np.prod(self.chunk_shape)).reshape(self.chunk_shape)
                    xmin = (
                        np.random.randint(0, int(self.shape[0] / self.chunk_shape[0]), 1)[0]
                        * self.chunk_shape[0]
                    )
                    xmax = xmin + self.chunk_shape[0]
                    ymin = (
                        np.random.randint(0, int(self.shape[1] / self.chunk_shape[1]), 1)[0]
                        * self.chunk_shape[1]
                    )
                    ymax = ymin + self.chunk_shape[1]
                    self.__chunks_created += 1
                    return DataChunk(data=data, selection=np.s_[xmin:xmax, ymin:ymax])
                else:
                    raise StopIteration

            next = __next__

            def recommended_chunk_shape(self):
                return self.chunk_shape

            def recommended_data_shape(self):
                return self.shape

            @property
            def dtype(self):
                return np.dtype(float)

            @property
            def maxshape(self):
                return self.shape

        data = SparseMatrixIterator(
            shape=(1000, 1000), num_chunks=100, chunk_shape=(10, 10)
        )

        from pynwb import NWBHDF5IO, NWBFile, TimeSeries
        from datetime import datetime
        from uuid import uuid4
        from dateutil.tz import tzlocal

        start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())
        nwbfile = NWBFile(
            session_description="demonstrate iterative write",
            identifier=str(uuid4()),
            session_start_time=start_time,
        )

        # Create our time series
        test_ts = TimeSeries(
            name="synthetic_timeseries",
            data=data,
            unit="n/a",
            rate=1.0,
        )
        nwbfile.add_acquisition(test_ts)

        # Write the data to file
        io = NWBHDF5IO("basic_sparse_iterwrite_example.nwb", "w")
        io.write(nwbfile)
        io.close()
        ```
3.  **Convert Large Binary Data Arrays:**

    *   Create a generator (e.g., `iter_largearray`) or derive a custom class from :py:class:`~hdmf.data_utils.AbstractDataChunkIterator` that reads data from a file one chunk at a time.
    *   Wrap the generator with `DataChunkIterator`, setting `maxshape` to the full array shape and adjusting `buffer_size` as needed.
    *   Alternatively, for controlling how HDF5 file is written, wrap the data iterator with `H5DataIO`.
    *   Write the data to an NWB file.
4.  **Convert Arrays Stored in Multiple Files:**

    *   Create a custom `AbstractDataChunkIterator` (e.g., `MultiFileArrayIterator`) that iterates over multiple files, each containing a portion of the data (e.g., one file per channel).
    *   Implement the `__next__` method to read data from the current file and return a `DataChunk` with the appropriate selection.
    *   Write the data to an NWB file.

**Alternative Approach: User-Defined Dataset Write**

1.  Create an NWB file and allocate the dataset with H5DataIO using `shape`, `maxshape`, `chunks`, `compression`, and other parameters. Leave a `fillvalue` such as `np.nan` if data will be written partially.
2.  Get the dataset to be updated in the NWBFile. For example retrieve the dataset object from a timeseries with `nwbfile.get_acquisition("synthetic_timeseries").data`.
3.  Directly write to the dataset with numpy-style indexing setting the data in chunks (e.g. assign to `dataset[0:3, :] = 1`).
4.  Close the file to flush changes.

**Important Considerations:**

*   **Chunk Size:**  Choose chunk sizes carefully to balance memory usage, I/O performance, and storage efficiency.
*   **Data Alignment:** Ensure that the shape of `DataChunk` objects and the chunking of the HDF5 dataset are compatible.
*   **h5py Compatibility:**  The selection used in `DataChunk` must be supported by h5py.
*   **Memory Usage:** While iterative writing avoids loading the entire dataset into memory, intermediate representations are still dense numpy arrays on read.
*   When using auto chunking make sure to set the recommended_data_shape to help h5py make an accurate guess on the chunk sizes.
