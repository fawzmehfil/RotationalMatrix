"""
Backwards-compatible entrypoint.

Prefer running the new CLI:
  python -m rotational_matrix.cli --shape cube --x 1 --y 2 --z 3
"""

# ruff: noqa: I001

from rotational_matrix.cli import main


if __name__ == "__main__":
    raise SystemExit(main())