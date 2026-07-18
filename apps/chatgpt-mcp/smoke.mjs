import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { httpServer } from "./server.js";

const transport = new StreamableHTTPClientTransport(new URL("http://127.0.0.1:8787/mcp"));
const client = new Client({ name: "codiscover-smoke-test", version: "0.1.0" });

try {
  await client.connect(transport);
  const listed = await client.listTools();
  const names = listed.tools.map((tool) => tool.name).sort();
  const expected = ["compare_use_cases", "discover_use_cases", "sharpen_use_case"];
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

  console.log(`MCP smoke test passed: ${names.join(", ")}`);
} finally {
  await client.close().catch(() => {});
  await new Promise((resolve) => httpServer.close(resolve));
}
