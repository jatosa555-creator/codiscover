import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { httpServer } from "./server.js";

const transport = new StreamableHTTPClientTransport(new URL("http://127.0.0.1:8787/mcp"));
const client = new Client({ name: "codiscover-smoke-test", version: "0.1.0" });

try {
  await client.connect(transport);
  const listed = await client.listTools();
  const names = listed.tools.map((tool) => tool.name).sort();
  const expected = ["compare_use_cases", "discover_use_cases", "learn_from_traces", "redesign_workflow", "sharpen_use_case"];
  if (JSON.stringify(names) !== JSON.stringify(expected)) {
    throw new Error(`Unexpected tools: ${names.join(", ")}`);
  }

  const result = await client.callTool({
    name: "discover_use_cases",
    arguments: {
      challenge: "Meeting decisions are lost and handoffs have no clear owner.",
      desired_outcome: "Reliable follow-through without removing human accountability"
    }
  });
  if (result?.structuredContent?.candidate_use_cases?.length !== 3) {
    throw new Error("discover_use_cases did not return three candidates");
  }

  const redesign = await client.callTool({
    name: "redesign_workflow",
    arguments: { selected_use_case: "Create a human-approved decision and handoff ledger" }
  });
  if (redesign?.structuredContent?.redesign?.routes?.length !== 3) {
    throw new Error("redesign_workflow did not return three routes");
  }

  const metaLab = await client.callTool({
    name: "learn_from_traces",
    arguments: { traces: [{ id: "CASE-1", learning: "Human checkpoint helped" }, { id: "CASE-2", learning: "Source links reduced disputes" }] }
  });
  if (metaLab?.structuredContent?.meta_lab?.case_ids?.length !== 2) {
    throw new Error("learn_from_traces did not return two cases");
  }

  console.log(`MCP smoke test passed: ${names.join(", ")}`);
} finally {
  await client.close().catch(() => {});
  await new Promise((resolve) => httpServer.close(resolve));
}
