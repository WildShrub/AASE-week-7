#Will basically be responsible for all of task 1
from pathlib import Path

from agents.base import BaseA2AAgent, Task
from config import CHANGE_REVIEWER_PORT
class ChangeReviewerAgent(BaseA2AAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Change_Reviewer",
            description="Reviews changes to Python code on Github for quality, style, and correctness issues.",
            skills=["code_review", "GitHub", "bug_detection"],
            port=CHANGE_REVIEWER_PORT,
        )

    async def handle(self, task: Task) -> str:
        range = task.message.strip()
        left, right = range.split("..", 1)
        start_ref = left      # "HEAD~3"
        end_ref = right       # "HEAD"

        print(start_ref, end_ref)

        beginning_section = (
            "Use the available tools to revise the previous analysis to address the issues in the critique. Then do the following:"
            f"Prior drafts and crtiques:\n{task.context}\n\n"
            if task.context else f"Use the git_diff tool to analyze the changes made to the code base from SHA {start_ref} to SHA {end_ref}.\n\n Then do the following:\n"
        )

        prompt = (
            f"{beginning_section}\n"
            "1. Identify potential issues or improvements\n"
            "2. Categorize change (feature, bugfix, refactor, etc.)\n"
            "3. Assess risk of bugs or code failure (low / medium / high)\n"
            "Support all claims with evidence from tools"
        )
        return await self.llm_call(prompt)