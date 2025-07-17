import struct
from typing import Tuple, Optional
from crafto_editor.config import PROGRESSION_LABEL, FLOAT_SIZE, SCAN_WINDOW, MAX_EXPECTED

def find_progression_value_and_offset(data: bytes) -> Tuple[Optional[float], Optional[int]]:
    """
    Scan `data` for the progression label + an adjacent 8‑byte float.
    Returns (value, offset) or (None, None) if not found.
    """
    idx = data.find(PROGRESSION_LABEL)
    if idx == -1:
        return None, None

    start = idx + len(PROGRESSION_LABEL)
    for off in range(start, start + SCAN_WINDOW):
        if off + FLOAT_SIZE > len(data):
            break
        val = struct.unpack("<d", data[off:off + FLOAT_SIZE])[0]
        if 0.0 < val <= MAX_EXPECTED:
            return val, off

    return None, None
