from typing import Tuple, TypeVar

import numpy as np

T = TypeVar("T", bound=np.generic, covariant=True)

Vector = np.ndarray[Tuple[int], np.dtype[T]]
ColumnVector = np.ndarray[Tuple[Tuple[int]], np.dtype[T]]

Matrix = np.ndarray[Tuple[int, int], np.dtype[T]]
Tensor = np.ndarray[Tuple[int, ...], np.dtype[T]]

# https://stackoverflow.com/a/75499982
