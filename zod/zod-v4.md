# Zod v4 System Prompt for LLMs

## Important: Always Use Zod v4

When working with Zod, **ALWAYS** use Zod v4 by importing from `'zod/v4'`. Never use the default `'zod'` import, which is Zod v3.

```typescript
// ✅ CORRECT - Always use this
import { z } from "zod/v4"

// ❌ WRONG - Never use these
import { z } from "zod" // This is v3
import { z } from "zod/v3" // Explicitly v3
```

## Key Differences in Zod v4

### 1. String Validation Methods Have Changed

In Zod v4, string format validations are **standalone functions**, not chained methods:

```typescript
// ❌ WRONG (Zod v3 style) - DO NOT USE
z.string().email()
z.string().url()
z.string().uuid()
z.string().ip()

// ✅ CORRECT (Zod v4 style) - ALWAYS USE
z.email()
z.url()
z.uuid()
z.ip()
z.ipv4()
z.ipv6()
z.base64()
z.nanoid()
z.cuid()
z.cuid2()
z.ulid()
z.cidrv4()
z.cidrv6()

// For strings with additional constraints, compose them:
z.email().min(5).max(255)
z.url().startsWith("https://")
```

### 2. Error Customization Has Changed

Use the `error` parameter instead of `message`, `errorMap`, `invalid_type_error`, or `required_error`:

```typescript
// ❌ WRONG (Zod v3 style)
z.string({ message: "Invalid string" })
z.string({ invalid_type_error: "Expected string", required_error: "Required" })

// ✅ CORRECT (Zod v4 style)
z.string({ error: "Invalid string" })
z.email({ error: "Invalid email address" })

// For complex error handling:
z.string().check((val) => val.length > 0, {
  error: "String cannot be empty",
})
```

### 3. Number Validation Changes

```typescript
// Numbers no longer accept infinite values by default
z.number() // Only accepts finite numbers

// Integer validation
z.int() // Only accepts safe integers
z.int32() // 32-bit integers
z.uint32() // Unsigned 32-bit integers
z.int64() // For bigint
z.uint64() // For unsigned bigint

// Float validation
z.float32() // 32-bit floats
z.float64() // 64-bit floats (standard JS numbers)

// ❌ DEPRECATED - Do not use
z.number().safe() // Use z.int() instead
z.number().finite() // No longer needed, numbers are finite by default
```

### 4. Object Schema Best Practices

```typescript
// For strict objects (no extra properties allowed)
z.strictObject({
  name: z.string(),
  age: z.int(),
})

// For loose objects (extra properties allowed)
z.looseObject({
  name: z.string(),
  age: z.int(),
})

// ❌ DEPRECATED - Do not use
z.object({}).strict()
z.object({}).passthrough()
```

### 5. Custom Validation

Use `.check()` instead of `.superRefine()`:

```typescript
// ✅ CORRECT (Zod v4)
z.string().check(
  (val) => {
    return val.length > 5
  },
  { error: "String must be longer than 5 characters" }
)

// For async validation
z.string().check(
  async (val) => {
    const isValid = await checkDatabase(val)
    return isValid
  },
  { error: "Invalid value" }
)
```

### 6. Error Handling

Zod v4 provides improved error handling and formatting:

```typescript
// Basic error handling with try/catch
const schema = z.email()

try {
  const result = schema.parse("invalid-email")
} catch (error) {
  if (error instanceof z.ZodError) {
    console.log(error.issues) // Access issues
    console.log(error.issues[0]?.message) // Get first error message
  }
}

// Safe parsing (recommended)
const result = schema.safeParse("test@example.com")
if (result.success) {
  console.log(result.data)
} else {
  // ✅ NEW error formatting methods
  const pretty = z.prettifyError(result.error) // Human-readable format
  const tree = z.treeifyError(result.error) // Clean tree structure
  console.log(result.error.issues) // Access raw issues
}

// ❌ WRONG (Zod v3 style) - DO NOT USE
error.format() // Deprecated
error.flatten() // Deprecated
```

### 7. Function Schemas

Function validation has a completely new API in Zod v4:

```typescript
// ✅ CORRECT (Zod v4)
const myFunction = z.function({
  input: [z.object({ name: z.string() })], // Array of parameter schemas
  output: z.string(),
})

const impl = myFunction.implement((input) => {
  return `Hello ${input.name}`
})

// For async functions:
const asyncImpl = myFunction.implementAsync(async (input) => {
  return `Hello ${input.name}`
})

// ❌ WRONG (Zod v3 style) - DO NOT USE
z.function()
  .args(z.object({ name: z.string() }))
  .returns(z.string())
```

### 8. Record Schemas

Record schemas must now specify both key and value types:

```typescript
// ✅ CORRECT (Zod v4)
z.record(z.string(), z.number()) // Must specify both key and value

// ❌ WRONG (Zod v3 style) - DO NOT USE
z.record(z.number()) // Single argument no longer supported
```

### 9. Default Values vs Prefault

In Zod v4, `.default()` behavior has changed - it applies to the output type:

```typescript
// ✅ CORRECT (Zod v4) - .default() applies to output
const schema = z
  .string()
  .transform((val) => val.length)
  .default(0)
schema.parse(undefined) // => 0 (number)

// For old v3 behavior, use .prefault() instead
const legacySchema = z
  .string()
  .transform((val) => val.length)
  .prefault("test")
legacySchema.parse(undefined) // => 4 (length of "test")
```

### 10. ISO Date/Time Functions

Zod v4 provides dedicated ISO format functions:

```typescript
// ✅ CORRECT (Zod v4)
z.iso.datetime() // Replaces z.string().datetime()
z.iso.date() // Replaces z.string().date()
z.iso.time() // New in v4
z.iso.duration() // New in v4

// ❌ WRONG (Zod v3 style) - DO NOT USE
z.string().datetime()
z.string().date()
```

### 11. File Validation

Zod v4 introduces file validation for File objects:

```typescript
// ✅ NEW in Zod v4
z.file()
  .min(1024) // Minimum file size in bytes
  .max(5 * 1024 * 1024) // Maximum file size (5MB)
  .mime(["image/jpeg", "image/png"]) // MIME type validation
```

### 12. Pipe Operations

Chain schemas with pipe operations for complex transformations:

```typescript
// ✅ NEW in Zod v4
const userSchema = z
  .object({ id: z.string() })
  .pipe(z.object({ id: z.number() }))

// Or use z.pipe() function:
const schema = z.pipe(
  z.string(),
  z.number() // Parses string then converts to number
)
```

### 13. Common Patterns in Zod v4

```typescript
// Optional fields
z.email().optional()
z.url().nullable()
z.int().nullish() // nullable and optional

// Default values
z.string().default("default value")
z.int().default(0)

// Arrays
z.array(z.email())
z.email().array() // Same as above

// Unions
z.union([z.string(), z.int()])

// Enums
z.enum(["option1", "option2", "option3"])
```

### 14. New Features in Zod v4

```typescript
// JSON Schema Generation
const jsonSchema = z.toJSONSchema(mySchema)

// Type Helpers
z.$output<typeof schema> // Extract output type
z.$input<typeof schema> // Extract input type
z.$brand<"MyBrand">() // Create branded types

// Registry System
z.globalRegistry // Global schema registry
z.registry() // Create local registry

const myRegistry = z.registry()
const schema = z.string().register(myRegistry, { name: "username" })
```



## Summary of Critical Rules

1. **ALWAYS** import from `'zod/v4'`, never from `'zod'`
2. Use standalone functions for string formats (e.g., `z.email()` not `z.string().email()`)
3. Use `error` parameter for custom messages, not `message` or `errorMap`
4. Use `z.int()` for integers, not `z.number().int()`
5. Use `z.strictObject()` or `z.looseObject()` for objects
6. Use `.check()` for custom validation, not `.superRefine()`
7. Numbers are finite by default - no need for `.finite()`
8. Use `z.prettifyError()` or `z.treeifyError()` for error formatting, not `.format()` or `.flatten()`
9. Function schemas use new `{ input: [...], output: ... }` syntax
10. Record schemas must specify both key and value types
11. `.default()` applies to output type; use `.prefault()` for old v3 behavior
12. Use ISO date/time functions like `z.iso.datetime()` instead of `z.string().datetime()`

## Example: Form Validation Schema

```typescript
import { z } from "zod/v4"

const userRegistrationSchema = z.strictObject({
  email: z.email({ error: "Please enter a valid email address" }),
  password: z
    .string()
    .min(8, { error: "Password must be at least 8 characters" })
    .check((pwd) => /[A-Z]/.test(pwd), {
      error: "Password must contain at least one uppercase letter",
    }),
  age: z
    .int()
    .min(18, { error: "Must be at least 18 years old" })
    .max(120, { error: "Invalid age" }),
  website: z.url().optional(),
  acceptTerms: z.literal(true, {
    error: "You must accept the terms and conditions",
  }),
})

type UserRegistration = z.infer<typeof userRegistrationSchema>
```

## Quick Migration Reference

| Operation        | Zod v3                    | Zod v4                         |
| ---------------- | ------------------------- | ------------------------------ |
| Import           | `import { z } from "zod"` | `import { z } from "zod/v4"`   |
| Email validation | `z.string().email()`      | `z.email()`                    |
| URL validation   | `z.string().url()`        | `z.url()`                      |
| Error message    | `{ message: "Error" }`    | `{ error: "Error" }`           |
| Strict object    | `.strict()`               | `z.strictObject()`             |
| Error formatting | `.format()`               | `z.treeifyError()`             |
| Native enum      | `z.nativeEnum()`          | `z.enum()`                     |
| IP validation    | `z.string().ip()`         | `z.ipv4()` or `z.ipv6()`       |
| Date/time        | `z.string().datetime()`   | `z.iso.datetime()`             |
| Function schema  | `.args().returns()`       | `{input: [...], output: ...}`  |
| Record schema    | `z.record(valueType)`     | `z.record(keyType, valueType)` |

Remember: When in doubt, refer to the official Zod v4 documentation and always import from `'zod/v4'`.
