import os
import getpass
import struct
from typing import List, Tuple, Optional
from crafto_editor.model import find_progression_value_and_offset

def get_save_dir() -> str:
    """Return the Craftomation101 save‑folder for the current user."""
    user = getpass.getuser()
    return os.path.join("C:\\", "Users", user, "AppData", "Roaming", "Craftomation101")

def list_save_files() -> List[str]:
    """List all files (no extension) in the save directory."""
    d = get_save_dir()
    if not os.path.isdir(d):
        return []
    return sorted(
        f for f in os.listdir(d)
        if os.path.isfile(os.path.join(d, f)) and os.path.splitext(f)[1] == ""
    )

def read_progression_points(path: str) -> Tuple[Optional[float], Optional[int]]:
    """Read raw bytes and return (value, offset)."""
    with open(path, "rb") as f:
        data = f.read()
    return find_progression_value_and_offset(data)

def write_progression_points(path: str, offset: int, new_value: float) -> None:
    """Overwrite the 8‑byte float at `offset` with `new_value`."""
    with open(path, "r+b") as f:
        f.seek(offset)
        f.write(struct.pack("<d", new_value))
