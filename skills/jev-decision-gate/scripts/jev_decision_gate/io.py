"""Bounded local JSON I/O for CLI and a trusted MCP workspace."""
import json
from pathlib import Path


def read_json(path, root=None):
    path = Path(path)
    if root is not None:
        root = Path(root).resolve(strict=True)
        if path.is_absolute():
            raise ValueError("use paths relative to data_root")
        path = (root / path).resolve(strict=True)
        if not path.is_relative_to(root):
            raise ValueError("file must remain within data_root")
    if path.suffix != ".json":
        raise ValueError("only .json files are accepted")
    with path.open("rb") as stream:
        data = stream.read(8 * 1024 * 1024 + 1)
    if len(data) > 8 * 1024 * 1024:
        raise ValueError("JSON file exceeds 8 MiB")
    def invalid(value):
        raise ValueError("JSON must not contain non-finite numbers")
    return json.loads(data, parse_constant=invalid)


def write_json(path, value):
    # Do not accidentally replace an input, labels, an earlier report or policy.
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, allow_nan=False, indent=2)
        stream.write("\n")
