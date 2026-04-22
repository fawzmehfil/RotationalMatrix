from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Wireframe:
    """
    A simple wireframe: vertices (Nx3) and edges (Mx2 indices).
    """

    vertices: np.ndarray
    edges: np.ndarray

    def __post_init__(self) -> None:
        v = np.asarray(self.vertices, dtype=float)
        e = np.asarray(self.edges, dtype=int)
        if v.ndim != 2 or v.shape[1] != 3:
            raise ValueError("vertices must be Nx3")
        if e.ndim != 2 or e.shape[1] != 2:
            raise ValueError("edges must be Mx2")
        object.__setattr__(self, "vertices", v)
        object.__setattr__(self, "edges", e)


def cube(size: float = 100.0) -> Wireframe:
    s = float(size)
    v = np.array(
        [
            [s, s, s],
            [s, -s, s],
            [-s, -s, s],
            [-s, s, s],
            [s, s, -s],
            [s, -s, -s],
            [-s, -s, -s],
            [-s, s, -s],
        ],
        dtype=float,
    )
    e = np.array(
        [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4],
            [0, 4],
            [1, 5],
            [2, 6],
            [3, 7],
        ],
        dtype=int,
    )
    return Wireframe(vertices=v, edges=e)


def tetrahedron(size: float = 120.0) -> Wireframe:
    s = float(size)
    v = np.array(
        [
            [s, s, s],
            [s, -s, -s],
            [-s, s, -s],
            [-s, -s, s],
        ],
        dtype=float,
    )
    e = np.array(
        [
            [0, 1],
            [0, 2],
            [0, 3],
            [1, 2],
            [1, 3],
            [2, 3],
        ],
        dtype=int,
    )
    return Wireframe(vertices=v, edges=e)


def axes(length: float = 150.0) -> Wireframe:
    length_val = float(length)
    v = np.array(
        [
            [0.0, 0.0, 0.0],
            [length_val, 0.0, 0.0],
            [0.0, length_val, 0.0],
            [0.0, 0.0, length_val],
        ],
        dtype=float,
    )
    e = np.array([[0, 1], [0, 2], [0, 3]], dtype=int)
    return Wireframe(vertices=v, edges=e)


def shape_by_name(name: str, size: float) -> Wireframe:
    n = name.strip().lower()
    if n in {"cube", "box"}:
        return cube(size=size)
    if n in {"tetra", "tetrahedron"}:
        return tetrahedron(size=size)
    if n in {"axes", "axis"}:
        return axes(length=size)
    raise ValueError(f"unknown shape: {name!r}")

