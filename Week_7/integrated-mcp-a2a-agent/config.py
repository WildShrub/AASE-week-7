import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST  = os.getenv("OLLAMA_HOST",  "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")

MCP_PORT     = int(os.getenv("MCP_PORT", "8050"))
ANALYZER_PORT = int(os.getenv("ANALYZER_PORT", "8101"))
REVIEWER_PORT = int(os.getenv("REVIEWER_PORT", "8102"))

CHANGE_REVIEWER_PORT = int(os.getenv("CHANGE_REVIEWER_PORT", "8103"))
CRITIC_PORT = int(os.getenv("CRITIC_PORT", "8104"))
DRAFTER_PORT = int(os.getenv("DRAFTER_PORT", "8105"))
PLANNER_PORT = int(os.getenv("PLANNER_PORT", "8106"))
