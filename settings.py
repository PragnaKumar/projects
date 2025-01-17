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

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
WEBCAM = 'Webcam'

SOURCES_LIST = [IMAGE, VIDEO, WEBCAM]

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / r'C:\Users\rrk\projects\P&ID-diagram-analysis\P&ID-diagram-analysis\original.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / r'C:\Users\rrk\projects\P&ID-diagram-analysis\P&ID-diagram-analysis\result.jpg'

# Videos config
VIDEO_DIR = ROOT / 'videos'
VIDEO_1_PATH = VIDEO_DIR / r'D:\Projects\steel_bar_analysis\video_1.mp4' #add the correct path
VIDEO_2_PATH = VIDEO_DIR / r'D:\Projects\steel_bar_analysis\video_2.mp4'
VIDEO_3_PATH = VIDEO_DIR / r'D:\Projects\steel_bar_analysis\video_3.mp4'
VIDEOS_DICT = {
    'video_1': VIDEO_1_PATH,
    'video_2': VIDEO_2_PATH,
    'video_3': VIDEO_3_PATH,
}

# ML Model config
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL =  MODEL_DIR / r'C:\Users\rrk\projects\P&ID-diagram-analysis\P&ID-diagram-analysis\best.pt'

# Webcam
WEBCAM_PATH = 0
