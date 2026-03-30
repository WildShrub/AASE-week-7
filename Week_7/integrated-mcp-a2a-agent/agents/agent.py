"""
MCPAgent — orchestrator

Composes MCPSession, AgenticLoop, and OllamaClient.
Connects to a running MCP server via HTTP/SSE.

Usage:
    async with MCPAgent() as agent: ...                              # default port
    async with MCPAgent("http://localhost:8050/sse") as agent: ...  # explicit URL
"""
from __future__ import annotations

from loop import AgenticLoop
from session import MCPSession, DEFAULT_URL
from llm import OllamaClient


class MCPAgent:
    def __init__(self, url: str = DEFAULT_URL) -> None:
        self._session = MCPSession(url)
        self._loop: AgenticLoop | None = None

    async def analyze(self, target: str, verbose: bool = False) -> str:
        task = (
            f"Analyze the Python code at: {target}\n\n"
            "Use the available tools to explore the code. Then provide:\n"
            "1. What the code does (2-3 sentences)\n"
            "2. Quality or style issues found\n"
            "3. Three concrete improvement suggestions"
        )
        return await self._loop.run(task, verbose=verbose)

#-------------------------------------------------------------------------------------------------------
#                                                  TASK 1
#-------------------------------------------------------------------------------------------------------
    async def analyze_changes(self, BASE_SHA: object, HEAD_SHA: object, verbose: bool = False) -> str:
        task = (
            f"Use the git_diff tool to analyze the changes made to the code base from SHA {BASE_SHA} to SHA {HEAD_SHA}.\n\n Then do the following:"   #available tools 
            "1. Identify potential issues or improvements\n"
            "2. Categorize change (feature, bugfix, refactor, etc.)\n"
            "3. Assess risk of bugs or code failure (low / medium / high)\n"
            "Support all claims with evidence from tools"
        )
        return await self._loop.run(task, verbose=verbose)
    
    async def test_apis(self, BASE_SHA: object, HEAD_SHA: object, verbose: bool = False) -> str:
        task = (
            f"Use the git_diff tool to see the changes made to the code base from SHA {BASE_SHA} to SHA {HEAD_SHA}, then output exactly what it said.\n\n"
        )
        return await self._loop.run(task, verbose=verbose)
    
    async def test_easy_apis(self, issue_number: int, verbose: bool = False) -> str:
        task = (
            f"Use the get_github_issue tool to get issue {issue_number}, then output exactly what it said.\n\n"
        )
        return await self._loop.run(task, verbose=verbose)
    

    async def critic_analysis_of_changes(self, analysis: str, verbose: bool = False) -> str:
        task = (
            "Decide if the analysis given meets each of the following criteria, if it does, output only '1', if not, describe what it needs to do better.\n"
            "1. potential issues have been supported by evidence, including at least 1 line of code and a line number.\n"
            "2. categorize change is formated as follows: (change type here), (evidence here)\n"
            "3. Risk of bugs or code failure is low, medium, or high.\n"
            "4. Evidence is given for risk of bugs or code failure."
            "Support all claims with evidence"
            f"analysis of changes: {analysis}"
        )
        return await self._loop.run(task, verbose=verbose)
    

    async def revise_change_analysis(self, BASE_SHA: str, HEAD_SHA: str, original_draft: str, critque: str, verbose: bool = False) -> str:
        task = (
            "Use the available tools to revise the previous analysis to address the issues in the critique. Then do the following:"
            f"Original Draft:\n {original_draft}\n\n"
            f"Critique:\n {critque}"
            
            "1. Identify potential issues or improvements\n"
            "2. Categorize change (feature, bugfix, refactor, etc.)\n"
            "3. Assess risk of bugs or code failure (low / medium / high)\n"
            "Support all claims with evidence from tools"
        )
        return await self._loop.run(task, verbose=verbose)

#---------------------------------------------------------------------------------------------

    async def evaluate_next_action(self, analysis: str, verbose: bool = False) -> str:
        task = (
            "Given the analysis of the changes made, decide the best course of action listed below:\n"
            "1. Create a GitHub issue\n"
            "2. Create a GitHub pull request\n"
            "3. No action required\n"
            "Support all claims with evidence"
            f"analysis of changes: {analysis}"

        )
        return await self._loop.run(task, verbose=verbose)


#---------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                     TASKS 2 & 3
#---------------------------------------------------------------------------------------------------------------------------------------------------------


    async def draft_issue(self, instructions: str, instruction_option: str, verbose: bool = False) -> str:
        task = (
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
        return await self._loop.run(task, verbose=verbose)


    async def critique_issue_draft(self, issue_draft: str, verbose: bool = False) -> str:
        task = (
            
            "Decide if the issue draft given meets each of the following criteria, if it does, output only '1', if not, describe what it needs to do better:\n\n"
            "Use the available tools to explore the code. Then do the following:\n"
            "1. The title lest than 10 words\n"
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
            f"Issue Draft: {issue_draft}"
        )
        return await self._loop.run(task, verbose=verbose)
    

    async def suggest_improvements_of_issue(self, instructions: str, instruction_option: str, original_draft: str, critique: str, verbose: bool = False) -> str:
        task = (
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
            f"Original Draft: {original_draft}\n\n"

            f"Critique: {critique}"

            ""
        )
        return await self._loop.run(task, verbose=verbose)
    

    async def revise_issue(self, instructions: str, instruction_option: str, original_draft: str, suggested_improvements: str, verbose: bool = False) -> str:
        task = (
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
        return await self._loop.run(task, verbose=verbose)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def draft_pr(self, instructions: str, instruction_option: str, source_branch: str, target_branch: str, verbose: bool = False) -> str:
        task = (
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
        return await self._loop.run(task, verbose=verbose)


    async def critique_pr_draft(self, pr_draft: str, source_branch: str, target_branch: str, verbose: bool = False) -> str:
        task = (
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
            f"PR Draft: {pr_draft}"
        )
        return await self._loop.run(task, verbose=verbose)


    async def suggest_improvements_of_pr(self, instructions: str, instruction_option: str, original_draft: str, critique: str, verbose: bool = False) -> str:
        task = (
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
            f"Original Draft: {original_draft}\n\n"
            f"Critique: {critique}"
        )
        return await self._loop.run(task, verbose=verbose)


    async def revise_pr(self, instructions: str, instruction_option: str, original_draft: str, suggested_improvements: str, verbose: bool = False) -> str:
        task = (
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
        return await self._loop.run(task, verbose=verbose)





    async def list_tools(self) -> list[dict]:
        return await self._session.list_tools()

    async def __aenter__(self) -> "MCPAgent":
        await self._session.__aenter__()
        self._loop = AgenticLoop(self._session, OllamaClient())
        return self

    async def __aexit__(self, *args) -> None:
        await self._session.__aexit__(*args)
