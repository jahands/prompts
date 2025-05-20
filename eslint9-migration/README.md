# Eslint 9 Migration

This guide is for migrating from eslint 8 to 9.

## Prerequisites

Before running the prompt, add this file to your repo:

[eslint9-migration.md](./eslint9-migration.md)

## Prompt

Note: This is a large prompt with many steps. Cursor and similar editors will likely require saying "continue" multiple times.

```
You are an expert AI programmer tasked with migrating a monorepo from ESLint 8 to ESLint 9. Your primary reference for this task is the "LLM-Guided ESLint 8 to ESLint 9 Monorepo Migration" guide, the content of which will be provided to you.

**Goal:**
Automate the migration of the specified monorepo from its current ESLint 8 setup to an ESLint 9 setup using flat configurations.

**Monorepo Details:**
*   Root Path: `[Specify Path to Monorepo Root Here, e.g., /path/to/your/project]`
*   Package Manager: `[Specify pnpm, yarn, or npm - if known, otherwise, instruct LLM to detect]`

**User Preferences:**
*   **Configuration File Type:** Do you want the new ESLint configuration files to be named `eslint.config.ts` (TypeScript) or `eslint.config.js` (JavaScript)? (If TypeScript, the guide's instructions regarding `tsconfig.json` exclusions for these files are particularly relevant. The `workers` example project uses `eslint.config.ts`.)

**Key Instructions & Behavior:**

1.  **Strictly Follow the Guide:** Adhere to all phases, steps, and "LLM Action" items detailed in the "LLM-Guided ESLint 8 to ESLint 9 Monorepo Migration" guide.
2.  **Workspace Context:** You have access to the file system of the specified monorepo to read files, write files, and execute terminal commands as outlined in the guide.
3.  **Tool Usage:** You can use standard command-line tools (like `pnpm`/`yarn`/`npm`, `git`, `node`) and have the ability to read/write/edit files.
4.  **Incremental Progress & Reporting:**
    *   Announce the start and end of each major phase from the guide.
    *   For each significant action taken (e.g., modifying a `package.json`, creating an ESLint config file), briefly state the action and its outcome.
    *   If the guide requires you to choose between options, state your choice and the reason based on the guide's heuristics.
5.  **Error Handling & Clarification:**
    *   If you encounter an error (e.g., a command fails, a plugin is incompatible beyond `FlatCompat`'s capabilities), report the error in detail.
    *   If a situation arises that is not explicitly covered by the guide, or if an instruction is ambiguous for the current context, clearly state the ambiguity and ask for clarification before proceeding.
    *   If the guide instructs you to flag an item for manual review (e.g., `// TODO-LLM:`), ensure this is done clearly in the code or in your summary report.
6.  **Idempotency (Where Possible):** If you need to retry a step, aim to do so in a way that is safe if the step was partially completed.
7.  **Verification:** Perform all verification steps mentioned in the guide, including running ESLint to check for config errors and, finally, to lint the codebase.
8.  **Final Deliverables:**
    *   All `package.json` files updated with new ESLint 9 compatible dependencies.
    *   All legacy ESLint configurations (`.eslintrc.*`, `package.json#eslintConfig`) replaced with the chosen flat configuration file type (`eslint.config.ts` or `eslint.config.js`).
    *   A final summary report detailing:
        *   All actions taken.
        *   Any errors encountered and how they were resolved (or if they remain).
        *   A list of all files modified.
        *   Any items specifically flagged for manual human review (e.g., `// TODO-LLM:` comments).
        *   The outcome of running `eslint . --fix` and any remaining lint errors/warnings.
        *   Confirmation that automated tests (if available and runnable via a standard command like `pnpm test`) were executed and their outcome.

**Before You Begin:**
*   Confirm you have access to the content of the "LLM-Guided ESLint 8 to ESLint 9 Monorepo Migration" guide.
*   Confirm the root path of the monorepo to be migrated.
*   Confirm the user's preference for `eslint.config.ts` or `eslint.config.js`.
*   List the high-level phases from the guide you intend to follow.

Let's begin the migration.
```
