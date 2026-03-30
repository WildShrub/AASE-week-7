"""
Tool handlers — pure Python functions, one per tool.

Function names must match the tool names in schemas.py exactly;
app.py dispatches by name using getattr(handlers, name).

No MCP imports here — these are plain functions that can be
tested independently of the MCP server.
"""
import subprocess
from pathlib import Path
from os import getenv
import requests
MAX_FILE_CHARS = 8_000

REPO_OWNER = "WildShrub"
REPO_NAME = "literate-chainsaw"
#put an access token here
GITHUB_API_TIMEOUT = 30



def read_file(path: str) -> str:
    return Path(path).read_text(errors="replace")[:MAX_FILE_CHARS]


def list_directory(path: str) -> str:
    entries = sorted(Path(path).iterdir(), key=lambda e: (e.is_file(), e.name))
    lines   = [f"{'DIR ' if e.is_dir() else 'FILE'} {e.name}" for e in entries]
    return "\n".join(lines) or "(empty)"


def grep_code(pattern: str, path: str) -> str:
    result = subprocess.run(
        ["grep", "-rH", "--include=*.py", "-n", pattern, path],
        capture_output=True, text=True, timeout=15,
    )
    return result.stdout.strip() or "No matches found."


#------------------------------------------------------------------------------------------------------------


def get_github_issue(issue_number: str) -> dict:
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"{ACCESS_TOKEN}"
    }
    try:
        response = requests.get(url=url,headers=headers)
        issue_data=response.json()

        issue_content = {
            'title': issue_data['title'],
            'body': issue_data['body'],
        }
        print(str(issue_content))
        return issue_content
    except Exception as e:
        print("Error getting issue: {str(e)}")
        return {"status": "error", "message": str(e)}


def create_github_issue(title: str, body: str): #, labels: list[str]
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"{ACCESS_TOKEN}"
    }
    print("Creating issue")
    try:
        #issue_labels = ['mcp'] if not labels else labels + ['mcp']
        response = requests.post(url, headers=headers, json={
            'title': title,
            'body': body#,
            #'labels': issue_labels
        }, timeout=GITHUB_API_TIMEOUT)
        response.raise_for_status()
            
        print("Issue created successfully")
        print(response)
        return(response)

    except Exception as e:
        print("Error creating issue: {str(e)}")

        print(response)
        return {"status": "error", "message": str(e)}

#------------------------------------------------------------------------------------------------------------

def get_github_PR(pr_number: int) -> dict:
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"{ACCESS_TOKEN}"
    }
    try:
        response = requests.get(url, headers=headers, timeout=GITHUB_API_TIMEOUT)
        response.raise_for_status()
        pr_data = response.json()
            
        pr_content = {
            'title': pr_data['title'],
            'description': pr_data['body'],
            'author': pr_data['user']['login'],
            'created_at': pr_data['created_at'],
            'updated_at': pr_data['updated_at'],
            'state': pr_data['state']
        }

        print("Successfully fetched PR content:")
        print(pr_content)
        return pr_content
            
    except Exception as e:
        print("Error fetching PR content")
        return {"status": "error", "message": str(e)}


def create_github_PR(title: str, body: str, head: str, base: str, draft: bool) -> dict:
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    headers = {
        "Accept":"application/vnd.github.v3+json",
        "Authorization": f"{ACCESS_TOKEN}"
    }
    try:
            response = requests.post(url, headers=headers, json={
                'title': title,
                'body': body,
                'head': head,
                'base': base,
                'draft': draft
            }, timeout=GITHUB_API_TIMEOUT)
            response.raise_for_status()
            pr_data = response.json()

            print("PR created successfully")
            response = {
                "pr_url": pr_data.get('html_url'),
                "pr_number": pr_data.get('number'),
                "status": pr_data.get('state'),
                "title": pr_data.get('title'),
            }
            print(response)
            return(response)
            

    except Exception as e:
        print("Error creating PR:")
        return {"status": "error", "message": str(e)}


#------------------------------------------------------------------------------------------------------------


def git_diff(base_SHA: str, head_SHA: str) -> str:
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/compare/{base_SHA}...{head_SHA}"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"{ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url=url,headers=headers)
        print(str(response.json()))
        return(str(response.json()))
    except Exception as e:

        print("Error getting diff:")
        return str(e)
        

#------------------------------------------------------------------------------------------------------------


def check_code():
    url = ''
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"{ACCESS_TOKEN}"
    }

    response = requests.get()
    print(response.json)