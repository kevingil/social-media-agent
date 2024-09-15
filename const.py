from dotenv import load_dotenv
import os

load_dotenv()

ROOT_DIR = os.path.abspath(os.curdir)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
