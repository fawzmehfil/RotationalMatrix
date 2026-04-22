from __future__ import annotations

import argparse

from .shapes import shape_by_name
from .visualize import AnimationConfig, animate_wireframe


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="rotmat",
        description="Rotate a simple 3D wireframe using rotation matrices.",
    )
    p.add_argument("--shape", default="cube", help="cube | tetrahedron | axes")
    p.add_argument("--size", type=float, default=100.0, help="Shape size (units)")
    p.add_argument("--fps", type=int, default=60, help="Animation FPS")
    p.add_argument(
        "--steps",
        type=int,
        default=None,
        help="Number of frames (default: run until closed)",
    )

    p.add_argument("--x", type=float, default=1.0, help="Degrees per step around X")
    p.add_argument("--y", type=float, default=1.0, help="Degrees per step around Y")
    p.add_argument("--z", type=float, default=1.0, help="Degrees per step around Z")

    p.add_argument(
        "--mode",
        default="euler",
        help="euler | quaternion | axis-angle",
    )
    p.add_argument(
        "--axis",
        default="0,1,0",
        help="Axis for axis-angle mode, as 'x,y,z' (default: 0,1,0)",
    )
    p.add_argument(
        "--axis-deg",
        type=float,
        default=2.0,
        help="Degrees per step in axis-angle mode",
    )

    p.add_argument("--limits", type=float, default=175.0, help="Plot axis limits")
    p.add_argument("--title", default="Rotation Matrix Visual", help="Figure title")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    shape = shape_by_name(args.shape, size=args.size)
    axis_parts = [p.strip() for p in str(args.axis).split(",")]
    if len(axis_parts) != 3:
        raise SystemExit("--axis must be 'x,y,z'")
    axis = (float(axis_parts[0]), float(axis_parts[1]), float(axis_parts[2]))
    cfg = AnimationConfig(
        fps=args.fps,
        steps=args.steps,
        x_deg_per_step=args.x,
        y_deg_per_step=args.y,
        z_deg_per_step=args.z,
        mode=args.mode,
        axis=axis,
        axis_deg_per_step=args.axis_deg,
        limits=args.limits,
        title=args.title,
    )
    animate_wireframe(shape, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
