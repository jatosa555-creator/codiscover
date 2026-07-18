import { createServer } from "node:http";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";
import { compareUseCases, discoverUseCases, sharpenUseCase } from "./discovery.js";

const textResult = (message, structuredContent) => ({
  content: [{ type: "text", text: message }],
  structuredContent
});

export function createCoDiscoverServer() {
  const server = new McpServer({ name: "codiscover", version: "0.1.0" });

  server.registerTool(
    "discover_use_cases",
    {
      title: "Discover Human-AI use cases",
      description: "Use when a person wants practical AI opportunities from a real work challenge, workflow, KPI, role, decision, document, or desired outcome. Returns no more than three materially different workflow-level candidates, a conditional recommendation, a minimum test, non-AI alternatives, and responsibility gates. Do not use when implementation is already decided.",
      inputSchema: {
        challenge: z.string().min(10).describe("The real work challenge, friction, task, workflow, KPI, role, decision, or document context."),
        desired_outcome: z.string().optional().describe("The meaningful outcome the person wants, if known."),
        work_context: z.string().optional().describe("Actors, workflow, constraints, affected people, systems, or organizational context."),
        language: z.enum(["auto", "th", "en"]).default("auto").describe("Preferred response language; use auto to follow the conversation.")
      },
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
    },
    async (args) => textResult("CoDiscover prepared three bounded Human-AI use-case options and a responsible next test.", discoverUseCases(args))
  );

  server.registerTool(
    "compare_use_cases",
    {
      title: "Compare Human-AI use cases",
      description: "Use when a person already has two to five AI use-case ideas and wants a transparent comparison. Keeps Productivity, Impact, Inclusion, and Innovation separate; exposes trade-offs, non-AI paths, and responsibility gaps instead of producing a misleading total score.",
      inputSchema: {
        candidates: z.array(z.string().min(5)).min(2).max(5).describe("Two to five existing use-case ideas."),
        desired_outcome: z.string().optional().describe("The outcome against which the options should be compared."),
        work_context: z.string().optional().describe("Relevant actors, constraints, affected people, data, systems, or decision context."),
        language: z.enum(["auto", "th", "en"]).default("auto")
      },
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
    },
    async (args) => textResult("CoDiscover normalized the options for a transparent, non-aggregated comparison.", compareUseCases(args))
  );

  server.registerTool(
    "sharpen_use_case",
    {
      title: "Sharpen an AI use-case idea",
      description: "Use when an idea is broad, tool-led, feature-led, or vague and needs to become a workflow-level Human-AI use case with actor, trigger, inputs, roles, decision, output, checkpoint, intended value, and a minimum test.",
      inputSchema: {
        idea: z.string().min(10).describe("The current AI idea, however broad or incomplete."),
        desired_outcome: z.string().optional().describe("The intended outcome, if known."),
        work_context: z.string().optional().describe("Relevant actors, workflow, constraints, systems, data, and affected people."),
        language: z.enum(["auto", "th", "en"]).default("auto")
      },
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
    },
    async (args) => textResult("CoDiscover reframed the idea as a bounded Human-AI workflow and minimum test.", sharpenUseCase(args))
  );

  return server;
}

const port = Number(process.env.PORT ?? 8787);
const MCP_PATH = "/mcp";

export const httpServer = createServer(async (req, res) => {
  if (!req.url) return res.writeHead(400).end("Missing URL");
  const url = new URL(req.url, `http://${req.headers.host ?? "localhost"}`);

  if (req.method === "OPTIONS" && url.pathname.startsWith(MCP_PATH)) {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, GET, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "content-type, mcp-session-id",
      "Access-Control-Expose-Headers": "Mcp-Session-Id"
    });
    return res.end();
  }

  if (req.method === "GET" && url.pathname === "/") {
    return res.writeHead(200, { "content-type": "application/json; charset=utf-8" }).end(JSON.stringify({
      name: "CoDiscover ChatGPT App",
      status: "ok",
      mcp: MCP_PATH,
      version: "0.1.0"
    }));
  }

  const mcpMethods = new Set(["POST", "GET", "DELETE"]);
  if (url.pathname === MCP_PATH && req.method && mcpMethods.has(req.method)) {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Expose-Headers", "Mcp-Session-Id");
    const server = createCoDiscoverServer();
    const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
    res.on("close", () => {
      transport.close();
      server.close();
    });
    try {
      await server.connect(transport);
      await transport.handleRequest(req, res);
    } catch (error) {
      console.error("CoDiscover MCP request failed", error);
      if (!res.headersSent) res.writeHead(500).end("Internal server error");
    }
    return;
  }

  res.writeHead(404).end("Not Found");
});

httpServer.listen(port, () => {
  console.log(`CoDiscover MCP server listening on http://localhost:${port}${MCP_PATH}`);
});
