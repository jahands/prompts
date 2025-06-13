<eslint9-migration-guide>

<title>LLM-Guided ESLint 8 to ESLint 9 Monorepo Migration</title>

<description>Comprehensive step-by-step guide for LLMs to automate migration of TypeScript monorepos from ESLint 8 to ESLint 9 using flat config</description>

<introduction>
<purpose>
<title>Purpose of Guide</title>
<content>
Document serves as comprehensive step-by-step guide for Large Language Model to automate migration of TypeScript-based monorepo from ESLint version 8 to ESLint version 9. Focus exclusively on projects using eslint.config.ts for ESLint configuration (flat config model)
</content>
</purpose>

<eslint9-changes>
<title>Overview of ESLint 9 Changes</title>
<key-changes>
- Full adoption of flat config system using eslint.config.ts file that exports array of configuration objects
- Replaces legacy .eslintrc.* file formats and eslintConfig key in package.json
- Explicit plugin imports required
- Different handling of extends
- More granular control through files and ignores properties within config objects
</key-changes>
</eslint9-changes>

<migration-goals>
<title>Goals of Automated Migration</title>
<goals>
- Prerequisite Checks: Verify necessary tools and assess initial ESLint setup
- Dependency Management: Update ESLint and core plugins to ESLint 9 compatible versions
- Flat Config Migration: Convert all existing ESLint configurations to new eslint.config.ts format
- Shared Configuration Handling: Migrate dedicated shared ESLint configuration package correctly
- Rule Updates: Address deprecated, removed, or changed rules
- Verification: Execute ESLint to ensure it runs without configuration errors
- Maintainability: Produce clean, maintainable, type-safe ESLint setup
- TypeScript Focus: Tailored for monorepos where TypeScript is primary language
</goals>
</migration-goals>
</introduction>

<prerequisites>
<title>Prerequisites and Setup</title>

<required-tools>
<title>Required Tools</title>
<tools>
- Node.js: v18.18.0, v20.9.0 or later (required by ESLint v9)
- Package manager: pnpm, yarn, or npm (commands may assume pnpm, adjust as needed)
- jq: Useful for parsing package.json files from command line (optional)
</tools>
<llm-action>Verify these tools are available or guide user on installation</llm-action>
</required-tools>

<workspace-assessment>
<title>Initial Workspace Assessment</title>
<commands>
<command type="primary">
<description>Check ESLint version at monorepo root</description>
<code>pnpm exec eslint --version</code>
<note>Primary indicator of ESLint version used for development and CLI tasks</note>
</command>
<command type="optional">
<description>Check shared ESLint config package</description>
<note>Examine package.json of dedicated shared ESLint configuration package if identified</note>
</command>
</commands>
<llm-actions>
- Store primary ESLint version for later comparison
- Identify monorepo package manager by checking lock files
- Avoid running eslint --version in every individual package
</llm-actions>
</workspace-assessment>
</prerequisites>

<phase-1-discovery>
<title>Phase 1: Discovery and Planning</title>

<identify-packages>
<title>Identifying All Packages in Monorepo</title>
<llm-actions>
- Parse workspace configuration to find all member packages
- For pnpm: Read pnpm-workspace.yaml packages list
- For yarn/npm: Read workspaces array in root package.json
- For lerna: Read packages array in lerna.json
- Create list of absolute or relative paths to each package directory
</llm-actions>
</identify-packages>

<locate-configs>
<title>Locating ESLint Configurations</title>
<search-locations>
- .eslintrc.js
- .eslintrc.cjs
- .eslintrc.yaml
- .eslintrc.yml
- .eslintrc.json
- eslintConfig key in package.json
</search-locations>
<llm-actions>
- Search each identified package and monorepo root
- Record path and format of each found configuration file
- Determine if any configurations belong to dedicated shared ESLint configuration package
- Look for packages named eslint-config, @repo/eslint-config, shared/eslint-config
</llm-actions>
</locate-configs>

<identify-dependencies>
<title>Identifying ESLint-related Dependencies</title>
<locations>
<location type="primary">
<name>Shared ESLint Config Package</name>
<actions>
- Read package.json file
- Extract all dependencies and devDependencies with ESLint-related prefixes
</actions>
</location>
<location type="secondary">
<name>Monorepo Root</name>
<actions>
- Read root package.json file
- Extract all dependencies and devDependencies with ESLint-related prefixes
</actions>
</location>
</locations>
<prefixes>
- eslint (core library)
- eslint-plugin-
- eslint-config-
- @eslint/
- @typescript-eslint/ (parser and plugin)
- eslint-import-resolver-typescript
- eslint-plugin-react
</prefixes>
<llm-action>Compile comprehensive list of unique ESLint-related packages and versions</llm-action>
</identify-dependencies>

<migration-plan>
<title>Creating Migration Plan</title>
<order-of-operations>
1. Update shared ESLint config packages dependencies
2. Migrate shared ESLint configs to flat format
3. Update consuming packages dependencies
4. Migrate consuming packages ESLint configs to flat format
5. Address root monorepo ESLint configuration
</order-of-operations>
<critical-checkpoint>
<condition>No dedicated shared ESLint configuration package found</condition>
<action>ABORT MIGRATION</action>
<message>Migration aborted. This automated process is designed for monorepos that include a dedicated package for shared ESLint configurations. No such package was identified in this monorepo.</message>
</critical-checkpoint>
</migration-plan>
</phase-1-discovery>

<phase-2-dependencies>
<title>Phase 2: Updating Dependencies</title>

<goal>Update ESLint, core plugins, and all ESLint-related packages to latest versions. FlatCompat will be used in Phase 5 for plugins not yet supporting flat config directly</goal>

<target-versions>
<version package="eslint">Target latest ESLint v9.x.x</version>
<version package="others">Target latest available version for all plugins, configs, parsers</version>
<rationale>Attempting to update to absolute latest version first simplifies process. Compatibility addressed in Phase 5 using FlatCompat if necessary</rationale>
</target-versions>

<update-process>
<step name="determine-target">
<title>Determine Target Version</title>
<actions>
- For eslint: Target latest ESLint v9.x.x
- For all other packages: Target latest available version
</actions>
</step>

<step name="update-via-package-manager">
<title>Update Dependencies via Package Manager</title>
<actions>
- Construct appropriate command for detected package manager
- Update dependency to target version/tag
- Package manager resolves tags and writes final semantic version
</actions>
<examples>
<example type="pnpm">
<code>pnpm add -D eslint@^9.0.0 some-plugin@latest --filter my-app</code>
</example>
<example type="yarn">
<code>yarn workspace my-app add -D eslint@^9.0.0 some-plugin@latest</code>
</example>
<example type="npm">
<code>cd packages/my-app && npm install -D eslint@^9.0.0 some-plugin@latest && cd -</code>
</example>
</examples>
</step>

<step name="install-consolidate">
<title>Install Updated Dependencies</title>
<actions>
- Run general install command from monorepo root
- Ensure lockfile is fully updated
- All dependencies correctly installed according to modified package.json files
</actions>
</step>

<step name="initial-verification">
<title>Initial Verification (Optional)</title>
<actions>
- Run eslint --version in key packages or root
- Ensure core ESLint version updated as expected
</actions>
</step>
</update-process>
</phase-2-dependencies>

<phase-3-flat-config>
<title>Phase 3: Migrating to Flat Config</title>

<core-tooling>
<tool name="eslint.config.ts">New configuration file name</tool>
<tool name="@eslint/eslintrc">Provides FlatCompat utility for legacy configurations/plugins</tool>
</core-tooling>

<flat-config-principles>
<title>General Principles of Flat Config</title>
<principles>
- Config is array of configuration objects exported as default from eslint.config.ts
- Each object can specify: files, ignores, languageOptions, plugins, rules, processor, settings
- Configuration applied by merging objects in array
- Later objects can override earlier ones if they apply to same files
- extends no longer direct key - shareable configs imported and spread into main array
- Plugins explicitly imported and configured in plugins key
</principles>
</flat-config-principles>

<migration-steps>
<title>Key Steps for Migration</title>

<step name="create-config">
<title>Create eslint.config.ts</title>
<actions>
- Create new eslint.config.ts in same directory as old config
- Ensure excluded from project tsconfig.json to avoid conflicts
- Add to exclude array in tsconfig.json
</actions>
</step>

<step name="initialize-flatcompat">
<title>Initialize FlatCompat if Needed</title>
<condition>Old config uses plugins or extends configs not flat-config-ready</condition>
<example>
<code language="typescript">
import { FlatCompat } from "@eslint/eslintrc";
import path from "path";
import { fileURLToPath } from "url";
import js from '@eslint/js';

const **filename = fileURLToPath(import.meta.url);
const **dirname = path.dirname(\_\_filename);

const compat = new FlatCompat({
baseDirectory: \_\_dirname,
// recommendedConfig: js.configs.recommended,
// allConfig: js.configs.all
});
</code>
</example>
</step>

<step name="translate-config">
<title>Translate Configuration Sections</title>
<note>Detailed mapping provided in subsequent sections</note>
</step>

<step name="delete-old">
<title>Delete Old Config File</title>
<actions>
- Delete old .eslintrc.* file after successful migration
- Remove eslintConfig from package.json if present
</actions>
</step>
</migration-steps>

<config-mapping>
<title>Mapping Legacy Config Keys to Flat Config</title>

<mapping key="extends">
<legacy>extends</legacy>
<flat-approach>Import shareable config directly and spread into array</flat-approach>
<examples>
<example type="direct-import">
<code language="typescript">
import someSharedFlatConfig from '@repo/eslint-config/flat';
import { defineConfig } from 'eslint/config';

export default defineConfig([
...someSharedFlatConfig,
// ... other configs
]);
</code>
</example>
<example type="flatcompat">
<code language="typescript">
import { FlatCompat } from "@eslint/eslintrc";
import { defineConfig } from 'eslint/config';

export default defineConfig([
...compat.extends("eslint:recommended", "plugin:react/recommended"),
// ... other configs
]);
</code>
</example>
</examples>
</mapping>

<mapping key="plugins">
<legacy>plugins</legacy>
<flat-approach>Import plugin and add to plugins object within config block</flat-approach>
<examples>
<example type="native">
<code language="typescript">
import somePlugin from 'eslint-plugin-some-plugin';
import { defineConfig } from 'eslint/config';

export default defineConfig([
{
plugins: { 'some-prefix': somePlugin },
rules: { 'some-prefix/some-rule': 'error' }
}
]);
</code>
</example>
<example type="import-plugin">
<code language="typescript">
// @ts-expect-error eslint-plugin-import has no types
import \* as importPlugin from 'eslint-plugin-import';

export default defineConfig([
{
plugins: { 'import': importPlugin },
settings: { 'import/resolver': { typescript: {} } },
rules: { ...importPlugin.configs.recommended.rules }
}
]);
</code>
</example>
</examples>
</mapping>

<mapping key="rules">
<legacy>rules</legacy>
<flat-approach>Place directly in config object rules key</flat-approach>
<example>
<code language="typescript">
export default defineConfig([
    {
        files: ["**/*.js"],
        rules: {
            semi: ["error", "always"],
            'no-unused-vars': 'warn'
        }
    }
]);
</code>
</example>
</mapping>

<mapping key="parser-options">
<legacy>parser and parserOptions</legacy>
<flat-approach>Placed under languageOptions.parser and languageOptions.parserOptions</flat-approach>
<example>
<code language="typescript">
import tsParser from '@typescript-eslint/parser';
import { defineConfig } from 'eslint/config';

export default defineConfig([
{
files: ["**/*.ts", "**/*.tsx"],
languageOptions: {
parser: tsParser,
parserOptions: {
project: './tsconfig.json',
sourceType: 'module',
ecmaVersion: 2022
}
}
}
]);
</code>
</example>
</mapping>

<mapping key="env-globals">
<legacy>env and globals</legacy>
<flat-approach>Mapped to languageOptions.globals using helper objects</flat-approach>
<example>
<code language="typescript">
import globals from 'globals';
import { defineConfig } from 'eslint/config';

export default defineConfig([
{
languageOptions: {
globals: {
...globals.browser,
...globals.node,
myCustomGlobal: 'readonly'
}
}
}
]);
</code>
</example>
</mapping>

<mapping key="overrides">
<legacy>overrides</legacy>
<flat-approach>Each override becomes separate configuration object in top-level array</flat-approach>
<example>
<code language="typescript">
export default defineConfig([
    { // Default rules
        rules: { 'default-rule': 'error' }
    },
    { // Override for test files
        files: ["*.test.js"],
        rules: { 'test-specific-rule': 'warn' }
    }
]);
</code>
</example>
</mapping>

<mapping key="ignore-patterns">
<legacy>ignorePatterns</legacy>
<flat-approach>Placed in ignores array at top level of config object</flat-approach>
<example>
<code language="typescript">
export default defineConfig([
    {
        ignores: ["dist/", "node_modules/", "**/*.bak"]
    },
    // ...other configuration objects
]);
</code>
</example>
</mapping>

<mapping key="settings">
<legacy>settings</legacy>
<flat-approach>Placed in settings object within configuration block</flat-approach>
<example>
<code language="typescript">
export default defineConfig([
    {
        settings: {
            'import/resolver': { typescript: {} }
        }
    }
]);
</code>
</example>
</mapping>
</config-mapping>

<shared-config-structure>
<title>Structuring Shared ESLint Configuration Package</title>

<recommended-structure>
<structure-item>
<name>Configuration Files</name>
<description>Define different base configurations in separate files within shared package</description>
<examples>
- packages/eslint-config/src/default.config.ts
- packages/eslint-config/src/react.config.ts
</examples>
</structure-item>

<structure-item>
<name>Exported Functions</name>
<description>Each file exports function returning flat config array wrapped with defineConfig</description>
<important>Exported functions must return array explicitly wrapped with defineConfig from eslint/config</important>
<example>
<code language="typescript">
import tseslint from 'typescript-eslint';
import js from '@eslint/js';
import { defineConfig } from 'eslint/config';

export function getDefaultConfig(importMetaUrl: string) {
return defineConfig([
js.configs.recommended,
tseslint.configs.recommended,
{
files: ["**/*.{ts,tsx,mts}"],
languageOptions: {
parser: tseslint.parser,
parserOptions: {
project: true,
sourceType: "module",
},
},
rules: {
'@typescript-eslint/no-unused-vars': 'warn',
},
},
]);
}
</code>
</example>
</structure-item>

<structure-item>
<name>Package.json Exports</name>
<description>Use exports field to define how configurations are imported</description>
<example>
<code language="json">
{
    "name": "@repo/eslint-config",
    "main": "./src/default.config.ts",
    "exports": {
        ".": "./src/default.config.ts",
        "./default": "./src/default.config.ts",
        "./react": "./src/react.config.ts"
    }
}
</code>
</example>
</structure-item>
</recommended-structure>

<consuming-packages>
<title>Consuming Shared Configurations</title>
<example>
<code language="typescript">
import tseslint from 'typescript-eslint';
import { getDefaultConfig } from '@repo/eslint-config/default';
import { defineConfig } from 'eslint/config';
import type { Linter } from 'eslint';

const baseConfigArray = getDefaultConfig(import.meta.url);

const finalConfig: Linter.FlatConfig[] = [
...baseConfigArray,
{
files: ["src/**/*.ts"],
rules: {
"my-app-specific-rule": "warn"
}
}
];

export default defineConfig(finalConfig);
</code>
</example>
</consuming-packages>
</shared-config-structure>
</phase-3-flat-config>

<phase-4-rule-changes>
<title>Phase 4: Addressing Rule Changes and Deprecations</title>

<goal>Identify and update ESLint rules that have been deprecated, removed, or had options changed due to upgrade to ESLint v9 and new plugin versions</goal>

<identifying-issues>
<title>Identifying Deprecated/Changed Rules</title>
<steps>
<step>
<name>Run ESLint</name>
<action>Execute eslint . across codebase with new eslint.config.ts files</action>
<expected-outcomes>
- Unknown rules (if rule was removed)
- Invalid rule options (if rule configuration schema changed)
- Deprecation warnings for rules still functional but will be removed
</expected-outcomes>
</step>
<step>
<name>Parse ESLint Output</name>
<action>Capture and analyze output from ESLint command</action>
<task>Systematically list all reported rule-specific errors and warnings</task>
</step>
<step>
<name>Consult Changelogs</name>
<actions>
- Determine if core ESLint rule or from plugin
- Search changelog of ESLint core or specific plugin
- Look for Breaking Changes, Deprecations, or New Rules/Features sections
</actions>
</step>
</steps>
</identifying-issues>

<replacement-patterns>
<title>Common Patterns for Replacing/Updating Rules</title>

<pattern type="renamed">
<symptom>ESLint reports unknown rule but changelog indicates renamed or moved</symptom>
<action>Update rule name in eslint.config.ts and ensure new plugin installed</action>
</pattern>

<pattern type="options-changed">
<symptom>ESLint reports invalid options for rule</symptom>
<action>Consult rule documentation for new valid options and update configuration</action>
</pattern>

<pattern type="deprecated-with-replacement">
<symptom>ESLint issues deprecation warning with suggested replacement</symptom>
<action>Replace old rule with new rule and adjust options as needed</action>
</pattern>

<pattern type="functionality-merged">
<symptom>Deprecation warning indicates functionality merged into another rule</symptom>
<action>Remove deprecated rule and ensure broader rule configured appropriately</action>
</pattern>

<pattern type="no-replacement">
<symptom>Deprecation warning or unknown rule with no direct replacement</symptom>
<actions>
- Understand intent of original rule
- Search for alternative rules achieving similar goal
- Flag for manual review with TODO-LLM comment
- Consider removing if minor stylistic preference
</actions>
</pattern>

<pattern type="plugin-deprecated">
<symptom>Entire plugin no longer maintained or superseded</symptom>
<actions>
- Remove old plugin from dependencies
- Install new plugin if applicable
- Re-evaluate rules from old plugin
</actions>
</pattern>
</replacement-patterns>

<iterative-refinement>
<title>Iterative Refinement</title>
<actions>
- Re-run ESLint after attempting fixes
- Repeat identification and replacement steps
- Continue until ESLint runs without configuration errors
</actions>
</iterative-refinement>
</phase-4-rule-changes>

<phase-5-verification>
<title>Phase 5: Execution and Verification</title>

<goal>Ensure new ESLint setup works correctly across entire monorepo, apply auto-fixable changes, identify remaining issues</goal>

<execution-steps>
<step name="run-comprehensive">
<title>Running ESLint Across Monorepo</title>
<command>pnpm exec eslint . --format stylish</command>
<tasks>
- Examine output for unexpected errors or large volume of new warnings
- If configuration errors, revisit Phase 3 and Phase 4
- Goal is clean ESLint run showing only actual lint violations
</tasks>
</step>

<step name="apply-fixes">
<title>Applying Auto-fixes</title>
<command>pnpm exec eslint . --fix</command>
<caution>Inform user that --fix will modify files. Ensure version control active</caution>
<follow-up>Re-run eslint without --fix to see remaining warnings/errors</follow-up>
</step>

<step name="manual-review">
<title>Manual Review of Remaining Issues</title>
<actions>
- Categorize remaining issues
- Present summary of remaining ESLint issues
- Include file path, line number, rule ID, and message
- Report any TODO-LLM comments added
- Count critical errors vs warnings
</actions>
<guidance>Do not attempt to auto-fix complex issues requiring deep semantic understanding</guidance>
</step>

<step name="run-tests">
<title>Running Tests to Catch Regressions</title>
<command>pnpm test</command>
<importance>Critical safety net to ensure migration and auto-fixes haven't broken functionality</importance>
<action>Report any test failures clearly</action>
</step>

<step name="final-checks">
<title>Final Sanity Checks</title>
<suggestions>
- Manually inspect key files heavily modified by --fix
- Review diff of all changes before committing
</suggestions>
</step>
</execution-steps>
</phase-5-verification>

<troubleshooting>
<title>Troubleshooting and Common Issues</title>

<issue type="flatcompat-errors">
<symptom>TypeError: Missing parameter recommendedConfig or allConfig in FlatCompat constructor</symptom>
<cause>FlatCompat used to extend eslint:recommended or eslint:all without initialization</cause>
<fix>
<code language="typescript">
import { FlatCompat } from "@eslint/eslintrc";
import js from "@eslint/js";

const compat = new FlatCompat({
baseDirectory: \_\_dirname,
recommendedConfig: js.configs.recommended,
allConfig: js.configs.all
});
</code>
</fix>
</issue>

<issue type="plugin-not-found">
<symptom>Plugin not found errors when using compat.extends or compat.plugins</symptom>
<causes>
- baseDirectory not set correctly
- Plugin not correctly installed
- Plugin incompatible with FlatCompat
</causes>
<fixes>
- Ensure baseDirectory correctly set to directory of eslint.config.ts
- Verify plugin listed in package.json and installed
- Check plugin name and config name
</fixes>
</issue>

<issue type="typescript-config">
<symptom>Errors related to parserOptions.project not finding tsconfig.json</symptom>
<causes>
- tsconfigRootDir or project path not correctly resolving
- eslint.config.ts being type-checked by incompatible tsconfig.json
</causes>
<fixes>
- Set parserOptions.project to path relative to package
- Use helper function to determine tsconfigRootDir
- Add eslint.config.ts to exclude array of main tsconfig.json
</fixes>
</issue>

<issue type="plugin-incompatibility">
<symptom>Plugins throw errors even with FlatCompat</symptom>
<troubleshooting-steps>
- Check plugin GitHub for ESLint 9 issues
- Try simpler config to isolate plugin
- Look for alternative plugins
- Flag for manual review
</troubleshooting-steps>
</issue>

<issue type="performance">
<symptom>ESLint runs significantly slower after migration</symptom>
<causes>
- Type-aware rules newly enabled
- Inefficient globs or ignores
- Specific performance-intensive rules
</causes>
<fixes>
- Verify parserOptions.project correctly scoped
- Review glob patterns for efficiency
- Ensure node_modules and build directories globally ignored
- Use --debug flag to identify bottleneck rules
</fixes>
</issue>

<issue type="global-ignores">
<symptom>Files intended to be ignored still being linted</symptom>
<cause>ignores property needs to be part of configuration object</cause>
<fix>
<code language="typescript">
export default defineConfig([
  { ignores: ["coverage/", ".turbo/", "dist/"] },
  // ... other configurations
]);
</code>
</fix>
</issue>
</troubleshooting>

<appendix>
<title>Appendix</title>

<useful-links>
<title>Useful Links and Documentation</title>
<links>
<link type="eslint-official">
<name>Migrating to v9.x</name>
<url>https://eslint.org/docs/latest/use/migrate-to-9.0.0</url>
</link>
<link type="eslint-official">
<name>Configure ESLint (Flat Config)</name>
<url>https://eslint.org/docs/latest/use/configure/configuration-files-new</url>
</link>
<link type="eslint-official">
<name>FlatCompat Utility</name>
<url>https://github.com/eslint/eslintrc#readme</url>
</link>
<link type="typescript-eslint">
<name>TypeScript ESLint Getting Started</name>
<url>https://typescript-eslint.io/getting-started</url>
</link>
<link type="plugin">
<name>eslint-plugin-import</name>
<url>https://github.com/import-js/eslint-plugin-import#readme</url>
</link>
<link type="plugin">
<name>eslint-config-prettier</name>
<url>https://github.com/prettier/eslint-config-prettier#readme</url>
</link>
</links>
</useful-links>

<complex-example>
<title>Complex Consuming Package Example</title>
<code language="typescript">
import { defineConfig } from 'eslint/config';
import tseslint from 'typescript-eslint';
import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";
import path from "path";
import { fileURLToPath } from "url";

import reactPlugin from "eslint-plugin-react";
import reactHooksPlugin from "eslint-plugin-react-hooks";
import jsxA11yPlugin from "eslint-plugin-jsx-a11y";
// @ts-expect-error eslint-plugin-import has no official types yet
import \* as importPlugin from 'eslint-plugin-import';
import unusedImportsPlugin from 'eslint-plugin-unused-imports';
import prettierConfig from 'eslint-config-prettier';

import globals from "globals";

const **filename = fileURLToPath(import.meta.url);
const **dirname = path.dirname(**filename);
const compat = new FlatCompat({
baseDirectory: **dirname,
recommendedConfig: js.configs.recommended,
});

export default defineConfig([
{ ignores: ["**/dist/", "**/node_modules/", "**/.turbo/", "**/.wrangler/"] },

    js.configs.recommended,

    ...tseslint.configs.recommended,
    {
        files: ["**/*.{ts,tsx,mts}"],
        languageOptions: {
            parser: tseslint.parser,
            parserOptions: {
                project: true,
                tsconfigRootDir: __dirname,
            },
        },
    },

    {
        files: ["**/*.{ts,tsx}"],
        plugins: {
            react: reactPlugin,
            'react-hooks': reactHooksPlugin,
            'jsx-a11y': jsxA11yPlugin,
        },
        languageOptions: {
            globals: globals.browser,
        },
        settings: {
            react: { version: "detect" },
        },
        rules: {
            ...reactPlugin.configs.recommended.rules,
            ...reactHooksPlugin.configs.recommended.rules,
            ...jsxA11yPlugin.configs.recommended.rules,
            "react/react-in-jsx-scope": "off",
        },
    },

    {
        files: ["**/*.{ts,tsx,mts,js,jsx}"],
        plugins: { 'import': importPlugin, 'unused-imports': unusedImportsPlugin },
        settings: {
            'import/resolver': {
                typescript: { project: [`${__dirname}/tsconfig.json`] },
                node: true,
            },
        },
        rules: {
            'unused-imports/no-unused-imports': 'warn',
            'import/order': ['warn', { 'newlines-between': 'always' }],
        },
    },

    {
        files: ["**/*.test.{ts,tsx}", "**/*.spec.{ts,tsx}"],
        languageOptions: {
            globals: {
                ...globals.jest,
            },
        },
        rules: {
            "@typescript-eslint/no-explicit-any": "off",
        },
    },

    {
        files: ["eslint.config.ts", "scripts/**/*.js"],
        languageOptions: {
            globals: globals.node,
        },
    },

    prettierConfig,

]);
</code>
</complex-example>

<quick-mapping>
<title>Quick Mapping Reference</title>
<mappings>
<map>
<legacy>extends</legacy>
<flat>Spread imported configs or compat.extends()</flat>
<note>No direct extends key</note>
</map>
<map>
<legacy>plugins</legacy>
<flat>plugins: { prefix: pluginObj } or compat.plugins()</flat>
<note>Plugins are imported and keyed</note>
</map>
<map>
<legacy>rules</legacy>
<flat>rules: { ... }</flat>
<note>Largely the same within config object</note>
</map>
<map>
<legacy>parser</legacy>
<flat>languageOptions: { parser: parserObj }</flat>
</map>
<map>
<legacy>parserOptions</legacy>
<flat>languageOptions: { parserOptions: { ... } }</flat>
</map>
<map>
<legacy>env</legacy>
<flat>languageOptions: { globals: { ...globals.envName } } or compat.env()</flat>
<note>Use globals package</note>
</map>
<map>
<legacy>globals</legacy>
<flat>languageOptions: { globals: { ... } }</flat>
</map>
<map>
<legacy>overrides</legacy>
<flat>Separate objects in top-level config array using files key</flat>
<note>Each override becomes distinct config object</note>
</map>
<map>
<legacy>ignorePatterns</legacy>
<flat>ignores: [...]</flat>
</map>
</mappings>
</quick-mapping>
</appendix>

</eslint9-migration-guide>
