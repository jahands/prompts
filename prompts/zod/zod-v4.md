# Zod v4 Coding Guidelines

Use these rules when working with Zod for TypeScript schema validation. Copy this to your Cursor rules, Claude project instructions, or other AI coding assistant configuration.

**CRITICAL: Always import from 'zod/v4', never 'zod'**

## Core Rules

1. **Every schema MUST have inferred type above it**

   ```typescript
   export type User = z.infer<typeof User>
   export const User = z.object({...})
   ```

   - Same name for type & schema
   - No "Schema" suffix
   - Use JSDoc (`/** */`), not `//`

2. **Type extraction from schemas**

   ```typescript
   // Extract output (parsed) & input (raw) types
   type UserOutput = z.output<typeof User>
   type UserInput = z.input<typeof User>

   // Never use: typeof User['_type'] // or _input, _output
   ```

3. **String validations are standalone functions**

   ```typescript
   // ❌ z.string().email()
   // ✅ z.email(), z.url(), z.uuid(), z.ip()
   ```

4. **Use `error` param sparingly** - Zod's defaults are excellent

   ```typescript
   // ❌ z.email({error: "Invalid email"}) // Redundant!
   // ✅ z.email() // Zod says "Invalid email"
   // ✅ Only for business logic:
   z.string().check((val) => /[A-Z]/.test(val), {
     error: "Must contain uppercase",
   })
   ```

5. **Number changes**

   - Use `z.number()` for general numbers
   - `z.int()` for integers only (not `z.number().int()`)
   - `z.int32()`, `z.float64()` for specific types
   - Numbers finite by default

6. **Object types**

   - `z.object()` - strips unknowns (default)
   - `z.strictObject()` - rejects extras
   - `z.looseObject()` - allows extras

7. **Custom validation**: Use `.check()` not `.superRefine()`

8. **Error formatting**: `z.prettifyError()` or `z.treeifyError()`

9. **Functions**:

   ```typescript
   z.function({
     input: [z.string()],
     output: z.number(),
   })
   ```

10. **Records**: `z.record(keyType, valueType)`

11. **ISO formats**: `z.iso.datetime()`, `z.iso.date()`

12. **Other key features**:
    - **Default**: `.default()` applies to output; use `.prefault()` for v3 behavior
    - **File validation**: `z.file().min(1024).max(5*1024*1024).mime(['image/jpeg'])`
    - **Pipe**: `z.pipe(z.string(), z.number())` for transformations
    - **Async**: Use `.check(async (val) => {...})` for async validation
    - **Arrays**: `z.array(z.email())` or `z.email().array()`
    - **Optional**: `.optional()`, `.nullable()`, `.nullish()`

## Quick Reference

| v3                      | v4                          |
| ----------------------- | --------------------------- |
| `z.string().email()`    | `z.email()`                 |
| `{message: "err"}`      | `{error: "err"}`            |
| `.strict()`             | `z.strictObject()`          |
| `.format()`             | `z.treeifyError()`          |
| `z.string().datetime()` | `z.iso.datetime()`          |
| `.args().returns()`     | `{input:[...], output:...}` |

## Example

```typescript
import { z } from "zod/v4"

/** User registration */
export type UserReg = z.infer<typeof UserReg>
export const UserReg = z.object({
  email: z.email(),
  password: z
    .string()
    .min(8)
    .check((pwd) => /[A-Z]/.test(pwd) && /\d/.test(pwd), {
      error: "Need uppercase & number",
    }),
  age: z.number().min(18),
})
```
