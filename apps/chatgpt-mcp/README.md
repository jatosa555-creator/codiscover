# CoDiscover ChatGPT App — MCP server

This directory adds a lightweight, read-only ChatGPT App layer to the same CoDiscover product. It is designed for ordinary ChatGPT conversations on web and mobile; no separate Custom GPT or standalone user interface is required.

## Tools

- `discover_use_cases` — find up to three materially different Human-AI workflow opportunities.
- `compare_use_cases` — compare two to five existing ideas without collapsing four value dimensions into one score.
- `sharpen_use_case` — turn a broad or tool-led idea into a workflow-level use case and minimum test.
- `redesign_workflow` — run the optional ReDesign extension with an As-Is X-ray, Lean scan, routes, and human-owned decision gates.
- `learn_from_traces` — run the optional Meta-Lab layer across at least two completed traces or experiments.

All tools are read-only. They label assumptions, retain a non-AI alternative, keep consequential decisions with a named human owner, and do not fabricate ROI or evidence.

## Run locally

```sh
npm install
npm test
npm start
```

The health endpoint is `http://localhost:8787/` and the MCP endpoint is `http://localhost:8787/mcp`.

## Connect during development

1. Expose port `8787` through an HTTPS tunnel or deploy this directory to a Node-compatible host.
2. In ChatGPT, enable Developer mode under **Settings → Security and login**.
3. Under **Settings → Plugins**, create a developer-mode app using `https://YOUR-HOST/mcp`.
4. Add CoDiscover to a new conversation and test it on desktop, web, and mobile.

Public `@CoDiscover` availability requires a stable HTTPS deployment and approval through OpenAI's plugin submission process. The platform supplies the final Apps SDK app ID; do not invent an ID in `.app.json`.
