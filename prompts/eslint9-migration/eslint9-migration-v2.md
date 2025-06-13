<eslint9-migration-guide>

<title>ESLint 8 to 9 Migration Guide for TypeScript Monorepos</title>

<description>Step-by-step instructions for migrating a TypeScript monorepo from ESLint 8 (legacy config) to ESLint 9 (flat config)</description>

<context>
<applies-to>TypeScript monorepos using ESLint 8 with .eslintrc.cjs files</applies-to>
<target>ESLint 9 with flat config using eslint.config.ts files</target>
</context>

<overview>
<title>Migration Overview</title>
<transformation>
<before>
- Uses .eslintrc.cjs files throughout the monorepo
- Single shared config: packages/eslint-config/default.cjs
- Simple package.json exports
- Legacy configuration format
</before>
<after>
- Uses eslint.config.ts files throughout the monorepo
- Multiple shared configs with TypeScript support
- Enhanced package.json exports
- Flat configuration format with better TypeScript integration
</after>
</transformation>
</overview>

<migration-steps>

<step number="1">
<name>Update Shared ESLint Config Package</name>

<substep number="1.1">
<name>Update package.json</name>
<description>Replace existing packages/eslint-config/package.json with updated exports and dependencies</description>
<code language="json">
{
  "name": "@repo/eslint-config",
  "version": "0.2.3",
  "private": true,
  "sideEffects": false,
  "exports": {
    ".": "./src/default.config.ts",
    "./react": "./src/react.config.ts"
  },
  "devDependencies": {
    "@eslint/compat": "1.2.9",
    "@eslint/js": "9.27.0",
    "@types/eslint": "9.6.1",
    "@types/node": "22.15.21",
    "@typescript-eslint/eslint-plugin": "8.32.1",
    "@typescript-eslint/parser": "8.32.1",
    "eslint": "9.27.0",
    "eslint-config-prettier": "10.1.5",
    "eslint-config-turbo": "2.5.3",
    "eslint-import-resolver-typescript": "4.3.5",
    "eslint-plugin-astro": "1.3.1",
    "eslint-plugin-import": "2.31.0",
    "eslint-plugin-jsx-a11y": "6.10.2",
    "eslint-plugin-only-warn": "1.1.0",
    "eslint-plugin-react": "7.37.5",
    "eslint-plugin-react-hooks": "5.2.0",
    "eslint-plugin-unused-imports": "4.1.4",
    "typescript": "5.8.2",
    "typescript-eslint": "8.32.1",
    "vitest": "3.1.4"
  }
}
</code>
</substep>

<substep number="1.2">
<name>Create src directory structure</name>
<action>Create packages/eslint-config/src/ directory</action>
</substep>

<substep number="1.3">
<name>Create helpers.ts</name>
<location>packages/eslint-config/src/helpers.ts</location>
<code language="typescript">
import { existsSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { includeIgnoreFile } from '@eslint/compat'

import type { FlatConfig } from '@eslint/compat'

export function getDirname(importMetaUrl: string) {
const **filename = fileURLToPath(importMetaUrl)
return path.dirname(**filename)
}

export function getGitIgnoreFiles(importMetaUrl: string) {
// always include the root gitignore file
const rootGitignorePath = fileURLToPath(new URL('../../../.gitignore', import.meta.url))

const ignoreFiles: FlatConfig[] = [includeIgnoreFile(rootGitignorePath)]

const packageDir = getDirname(importMetaUrl)
const packageGitignorePath = path.join(packageDir, '.gitignore')
if (existsSync(packageGitignorePath)) {
ignoreFiles.push(includeIgnoreFile(packageGitignorePath))
}

return ignoreFiles
}

export function getTsconfigRootDir(importMetaUrl: string) {
const tsconfigRootDir = getDirname(importMetaUrl)
return existsSync(path.join(tsconfigRootDir, 'tsconfig.json')) ? tsconfigRootDir : undefined
}
</code>
</substep>

<substep number="1.4">
<name>Create default.config.ts</name>
<location>packages/eslint-config/src/default.config.ts</location>
<code language="typescript">
import { FlatCompat } from '@eslint/eslintrc'
import eslint from '@eslint/js'
import tsEslintPlugin from '@typescript-eslint/eslint-plugin'
import tsEslintParser from '@typescript-eslint/parser'
import eslintConfigPrettier from 'eslint-config-prettier'
import turboConfig from 'eslint-config-turbo/flat'
// @ts-ignore eslint-plugin-import has no types
import * as importPlugin from 'eslint-plugin-import'
import unusedImportsPlugin from 'eslint-plugin-unused-imports'
import { defineConfig } from 'eslint/config'
import tseslint from 'typescript-eslint'

import { getDirname, getGitIgnoreFiles, getTsconfigRootDir } from './helpers'

export { defineConfig }

const compat = new FlatCompat({
// This helps FlatCompat resolve plugins relative to this config file
baseDirectory: getDirname(import.meta.url),
})

export function getConfig(importMetaUrl: string) {
return defineConfig([
// Global ignores
{
ignores: [
'.*.{js,cjs}',
'**/*.{js,cjs}',
'**/node_modules/**',
'**/dist/**',
'eslint.config.ts',
'**/eslint.config.ts',
'**/worker-configuration.d.ts',
],
},

    ...getGitIgnoreFiles(importMetaUrl),

    eslint.configs.recommended,
    tseslint.configs.recommended,
    importPlugin.flatConfigs?.recommended,
    ...turboConfig,

    // TypeScript Configuration
    {
      files: ['**/*.{ts,tsx,mts}'],
      languageOptions: {
        parser: tsEslintParser,
        parserOptions: {
          ecmaFeatures: {
            jsx: true,
          },
          sourceType: 'module',
          project: true,
          tsconfigRootDir: getTsconfigRootDir(importMetaUrl),
        },
      },
      plugins: {
        'unused-imports': unusedImportsPlugin,
      },
      settings: {
        'import/resolver': {
          typescript: {
            project: './tsconfig.json',
          },
        },
        'import/parsers': {
          '@typescript-eslint/parser': ['.ts', '.tsx', '*.mts'],
        },
      },
      rules: {
        ...tsEslintPlugin.configs.recommended.rules,
        ...importPlugin.configs?.typescript.rules,

        '@typescript-eslint/consistent-type-imports': ['warn', { prefer: 'type-imports' }],
        '@typescript-eslint/explicit-function-return-type': 'off',
        '@typescript-eslint/ban-ts-comment': 'off',
        '@typescript-eslint/no-floating-promises': 'warn',
        'unused-imports/no-unused-imports': 'warn',
        '@typescript-eslint/array-type': ['warn', { default: 'array-simple' }],
        '@typescript-eslint/no-unused-vars': [
          'warn',
          {
            argsIgnorePattern: '^_',
            varsIgnorePattern: '^_',
          },
        ],
        '@typescript-eslint/no-empty-object-type': 'off',
        '@typescript-eslint/no-explicit-any': 'off',
        'import/no-named-as-default': 'off',
        'import/no-named-as-default-member': 'off',
        'prefer-const': 'warn',
        'no-mixed-spaces-and-tabs': ['error', 'smart-tabs'],
        'no-empty': 'warn',

        // Add Prettier last to override other formatting rules
        ...eslintConfigPrettier.rules,
      },
    },

    // Import plugin's TypeScript specific rules using FlatCompat
    ...compat.extends('plugin:import/typescript').map((config) => ({
      ...config,
      files: ['**/*.{ts,tsx,mjs}'],
    })),

    {
      files: ['**/*.spec.ts', '**/*.test.ts', '**/test/**/*.ts', '**/mocks.ts'],
      rules: {
        'import/no-unresolved': 'off',
      },
    },
    {
      files: ['**/*.ts'],
      rules: {
        'import/no-unresolved': 'off',
      },
    },
    {
      files: ['tailwind.config.ts', 'postcss.config.mjs'],
      rules: {
        '@typescript-eslint/no-require-imports': 'off',
      },
    },

    // Prettier (should be last to override other formatting rules)
    { rules: eslintConfigPrettier.rules },

])
}
</code>
</substep>

<substep number="1.5">
<name>Create react.config.ts</name>
<location>packages/eslint-config/src/react.config.ts</location>
<code language="typescript">
import tsEslintParser from '@typescript-eslint/parser'
import eslintConfigPrettier from 'eslint-config-prettier'
import react from 'eslint-plugin-react'
import * as reactHooks from 'eslint-plugin-react-hooks'
import unusedImportsPlugin from 'eslint-plugin-unused-imports'

import { defineConfig, getConfig } from './default.config'
import { getTsconfigRootDir } from './helpers'

export function getReactConfig(importMetaUrl: string) {
return defineConfig([
...getConfig(importMetaUrl),
{
files: ['**/*.{js,jsx,mjs,cjs,ts,tsx}'],
plugins: {
react,
'unused-imports': unusedImportsPlugin,
},
languageOptions: {
parser: tsEslintParser,
parserOptions: {
ecmaFeatures: {
jsx: true,
},
sourceType: 'module',
project: true,
tsconfigRootDir: getTsconfigRootDir(importMetaUrl),
},
},
},
reactHooks.configs['recommended-latest'],
{
rules: {
// this commonly causes false positives with Hono middleware
// that have a similar naming scheme (e.g. useSentry())
'react-hooks/rules-of-hooks': 'off',
},
},

    // Prettier (should be last to override other formatting rules)
    { rules: eslintConfigPrettier.rules },

])
}
</code>
</substep>

<substep number="1.6">
<name>Create eslint.config.ts for config package</name>
<location>packages/eslint-config/eslint.config.ts</location>
<code language="typescript">
import { defineConfig, getConfig } from './src/default.config'

const config = getConfig(import.meta.url)

export default defineConfig([...config])
</code>
</substep>

<substep number="1.7">
<name>Remove old files</name>
<action>Delete packages/eslint-config/default.cjs</action>
</substep>

</step>

<step number="2">
<name>Update Root ESLint Configuration</name>
<action>Replace root .eslintrc.cjs with eslint.config.ts</action>
<code language="typescript">
import { defineConfig, getConfig } from '@repo/eslint-config'

const config = getConfig(import.meta.url)

export default defineConfig([...config])
</code>
<cleanup>Delete old .eslintrc.cjs file</cleanup>
</step>

<step number="3">
<name>Update Package ESLint Configurations</name>

<config-type name="default">
<description>For packages using default config</description>
<action>Replace .eslintrc.cjs with eslint.config.ts</action>
<code language="typescript">
import { defineConfig, getConfig } from '@repo/eslint-config'

const config = getConfig(import.meta.url)

export default defineConfig([...config])
</code>
</config-type>

<config-type name="react">
<description>For packages using React config</description>
<action>Replace .eslintrc.cjs with eslint.config.ts</action>
<code language="typescript">
import { defineConfig } from '@repo/eslint-config'
import { getReactConfig } from '@repo/eslint-config/react'

const config = getReactConfig(import.meta.url)

export default defineConfig([...config])
</code>
</config-type>

</step>

<step number="4">
<name>Update TypeScript Configuration</name>
<description>Exclude eslint.config.ts files from TypeScript compilation</description>

<llm-instructions>
<instruction>Find the TypeScript config package (like packages/typescript-config/)</instruction>
<instruction>Identify all TypeScript config files (.json files)</instruction>
<instruction>For each config file with an exclude array, add "${configDir}/eslint.config.ts"</instruction>
<instruction>Preserve all existing excludes and JSON formatting</instruction>
<instruction>Check individual package tsconfig.json files for custom exclude arrays</instruction>
</llm-instructions>

<transformation>
<before>
<code language="json">
"exclude": ["${configDir}/node_modules/", "${configDir}/dist/"]
</code>
</before>
<after>
<code language="json">
"exclude": ["${configDir}/node_modules/", "${configDir}/dist/", "${configDir}/eslint.config.ts"]
</code>
</after>
</transformation>
</step>

<step number="5">
<name>Update Scripts and Dependencies</name>

<substep number="5.1">
<name>Dependencies</name>
<monorepo-setup>
<description>For monorepos with pnpm workspaces</description>
<note>No additional ESLint dependencies needed - packages will be hoisted from @repo/eslint-config</note>
<npmrc-requirements>
<code language="ini">
auto-install-peers=true
public-hoist-pattern[]=*eslint*
</code>
</npmrc-requirements>
</monorepo-setup>
</substep>

<substep number="5.2">
<name>Update lint scripts</name>
<code language="json">
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix"
  }
}
</code>
</substep>

</step>

<step number="6">
<name>Migration Checklist</name>
<checklist>
- Updated packages/eslint-config/package.json with new exports and dependencies
- Created packages/eslint-config/src/ directory structure
- Created packages/eslint-config/src/helpers.ts
- Created packages/eslint-config/src/default.config.ts
- Created packages/eslint-config/src/react.config.ts
- Created packages/eslint-config/eslint.config.ts
- Deleted old packages/eslint-config/default.cjs
- Updated all TypeScript configs in packages/typescript-config/ to exclude eslint.config.ts
- Replaced root .eslintrc.cjs with eslint.config.ts
- Replaced all package .eslintrc.cjs files with eslint.config.ts
- Verified ESLint dependencies are properly hoisted (no additional dependencies needed)
- Tested linting works using repository's existing commands
- Verified auto-fix works using repository's existing commands
</checklist>
</step>

</migration-steps>

<troubleshooting>
<title>Common Issues and Solutions</title>

<issue>
<name>Import errors for @repo/eslint-config</name>
<solution>
<description>Ensure package.json exports are correct and rebuild workspace dependencies</description>
<code language="bash">
pnpm install
</code>
</solution>
</issue>

<issue>
<name>eslint: command not found in pnpm workspaces</name>
<solution>
<description>Known pnpm issue where .bin symlinks don't get updated properly</description>
<code language="bash">
find . -type d -name node_modules -delete
pnpm install
</code>
<note>With proper dependency hoisting via .npmrc, eslint binary should be available workspace-wide</note>
</solution>
</issue>

<issue>
<name>TypeScript parser errors</name>
<solution>Verify @typescript-eslint/parser version matches across all packages and tsconfig.json exists in package root</solution>
</issue>

<issue>
<name>Plugin resolution errors</name>
<solution>Ensure all required ESLint plugins are installed in packages/eslint-config package, not in individual packages</solution>
</issue>

</troubleshooting>

<testing>
<title>Testing the Migration</title>

<analyze-repository>
<title>Analyze repository tooling</title>
<llm-instructions>
<instruction>Check package.json scripts for lint-related commands (lint, check, eslint)</instruction>
<instruction>Note the package manager (pnpm, npm, yarn)</instruction>
<instruction>Check for build tools (Justfile, Makefile)</instruction>
<instruction>Check turbo.json or turbo.jsonc for lint tasks</instruction>
<instruction>Look for other monorepo tools (Lerna, Nx)</instruction>
</llm-instructions>

<command-determination>
- If Justfile exists with lint/check commands → use `just <command>`
- If package.json has lint scripts → use `<package-manager> run <script>`
- If turbo.json has lint tasks → use `<package-manager> turbo <task>`
- Otherwise → use direct ESLint commands
</command-determination>
</analyze-repository>

<test-steps>
<instruction>Install dependencies using repository's package manager</instruction>
<instruction>Run the linting commands identified above</instruction>
<instruction>Test auto-fix if available</instruction>
<instruction>Verify individual packages can be linted if needed</instruction>
</test-steps>

<verification-checklist>
- ESLint runs without configuration errors
- TypeScript files are properly linted
- Import/export rules work correctly
- Auto-fix functionality works
- All packages can be linted individually
</verification-checklist>

</testing>

<llm-notes>
<title>Notes for LLMs</title>
<guidelines>
- Always backup existing ESLint configurations before starting
- Check for custom rules in existing .eslintrc.cjs files and port them to new config
- Verify package structure matches expected monorepo layout
- Verify pnpm workspace setup - ensure .npmrc has proper hoisting configuration
- If "eslint: command not found" - remove all node_modules and reinstall to fix pnpm .bin symlink issues
- Test thoroughly after migration by running lint commands
- Handle React packages separately using the React config
- Update any CI/CD scripts that reference old ESLint configuration paths
- Check for additional ignore patterns that may need to be added to global ignores
</guidelines>
<note>Migration preserves all existing functionality while providing better TypeScript integration and modern ESLint 9 features</note>
</llm-notes>

</eslint9-migration-guide>
