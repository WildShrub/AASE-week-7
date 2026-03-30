#will do all the writing and revising, just not the critiquing or suggesting parts, this can be don by changing the prompt based on if statements, and if 



#if it contains "Original Draft"? or would that be too late.
# from pathlib import Path

from agents.base import BaseA2AAgent, Task
from config import DRAFTER_PORT


class DrafterAgent(BaseA2AAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Drafter",
            description="Drafts or revises Github Issues and Pull Requests.",
            skills=["Writing", "GitHub_Issues", "Pull_Requests"],
            port=DRAFTER_PORT,
        )
    
    async def handle(self, task: Task) -> str:
        message = task.message.strip()
        first_word, rest = message.split(" ", 1)
        
        if first_word == "draft_issue":
            content = rest.strip()
            instructions, instruction_option = content.split("$$$$", 1)
            prompt = (
                f"{instructions}"   #proposed problem   #nothing
                "Analyze the code in the github repository:\n\n"
                "Use the available tools to explore the code. Then do the following:\n"
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
                "Risk Level: <risk level here>"
            )
        elif first_word == "revise_issue":
            content = rest.strip()
            instructions, instruction_option, original_draft, suggested_improvements = content.split("$$$$", 3)
            prompt = (
                f"{instructions}"   #proposed problem   #nothing
                "Revise the original issue draft by implementing the suggestions from Suggested Improvements.\n\n"
                "Original rules:\n\n"
                "Use the available tools to explore the code. Then do the following:\n"
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
                f"Original Issue Draft: {original_draft}\n\n"

                f"Suggested Improvements: {suggested_improvements}"

                ""
            )

        elif first_word == "draft_pr":
            content = rest.strip()
            instructions, instruction_option, source_branch, target_branch = content.split("$$$$", 3)
            prompt = (
                f"{instructions}"
            "Analyze the code in the GitHub repository:\n\n"
            f"Source Branch: {source_branch}\n"
            f"Target Branch: {target_branch}\n"
            "Use the available tools to explore the changes in code. Then do the following:\n"
            f"1. Identify {instruction_option}\n"
            "2. Give the pull request a title\n"
            "3. Write a 2-3 sentence summary of the proposed change\n"
            "4. List the files affected by the change, including file names and relevant line numbers if applicable\n"
            "5. Describe the behavior change introduced by the pull request\n"
            "6. Create a test plan for verifying the change\n"
            "7. Decide the risk level of the change. How risky is it to merge?\n"
            "Format the response in the following way:\n"
            "Title: <title here>\n"
            f"Source Branch: {source_branch}\n"
            f"Target Branch: {target_branch}\n"
            "Summary: <summary here>\n"
            "Files Affected: 1.) <file name>, <why affected>; 2.) <file name>, <why affected>; 3.) <file name>, <why affected>; <etc>\n"
            "Behavior Change: <behavior change here>\n"
            "Test Plan: 1.) <test plan item 1>; 2.) <test plan item 2>; 3.) <test plan item 3>; <etc>\n"
            "Risk Level: <risk level here>"
            )

        elif first_word == "revise_pr":
            content = rest.strip()
            instructions, instruction_option, original_draft, suggested_improvements = content.split("$$$$", 4)
            prompt = (
                f"{instructions}"
                "Revise the original PR draft by implementing the suggestions from Suggested Improvements.\n\n"
                "Original rules:\n\n"
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
                f"Original PR Draft: {original_draft}\n\n"
                f"Suggested Improvements: {suggested_improvements}"
            )

        return await self._loop.run(prompt, verbose=verbose)