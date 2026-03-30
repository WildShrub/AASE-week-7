"""
A2A Coordinator

Discovers available A2A agents, then orchestrates a sequential code-review
pipeline by delegating tasks via HTTP.

Discovery:
  Each agent exposes GET /.well-known/agent.json  →  Agent Card
  The coordinator fetches these to learn what agents are available.

Delegation:
  POST /tasks/send  with  {task_id, message, context}
  The agent returns      {task_id, status, output, agent}
"""
from __future__ import annotations

import uuid

import httpx
from rich.console import Console

from config import ANALYZER_PORT, REVIEWER_PORT

console = Console()

KNOWN_ENDPOINTS = [
    f"http://localhost:{ANALYZER_PORT}",
    f"http://localhost:{REVIEWER_PORT}",
]


class A2ACoordinator:
    def __init__(self) -> None:
        self.agents: list[dict] = []

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover(self) -> list[dict]:
        """Fetch Agent Cards from all known endpoints."""
        self.agents = []
        for endpoint in KNOWN_ENDPOINTS:
            try:
                resp = httpx.get(
                    f"{endpoint}/.well-known/agent.json", timeout=5
                )
                resp.raise_for_status()
                card = resp.json()
                card["endpoint"] = endpoint
                self.agents.append(card)
                console.print(
                    f"  [green]✓[/] [bold]{card['name']}[/]"
                    f"  skills={card['skills']}"
                    f"  → {endpoint}"
                )
            except Exception as exc:
                console.print(f"  [red]✗[/] {endpoint}: {exc}")
        return self.agents

    # ------------------------------------------------------------------
    # Task delegation
    # ------------------------------------------------------------------

    def send_task(
        self, endpoint: str, message: str, context: str = ""
    ) -> dict:
        """Send a task to an A2A agent and return the result dict."""
        payload = {
            "task_id": str(uuid.uuid4())[:8],
            "message": message,
            "context": context,
        }
        resp = httpx.post(
            f"{endpoint}/tasks/send", json=payload, timeout=120
        )
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Pipeline
    # ------------------------------------------------------------------

    def run_review(self, target: str) -> dict[str, str]:
        """
        Sequential review pipeline:
          Analyzer  →  Reviewer (receives Analyzer output as context)
        """
        analyzer = next(
            (a for a in self.agents if a["name"] == "Analyzer"), None
        )
        reviewer = next(
            (a for a in self.agents if a["name"] == "Reviewer"), None
        )

        results: dict[str, str] = {}

        if analyzer:
            console.print("\n[cyan]→ Analyzer[/]  sending task …")
            r = self.send_task(analyzer["endpoint"], message=target)    #send task means run a post request to an endpoint
            results["analysis"] = r["output"]
            console.print("[green]  ✓ Analysis complete[/]")

        if reviewer:
            console.print("[cyan]→ Reviewer[/]  sending task (with analysis context) …")
            context = results.get("analysis", "")
            r = self.send_task(reviewer["endpoint"], message=target, context=context)
            results["review"] = r["output"]
            console.print("[green]  ✓ Review complete[/]")

        return results
    
        #message must be Head~2..Head or older_SHA..recent_SHA
    def test_change_review_with_A2A(self, message: str) -> dict[str, str]:
        """
        Sequential review pipeline:
          Change_Reviewer  →  Reviewer (receives Analyzer output as context)
        """
        change_reviewer = next((a for a in self.agents if a["name"] == "Change_Reviewer"), None)
        critic = next((a for a in self.agents if a["name"] == "Critic"), None)
        planner = next((a for a in self.agents if a["name"] == "Planner"), None)
        results: dict[str, str] = {}

        if change_reviewer:
            console.print("\n[cyan]→ Change_Reviewer[/]  sending task …")
            r = self.send_task(change_reviewer["endpoint"], message=message)    #send task means run a post request to an endpoint
            results["change analysis"] = r["output"]
            console.print("[green]  ✓ Analysis complete[/]")
            console.print("[red] waiting on critic [/]")
            while "1" != results.get("critique", ""):
                console.print("Looks like the critic didn't like it. Let's try again!")
                context = results.get("critique", "")
                r = self.send_task(change_reviewer["endpoint"], message=message, context=context)
                results["change analysis"] = r["output"]
                console.print("[green]  ✓ Analysis complete[/]")
        

        if critic:
            console.print("[cyan]→ Critic[/]  sending task (with analysis context) …")
            context = results.get("change_analysis", "")   #needs to be changed
            r = self.send_task(critic["endpoint"], message="change_analysis", context=context)
            results["critique"] = r["output"]
            console.print("[green]  ✓ Critique complete[/]")
            if results.get("critique", "") != "1":
                console.print("[CRITIC]: I don't like it...")
            else:
                console.print("[CRITIC]: I LIKE IT!!!!!")
            while results.get("critique", "") != "1":
                if results.get("change_analysis", "") != context:
                    console.print("[cyan]→ Critic[/]  sending task (with analysis context) …")
                    context = results.get("change_analysis", "")   #needs to be changed
                    r = self.send_task(critic["endpoint"], message="change_analysis", context=context)
                    results["critique"] = r["output"]

        if planner:
            console.print("Deciding what to do...")
            i = 0
            while results.get("critic", "") != "1":
                i+= 0.0001
            context = results.get("change_analysis", "")
            r = self.send_task(planner["endpoint"], message=message, context=context)
            results["plan"] = r["output"]
            console.print("[green]  ✓Planning complete[/]")


        return results
    
    def test_github_with_A2A(self, message: str) -> dict[str, str]:
        """
        Sequential review pipeline:
          Change_Reviewer  →  Reviewer (receives Analyzer output as context)
        """

        """
        The message will be the command, it will be split and interpreted into the 2 different SHA numbers 
        """
        change_reviewer = next((a for a in self.agents if a["name"] == "Change_Reviewer"), None)
        critic = next((a for a in self.agents if a["name"] == "Critic"), None)
        drafter = next((a for a in self.agents if a["name"] == "Drafter"), None)
        planner = next((a for a in self.agents if a["name"] == "Planner"), None)
        results: dict[str, str] = {}

        if change_reviewer:
            console.print("\n[cyan]→ Change_Reviewer[/]  sending task …")
            r = self.send_task(change_reviewer["endpoint"], message=message)    #send task means run a post request to an endpoint
            results["change analysis"] = r["output"]
            console.print("[green]  ✓ Analysis complete[/]")

        if critic:
            console.print("[cyan]→ Critic[/]  sending task (with analysis context) …")
            context = results.get("analysis", "")   #needs to be changed
            r = self.send_task(critic["endpoint"], message=message, context=context)
            results["critique"] = r["output"]
            console.print("[green]  ✓ Review complete[/]")

        return results
    

    
    
