# Tasks

## 1. Ignore Local Environments and Secrets

- [x] 1.1 Update `.gitignore` to exclude `.venv-cashsave/`, `venv/`, nested `.env` variants, and generated-file duplicates; verify matching paths with `git check-ignore`.
- [x] 1.2 Preserve `.env.example` as trackable and confirm ignored paths are excluded from `git status` without changing already tracked files.

## 2. Verify Documentation

- [x] 2.1 Validate `corrigir-gitignore-ambiente` with OpenSpec and run `git diff --check`.
