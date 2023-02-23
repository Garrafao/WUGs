# DURel System

This folder contains any files relevant for the [DURel Annotation System](https://www.ims.uni-stuttgart.de/data/durel-tool).

It currently contains these folders with test data:

- `test_english`: English annotation data, large number of uses and annotations
- `test_errors`: erroneous data to avoid bugs in the system:
    - `uses/blockera.csv` contains target word and sentence indices exceeding the number of characters in context
- `test_project`: English annotation data, very small
- `test_uug`: German annotation data, mix of words with large and small numbers of uses and annotations, contains Umlauts
