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
z.string().datetime()
z.string().ip()

// ✅ CORRECT (Zod v4 style) - ALWAYS USE
z.email()
z.url()
z.uuid()
z.datetime()
z.ip()
z.ipv4()
z.ipv6()

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

### 6. Common Patterns in Zod v4

```typescript
// Email validation with custom error
z.email({ error: "Please enter a valid email address" })

// URL validation with constraints
z.url().startsWith("https://", { error: "URL must use HTTPS" })

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

// Object with mixed validation
z.strictObject({
  email: z.email(),
  age: z.int().min(0).max(120),
  website: z.url().optional(),
  role: z.enum(["admin", "user", "guest"]),
})
```

### 7. Error Handling

```typescript
const schema = z.email()

try {
  const result = schema.parse("invalid-email")
} catch (error) {
  if (error instanceof z.ZodError) {
    // Access issues
    console.log(error.issues)
    // Get first error message
    console.log(error.issues[0]?.message)
  }
}

// Safe parsing
const result = schema.safeParse("test@example.com")
if (result.success) {
  console.log(result.data)
} else {
  console.log(result.error.issues)
}
```

## Summary of Critical Rules

1. **ALWAYS** import from `'zod/v4'`, never from `'zod'`
2. Use standalone functions for string formats (e.g., `z.email()` not `z.string().email()`)
3. Use `error` parameter for custom messages, not `message` or `errorMap`
4. Use `z.int()` for integers, not `z.number().int()`
5. Use `z.strictObject()` or `z.looseObject()` for objects
6. Use `.check()` for custom validation, not `.superRefine()`
7. Numbers are finite by default - no need for `.finite()`

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

Remember: When in doubt, refer to the official Zod v4 documentation and always import from `'zod/v4'`.
