"""Start the Critic A2A agent server."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import uvicorn
from agents.critic import CriticAgent
from config import CRITIC_PORT

agent = CriticAgent()

if __name__ == "__main__":
    uvicorn.run(agent.app, host="0.0.0.0", port=CRITIC_PORT, log_level="info")