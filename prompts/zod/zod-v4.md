<zod-v4-guidelines>

<title>Zod v4 Coding Guidelines</title>

<overview>
Use these rules when working with Zod for TypeScript schema validation. Copy this to your Cursor rules, Claude project instructions, or other AI coding assistant configuration.
</overview>

<critical>
CRITICAL: Always import from 'zod/v4', never 'zod'
</critical>

<core-rules>

<rule>
Every schema MUST have inferred type above it

<example type="good">
```typescript
export type User = z.infer<typeof User>
export const User = z.object({...})
```
</example>

- Same name for type & schema
- No "Schema" suffix
- Use JSDoc (`/** */`), not `//`
</rule>

<rule>
Type extraction from schemas

<example type="good">
```typescript
// Extract output (parsed) & input (raw) types
type UserOutput = z.output<typeof User>
type UserInput = z.input<typeof User>

// Never use: typeof User['_type'] // or _input, _output
```
</example>
</rule>

<rule>
String validations are standalone functions

<example type="avoid">
```typescript
z.string().email()
```
</example>

<example type="preferred">
```typescript
z.email(), z.url(), z.uuid(), z.ip()
```
</example>
</rule>

<rule>
Use `error` param sparingly - Zod's defaults are excellent

<example type="avoid">
```typescript
z.email({error: "Invalid email"}) // Redundant!
```
</example>

<example type="preferred">
```typescript
z.email() // Zod says "Invalid email"
// Only for business logic:
z.string().check((val) => /[A-Z]/.test(val), {
  error: "Must contain uppercase",
})
```
</example>
</rule>

<rule>
Number changes

- Use `z.number()` for general numbers
- `z.int()` for integers only (not `z.number().int()`)
- `z.int32()`, `z.float64()` for specific types
- Numbers finite by default
</rule>

<rule>
Object types

- `z.object()` - strips unknowns (default)
- `z.strictObject()` - rejects extras
- `z.looseObject()` - allows extras
</rule>

<rule>
Custom validation: Use `.check()` not `.superRefine()`
</rule>

<rule>
Error formatting: `z.prettifyError()` or `z.treeifyError()`
</rule>

<rule>
Functions:

<example type="good">
```typescript
z.function({
  input: [z.string()],
  output: z.number(),
})
```
</example>
</rule>

<rule>
Records: `z.record(keyType, valueType)`
</rule>

<rule>
ISO formats: `z.iso.datetime()`, `z.iso.date()`
</rule>

<rule>
Other key features:
- Default: `.default()` applies to output; use `.prefault()` for v3 behavior
- File validation: `z.file().min(1024).max(5*1024*1024).mime(['image/jpeg'])`
- Pipe: `z.pipe(z.string(), z.number())` for transformations
- Async: Use `.check(async (val) => {...})` for async validation
- Arrays: `z.array(z.email())` or `z.email().array()`
- Optional: `.optional()`, `.nullable()`, `.nullish()`
</rule>
</core-rules>

<quick-reference>

| v3                      | v4                          |
| ----------------------- | --------------------------- |
| `z.string().email()`    | `z.email()`                 |
| `{message: "err"}`      | `{error: "err"}`            |
| `.strict()`             | `z.strictObject()`          |
| `.format()`             | `z.treeifyError()`          |
| `z.string().datetime()` | `z.iso.datetime()`          |
| `.args().returns()`     | `{input:[...], output:...}` |

</quick-reference>

<example type="complete">

```typescript
import { z } from 'zod/v4'

/** User registration */
export type UserReg = z.infer<typeof UserReg>
export const UserReg = z.object({
  email: z.email(),
  password: z
    .string()
    .min(8)
    .check((pwd) => /[A-Z]/.test(pwd) && /\d/.test(pwd), {
      error: 'Need uppercase & number',
    }),
  age: z.number().min(18),
})
```

</example>

</zod-v4-guidelines>