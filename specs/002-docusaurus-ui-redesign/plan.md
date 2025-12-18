# Implementation Plan: Docusaurus Book Theme UI Redesign (Black & Green)

**Branch**: `002-docusaurus-ui-redesign` | **Date**: 2025-12-16 | **Spec**: [specs/002-docusaurus-ui-redesign/spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-docusaurus-ui-redesign/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Redesign the Docusaurus v2 book/classic theme with a dark-first black-and-green UI using CSS variables, applying consistent styling to navbar, sidebar, footer, and chapter pages (headings, code, tables, admonitions, pagination). Replace the default robotic logo with a minimal abstract or typography-based tech logo, ensuring WCAG AA contrast, dark/light toggle support, and responsive validation without plugins or content changes.

## Technical Context

**Language/Version**: CSS, SCSS, TypeScript/JavaScript (Node.js 18+)
**Primary Dependencies**: Docusaurus v2, React, CSS Modules, CSS-in-JS
**Storage**: N/A (styling only)
**Testing**: Visual validation, accessibility testing, browser compatibility testing
**Target Platform**: Web browsers, responsive design for desktop/mobile
**Project Type**: Web (frontend styling enhancement)
**Performance Goals**: <200ms page load time with new CSS assets, maintain existing performance
**Constraints**: Must follow Docusaurus theming best practices, CSS-only changes (no backend), WCAG AA compliance
**Scale/Scope**: Single textbook site with multiple chapters and pages, responsive across all devices

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the constitution, this plan:
- ✅ Maintains technical accuracy by following Docusaurus theming standards
- ✅ Preserves educational clarity by improving readability with proper contrast ratios
- ✅ Ensures reproducibility by using standard Docusaurus customization methods
- ✅ Adheres to specified tools (Docusaurus v2) without introducing new dependencies
- ✅ Maintains responsive design for all devices (as required by constitution)
- ✅ Complies with WCAG AA contrast requirements (as specified in feature requirements)

*Post-design evaluation:*
- ✅ All styling uses CSS variables following Docusaurus best practices
- ✅ No changes to backend or content structure as required
- ✅ Responsive design maintained across all components
- ✅ Accessibility standards met with proper contrast ratios
- ✅ Full compatibility with existing Docusaurus functionality preserved

## Project Structure

### Documentation (this feature)

```text
specs/002-docusaurus-ui-redesign/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
my-textbook/
├── src/
│   ├── components/      # Custom Docusaurus components (navbar, footer, etc.)
│   ├── pages/           # Custom pages if needed
│   └── theme/           # Custom theme components
├── static/
│   └── img/             # New logo assets
├── styles/              # Custom CSS files for theme
├── docusaurus.config.js # Docusaurus configuration
├── sidebars.js          # Sidebar navigation
└── package.json         # Dependencies
```

**Structure Decision**: Web application styling enhancement. The changes will be focused on CSS customization and component overrides within the existing Docusaurus structure, with new logo assets stored in the static directory and custom styles organized in a dedicated styles directory.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
