# Triage guide for the testnet owner

Use this guide to turn an incoming support issue into a clear next step without requesting secrets or promising a response deadline. The [support policy](SUPPORT.md) and [security policy](SECURITY.md) apply throughout.

## First pass

1. Read the selected template and check whether the report includes secrets, precise location, private host details or a suspected vulnerability before quoting or copying it.
2. If sensitive material appears, do not repeat it or ask for more in public; direct the reporter to the security policy and use GitHub's sensitive-data handling process as appropriate.
3. Check for an existing report of the same symptom and version; link related issues rather than making the reporter repeat their evidence.
4. Add an existing label, state what is known, and ask only for the smallest missing evidence needed to choose the next step.
5. Record the affected version, reproduction status and next owner/action in a comment; update the reporter when the diagnosis changes.

## Labels

The repository already has the following labels; this guide does not create a new label scheme or change settings.

| Label | When to use it |
| --- | --- |
| `question` | Setup help or an unanswered usage question. |
| `bug` | A reproducible defect, or a concrete defect report awaiting reproduction. |
| `documentation` | Missing, misleading or outdated instructions. |
| `enhancement` | A proposed capability rather than a malfunction. |
| `duplicate` | The same problem is tracked elsewhere; include the canonical issue link. |
| `help wanted` | A defined task where outside assistance is welcome. |
| `good first issue` | A small, well-described task with clear acceptance criteria. |
| `invalid` | Evidence shows the report does not apply; explain why courteously. |

Do not label a report invalid merely because it lacks detail, and do not promise a feature or schedule when applying enhancement labels.

## First-response templates

Adapt these replies to evidence already present; do not ask the reporter to resend it.

### Wallet help

> Thanks for the report. Which app/page and version are you using, and did this happen during creation, unlock, receive or send? Please share the safe error text and approximate time. An existing transaction ID is optional if you are comfortable making it public. Never send recovery words, private keys or passwords, and do not send another transaction just to reproduce the problem.

### Faucet help

> Please share the page/app version, approximate request time and safe response text. Did the request return a transaction ID, or stop before submission? A public address or transaction ID is optional. Test tokens have no monetary value; please avoid repeated requests while we investigate.

### Station connection help

> Which station type and app/page version are involved, and at which connection or submission step does it stop? Please share a redacted error and whether this worked previously. Do not include station API keys, credentials, precise coordinates or private network addresses.

### Node problem

> Please use the [Node problem template](.github/ISSUE_TEMPLATE/node_operator.md) to provide OS/CPU architecture, software version, the safe join summary and redacted local chain summary. If your build has a dashboard, a cropped screenshot with its data timestamp is optional; never include the operator-token field.

### Bug report

> Please provide the smallest reproduction steps, expected and actual results, version and safe error text. Does it happen consistently? Review screenshots and logs for secrets and private details before posting; a complete log or configuration file is not needed.

### Feature request

> What task are you trying to complete, and what limitation prevents it today? Describe the outcome you need and any workaround. We can discuss scope and constraints here, but this does not commit the project to delivery or a date.

## When to request the node-problem bundle

Request the bundle when the issue concerns installation, joining, synchronization, peers or local node status, or when a client report has been narrowed to the reporter's own node. Do not request it for a general website/wallet question without evidence of a node-side cause.

The [Node problem template](.github/ISSUE_TEMPLATE/node_operator.md) defines the bundle: OS/platform and version, redacted join-script summary, reviewed output of `curl -s localhost:8556/network/info`, and an optional dashboard screenshot when available. If the command fails, safe error text is enough. Do not ask for a bearer token, full logs, `.env`, key files or a remote-access session.

## Security routing

Suspected key exposure, unauthorized access, signature/authentication bypass, exploitable privacy leakage or other vulnerabilities belong at **security@wrfcoin.com**, following [SECURITY.md](SECURITY.md), rather than in public issue details. A suitable reply is:

> This may be security-sensitive. Please stop posting technical details here and follow our private security-reporting policy. Do not send us private keys, recovery words or access tokens. We will keep any public tracking note free of exploit details and secrets.

A routine unavailable service is not automatically a vulnerability; ask for safe symptoms before choosing the route. Never promise a bounty.

## Response expectations and follow-through

Support is best effort: there is **no guaranteed response time, uptime, recovery of funds or delivery date**. Acknowledge what is known and say when there is no update; do not invent an SLA or imply a queue position guarantees action.

When a change becomes available, link the relevant public change and describe the version and evidence. Ask the reporter to confirm the original symptom with safe steps, distinguish source changes from deployed behavior, and document any remaining limitation before the owner changes the issue's status. A passing test alone does not establish the reporter's device or node is working.
