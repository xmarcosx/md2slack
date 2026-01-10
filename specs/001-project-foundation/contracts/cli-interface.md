# CLI Interface Contract: Project Foundation

**Feature**: 001-project-foundation
**Date**: 2026-01-09

## Overview

This document defines the command-line interface contract for the md2slack CLI skeleton. These are the expected behaviors that tests should verify.

## Commands

### md2slack (root)

**Invocation**: `md2slack` or `md2slack --help`

**Behavior**:
- When invoked without arguments: Display help and exit with code 0
- When invoked with `--help`: Display help and exit with code 0
- When invoked with unknown subcommand: Display error and exit with non-zero code

**Help Output Must Include**:
- Tool name and brief description
- List of available subcommands (convert, post)
- Usage pattern

**Exit Codes**:
| Code | Meaning |
|------|---------|
| 0 | Success (help displayed) |
| 2 | Usage error (unknown command/option) |

---

### md2slack convert

**Invocation**: `md2slack convert` or `md2slack convert --help`

**Behavior**:
- When invoked without arguments: Print "not implemented yet" message and exit with code 0
- When invoked with `--help`: Display help for convert subcommand

**Output**:
```
Convert command is not implemented yet.
```

**Exit Codes**:
| Code | Meaning |
|------|---------|
| 0 | Success (placeholder message or help) |

---

### md2slack post

**Invocation**: `md2slack post` or `md2slack post --help`

**Behavior**:
- When invoked without arguments: Print "not implemented yet" message and exit with code 0
- When invoked with `--help`: Display help for post subcommand

**Output**:
```
Post command is not implemented yet.
```

**Exit Codes**:
| Code | Meaning |
|------|---------|
| 0 | Success (placeholder message or help) |

## Test Cases

### Smoke Tests

1. **CLI Help**: `md2slack --help` exits 0 and outputs "convert" and "post"
2. **Convert Placeholder**: `md2slack convert` exits 0 and outputs "not implemented"
3. **Post Placeholder**: `md2slack post` exits 0 and outputs "not implemented"
4. **Unknown Command**: `md2slack unknown` exits non-zero

### Installation Tests

1. **Package Installs**: `uv pip install -e .` completes without error
2. **Entry Point Works**: `md2slack` command is available after installation
