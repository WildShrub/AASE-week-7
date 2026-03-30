#!/usr/bin/env python3
"""Start the Change Reviewer A2A agent server."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import uvicorn
from agents.change_reviewer import ChangeReviewerAgent
from config import CHANGE_REVIEWER_PORT

agent = ChangeReviewerAgent()

if __name__ == "__main__":
    uvicorn.run(agent.app, host="0.0.0.0", port=CHANGE_REVIEWER_PORT, log_level="info")
