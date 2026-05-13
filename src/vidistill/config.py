from pathlib import Path

# Root paths
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
QUEUE_FILE = ROOT_DIR / "queue.txt"

# Data subdirectories
LECTURES_DIR = DATA_DIR / "lectures"

# Databases
DB_DIR = DATA_DIR / "db"
DB_PATH = DB_DIR / "vidistill.db"
CHROMA_PERSIST_DIR = DB_DIR / "chroma_db"
CHROMA_COLLECTION_NAME = "vidistill"

# FFmpeg / Extraction
INTRO_TRIM_SEC = 15
OUTRO_TRIM_SEC = 7
FRAME_SAMPLE_INTERVAL_SEC = 8
PHASE_DIFF_THRESHOLD = 10

# Mask (Teacher Region - Bottom Right)
MASK_HEIGHT_FRACTION = 0.49
MASK_WIDTH_FRACTION = 0.317

# Faster Whisper
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_VISION_MODEL = "moondream"
OLLAMA_LLM_MODEL = "qwen2.5:3b"
OLLAMA_TIMEOUT_SEC = 120

# Report
REPORT_FORMAT = "md"

# Naming
FOLDER_NAME_MAX_LEN = 50
