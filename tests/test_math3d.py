import numpy as np

from rotational_matrix.math3d import (
    Quaternion,
    euler_xyz_to_matrix,
    matrix_to_quaternion,
    quaternion_to_matrix,
    rotate_points_matrix,
)


def test_rotation_matrix_is_orthonormal() -> None:
    r = euler_xyz_to_matrix(10, 20, 30)
    should_be_i = r.T @ r
    assert np.allclose(should_be_i, np.eye(3), atol=1e-9)


def test_rotate_points_preserves_norms() -> None:
    points = np.array([[1.0, 2.0, 3.0], [-4.0, 0.5, 9.0]])
    r = euler_xyz_to_matrix(12, 34, 56)
    out = rotate_points_matrix(points, r)
    assert np.allclose(np.linalg.norm(out, axis=1), np.linalg.norm(points, axis=1))


def test_matrix_quaternion_roundtrip() -> None:
    r = euler_xyz_to_matrix(15, 25, 35)
    q = matrix_to_quaternion(r)
    r2 = quaternion_to_matrix(q)
    assert np.allclose(r, r2, atol=1e-8)


def test_quaternion_to_matrix_identity() -> None:
    r = quaternion_to_matrix(Quaternion(1.0, 0.0, 0.0, 0.0))
    assert np.allclose(r, np.eye(3))
