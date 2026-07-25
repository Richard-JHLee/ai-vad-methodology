# File Map

> The File Map describes the purpose, ownership, and modification rules for the files and directories in a software project.

---

# Purpose

AI can generate better software when it understands the structure of a project.

A File Map provides architectural context by documenting the responsibility of each file and directory before implementation begins.

Unlike a System Map, which explains component interactions, a File Map focuses on the organization and responsibilities of the project's files.

---

# Goals

The File Map helps developers and AI systems:

- understand project organization,
- identify where new code should be placed,
- avoid modifying unrelated files,
- preserve architectural consistency,
- improve traceability.

---

# Relationship to Other Artifacts

| Artifact | Purpose |
|----------|---------|
| Requirement Contract | Defines what needs to be built |
| System Map | Explains how components interact |
| **File Map** | Explains where implementation belongs |
| Approved Change Scope | Defines which files may change |
| Change Map | Records why files changed |

---

# Directory Structure

Example:

```text
app/
├── api/
├── services/
├── repositories/
├── models/
├── schemas/
├── middleware/
├── config/
└── tests/
```

---

# File Responsibilities

| Directory | Responsibility |
|------------|----------------|
| api | HTTP endpoints |
| services | Business logic |
| repositories | Data access |
| models | Domain models |
| schemas | Request and response models |
| middleware | Request processing |
| config | Configuration |
| tests | Automated tests |

---

# File Ownership

Each file should have a single primary responsibility.

Example:

| File | Responsibility |
|------|----------------|
| UserController | HTTP request handling |
| UserService | Business logic |
| UserRepository | Database access |
| UserModel | Domain representation |

Files should avoid mixing multiple responsibilities.

---

# Placement Rules

The File Map defines where new functionality should be implemented.

Example:

| New Feature | Location |
|-------------|----------|
| New API | api/ |
| Business Rules | services/ |
| SQL Queries | repositories/ |
| DTO | schemas/ |
| Unit Tests | tests/ |

---

# Modification Rules

Some files are expected to change frequently.

Others should remain stable.

Example:

| File | Modification Policy |
|------|---------------------|
| api/* | Allowed |
| services/* | Allowed |
| repositories/* | Allowed |
| config/* | Approval Required |
| authentication/* | Restricted |
| database/migrations/* | Restricted |

---

# AI Guidance

Before generating code, AI should determine:

1. Which files should be modified?
2. Which files must not be modified?
3. Does a suitable file already exist?
4. Is a new file required?
5. Does the proposed change violate project organization?

If these questions cannot be answered confidently, implementation should pause for human review.

---

# Example

Requirement

```
Add User Profile API
```

Expected implementation:

```text
api/profile.py

↓

ProfileService.py

↓

ProfileRepository.py

↓

tests/test_profile.py
```

No authentication or payment files should be modified.

---

# Best Practices

- Keep one responsibility per file.
- Avoid placing business logic inside controllers.
- Prefer extending existing modules before creating new ones.
- Group related files consistently.
- Keep naming conventions consistent.

---

# Benefits

A well-maintained File Map:

- improves AI-generated code quality,
- reduces unnecessary file modifications,
- simplifies code reviews,
- improves onboarding,
- preserves architectural consistency.

---

# Related Pages

- [[System Map]]
- [[Approved Change Scope]]
- [[Change Map]]
- [[Architecture Decision Record]]
