# Research: Project Foundation

**Feature**: 001-project-foundation
**Date**: 2026-01-09

## Overview

This document captures research decisions for bootstrapping the md2slack Python package. Since this is a well-defined infrastructure feature with no ambiguous requirements, research focuses on best practices for the chosen technologies.

## Decisions

### 1. Python Package Layout

**Decision**: Use src-layout with `src/md2slack/` directory

**Rationale**:
- Prevents accidental imports of the local package during development
- Ensures tests run against the installed package, not source directory
- Matches modern Python packaging best practices (PEP 517/518)
- Specified in requirements (FR-001)

**Alternatives Considered**:
- Flat layout (package at root): Rejected - can cause import confusion during development

### 2. CLI Framework

**Decision**: Click

**Rationale**:
- Specified in feature requirements (FR-007)
- Well-established, production-ready library
- Excellent support for subcommands (groups)
- Automatic help generation
- Clean decorator-based syntax

**Alternatives Considered**:
- argparse (stdlib): More verbose, less intuitive for subcommands
- Typer: Built on Click, adds type hints but unnecessary for this scope

### 3. Package Configuration

**Decision**: pyproject.toml with setuptools backend

**Rationale**:
- Modern Python standard (PEP 517/518/621)
- Compatible with uv package manager
- Single file for all package metadata
- Entry points defined declaratively

**Alternatives Considered**:
- setup.py: Legacy approach, being phased out
- Poetry: Different tooling ecosystem than uv

### 4. Development Dependencies

**Decision**: ruff for linting, pytest for testing

**Rationale**:
- Both specified in requirements (FR-008)
- ruff: Fast, modern linter replacing flake8/isort/black check modes
- pytest: De facto standard for Python testing

**Alternatives Considered**:
- flake8 + isort + black: More tools to manage, ruff consolidates
- unittest: Stdlib but more verbose test syntax

### 5. Python Version

**Decision**: Python 3.10+

**Rationale**:
- Documented in assumptions (spec.md)
- Provides match statements, improved type hints
- Widely available, reasonable minimum for new projects

**Alternatives Considered**:
- Python 3.12+: Too restrictive, limits user adoption
- Python 3.8+: End of life in 2024, no reason to support

## No Clarifications Needed

All requirements were clearly specified. No NEEDS CLARIFICATION items were identified during planning.
