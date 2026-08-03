import os

_CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_ROOT = os.path.dirname(_CONFIG_DIR)
_PROJECT_ROOT = os.path.dirname(_SRC_ROOT)
_OUTPUT_ROOT = os.path.join(_PROJECT_ROOT, "out")

def output_root():
    os.makedirs(_OUTPUT_ROOT, exist_ok=True)
    return _OUTPUT_ROOT
