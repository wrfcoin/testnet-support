---
name: Node problem
about: Report a node setup, synchronization or local status problem
title: "[Node problem] "
labels: ''
assignees: ''
---

## OS and platform

- OS name and version:
- CPU architecture (for example, Linux x86_64, Intel Mac, Apple Silicon, or Windows/WSL2):
- Docker and Compose versions, if used:
- Node software version or source commit:

## What happened?

Describe the setup or synchronization step, what you expected, and what happened.
Include the exact error after removing private information.

## Join-script summary

Paste only the relevant final summary lines from the join script, after reviewing
and redacting them. If the script did not reach its summary, give the failing step
and safe error message. Do not attach the full log, configuration or `.env` file.

## Local chain summary

On the computer running the node, run:

```bash
curl -s localhost:8556/network/info
```

Review the output before posting. Remove credentials, tokens, private host
addresses, personal paths and other private details. Paste the safe output below,
or describe the error if no response was returned. Do not add an authorization
token to this command or include one in this issue.

## Status-page screenshot (once available)

If your build includes `http://localhost:8556/dashboard`, attach a cropped,
redacted screenshot showing the problem and the "data as of" time. Otherwise
write "dashboard not available in this build"; a screenshot is optional.
Do not capture the operator-token field or private host details.

## Privacy check

- [ ] I reviewed all text and attachments and removed secrets and tokens,
  including operator tokens, recovery words, private keys, passwords and API keys.
- [ ] I removed private host addresses, personal paths and precise locations;
  I did not attach `.env`, configuration files or unredacted logs.

Report vulnerabilities privately to **security@wrfcoin.com**, not in this issue.
