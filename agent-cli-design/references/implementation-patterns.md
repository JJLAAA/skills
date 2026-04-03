# Implementation Patterns for Agent-Friendly CLIs

Ready-to-use code patterns in Python/Click, Go/Cobra, and Rust/Clap.

---

## Table of Contents

1. [TTY Detection & Auto-Format](#1-tty-detection--auto-format)
2. [Structured Output (stdout/stderr separation)](#2-structured-output-stdoutstderr-separation)
3. [Exit Code Semantics](#3-exit-code-semantics)
4. [Dry-Run Support](#4-dry-run-support)
5. [Enum Constraints & Input Validation](#5-enum-constraints--input-validation)
6. [Idempotent Operations](#6-idempotent-operations)
7. [Structured Error Messages](#7-structured-error-messages)
8. [Schema Introspection](#8-schema-introspection)
9. [Noun-Verb Command Structure](#9-noun-verb-command-structure)

---

## 1. TTY Detection & Auto-Format

### Python / Click

```python
import sys
import json
import click

def get_default_format():
    """Return 'json' in non-TTY (agent) context, 'table' for humans."""
    return "table" if sys.stdout.isatty() else "json"

@click.command()
@click.option("--format", "output_format",
              type=click.Choice(["json", "table", "csv"]),
              default=None,
              help="Output format: json|table|csv (default: table in TTY, json in pipe)")
def list_users(output_format):
    fmt = output_format or get_default_format()
    users = fetch_users()  # your data fetch

    if fmt == "json":
        # Data to stdout, nothing else
        click.echo(json.dumps(users))
    elif fmt == "table":
        # Status info to stderr, table to stdout
        click.echo("Fetching users...", err=True)
        for u in users:
            click.echo(f"{u['id']}\t{u['name']}\t{u['role']}")
    elif fmt == "csv":
        import csv, io
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=["id", "name", "role"])
        writer.writeheader()
        writer.writerows(users)
        click.echo(out.getvalue())
```

### Go / Cobra

```go
func isTerminal() bool {
    fileInfo, _ := os.Stdout.Stat()
    return (fileInfo.Mode() & os.ModeCharDevice) != 0
}

func defaultFormat() string {
    if isTerminal() {
        return "table"
    }
    return "json"
}

var listCmd = &cobra.Command{
    Use:   "list",
    Short: "List users",
    RunE: func(cmd *cobra.Command, args []string) error {
        format, _ := cmd.Flags().GetString("format")
        if format == "" {
            format = defaultFormat()
        }
        users, err := fetchUsers()
        if err != nil {
            return err
        }
        return outputUsers(users, format)
    },
}

func init() {
    listCmd.Flags().String("format", "", "Output format: json|table|csv")
}
```

---

## 2. Structured Output (stdout/stderr separation)

### Python / Click

```python
import sys
import json
import click

class AgentOutput:
    """Ensures data goes to stdout, status/logs go to stderr."""

    @staticmethod
    def data(obj):
        """Machine-readable data → stdout."""
        click.echo(json.dumps(obj, ensure_ascii=False))

    @staticmethod
    def status(msg):
        """Human-readable status → stderr (invisible to agent pipelines)."""
        click.echo(msg, err=True)

    @staticmethod
    def error(code, message, suggestion=None, retryable=False):
        """Structured error → stderr."""
        err = {
            "error": code,
            "message": message,
            "retryable": retryable,
        }
        if suggestion:
            err["suggestion"] = suggestion
        click.echo(json.dumps(err, ensure_ascii=False), err=True)

# Usage
out = AgentOutput()
out.status("Connecting to API...")  # agents never see this
out.data({"users": [...]})          # agents parse this
```

---

## 3. Exit Code Semantics

### Python / Click

```python
import sys
import click

class ExitCode:
    SUCCESS = 0
    GENERAL_ERROR = 1
    INVALID_ARGS = 2
    NOT_FOUND = 3
    PERMISSION_DENIED = 4
    CONFLICT = 5
    DRY_RUN_SUCCESS = 10  # Lightning Labs pattern

class AgentCLIError(click.ClickException):
    def __init__(self, message, exit_code=ExitCode.GENERAL_ERROR,
                 suggestion=None, retryable=False):
        super().__init__(message)
        self.exit_code = exit_code
        self.suggestion = suggestion
        self.retryable = retryable

    def format_message(self):
        import json
        err = {
            "error": self._code_name(),
            "message": self.format_message_text(),
            "retryable": self.retryable,
        }
        if self.suggestion:
            err["suggestion"] = self.suggestion
        return json.dumps(err, ensure_ascii=False)

    def _code_name(self):
        names = {
            ExitCode.INVALID_ARGS: "invalid_arguments",
            ExitCode.NOT_FOUND: "not_found",
            ExitCode.PERMISSION_DENIED: "permission_denied",
            ExitCode.CONFLICT: "conflict",
        }
        return names.get(self.exit_code, "error")

    def format_message_text(self):
        return self.message

# Usage
raise AgentCLIError(
    "Missing calendar:read permission",
    exit_code=ExitCode.PERMISSION_DENIED,
    suggestion="Run: mytool auth login --scope calendar:read",
    retryable=False
)
```

### Go / Cobra

```go
const (
    ExitSuccess         = 0
    ExitGeneralError    = 1
    ExitInvalidArgs     = 2
    ExitNotFound        = 3
    ExitPermissionDenied = 4
    ExitConflict        = 5
    ExitDryRunSuccess   = 10
)

type CLIError struct {
    Code       int
    ErrorCode  string `json:"error"`
    Message    string `json:"message"`
    Suggestion string `json:"suggestion,omitempty"`
    Retryable  bool   `json:"retryable"`
}

func (e *CLIError) Error() string {
    b, _ := json.Marshal(e)
    return string(b)
}

func exitWithError(err *CLIError) {
    fmt.Fprintln(os.Stderr, err.Error())
    os.Exit(err.Code)
}
```

---

## 4. Dry-Run Support

### Python / Click

```python
import json
import click

@click.command()
@click.option("--name", required=True, help="User name to delete")
@click.option("--dry-run", is_flag=True,
              help="Preview what would happen without executing")
def delete_user(name, dry_run):
    user = find_user(name)
    if not user:
        raise AgentCLIError(f"User '{name}' not found",
                           exit_code=ExitCode.NOT_FOUND)

    if dry_run:
        # Structured preview — not just "this is dry-run mode"
        preview = {
            "dry_run": True,
            "action": "delete",
            "target": {"id": user["id"], "name": user["name"]},
            "side_effects": [
                f"Removes user from {len(user['groups'])} groups",
                "Revokes all active sessions",
            ],
            "reversible": False,
        }
        click.echo(json.dumps(preview, ensure_ascii=False))
        sys.exit(ExitCode.DRY_RUN_SUCCESS)  # exit 10: dry-run success

    # Real execution
    perform_delete(user["id"])
    click.echo(json.dumps({"deleted": user["id"], "name": user["name"]}))
```

---

## 5. Enum Constraints & Input Validation

### Python / Click

```python
import re
import click

# Enum constraint — agents can't pass invalid values
@click.option("--role", type=click.Choice(["admin", "member", "viewer"]),
              default="member",
              help="User role: admin|member|viewer")

# URL validation — reject dangerous protocols
def validate_url(ctx, param, value):
    if value is None:
        return value
    dangerous = ["javascript:", "file:", "data:"]
    if any(value.lower().startswith(p) for p in dangerous):
        raise click.BadParameter(f"Dangerous URL protocol rejected: {value}")
    if "@" in value.split("//")[-1].split("/")[0]:
        raise click.BadParameter("URLs with embedded credentials are not allowed")
    return value

@click.option("--webhook-url", callback=validate_url,
              help="Webhook URL (https:// only)")

# Path validation — reject writes to sensitive directories
def validate_output_path(ctx, param, value):
    if value is None:
        return value
    import os
    abs_path = os.path.abspath(value)
    sensitive = [
        os.path.expanduser("~/.ssh"),
        os.path.expanduser("~/.gnupg"),
        os.path.expanduser("~/.aws"),
    ]
    for s in sensitive:
        if abs_path.startswith(s):
            raise click.BadParameter(
                f"Writing to {s} is not allowed for security reasons"
            )
    return value
```

---

## 6. Idempotent Operations

### Python / Click

```python
import click
import json

@click.command()
@click.option("--name", required=True, help="User name")
@click.option("--role", type=click.Choice(["admin", "member", "viewer"]),
              default="member")
@click.option("--if-not-exists", is_flag=True,
              help="Skip if user already exists (idempotent)")
@click.option("--idempotency-key", default=None,
              help="Unique key to prevent duplicate operations")
def create_user(name, role, if_not_exists, idempotency_key):
    # Check idempotency key first
    if idempotency_key and is_duplicate_request(idempotency_key):
        existing = get_result_for_key(idempotency_key)
        click.echo(json.dumps({**existing, "idempotent": True}))
        return

    existing = find_user_by_name(name)
    if existing:
        if if_not_exists:
            # Idempotent: return existing user, exit 0
            click.echo(json.dumps({**existing, "created": False, "existed": True}))
            return
        else:
            raise AgentCLIError(
                f"User '{name}' already exists",
                exit_code=ExitCode.CONFLICT,
                suggestion=f"Use --if-not-exists to skip, or update with: mytool user update --name '{name}'"
            )

    user = perform_create(name, role)
    if idempotency_key:
        store_result(idempotency_key, user)
    click.echo(json.dumps({**user, "created": True}))
```

---

## 7. Structured Error Messages

### Python / Click

```python
import json
import click
import sys

def agent_error(error_code: str, message: str,
                suggestion: str = None, retryable: bool = False,
                exit_code: int = 1):
    """Output structured error to stderr and exit."""
    err = {
        "error": error_code,
        "message": message,
        "retryable": retryable,
    }
    if suggestion:
        err["suggestion"] = suggestion

    click.echo(json.dumps(err, ensure_ascii=False), err=True)
    sys.exit(exit_code)

# Usage examples
agent_error(
    "permission_denied",
    "Missing calendar:read permission",
    suggestion="Run: mytool auth login --scope calendar:read",
    retryable=False,
    exit_code=4
)

agent_error(
    "rate_limited",
    "API rate limit exceeded (100 req/min)",
    suggestion="Wait 60 seconds and retry",
    retryable=True,
    exit_code=1
)

agent_error(
    "invalid_arguments",
    "--start-date must be before --end-date",
    suggestion="Example: --start-date 2024-01-01 --end-date 2024-01-31",
    retryable=False,
    exit_code=2
)
```

---

## 8. Schema Introspection

### Python / Click

```python
import json
import click

def build_schema(group, path=""):
    """Recursively build command schema for introspection."""
    schema = {
        "name": group.name,
        "help": group.help or "",
        "commands": {}
    }

    if hasattr(group, "commands"):
        for name, cmd in group.commands.items():
            cmd_path = f"{path} {name}".strip()
            if hasattr(cmd, "commands"):
                schema["commands"][name] = build_schema(cmd, cmd_path)
            else:
                params = []
                for p in cmd.params:
                    param_info = {
                        "name": p.name,
                        "required": p.required,
                        "type": str(p.type),
                        "help": p.help or "",
                    }
                    if hasattr(p.type, "choices"):
                        param_info["choices"] = list(p.type.choices)
                    if hasattr(p, "default") and p.default is not None:
                        param_info["default"] = p.default
                    params.append(param_info)
                schema["commands"][name] = {
                    "help": cmd.help or "",
                    "params": params
                }
    return schema

@click.group()
def cli():
    pass

@cli.command()
@click.option("--command", default=None,
              help="Specific command path to inspect (e.g., 'user create')")
@click.option("--format", "fmt",
              type=click.Choice(["json", "pretty"]),
              default="json")
def schema(command, fmt):
    """Output CLI schema for agent introspection."""
    full_schema = build_schema(cli)

    if command:
        # Navigate to specific command
        parts = command.split()
        node = full_schema
        for part in parts:
            node = node.get("commands", {}).get(part)
            if not node:
                agent_error("not_found", f"Command '{command}' not found",
                           exit_code=3)

    output = node if command else full_schema

    if fmt == "pretty":
        click.echo(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        click.echo(json.dumps(output, ensure_ascii=False))
```

---

## 9. Noun-Verb Command Structure

### Python / Click

```python
import click

@click.group()
def cli():
    """mytool — example of noun-verb CLI structure."""
    pass

# Noun: user
@cli.group()
def user():
    """Manage users."""
    pass

@user.command("list")
@click.option("--format", type=click.Choice(["json", "table", "csv"]))
def user_list(format):
    """List all users."""
    pass

@user.command("create")
@click.option("--name", required=True)
@click.option("--role", type=click.Choice(["admin", "member", "viewer"]),
              default="member")
@click.option("--if-not-exists", is_flag=True)
@click.option("--dry-run", is_flag=True)
def user_create(name, role, if_not_exists, dry_run):
    """Create a user."""
    pass

@user.command("ensure")
@click.option("--name", required=True)
@click.option("--role", type=click.Choice(["admin", "member", "viewer"]),
              default="member")
def user_ensure(name, role):
    """Ensure user exists with given role (idempotent)."""
    pass

# Noun: project
@cli.group()
def project():
    """Manage projects."""
    pass

@project.command("list")
def project_list():
    """List all projects."""
    pass

# The pattern: same verbs (list, create, ensure, delete, get) work
# consistently across all nouns. Agent learns one, infers the rest.
```

### Go / Cobra

```go
package main

import (
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
    Use:   "mytool",
    Short: "Example of noun-verb CLI structure",
}

// Noun: user
var userCmd = &cobra.Command{
    Use:   "user",
    Short: "Manage users",
}

var userListCmd = &cobra.Command{
    Use:   "list",
    Short: "List all users",
    RunE:  runUserList,
}

var userCreateCmd = &cobra.Command{
    Use:   "create",
    Short: "Create a user",
    RunE:  runUserCreate,
}

func init() {
    // Build the noun-verb tree
    rootCmd.AddCommand(userCmd)
    userCmd.AddCommand(userListCmd)
    userCmd.AddCommand(userCreateCmd)

    // Long flags only — no short flags for agent-critical params
    userCreateCmd.Flags().String("name", "", "User name (required)")
    userCreateCmd.Flags().String("role", "member", "User role: admin|member|viewer")
    userCreateCmd.Flags().Bool("if-not-exists", false, "Skip if user already exists")
    userCreateCmd.Flags().Bool("dry-run", false, "Preview without executing")
    userCreateCmd.MarkFlagRequired("name")
}
```

---

## Complete Example: Agent-Friendly User Management CLI

```python
#!/usr/bin/env python3
"""
Example: fully agent-friendly CLI for user management.
Demonstrates all 10 principles in one coherent implementation.
"""
import sys
import json
import click

# Exit codes (documented, stable across versions)
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_INVALID_ARGS = 2
EXIT_NOT_FOUND = 3
EXIT_PERMISSION_DENIED = 4
EXIT_CONFLICT = 5
EXIT_DRY_RUN = 10

def is_tty():
    return sys.stdout.isatty()

def output(data):
    """Data → stdout."""
    click.echo(json.dumps(data, ensure_ascii=False))

def log(msg):
    """Status → stderr (invisible to agent pipelines)."""
    click.echo(msg, err=True)

def error(code, message, suggestion=None, retryable=False, exit_code=EXIT_ERROR):
    """Structured error → stderr, then exit."""
    err = {"error": code, "message": message, "retryable": retryable}
    if suggestion:
        err["suggestion"] = suggestion
    click.echo(json.dumps(err, ensure_ascii=False), err=True)
    sys.exit(exit_code)

@click.group()
def cli():
    """User management CLI — agent-friendly by design."""
    pass

@cli.group()
def user():
    """Manage users. Subcommands: list, get, create, ensure, delete."""
    pass

@user.command("list")
@click.option("--format", "fmt",
              type=click.Choice(["json", "table", "csv"]),
              default=None,
              help="Output format: json|table|csv (default: table in TTY, json in pipe)")
def user_list(fmt):
    """List all users.

    Examples:
      mytool user list
      mytool user list --format json | jq '.[] | .name'
    """
    fmt = fmt or ("table" if is_tty() else "json")
    log("Fetching users...")
    users = [{"id": "1", "name": "alice", "role": "admin"}]  # placeholder

    if fmt == "json":
        output(users)
    else:
        for u in users:
            click.echo(f"{u['id']}\t{u['name']}\t{u['role']}")

@user.command("create")
@click.option("--name", required=True, metavar="<required>",
              help="User display name")
@click.option("--role",
              type=click.Choice(["admin", "member", "viewer"]),
              default="member",
              metavar="<optional, default: member>",
              help="User role: admin|member|viewer")
@click.option("--if-not-exists", is_flag=True,
              help="Skip silently if user already exists (idempotent)")
@click.option("--dry-run", is_flag=True,
              help="Preview what would happen without executing")
def user_create(name, role, if_not_exists, dry_run):
    """Create a user.

    Examples:
      mytool user create --name "alice" --role admin
      mytool user create --name "bob" --if-not-exists
      mytool user create --name "carol" --dry-run

    Exit codes:
      0  Created successfully
      2  Invalid arguments
      5  User already exists (without --if-not-exists)
      10 Dry-run completed
    """
    existing = None  # find_user(name) in real impl

    if dry_run:
        output({
            "dry_run": True,
            "action": "create",
            "would_create": {"name": name, "role": role},
            "already_exists": existing is not None,
        })
        sys.exit(EXIT_DRY_RUN)

    if existing:
        if if_not_exists:
            output({**existing, "created": False, "existed": True})
            return
        error("conflict", f"User '{name}' already exists",
              suggestion=f"Use --if-not-exists to skip, or: mytool user ensure --name '{name}' --role {role}",
              exit_code=EXIT_CONFLICT)

    user = {"id": "new-id", "name": name, "role": role}  # create in real impl
    output({**user, "created": True})

if __name__ == "__main__":
    cli()
```
