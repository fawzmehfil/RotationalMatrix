## RotationalMatrix

A small Python project for **visualizing 3D rotation**.

It started life as a single script that rotated a hard-coded cube by applying X/Y/Z rotations every frame. I initially used this to learn Matplotlib and later expanded on it. This cleaned-up version turns that idea into a tiny, testable package with:

- **Rotation matrices** (Euler XYZ and axis-angle)
- **Quaternions** (for incremental “keep rotating forever” style updates)
- A simple **matplotlib wireframe viewer**
- A CLI (`rotmat`) so you can play with shapes and rotation parameters

### Quick start

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install -e '.[dev]'
```

Run the visualizer:

```bash
rotmat --shape cube --x 1 --y 2 --z 3
```

Or without installing the CLI script:

```bash
python -m rotational_matrix.cli --shape cube --x 1 --y 2 --z 3
```

### Examples

- **Rotate a tetrahedron** at 60 FPS:

```bash
rotmat --shape tetrahedron --fps 60 --x 0.5 --y 1.0 --z 1.5
```

- **Axis-angle rotation** around the axis \( (1, 1, 0) \):

```bash
rotmat --mode axis-angle --axis 1,1,0 --axis-deg 2.5 --shape cube
```

- **Quaternion mode** (incremental rotation per frame):

```bash
rotmat --mode quaternion --shape cube --x 1 --y 2 --z 3
```

### What’s in the codebase

- **`src/rotational_matrix/math3d.py`**: rotation math (Euler → matrix, axis-angle → matrix, quaternion helpers)
- **`src/rotational_matrix/shapes.py`**: simple wireframe shapes (cube, tetrahedron, axes)
- **`src/rotational_matrix/visualize.py`**: matplotlib animation loop (`FuncAnimation`)
- **`src/rotational_matrix/cli.py`**: argparse-powered CLI
- **`tests/`**: a few quick sanity tests (orthonormal matrices, norm preservation, matrix↔quaternion roundtrip)

### Notes / design choices

- **Why numpy?** It keeps the math clear and makes it easy to rotate an entire point set at once.
- **Why multiple modes?**
  - *Euler* is straightforward and matches how the original project worked.
  - *Quaternion* mode is useful for incremental updates (apply a small “step rotation” repeatedly).
  - *Axis-angle* is a nice middle ground that’s compact and intuitive.

### Dev checks

With the venv active:

```bash
ruff check .
pytest
```
