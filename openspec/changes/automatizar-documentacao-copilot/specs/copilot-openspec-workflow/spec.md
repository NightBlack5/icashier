# copilot-openspec-workflow Specification

## Purpose

Ensure GitHub Copilot keeps OpenSpec documentation aligned with code changes it makes in this repository.

## ADDED Requirements

### Requirement: Document Copilot implementation work in OpenSpec

Repository-level Copilot instructions SHALL direct Copilot to consult the OpenSpec configuration, relevant specifications, and active changes before implementing a request that changes application code, configuration, dependencies, tests, or data structures. Copilot SHALL update a clearly related active change or create a new change with the artifacts required by the configured schema.

#### Scenario: Implementing a request with an existing related change

- **WHEN** Copilot starts implementing a request covered by an active OpenSpec change
- **THEN** it updates and follows that change instead of creating duplicate documentation

#### Scenario: Implementing a request without a related active change

- **WHEN** Copilot starts implementing a request not covered by an active change
- **THEN** it creates the required OpenSpec artifacts before changing project code

### Requirement: Keep task status and validation truthful

Copilot instructions SHALL require implementation tasks to reflect completed work and verification accurately, and require validation of the affected OpenSpec change.

#### Scenario: Completing an implementation

- **WHEN** Copilot finishes implementing a documented change
- **THEN** it runs OpenSpec validation and relevant checks, and marks tasks complete only when their work and verification have actually succeeded

### Requirement: State the automation boundary

The repository instructions SHALL make clear that they guide Copilot sessions and do not automatically observe edits made manually or by external tools.

#### Scenario: Editing outside Copilot

- **WHEN** a change is made manually or by an external tool
- **THEN** the repository does not claim that OpenSpec was automatically updated for that change
