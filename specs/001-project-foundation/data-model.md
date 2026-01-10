# Data Model: Project Foundation

**Feature**: 001-project-foundation
**Date**: 2026-01-09

## Overview

This feature is pure infrastructure (package setup and CLI skeleton). There are no persistent data entities, database tables, or state management. This document captures the conceptual entities for documentation purposes.

## Entities

### Package

**Description**: The md2slack Python distribution

**Attributes**:
| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | "md2slack" - package identifier |
| version | string | Semantic version (e.g., "0.1.0") |
| description | string | Brief package description |
| entry_point | string | CLI command name ("md2slack") |

**Relationships**: Contains CLI module

---

### CLI Command Group

**Description**: The root Click group that serves as the entry point

**Attributes**:
| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | "md2slack" |
| help_text | string | Tool description shown in --help |
| invoke_without_command | boolean | True (shows help when no subcommand) |

**Relationships**: Parent of convert and post subcommands

---

### Subcommand (convert)

**Description**: Placeholder command for future markdown conversion

**Attributes**:
| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | "convert" |
| help_text | string | Description of future functionality |
| implemented | boolean | False (placeholder) |

---

### Subcommand (post)

**Description**: Placeholder command for future Slack posting

**Attributes**:
| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | "post" |
| help_text | string | Description of future functionality |
| implemented | boolean | False (placeholder) |

## State Transitions

N/A - No stateful behavior in this feature.

## Validation Rules

N/A - No data validation in this feature.
