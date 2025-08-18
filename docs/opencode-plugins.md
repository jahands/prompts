# Opencode Plugins Documentation

Opencode provides a powerful plugin system that allows you to extend its functionality through TypeScript/JavaScript plugins. Plugins use a hook-based architecture to intercept and modify various operations throughout the application lifecycle.

## Plugin Architecture

Opencode plugins follow a **hook-based architecture** where plugins can:

- Intercept tool executions (bash, read, edit, etc.)
- Modify chat system behavior
- Handle authentication providers
- Manage permissions
- Respond to application events

## Plugin Discovery and Loading

Plugins are automatically discovered and loaded from three sources:

1. **Local Project Plugins**: `.opencode/plugin/*.{ts,js}` files in your project root
2. **Global User Plugins**: `~/.config/opencode/plugin/*.{ts,js}` files
3. **NPM Packages**: Distributed plugins with `opencode-*` naming pattern

## Core TypeScript Types

### Plugin Function Signature

```typescript
export type Plugin = (input: PluginInput) => Promise<Hooks>

export type PluginInput = {
  client: ReturnType<typeof createOpencodeClient> // SDK client for API calls
  app: App // Application instance
  $: BunShell // Shell execution API
}
```

### Available Hook Interfaces

```typescript
export interface Hooks {
  // General event handling
  event?: (input: { event: Event }) => Promise<void>

  // Authentication system
  auth?: {
    provider: string
    loader?: (
      auth: () => Promise<Auth>,
      provider: Provider
    ) => Promise<Record<string, any>>
    methods: AuthMethod[]
  }

  // Chat system hooks
  "chat.message"?: (
    input: {},
    output: { message: UserMessage; parts: Part[] }
  ) => Promise<void>
  "chat.params"?: (
    input: { model: Model; provider: Provider; message: UserMessage },
    output: { temperature: number; topP: number; options: Record<string, any> }
  ) => Promise<void>

  // Permission system
  "permission.ask"?: (
    input: Permission,
    output: { status: "ask" | "deny" | "allow" }
  ) => Promise<void>

  // Tool execution hooks
  "tool.execute.before"?: (
    input: { tool: string; sessionID: string; callID: string },
    output: { args: any }
  ) => Promise<void>

  "tool.execute.after"?: (
    input: { tool: string; sessionID: string; callID: string },
    output: { title: string; output: string; metadata: any }
  ) => Promise<void>
}
```

## Creating Your First Plugin

### 1. Basic Plugin Structure

Create a file at `.opencode/plugin/my-plugin.ts`:

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({ app, client, $ }) => {
  // Plugin initialization logic
  console.log("Plugin initializing...")

  return {
    // Hook implementations
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        console.log("Session went idle")
      }
    },

    "tool.execute.before": async (input, output) => {
      if (input.tool === "bash") {
        console.log(`Bash command: ${output.args.command}`)
      }
    },
  }
}
```

### 2. Advanced Plugin Example

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const SecurityPlugin: Plugin = async ({ app, client, $ }) => {
  const state = {
    dangerousCommands: ["rm -rf", "format", "del /f"],
    sessionActivity: new Map(),
  }

  return {
    // Block dangerous commands
    "tool.execute.before": async (input, output) => {
      if (input.tool === "bash") {
        const command = output.args.command?.toLowerCase() || ""

        for (const dangerous of state.dangerousCommands) {
          if (command.includes(dangerous)) {
            throw new Error(
              `Dangerous command "${dangerous}" blocked by security plugin`
            )
          }
        }
      }

      // Log tool usage
      const session = state.sessionActivity.get(input.sessionID) || []
      session.push({ tool: input.tool, timestamp: Date.now() })
      state.sessionActivity.set(input.sessionID, session)
    },

    // Modify chat parameters based on activity
    "chat.params": async (input, output) => {
      const session = state.sessionActivity.get(input.message.sessionId) || []

      // Reduce temperature for very active sessions
      if (session.length > 10) {
        output.temperature = Math.min(output.temperature * 0.8, 1.0)
      }
    },

    // Auto-deny access to sensitive files
    "permission.ask": async (input, output) => {
      if (input.type === "file.read" && input.path) {
        const sensitiveFiles = [".env", "secrets.json", "private.key"]

        if (sensitiveFiles.some((file) => input.path.includes(file))) {
          output.status = "deny"
          console.log(`Blocked access to sensitive file: ${input.path}`)
        }
      }
    },

    // Handle various events
    event: async ({ event }) => {
      switch (event.type) {
        case "session.updated":
          console.log("Session updated")
          break
        case "file.edited":
          console.log(`File edited: ${event.data?.path}`)
          break
        case "session.error":
          console.error("Session error occurred")
          break
      }
    },
  }
}
```

## Available APIs

### Shell API Integration

Plugins have access to Bun's shell API through the `$` parameter:

```typescript
export const ShellPlugin: Plugin = async ({ $, app, client }) => {
  return {
    "tool.execute.after": async (input, output) => {
      if (input.tool === "bash") {
        // Execute additional commands using shell API
        try {
          const result = await $`ls -la`
          console.log("Directory listing:", result.stdout.toString())
        } catch (error) {
          console.error("Shell command failed:", error)
        }
      }
    },
  }
}
```

### SDK Client Access

The `client` parameter provides access to the opencode SDK:

```typescript
export const APIPlugin: Plugin = async ({ client, app, $ }) => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.updated") {
        // Make API calls using the SDK client
        try {
          const sessions = await client.session.list()
          console.log(`Total sessions: ${sessions.length}`)
        } catch (error) {
          console.error("API call failed:", error)
        }
      }
    },
  }
}
```

## Event Types

The plugin system provides access to these event types:

- `installation.updated` - Installation version changes
- `lsp.client.diagnostics` - Language server diagnostics
- `message.updated/removed` - Chat message changes
- `message.part.updated/removed` - Message part changes
- `storage.write` - Storage operations
- `permission.updated/replied` - Permission system events
- `file.edited` - File modification events
- `session.updated/deleted/idle/error` - Session lifecycle
- `server.connected` - Server connection events
- `file.watcher.updated` - File watching events
- `ide.installed` - IDE integration events

## Tool Interception

Plugins can intercept and modify execution of any opencode tool:

- `bash` - Shell command execution
- `read` - File reading operations
- `edit` - File editing operations
- `glob` - File pattern matching
- `grep` - Text searching
- All other opencode tools

## Authentication Plugins

Create custom authentication providers:

```typescript
export const CustomAuthPlugin: Plugin = async ({ app, client, $ }) => {
  return {
    auth: {
      provider: "custom-oauth",
      methods: [
        {
          type: "oauth",
          name: "Custom OAuth",
          config: {
            authUrl: "https://auth.example.com/oauth",
            tokenUrl: "https://auth.example.com/token",
            clientId: "your-client-id",
          },
        },
      ],
    },
  }
}
```

## Best Practices

### 1. Type Safety

Always use the `Plugin` type for proper TypeScript support:

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({ app, client, $ }) => {
  // TypeScript will provide full type checking
}
```

### 2. Error Handling

Wrap plugin logic in try-catch blocks to prevent crashes:

```typescript
export const SafePlugin: Plugin = async ({ app, client, $ }) => {
  return {
    "tool.execute.before": async (input, output) => {
      try {
        // Plugin logic here
      } catch (error) {
        console.error("Plugin error:", error)
        // Don't re-throw unless you want to block the operation
      }
    },
  }
}
```

### 3. Performance Considerations

Be mindful of performance in frequently called hooks:

```typescript
export const PerformantPlugin: Plugin = async ({ app, client, $ }) => {
  const cache = new Map()

  return {
    "tool.execute.before": async (input, output) => {
      // Cache expensive operations
      if (cache.has(input.tool)) {
        return cache.get(input.tool)
      }

      const result = expensiveOperation(input.tool)
      cache.set(input.tool, result)
      return result
    },
  }
}
```

### 4. Resource Cleanup

Clean up resources when possible:

```typescript
export const ResourcePlugin: Plugin = async ({ app, client, $ }) => {
  const intervals = new Set()

  // Clean up on process exit
  process.on("exit", () => {
    intervals.forEach(clearInterval)
  })

  return {
    event: async ({ event }) => {
      if (event.type === "session.updated") {
        const interval = setInterval(() => {
          // Periodic task
        }, 60000)
        intervals.add(interval)
      }
    },
  }
}
```

## Plugin Distribution

### Local Development

For local development, place plugins in `.opencode/plugin/` directory.

### Global Plugins

For user-wide plugins, place them in `~/.config/opencode/plugin/`.

### NPM Packages

For distributable plugins:

1. Create an NPM package with name pattern `opencode-*-plugin`
2. Export your plugin as the default export
3. Include proper TypeScript declarations
4. Users can install with `npm install opencode-your-plugin`

## Debugging Plugins

### Logging

Use console methods for debugging:

```typescript
export const DebugPlugin: Plugin = async ({ app, client, $ }) => {
  console.log("Plugin loaded")

  return {
    event: async ({ event }) => {
      console.debug("Event received:", event.type, event.data)
    },
  }
}
```

### Error Tracking

Track and report plugin errors:

```typescript
export const ErrorTrackingPlugin: Plugin = async ({ app, client, $ }) => {
  return {
    "tool.execute.before": async (input, output) => {
      try {
        // Plugin logic
      } catch (error) {
        console.error(`Plugin error in ${input.tool}:`, error)
        // Optionally report to external service
      }
    },
  }
}
```

## Configuration

Plugins can be configured through `opencode.json` or `opencode.jsonc`:

```json
{
  "plugins": {
    "local": ["security-plugin", "custom-auth"],
    "npm": ["opencode-analytics-plugin", "opencode-github-plugin"]
  }
}
```

This plugin system provides a powerful, type-safe way to extend opencode's functionality while maintaining clean separation of concerns and robust error handling.
