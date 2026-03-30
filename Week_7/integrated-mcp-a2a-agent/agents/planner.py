from agents.base import BaseA2AAgent, Task
from config import PLANNER_PORT


class PlannerAgent(BaseA2AAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Planner",
            description="Reviews analysis of code changes and decides next course of action.",
            skills=["Planning", "Deciding", "Github"],
            port=PLANNER_PORT,
        )

    async def handle(self, task: Task) -> str:
        analysis = task.context.strip()
        prompt = (
            "Given the analysis of the changes made, decide the best course of action listed below:\n"
            "1. Create a GitHub issue\n"
            "2. Create a GitHub pull request\n"
            "3. No action required\n"
            "Support all claims with evidence"
            f"analysis of changes: {analysis}"

        )
        return await self._loop.run(prompt, verbose=verbose)