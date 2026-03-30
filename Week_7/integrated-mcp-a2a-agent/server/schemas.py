"""
Tool schemas — the only place tool names, descriptions, and parameter
shapes are defined. server/app.py and server/handlers.py both derive
from this file; nothing else needs to change when a tool is added.
"""

TOOLS = [
    {
        "name": "read_file",
        "description": "Read the content of a source file (capped at 8 000 chars).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute or relative file path"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "list_directory",
        "description": "List files and subdirectories inside a directory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory path"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "grep_code",
        "description": "Search for a text pattern inside Python files under a directory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Search term or regex"},
                "path":    {"type": "string", "description": "Root directory to search"},
            },
            "required": ["pattern", "path"],
        },
    },
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    {
        "name": "get_github_issue",
        "description": "read the title and body of a github issue of a given issue number.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "issue_number": {"type": "str", "description": "identifier for the issue to read the contents of"},
            },
            "required": ["issue_number"],
        },
    },
    {
        "name": "create_github_issue",
        "description": "create a github issue consisting of a given title and body.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Title of the issue"},
                "body":    {"type": "string", "description": "Body of the issue"},
            },
            "required": ["title", "body"],
        },
    },
    {
        "name": "get_github_PR",
        "description": "Read the contents of a github pull request.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pr_number": {"type": "int", "description": "Identifier for the pull request to read the contents of."},
            },
            "required": ["pr_number"],
        },
    },
    {
        "name": "create_github_PR",
        "description": "Create a github pull request with a title and body requesting to merge the commit onto the base.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "The title of the pull request"},
                "body":    {"type": "string", "description": "The description of the pull request"},
                "head": {"type": "string", "description": "The SHA of the commit that is being added to the base"},
                "base":    {"type": "string", "description": "the SHA of the commit that the head is being added onto"},
                "draft": {"type": "bool", "description": "If this is only a rough draft of a pull request"},
            },
            "required": ["title", "body", "path", "head", "base", "draft"],
        },
    },
    {
        "name": "git_diff",
        "description": "read the file and code changes between an earlier commit and a newer one.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_SHA" : {"type": "str", "description": "The Identifier of the earlier commit chronologically"},
                "head_SHA" : {"type": "str", "description": "The Identifier of the later commit chronologically"},
            },
            "required": ["base_SHA","head_SHA"],
        },
    },
]
