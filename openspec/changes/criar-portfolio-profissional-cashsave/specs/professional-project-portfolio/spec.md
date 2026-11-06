# professional-project-portfolio Specification

## Purpose

Entregar uma apresentação visual pesquisável e honesta do CashSave, adequada
para portfólio pessoal e avaliação de recrutadores de tecnologia.

## ADDED Requirements

### Requirement: Present the project with verified evidence

The portfolio SHALL describe the product purpose, implemented capabilities,
technology stack, architecture, user experience, technical challenges,
verified status, limitations, and next steps using only evidence found in the
repository or captured from the local runtime.

#### Scenario: Recruiter scans the presentation

- **WHEN** a recruiter opens the PDF
- **THEN** the product, its purpose, the author's technical contribution, and
  the current verification boundaries are understandable without reading the
  source code

### Requirement: Include real application imagery

The portfolio SHALL include high-resolution screenshots captured from the
application and SHALL label public runtime captures separately from protected
flows that require external authentication or Xano access.

#### Scenario: Screenshot is shown

- **WHEN** a gallery image appears in the presentation
- **THEN** it has a professional caption and a short explanation of what the
  screen demonstrates

### Requirement: Explain the real technical design

The portfolio SHALL include a readable architecture diagram and categorized
technology descriptions based on the actual Python, Reflex, Xano, ReportLab,
and optional Ollama implementation.

#### Scenario: Architecture is reviewed

- **WHEN** a recruiter reviews the architecture section
- **THEN** the browser, Reflex state/UI, Xano API boundary, and optional local
  Ollama path are visually distinguishable

### Requirement: Provide editable developer identification

The portfolio SHALL reserve clearly labeled editable fields for the developer's
name, target role, GitHub, LinkedIn, professional email, and personal
portfolio, without inventing contact information.

#### Scenario: Developer details are unavailable

- **WHEN** the repository does not contain verified contact details
- **THEN** the presentation displays placeholders that are visibly intended for
  later replacement

### Requirement: Produce a robust PDF artifact

The delivered PDF SHALL be A4, readable in common PDF viewers, have selectable
text, embedded local images, page numbering, and no clipped or overflowing
content.

#### Scenario: PDF is reviewed before delivery

- **WHEN** the generated PDF is rendered page by page
- **THEN** every page has consistent margins, legible typography, intact
  images, and no broken asset references
