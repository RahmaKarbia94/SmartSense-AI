import sys
from pathlib import Path

SIMULATOR_DIR = Path(__file__).resolve().parent.parent / "simulator"
sys.path.insert(0, str(SIMULATOR_DIR))