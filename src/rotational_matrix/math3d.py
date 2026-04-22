from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def _deg2rad(deg: float) -> float:
    return deg * math.pi / 180.0


def euler_xyz_to_matrix(x_deg: float, y_deg: float, z_deg: float) -> np.ndarray:
    """
    Build a 3x3 rotation matrix from intrinsic XYZ Euler angles (degrees).
    Equivalent to applying X then Y then Z rotations to a point.
    """
    cx, sx = math.cos(_deg2rad(x_deg)), math.sin(_deg2rad(x_deg))
    cy, sy = math.cos(_deg2rad(y_deg)), math.sin(_deg2rad(y_deg))
    cz, sz = math.cos(_deg2rad(z_deg)), math.sin(_deg2rad(z_deg))

    rx = np.array([[1.0, 0.0, 0.0], [0.0, cx, -sx], [0.0, sx, cx]])
    ry = np.array([[cy, 0.0, sy], [0.0, 1.0, 0.0], [-sy, 0.0, cy]])
    rz = np.array([[cz, -sz, 0.0], [sz, cz, 0.0], [0.0, 0.0, 1.0]])

    # Apply X then Y then Z: p' = Rz * Ry * Rx * p
    return rz @ ry @ rx


def axis_angle_to_matrix(axis: np.ndarray, angle_deg: float) -> np.ndarray:
    """Rodrigues' rotation formula for a unit axis and degrees."""
    axis = np.asarray(axis, dtype=float).reshape(3)
    norm = np.linalg.norm(axis)
    if norm == 0:
        raise ValueError("axis must be non-zero")
    x, y, z = axis / norm
    theta = _deg2rad(angle_deg)
    c, s = math.cos(theta), math.sin(theta)
    C = 1.0 - c
    return np.array(
        [
            [x * x * C + c, x * y * C - z * s, x * z * C + y * s],
            [y * x * C + z * s, y * y * C + c, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, z * z * C + c],
        ],
        dtype=float,
    )


def rotate_points_matrix(points: np.ndarray, r: np.ndarray) -> np.ndarray:
    """Rotate Nx3 points using 3x3 rotation matrix."""
    p = np.asarray(points, dtype=float)
    if p.ndim != 2 or p.shape[1] != 3:
        raise ValueError("points must be Nx3")
    r = np.asarray(r, dtype=float)
    if r.shape != (3, 3):
        raise ValueError("r must be 3x3")
    return (r @ p.T).T


@dataclass(frozen=True)
class Quaternion:
    """(w, x, y, z) quaternion."""

    w: float
    x: float
    y: float
    z: float

    def as_array(self) -> np.ndarray:
        return np.array([self.w, self.x, self.y, self.z], dtype=float)


def quaternion_normalize(q: Quaternion) -> Quaternion:
    a = q.as_array()
    n = float(np.linalg.norm(a))
    if n == 0:
        raise ValueError("cannot normalize zero quaternion")
    a /= n
    return Quaternion(float(a[0]), float(a[1]), float(a[2]), float(a[3]))


def quaternion_multiply(a: Quaternion, b: Quaternion) -> Quaternion:
    aw, ax, ay, az = a.w, a.x, a.y, a.z
    bw, bx, by, bz = b.w, b.x, b.y, b.z
    return Quaternion(
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    )


def quaternion_to_matrix(q: Quaternion) -> np.ndarray:
    q = quaternion_normalize(q)
    w, x, y, z = q.w, q.x, q.y, q.z
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ],
        dtype=float,
    )


def matrix_to_quaternion(r: np.ndarray) -> Quaternion:
    """Convert a proper rotation matrix to a unit quaternion."""
    r = np.asarray(r, dtype=float)
    if r.shape != (3, 3):
        raise ValueError("r must be 3x3")

    t = float(np.trace(r))
    if t > 0:
        s = math.sqrt(t + 1.0) * 2.0
        w = 0.25 * s
        x = (r[2, 1] - r[1, 2]) / s
        y = (r[0, 2] - r[2, 0]) / s
        z = (r[1, 0] - r[0, 1]) / s
    else:
        i = int(np.argmax([r[0, 0], r[1, 1], r[2, 2]]))
        if i == 0:
            s = math.sqrt(1.0 + r[0, 0] - r[1, 1] - r[2, 2]) * 2.0
            w = (r[2, 1] - r[1, 2]) / s
            x = 0.25 * s
            y = (r[0, 1] + r[1, 0]) / s
            z = (r[0, 2] + r[2, 0]) / s
        elif i == 1:
            s = math.sqrt(1.0 + r[1, 1] - r[0, 0] - r[2, 2]) * 2.0
            w = (r[0, 2] - r[2, 0]) / s
            x = (r[0, 1] + r[1, 0]) / s
            y = 0.25 * s
            z = (r[1, 2] + r[2, 1]) / s
        else:
            s = math.sqrt(1.0 + r[2, 2] - r[0, 0] - r[1, 1]) * 2.0
            w = (r[1, 0] - r[0, 1]) / s
            x = (r[0, 2] + r[2, 0]) / s
            y = (r[1, 2] + r[2, 1]) / s
            z = 0.25 * s

    return quaternion_normalize(Quaternion(float(w), float(x), float(y), float(z)))


def quaternion_rotate_points(points: np.ndarray, q: Quaternion) -> np.ndarray:
    """Rotate Nx3 points by quaternion (via matrix conversion)."""
    return rotate_points_matrix(points, quaternion_to_matrix(q))

