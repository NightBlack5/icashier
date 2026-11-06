# Proposal

## Why

The documented Python environment `.venv-cashsave` is not covered by the
repository's `.gitignore`, and environment-specific files such as `.env.local`
could be accidentally tracked. Tightening these rules protects generated files
and local credentials from entering source control.

## What Changes

- Ignore the documented `.venv-cashsave` environment and other common local
  virtual-environment directories.
- Ignore root and nested `.env` variants while explicitly allowing the safe
  `.env.example` template.
- Remove duplicate ignore entries while preserving existing generated-file
  exclusions.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `version-control`: Specify complete exclusions for local Python environments
  and environment-specific secret files.

## Impact

- `.gitignore` rules for repository-local generated and secret files.
- The `version-control` OpenSpec capability and checks for tracked versus
  ignored paths.

