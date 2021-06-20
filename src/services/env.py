from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
env_path = Path('../../') / '.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")
CLOUDFLARE_TOKEN = os.getenv("CLOUDFLARE_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
YANDEX_CLOUD_FOLDER_ID = os.getenv("YANDEX_CLOUD_FOLDER_ID")
CLOUDFLARE_ZONE = os.getenv("CLOUDFLARE_ZONE")
