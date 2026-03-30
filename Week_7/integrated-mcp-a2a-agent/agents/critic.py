#will critique everything, and depending on the call, it will also offer suggestions.
from pathlib import Path

from agents.base import BaseA2AAgent, Task
from config import CRITIC_PORT
class CriticAgent(BaseA2AAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Critic",
            description="Critiques review drafts, pull request and issue drafts, and plans for quality, style, and correctness issues.",
            skills=["critique", "quality_assurance", "double_checking"],
            port=CRITIC_PORT,
        )

    async def handle(self, task: Task) -> str:
        message = task.message.strip()
        first_word, rest = message.split(" ", 1)
        
        if first_word == "change_analysis":
            prompt = (
                "Decide if the analysis given meets each of the following criteria, if it does, output only '1', if not, describe what it needs to do better.\n"
                "1. potential issues have been supported by evidence, including at least 1 line of code and a line number.\n"
                "2. categorize change is formated as follows: (change type here), (evidence here)\n"
                "3. Risk of bugs or code failure is low, medium, or high.\n"
                "4. Evidence is given for risk of bugs or code failure."
                "Support all claims with evidence"
                f"analysis of changes: {task.context}"
            )
        elif first_word == "issue_draft":
            prompt = (
                "Decide if the issue draft given meets each of the following criteria, if it does, output only '1', if not, describe what it needs to do better:\n\n"
                "1. The title is less than 10 words\n"
                "2. The problem description accurately describe the potential issue or improvement\n"
                "3. The evidence from the actual code\n"
                "4. The acceptance criteria will solve the issue\n"
                "5. The risk level of the issue is either 'Low', 'Medium', or 'High'\n"
                "6. The response is formatted in the following way:\n"
                "Title: <title here>\n"
                "Problem Description: <problem description here>\n"
                "Evidence: 1.) <file name>, <line number>, <code>;  2.) <file name>, <line number>, <code>;  3.) <file name>, <line number>, <code>;  <etc>\n"
                "Acceptance Criteria: 1.) <acceptance criteria 1>; 2.) <acceptance criteria 2>;  3.) <acceptance criteria 3>;  <etc>>\n"
                "Risk Level: <risk level here>\n\n"
                f"Issue Draft: {rest}"
            )
        elif first_word == "suggest_improvements_of_issue":
            content = rest.strip()
            instructions, instruction_option, issue_draft, critique = content.split("$$$$", 4)
            prompt = (
                "Use the given critique to provide suggestions on how to improve the previous issue draft:\n\n"
                "Original rules:\n\n"
                "Use the available tools to explore the code. Then do the following:\n"
                f"{instructions}"   #proposed problem   #nothing
                f"1. Identify {instruction_option}\n"                   #a potential issue or improvement that could be made,      #the code causing the proposed problem
                "2. Give the potential issue or improvement a title\n"
                "3. Create a 2-3 sentence problem description for the potential issue or improvement\n"
                "4. Provide evidence of the potential issue, including file name and line numbers, as well as the code on those lines\n"
                "5. Create acceptance criteria for the issue to be resolved\n"
                "6. Decide the risk level of the issue. How important is the bug being fixed?\n"
                "Format the response in the following way:\n"
                "Title: <title here>\n"
                "Problem Description: <problem description here>\n"
                "Evidence: 1.) <file name>, <line number>, <code>;  2.) <file name>, <line number>, <code>;  3.) <file name>, <line number>, <code>;  <etc>\n"
                "Acceptance Criteria: 1.) <acceptance criteria 1>; 2.) <acceptance criteria 2>;  3.) <acceptance criteria 3>;  <etc>>\n"
                "Risk Level: <risk level here>\n\n"
                f"Original Draft: {issue_draft}\n\n"
                f"Critique: {critique}"
                ""
            )

        elif first_word == "crtique_pr":
            prompt = (
                "Decide if the PR draft given meets each of the following criteria. If it does, output only '1'. "
                "If not, describe what it needs to do better:\n\n"
                "Use the available tools to explore the code. Then do the following:\n"
                "1. The title is less than 10 words\n"
                "2. The summary accurately describes the proposed change\n"
                "3. The files affected match the actual code changes\n"
                "4. The behavior change is clear and accurate\n"
                "5. The test plan is sufficient to verify the change\n"
                "6. The risk level is either 'Low', 'Medium', or 'High'\n"
                "7. The response is formatted in the following way:\n"
                "Title: <title here>\n"
                "Source Branch: <source branch here>\n"
                "Target Branch: <target branch here>\n"
                "Summary: <summary here>\n"
                "Files Affected: 1.) <file name>, <why affected>; 2.) <file name>, <why affected>; 3.) <file name>, <why affected>; <etc>\n"
                "Behavior Change: <behavior change here>\n"
                "Test Plan: 1.) <test plan item 1>; 2.) <test plan item 2>; 3.) <test plan item 3>; <etc>\n"
                "Risk Level: <risk level here>\n\n"
                f"PR Draft: {rest}"
            )

        elif first_word == "suggest_improvements_of_pr":
            content = rest.strip()
            instructions, instruction_option, pr_draft, critique = content.split("$$$$", 4)
            prompt = (
                "Use the given critique to provide suggestions on how to improve the previous PR draft:\n\n"
                "Original rules:\n\n"
                f"{instructions}"
                "Use the available tools to explore the code. Then do the following:\n"
                f"1. Identify {instruction_option}\n"
                "2. Give the pull request a title\n"
                "3. Write a 2-3 sentence summary of the proposed change\n"
                "4. List the files affected by the change, including file names and relevant line numbers if applicable\n"
                "5. Describe the behavior change introduced by the pull request\n"
                "6. Create a test plan for verifying the change\n"
                "7. Decide the risk level of the change. How risky is it to merge?\n"
                "Format the response in the following way:\n"
                "Title: <title here>\n"
                "Source Branch: <source branch here>\n"
                "Target Branch: <target branch here>\n"
                "Summary: <summary here>\n"
                "Files Affected: 1.) <file name>, <why affected>; 2.) <file name>, <why affected>; 3.) <file name>, <why affected>; <etc>\n"
                "Behavior Change: <behavior change here>\n"
                "Test Plan: 1.) <test plan item 1>; 2.) <test plan item 2>; 3.) <test plan item 3>; <etc>\n"
                "Risk Level: <risk level here>\n\n"
                f"Original Draft: {pr_draft}\n\n"
                f"Critique: {critique}"
            )

        return await self._loop.run(prompt, verbose=True)