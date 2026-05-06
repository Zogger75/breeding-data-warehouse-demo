# Local Demo Setup

## Purpose

This project is designed to support two database modes:

1. PostgreSQL for a production-style warehouse demonstration
2. SQLite for a no-admin local demo environment

SQLite is useful for reviewers, recruiters, and developers who want to run the demo without installing database server software.

## Recommended Local Setup

Create and activate a Python virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate