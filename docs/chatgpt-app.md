# CoDiscover in ordinary ChatGPT conversations

## Product decision

CoDiscover remains one product with one product contract. It now has two delivery surfaces:

1. **Skill surface** — the deeper installable workflow for ChatGPT Desktop and Codex.
2. **ChatGPT App surface** — a lightweight remote MCP layer for ordinary ChatGPT conversations on web and mobile.

This is not a separate Custom GPT and not a standalone website. A user should eventually be able to add `@CoDiscover` to a normal conversation, as they add other published ChatGPT Apps.

## Mobile-first scope

The initial App surface deliberately has no custom iframe UI. OpenAI's Apps SDK makes UI optional, and a conversational interface is the lowest-friction choice for small screens. The server exposes three read-only tools:

- `discover_use_cases`
- `compare_use_cases`
- `sharpen_use_case`

Each tool returns structured content that separates facts, assumptions, and unknowns; retains the four value dimensions; includes a non-AI path; and keeps consequential decisions with a human owner.

## Local QA

From `apps/chatgpt-mcp`:

```text
npm install
npm test
npm run smoke
```

The server health endpoint is `/`; the Streamable HTTP MCP endpoint is `/mcp`.

## Private developer test

1. Deploy the server or expose local port `8787` through an HTTPS tunnel.
2. In ChatGPT, open **Settings → Security and login** and enable Developer mode.
3. Open **Settings → Plugins**, create a developer-mode app, and enter `https://YOUR-HOST/mcp`.
4. Start a new ordinary chat, add CoDiscover from the More menu, and run the mobile test prompts below.
5. Refresh the app configuration after any tool or metadata change.

Suggested tests:

- “Find three Human-AI use cases for meeting decisions that disappear after handoffs.”
- “Compare an AI report drafter with an AI exception queue. Do not combine the four value dimensions into one score.”
- “Sharpen this idea: an agent that automatically handles every incoming request.”

## Public release gates

Public `@CoDiscover` availability cannot be created by inventing an app ID in the repository. The final `.app.json` must use the Apps SDK app ID issued by the platform after app creation. Before submission:

- host `/mcp` on a stable HTTPS service;
- test tools from a clean ChatGPT conversation on web and mobile;
- publish support, privacy, and terms URLs;
- confirm tool metadata, read-only annotations, data handling, and failure behavior;
- record evidence for the three core workflows;
- submit the plugin through OpenAI's plugin submission portal;
- add the platform-issued app ID to `.app.json`, then add `"apps": "./.app.json"` to the plugin manifest.

Until those gates are complete, the local plugin continues to work on Desktop/Codex and the App layer is a developer-testable release candidate.

Draft public documents are available in [Privacy Notice](privacy.md), [Terms of Use](terms.md), and [Support](support.md). Their final public URLs should be inserted into submission metadata after the repository changes are published.
