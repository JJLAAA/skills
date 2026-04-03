# Lark CLI: Parameter, Command & Output Design Patterns

Concrete design decisions from larksuite/cli source code, extracted as reusable patterns.

---

## Table of Contents

1. [Global Flag Set](#1-global-flag-set)
2. [Parameter Input Design](#2-parameter-input-design)
3. [Output Format Design](#3-output-format-design)
4. [Pagination Design](#4-pagination-design)
5. [Command Structure Design](#5-command-structure-design)
6. [Error Output Design](#6-error-output-design)
7. [Binary Response Handling](#7-binary-response-handling)
8. [Schema Command Design](#8-schema-command-design)

---

## 1. Global Flag Set

Every command in lark-cli shares the same flag set. This is the canonical reference:

```
--params <json>       URL/query parameters (GET params, path params)
--data <json>         Request body (POST/PATCH/PUT/DELETE only)
--as user|bot|auto    Identity: user = UAT, bot = TenantToken, auto = detect
--format json|ndjson|table|csv|pretty   Output format (default: json)
--page-all            Auto-paginate through all pages
--page-size <N>       Page size (0 = API default)
--page-limit <N>      Max pages with --page-all (default: 10, 0 = unlimited)
--page-delay <MS>     Delay between pages in ms (default: 200)
-o / --output <path>  Save binary response to file
--dry-run             Print request without executing
```

**Design decisions worth copying:**

- `--data` only appears on POST/PUT/PATCH/DELETE — GET commands don't show it. Reduces noise.
- `--as` defaults to `auto` (detect from config), not `user`. Avoids breaking bot-only setups.
- `--page-limit` defaults to 10, not unlimited. Prevents runaway pagination by default.
- `--page-delay` defaults to 200ms. Built-in rate limit protection.
- Short flag `-o` is the only short flag in the set — everything else is long-only.

---

## 2. Parameter Input Design

### Two-JSON pattern: `--params` vs `--data`

```bash
# --params: URL query params and path params
lark-cli calendar events list \
  --params '{"calendar_id":"primary","start_time":"1700000000"}'

# --data: request body (POST/PATCH only)
lark-cli im messages create \
  --params '{"receive_id_type":"chat_id"}' \
  --data '{"receive_id":"oc_xxx","msg_type":"text","content":"{\"text\":\"Hello\"}"}'
```

**Why two separate flags instead of one:**
- Mirrors HTTP semantics (query string vs body) — agents with API knowledge map naturally
- Prevents agents from accidentally putting body params in query string or vice versa
- `--params` is always safe to log; `--data` may contain sensitive content

### Path normalization

Raw API accepts multiple URL formats — all normalized to the same path:

```bash
# All equivalent:
lark-cli api GET /open-apis/calendar/v4/calendars
lark-cli api GET calendar/v4/calendars          # auto-prepends /open-apis/
lark-cli api GET https://open.feishu.cn/open-apis/calendar/v4/calendars  # strips host
```

`normalisePath()` strips the host prefix and ensures `/open-apis/` prefix. Agents don't need to remember the full URL format.

### JSON input validation

Both `--params` and `--data` are validated as JSON before the request is built:

```go
params, err := parseJsonOpt(opts.Params, "--params")
// Error: --params: invalid JSON: unexpected character 'x' at position 3
```

Fail fast at parse time, not at API call time. The error names the flag that failed.

---

## 3. Output Format Design

### Five formats, two use cases

| Format | Use case | Behavior |
|--------|----------|----------|
| `json` | Agent single-result, default | Full nested JSON, wait for all pages |
| `ndjson` | Agent streaming/pagination | One JSON object per line, stream as pages arrive |
| `table` | Human readable | Auto-detect columns from response array |
| `csv` | Data export, piping | Header row + data rows, stream as pages arrive |
| `pretty` | Human debugging | Indented JSON with color (dry-run default) |

**Key insight — streaming split:**

```go
// ndjson/table/csv: stream each page as it arrives (low memory, immediate output)
case output.FormatNDJSON, output.FormatTable, output.FormatCSV:
    ac.StreamPages(ctx, request, func(items []interface{}) {
        pf.FormatPage(items)  // write immediately
    }, pagOpts)

// json: collect all pages, merge, output once (complete result)
default:
    result, _ := ac.PaginateAll(ctx, request, pagOpts)
    output.FormatValue(out, result, format)
```

Use `ndjson` when paginating large datasets — agents can process records as they arrive without waiting for all pages or holding everything in memory.

### stdout/stderr strict separation

```
stdout: data only (JSON, table rows, CSV)
stderr: progress, warnings, page counters

# Example: --page-all writes progress to stderr, data to stdout
stderr: [page 1] fetching...
stderr: [page 2] fetching...
stdout: {"items": [...all merged items...]}
```

Agents can pipe stdout to `jq` without stderr contamination. Humans see progress on stderr.

### Binary response auto-handling

When Content-Type is non-JSON (file download), CLI auto-saves and outputs metadata to stdout:

```json
{
  "path": "/tmp/lark-cli-download-abc123.xlsx",
  "size": 204800,
  "mime_type": "application/vnd.ms-excel"
}
```

Agent receives `path` field and can continue processing. No special handling needed for file downloads vs JSON responses — the output contract is always JSON to stdout.

---

## 4. Pagination Design

### Auto-detect page token field name

Lark APIs use two different field names for pagination tokens:

```go
// Both supported transparently:
if pt, ok := data["page_token"].(string); ok && pt != "" { ... }
if pt, ok := data["next_page_token"].(string); ok && pt != "" { ... }
```

Agents don't need to know which field name a specific API uses.

### Merged output removes pagination artifacts

When using `--page-all` with `json` format, the merged result:
- Concatenates all `items` arrays across pages
- Removes `page_token` and `next_page_token` fields
- Sets `has_more: false`

The agent receives a single clean result as if the API returned everything at once.

### Safety defaults

```
--page-limit 10   (default) — stops after 10 pages even with --page-all
--page-delay 200  (default) — 200ms between requests
```

Agents must explicitly opt into unlimited pagination: `--page-all --page-limit 0`

---

## 5. Command Structure Design

### Shortcut (+prefix) design principles

Shortcuts are hand-crafted for the 80% case. Each shortcut:

1. **Minimal required params** — only what's truly necessary
2. **Smart defaults** — `msg_type` defaults to `text`, `receive_id_type` defaults to `chat_id`
3. **Table output default** — human-readable by default, override with `--format json`
4. **Dry-run built in** — all shortcuts support `--dry-run`
5. **Agent-tested** — success rate is the quality gate, not feature completeness

```bash
# Shortcut: 2 params needed
lark-cli im +messages-send --chat-id "oc_xxx" --text "Hello"

# Equivalent API Command: 4 params, nested JSON
lark-cli im messages create \
  --params '{"receive_id_type":"chat_id"}' \
  --data '{"receive_id":"oc_xxx","msg_type":"text","content":"{\"text\":\"Hello\"}"}'
```

### Long description with schema pointer

Every Layer 2 command's `--help` includes a pointer to its schema:

```
View parameter definitions before calling:
  lark-cli schema calendar.events.create
```

This is in the `Long` field of the Cobra command, not just a comment. Agents reading `--help` see it immediately.

### HTTP method determines available flags

```go
switch httpMethod {
case "POST", "PUT", "PATCH", "DELETE":
    cmd.Flags().StringVar(&opts.Data, "data", "", "request body JSON")
// GET commands don't get --data flag at all
}
```

GET commands don't show `--data`. Reduces confusion, prevents agents from trying to pass a body to a GET endpoint.

### Tips field for agent guidance

Each API command can carry a `tips` array from metadata — short hints shown in `--help`:

```
Tips:
  • Use --page-all to fetch all records
  • calendar_id "primary" refers to the user's default calendar
```

These are sourced from the API metadata, not hardcoded. Keeps guidance close to the command definition.

---

## 6. Error Output Design

### Structured error envelope (stderr)

All errors write a JSON envelope to stderr:

```json
{
  "error": {
    "type": "scope_insufficient",
    "code": 99991663,
    "message": "User not authorized: required scope calendar:calendar:readonly",
    "hint": "run: lark-cli auth login --scope \"calendar:calendar:readonly\"",
    "console_url": "https://open.feishu.cn/page/scope-apply?clientID=...&scopes=...",
    "identity": "user"
  }
}
```

Fields:
- `type`: machine-readable error category (agent can switch on this)
- `code`: Lark API error code (for debugging)
- `message`: human-readable description
- `hint`: **executable command** — the exact fix, ready to copy-paste or execute
- `console_url`: browser URL for admin actions (scope approval, etc.)
- `identity`: which identity was active when the error occurred

### MarkRaw: prevent double output

When `HandleResponse` already wrote the API response to stdout (including a business error), the error is marked `Raw`:

```go
// API response already on stdout — don't wrap it again in stderr envelope
return output.MarkRaw(err)
```

Root error handler checks `exitErr.Raw` and skips the stderr envelope if set. Prevents agents from seeing the same error twice in different formats.

### Exit code map

```
0  Success
1  API/business error
2  Validation error (bad params, mutually exclusive flags)
3  Network error
4  Internal error
```

Permission errors (scope insufficient, app scope not enabled) return exit code 1 with `type: scope_insufficient` — agents check `type`, not just exit code, to distinguish permission from other errors.

### Security policy errors: separate envelope

Security policy violations (prompt injection detected, challenge required) use a different envelope format:

```json
{
  "error": "challenge_required",
  "message": "...",
  "challenge_url": "https://...",
  "hint": "..."
}
```

Handled separately from normal errors because they require user action (browser challenge), not parameter fixes.

---

## 7. Binary Response Handling

### Content-Type routing

```
JSON response  → parse, check business errors, format and print to stdout
Binary response + --output → save to specified path, print metadata JSON to stdout
Binary response, no --output → auto-save with derived filename, print metadata JSON to stdout
Non-JSON error (4xx text/plain) → return HTTP error directly, don't try to save
```

### Auto-filename derivation

When no `--output` is specified for a binary response, filename is derived from:
1. `Content-Disposition: attachment; filename="..."` header
2. URL path last segment + Content-Type extension
3. Fallback: `lark-cli-download-<uuid>.<ext>`

### Mutually exclusive flags

```bash
# Error: --output and --page-all are mutually exclusive
lark-cli drive files download --output ./file.xlsx --page-all
```

File downloads don't paginate. Caught at validation time, not at runtime.

---

## 8. Schema Command Design

`lark-cli schema` is the third required piece of the P12 fallback mechanism — it lets agents discover parameter details after falling back to a Layer 2 API command.

### Four-level hierarchy

```bash
lark-cli schema                          # Level 0: list all services
lark-cli schema calendar                 # Level 1: list resources in a service
lark-cli schema calendar.events          # Level 2: list methods in a resource
lark-cli schema calendar.events.create   # Level 3: full method detail
```

Each level is a superset of the next — agents can navigate top-down without knowing the full path upfront.

### What Level 3 (method detail) outputs

```
calendar.events.create

  POST /open-apis/calendar/v4/calendars/{calendar_id}/events
  Create a calendar event

Parameters:

  --params  <json>  optional
      - calendar_id (string, path, required)
        The calendar to create the event in
        e.g. primary

  --data  <json>  optional
      - summary (string, required)
      - start_time.timestamp (string, required)
        Unix timestamp in seconds
      - end_time.timestamp (string, required)
      - attendees (array, optional)
      - attendees[].open_id (string, optional)

Response:

  - event.event_id (string)
  - event.summary (string)
  - event.status (string) — tentative | confirmed | cancelled

Identity: user, bot
Scopes:   calendar:calendar, calendar:calendar:readonly
CLI:      lark-cli calendar events create
Docs:     https://open.feishu.cn/document/...
```

**Key design decisions:**

- Required params sort before optional — agents see what's mandatory first
- Nested request body fields use dot notation (`attendees[].open_id`) — matches how `--data` JSON is structured
- `--params` and `--data` sections mirror the two-JSON flag split — agents know exactly which flag each field goes into
- `Identity` and `Scopes` fields tell agents which `--as` value to use and what auth is needed
- `CLI:` line gives the exact command to run — no guessing
- `Docs:` line links to official API docs for edge cases

### Two output formats

```bash
lark-cli schema calendar.events.create           # json (default) — machine-readable
lark-cli schema calendar.events.create --format pretty  # human-readable with colors
```

`json` format outputs the raw metadata object — agents can `jq` it. `pretty` format is for humans debugging in a terminal.

### Tab completion

The schema command ships with full tab completion for the dotted path:

```bash
lark-cli schema cal<TAB>          → calendar.
lark-cli schema calendar.<TAB>    → calendar.events. calendar.calendars. ...
lark-cli schema calendar.events.<TAB> → calendar.events.create calendar.events.list ...
```

Completion handles dotted resource names (e.g. `app.table.fields`) by iterating all resources and classifying each as prefix-match or fully-matched. This means agents using shell completion can discover the full path without reading docs.

### Error messages include available options

```json
{
  "error": "validation",
  "message": "Unknown resource: calendar.foo",
  "hint": "Available: calendars, events, freebusy, settings, timeoffEvents"
}
```

Wrong path → error lists valid options. Agents can self-correct in one retry.

### No auth required

`cmdutil.DisableAuthCheck(cmd)` — schema is a local metadata lookup, no API call, no token needed. Agents can call it at any time without worrying about auth state.
