from pathlib import Path
import sys


# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
ROOT = root_path.relative_to(Path.cwd())

# # Sources
# IMAGE = 'Image'

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / r'C:\Users\rrk\OneDrive\Desktop\sem-end-projects\Intelligent-Analytics\pneumonia-yolo\original.jpg' #add the correct location
DEFAULT_DETECT_IMAGE = IMAGES_DIR / r'C:\Users\rrk\OneDrive\Desktop\sem-end-projects\Intelligent-Analytics\pneumonia-yolo\result.jpg' #add the correct location

# ML Model config
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL =  MODEL_DIR / r'C:\Users\rrk\OneDrive\Desktop\sem-end-projects\Intelligent-Analytics\pneumonia-yolo\best.pt' #add the correct location

