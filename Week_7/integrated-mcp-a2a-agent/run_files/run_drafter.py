"""Start the Drafter A2A agent server."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import uvicorn
from agents.drafter import DrafterAgent
from config import DRAFTER_PORT

agent = DrafterAgent()

if __name__ == "__main__":
    uvicorn.run(agent.app, host="0.0.0.0", port=DRAFTER_PORT, log_level="info")