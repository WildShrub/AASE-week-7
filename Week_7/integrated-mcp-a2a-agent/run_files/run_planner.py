"""Start the Planner A2A agent server."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import uvicorn
from agents.planner import PlannerAgent
from config import PLANNER_PORT

agent = PlannerAgent()

if __name__ == "__main__":
    uvicorn.run(agent.app, host="0.0.0.0", port=PLANNER_PORT, log_level="info")