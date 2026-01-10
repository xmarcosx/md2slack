# Feature Brief Template

Use this template when creating feature briefs in `.specify/features/`.

---

### NNN - [Feature Title]

**Problem**: [1-2 sentences. What's wrong or missing? Be specific about the user pain point.]

**Desired State**: [1-2 sentences. What do we want instead? Focus on outcomes, not implementation.]

**Why This Matters**:
1. [Reason with specific impact]
2. [Reason with specific impact]

**CLI Interface** (optional):
- Command: `md2slack [command] [options]`
- Input: [Where does input come from? stdin, file, argument?]
- Output: [What does the user see? stdout, stderr, side effects?]

**Example** (optional):
- Current: [How it works now, or "Not supported"]
- Desired: [How it should work]

**Notes** (optional): [Constraints, technical considerations, or context that affects the solution]

---

## Guidelines

1. **Keep it short** — Briefs capture WHAT and WHY, never HOW
2. **One brief per feature** — If it's getting long, break it into multiple features
3. **Be specific about the problem** — Vague problems lead to vague solutions
4. **Focus on user outcomes** — What can the user do that they couldn't before?
5. **Include CLI details** — For a CLI tool, command interface matters
