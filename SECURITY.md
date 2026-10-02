# Security and data boundaries

No telemetry, GitHub writes, remote code execution or automatic actions. Rules mode is local. Jev mode sends only selected issue title/body to TypeSafe over a fixed HTTPS endpoint. Expected labels and extra input fields are not sent. Keys come from the process environment; responses and transport errors are not printed verbatim. Redirects and automatic retries are disabled.

Issue text is untrusted. Prompt instructions, a fixed taxonomy and output validation reduce some failure modes, but do not prevent all prompt injection or semantic errors. Never use these recommendations for security-sensitive access decisions without separate controls.

MCP is a local stdio process for one trusted user. It is not an internet server or multi-tenant service. The directory boundary rejects traversal and escaping symlinks; it does not defend against a hostile process modifying paths concurrently. Scope each server to an explicit data directory.

Input files are bounded to 8 MiB; one issue's title/body to 16,000 UTF-8 bytes; model payloads to 24,000 bytes; responses to 1 MiB; issue batches to 200. No token truncation is performed. Context or rate errors return review. A maximum per-invocation request count is not an account-wide spending cap.

Policy files are trusted local artifacts. Editing a threshold can invalidate its statistical interpretation. Do not treat a policy JSON as a signed certificate. Reports may contain issue IDs and labels; keep private reports out of public repositories. Reports omit title/body but are not guaranteed anonymous.

Do not post credentials or private issue content in public bug reports. Provide a minimal sanitized reproduction. There is no contractual security support or uptime SLA in this preview.
