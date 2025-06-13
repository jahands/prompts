// @ts-check

/** @type {import("prettier").Config} */
const config = {
	trailingComma: 'es5',
	tabWidth: 2,
	useTabs: true,
	semi: false,
	singleQuote: true,
	printWidth: 100,
	overrides: [
		{
			files: ['*.jsonc', '*.code-workspace'],
			options: {
				trailingComma: 'none',
			},
		},
		{
			files: 'Justfile',
			options: {
				useTabs: false,
			},
		},
		{
			files: '*.md',
			options: {
				useTabs: false,
			},
		},
		{
			files: '*.mdc',
			options: {
				useTabs: false,
			},
		},
	],
}

module.exports = config
