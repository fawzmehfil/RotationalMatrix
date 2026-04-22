from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from .math3d import (
    Quaternion,
    axis_angle_to_matrix,
    euler_xyz_to_matrix,
    matrix_to_quaternion,
    quaternion_multiply,
    quaternion_normalize,
    quaternion_to_matrix,
    rotate_points_matrix,
)
from .shapes import Wireframe


@dataclass(frozen=True)
class AnimationConfig:
    fps: int = 60
    steps: int | None = None
    x_deg_per_step: float = 1.0
    y_deg_per_step: float = 1.0
    z_deg_per_step: float = 1.0
    mode: str = "euler"
    axis: tuple[float, float, float] = (0.0, 1.0, 0.0)
    axis_deg_per_step: float = 2.0
    limits: float = 175.0
    title: str = "Rotation Matrix Visual"


def _draw_wireframe(ax, vertices: np.ndarray, edges: np.ndarray, *, color: str) -> None:
    for a, b in edges:
        xs = [vertices[a, 0], vertices[b, 0]]
        ys = [vertices[a, 1], vertices[b, 1]]
        zs = [vertices[a, 2], vertices[b, 2]]
        ax.plot(xs, ys, zs, color=color, linewidth=1.8)


def animate_wireframe(shape: Wireframe, cfg: AnimationConfig) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.set_title(cfg.title)

    base_vertices = np.asarray(shape.vertices, dtype=float)
    edges = np.asarray(shape.edges, dtype=int)

    def setup_axes() -> None:
        ax.set_xlim([-cfg.limits, cfg.limits])
        ax.set_ylim([-cfg.limits, cfg.limits])
        ax.set_zlim([-cfg.limits, cfg.limits])
        ax.set_box_aspect((1, 1, 1))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

    mode = cfg.mode.strip().lower()
    if mode not in {"euler", "quaternion", "axis-angle"}:
        raise ValueError("mode must be one of: euler, quaternion, axis-angle")

    step_r = euler_xyz_to_matrix(
        cfg.x_deg_per_step,
        cfg.y_deg_per_step,
        cfg.z_deg_per_step,
    )
    step_q = matrix_to_quaternion(step_r)
    q_accum = Quaternion(1.0, 0.0, 0.0, 0.0)

    axis = np.array(cfg.axis, dtype=float)

    def update(frame: int) -> None:
        ax.clear()
        setup_axes()
        ax.set_title(cfg.title)

        nonlocal q_accum
        if mode == "euler":
            r = euler_xyz_to_matrix(
                cfg.x_deg_per_step * frame,
                cfg.y_deg_per_step * frame,
                cfg.z_deg_per_step * frame,
            )
        elif mode == "axis-angle":
            r = axis_angle_to_matrix(axis, cfg.axis_deg_per_step * frame)
        else:
            if frame == 0:
                q_accum = Quaternion(1.0, 0.0, 0.0, 0.0)
            else:
                q_accum = quaternion_normalize(quaternion_multiply(q_accum, step_q))
            r = quaternion_to_matrix(q_accum)

        v = rotate_points_matrix(base_vertices, r)
        _draw_wireframe(ax, v, edges, color="tab:blue")

    interval_ms = int(1000 / max(1, cfg.fps))
    frames = cfg.steps if cfg.steps is not None else 10_000_000
    _ = FuncAnimation(fig, update, frames=frames, interval=interval_ms)
    plt.show()

