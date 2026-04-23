import sys
from pathlib import Path

_api = Path(__file__).resolve().parent.parent / "api"
if str(_api) not in sys.path:
    sys.path.insert(0, str(_api))
