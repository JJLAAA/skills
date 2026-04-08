# Implementation Patterns for Agent-Friendly CLIs

Language-agnostic patterns for each agent-friendly principle. Apply these in whatever
framework you're using (Click, Cobra, Clap, Commander, etc.).

---

## 1. TTY Detection & Auto-Format

**Problem**: Agents pipe output; humans use terminals. One format doesn't serve both.

**Pattern**:
```
if stdout is a TTY:
    default_format = "table"
else:
    default_format = "json"

format = user_flag("--format") or default_format

if format == "json":
    write data to stdout as JSON
elif format == "table":
    write status messages to stderr
    write table rows to stdout
```

**Key rule**: Status/progress messages always go to stderr. Data always goes to stdout.

---

## 2. Structured Output (stdout/stderr separation)

**Problem**: Agents parse stdout. Mixed output (data + logs) breaks parsing.

**Pattern**:
```
function output_data(obj):
    write JSON(obj) to stdout

function output_status(msg):
    write msg to stderr          # agents never see this

function output_error(code, message, suggestion, retryable):
    write JSON({error, message, suggestion, retryable}) to stderr
    exit with appropriate code
```

**Key rule**: stdout is a contract. Never write non-data to stdout.

---

## 3. Exit Code Semantics

**Problem**: Exit 1 means "something failed" — agents can't distinguish auth errors from
not-found from rate limits, so they can't decide whether to retry, re-auth, or abort.

**Pattern**:
```
EXIT_SUCCESS          = 0
EXIT_GENERAL_ERROR    = 1
EXIT_INVALID_ARGS     = 2   → agent should fix its command
EXIT_NOT_FOUND        = 3   → agent should check the resource name
EXIT_PERMISSION_DENIED = 4  → agent should re-auth or escalate
EXIT_CONFLICT         = 5   → agent should use --if-not-exists or update
EXIT_DRY_RUN_SUCCESS  = 10  → dry-run completed, no side effects taken
```

Map every error type to a distinct exit code. Document the map in `--help`.

---

## 4. Dry-Run Support

**Problem**: Agents can't undo destructive operations. They need to preview before committing.

**Pattern**:
```
command delete-resource --name X [--dry-run]

if --dry-run:
    validate inputs
    resolve what would be affected
    output JSON preview:
        {
          "dry_run": true,
          "action": "delete",
          "target": { resolved resource },
          "side_effects": [ list of consequences ],
          "reversible": false
        }
    exit EXIT_DRY_RUN_SUCCESS (10)

else:
    perform the real operation
    output result JSON
    exit 0
```

**Key rule**: Dry-run must do real validation (catch errors early) but zero side effects.

---

## 5. Enum Constraints & Input Validation

**Problem**: Agents hallucinate parameter values. Free-text inputs accept garbage silently.

**Pattern**:
```
--role: enum["admin", "member", "viewer"]   # reject anything else at parse time
--format: enum["json", "table", "csv"]

for free-text inputs, validate at entry:
    reject dangerous patterns (e.g. javascript: URLs, path traversal)
    reject ambiguous values with a clear error + valid examples

error message format:
    "Invalid value 'X' for --role. Valid values: admin, member, viewer"
```

**Key rule**: Fail fast at argument parsing, before any side effects occur.

---

## 6. Idempotent Operations

**Problem**: Agents retry on failure. Non-idempotent commands create duplicates.

**Pattern**:
```
command create-resource --name X [--if-not-exists] [--idempotency-key KEY]

if idempotency-key provided and already seen:
    return cached result with {"idempotent": true}
    exit 0

if resource already exists:
    if --if-not-exists:
        return existing resource with {"created": false, "existed": true}
        exit 0
    else:
        error: conflict, suggest --if-not-exists or update command
        exit EXIT_CONFLICT (5)

create resource, store idempotency-key result if provided
return {"created": true, ...resource}
```

**Key rule**: Retrying a successful operation must return the same result, not an error.

---

## 7. Structured Error Messages

**Problem**: "Error: something went wrong" tells an agent nothing actionable.

**Pattern**:
```
error output schema (to stderr):
{
  "error": "machine_readable_code",   // e.g. "permission_denied"
  "message": "human description",
  "suggestion": "exact command to fix this",  // optional but powerful
  "retryable": true/false
}
```

**Examples**:
- `"suggestion": "Run: mytool auth login --scope calendar:read"`
- `"suggestion": "Wait 60 seconds and retry"`
- `"suggestion": "Use --if-not-exists to skip, or: mytool resource update --name X"`

**Key rule**: Every error should tell the agent exactly what to do next.

---

## 8. Schema Introspection

**Problem**: Agents explore CLIs via `--help`, but `--help` is unstructured text.

**Pattern**:
```
command schema [--command "noun verb"] [--format json|pretty]

output: machine-readable command tree
{
  "name": "mytool",
  "commands": {
    "user": {
      "commands": {
        "list": {
          "help": "...",
          "params": [
            {"name": "format", "required": false, "choices": ["json","table"], "default": "json"}
          ]
        }
      }
    }
  }
}
```

**Key rule**: Schema output must be stable across versions (it's a contract).

---

## 9. Noun-Verb Command Structure

**Problem**: Flat command lists don't scale. Agents can't infer what commands exist.

**Pattern**:
```
mytool <noun> <verb> [flags]

nouns = resources the CLI manages (user, project, config, token, ...)
verbs = consistent across all nouns: list, get, create, update, delete, ensure

mytool user list
mytool user create --name X --role admin
mytool user ensure --name X --role admin   # idempotent upsert
mytool project list
mytool project create --name Y
```

**Key rule**: Once an agent learns `user list`, it can infer `project list` exists.
Use the same verb names across all nouns — never mix `list`/`ls`/`show`/`get-all`.

---

## 10. Stdin Input Support

**Problem**: Agents compose pipelines. Commands that only accept file paths can't be piped to.

**Pattern**:
```
command import [--file PATH] [--stdin]

priority order:
1. if --file provided: read from file
2. if --stdin flag set: read from stdin
3. if stdin is a pipe (not a TTY): auto-read from stdin
4. else: error "provide --file <path> or pipe input via --stdin"

pipe example:  cat config.json | mytool config import
flag example:  mytool config import --stdin < config.json
file example:  mytool config import --file config.json
```

**Key rule**: Auto-detect pipes so agents don't need to add `--stdin` explicitly.
