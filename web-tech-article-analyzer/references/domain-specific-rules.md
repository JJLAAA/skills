# Domain-Specific Fetching Rules

Some websites require special handling due to authentication, anti-scraping measures, or other restrictions. Check this file before choosing a fetch tool.

## Rules

| Domain | Tool | Reason |
|--------|------|--------|
| `reddit.com` | chrome-devtools | Requires full page rendering + comment loading |
| `linux.do` | chrome-devtools | Requires login state; curl/fetch/webReader will fail or return incomplete content |
| `mp.weixin.qq.com` | `tap wechat article --url {url}` | WeChat article extraction should use the TAP adapter instead of browser rendering |

## Guidelines

- When a URL matches a domain in this table, use the specified tool exclusively — do NOT fall back to curl, fetch, or webReader.
- For domains not listed here, use webReader as the default only if there is no interception.
- If login-state or anti-scraping interception appears on any domain (e.g., 401/403, captcha/challenge pages, "sign in to continue"), switch directly to chrome-devtools and do NOT try other fetch methods.
- If a new domain is found to require special handling (e.g., login-gated content, JS rendering), add it to this table.
