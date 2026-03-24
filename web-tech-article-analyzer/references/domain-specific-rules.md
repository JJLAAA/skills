# Domain-Specific Fetching Rules

Some websites require special handling due to authentication, anti-scraping measures, or other restrictions. Check this file before choosing a fetch tool.

## Rules

| Domain | Tool | Reason |
|--------|------|--------|
| `reddit.com` | chrome-devtools | Requires full page rendering + comment loading |
| `linux.do` | chrome-devtools | Requires login state; curl/fetch/webReader will fail or return incomplete content |

## Guidelines

- When a URL matches a domain in this table, use the specified tool exclusively — do NOT fall back to curl, fetch, or webReader.
- For domains not listed here, use webReader as the default.
- If a new domain is found to require special handling (e.g., login-gated content, JS rendering), add it to this table.
