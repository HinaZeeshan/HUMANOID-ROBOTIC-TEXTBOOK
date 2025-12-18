---
description: "Task list for Docusaurus Book Theme UI Redesign (Black & Green)"
---

# Tasks: Docusaurus Book Theme UI Redesign (Black & Green)

**Input**: Design documents from `/specs/002-docusaurus-ui-redesign/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `src/`, `static/`, `styles/` at repository root
- Paths based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 [P] Set up Docusaurus development environment
- [ ] T003 [P] Verify Docusaurus v2 installation and configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 [P] Create custom styles directory at `my-textbook/styles/`
- [ ] T005 [P] Create static assets directory at `my-textbook/static/img/` for new logo
- [ ] T006 Set up CSS variables for black-and-green theme in `my-textbook/src/css/custom.css`
- [ ] T007 Configure Docusaurus to use custom CSS in `my-textbook/docusaurus.config.js`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Dark-First Theme Application (Priority: P1) 🎯 MVP

**Goal**: Apply consistent black-and-green theme across all pages with WCAG AA contrast compliance

**Independent Test**: Can be fully tested by visiting any page on the site and verifying that the black-and-green color scheme is consistently applied with WCAG AA contrast compliance, delivering a professional and accessible reading experience.

### Implementation for User Story 1

- [ ] T008 [P] [US1] Define dark theme CSS variables for background (#0b0f14) in `my-textbook/src/css/custom.css`
- [ ] T009 [P] [US1] Define dark theme CSS variables for text (#e6f4ea) in `my-textbook/src/css/custom.css`
- [ ] T010 [P] [US1] Define dark theme CSS variables for primary color (#00c853) in `my-textbook/src/css/custom.css`
- [ ] T011 [US1] Apply dark theme variables to navbar in `my-textbook/src/css/custom.css`
- [ ] T012 [US1] Apply dark theme variables to sidebar in `my-textbook/src/css/custom.css`
- [ ] T013 [US1] Apply dark theme variables to footer in `my-textbook/src/css/custom.css`
- [ ] T014 [US1] Ensure WCAG AA contrast compliance across all elements in `my-textbook/src/css/custom.css`
- [ ] T015 [US1] Test responsive layouts with new theme across different screen sizes

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Updated Logo and Branding (Priority: P1)

**Goal**: Replace robotic logo with modern, tech-focused logo that aligns with the black-and-green theme

**Independent Test**: Can be fully tested by viewing the navbar header and metadata and verifying that the new logo is present, accessible, and appropriately sized, delivering a cohesive brand identity.

### Implementation for User Story 2

- [ ] T016 [P] [US2] Design and create minimal tech-focused logo in SVG format at `my-textbook/static/img/logo.svg`
- [ ] T017 [P] [US2] Create alternative logo formats (PNG) at `my-textbook/static/img/logo.png`
- [ ] T018 [US2] Update navbar configuration to use new logo in `my-textbook/docusaurus.config.js`
- [ ] T019 [US2] Update site metadata to use new logo in `my-textbook/docusaurus.config.js`
- [ ] T020 [US2] Ensure logo scales appropriately across different devices
- [ ] T021 [US2] Test logo accessibility and proper alt text

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Styled Chapter Content (Priority: P2)

**Goal**: Style chapter content (headings, code blocks, callouts) to match the black-and-green theme for improved readability

**Independent Test**: Can be fully tested by viewing any documentation page and verifying that headings, links, code blocks, and admonitions follow the established color scheme, delivering improved readability.

### Implementation for User Story 3

- [ ] T022 [P] [US3] Style H1-H4 headings to match theme in `my-textbook/src/css/custom.css`
- [ ] T023 [P] [US3] Style links and interactive elements with theme colors in `my-textbook/src/css/custom.css`
- [ ] T024 [US3] Style code blocks with black-and-green theme in `my-textbook/src/css/custom.css`
- [ ] T025 [US3] Style inline code elements with theme colors in `my-textbook/src/css/custom.css`
- [ ] T026 [US3] Style admonitions (callouts) to match theme in `my-textbook/src/css/custom.css`
- [ ] T027 [US3] Style pagination controls with theme colors in `my-textbook/src/css/custom.css`
- [ ] T028 [US3] Style tables to match the black-and-green theme in `my-textbook/src/css/custom.css`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T029 [P] Update documentation with new styling guidelines in `my-textbook/docs/`
- [ ] T030 [P] Test dark/light toggle functionality across all pages
- [ ] T031 [P] Optimize CSS assets for performance under 200ms load time
- [ ] T032 [P] Run accessibility validation across all pages
- [ ] T033 [P] Run responsive design validation across different devices
- [ ] T034 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all CSS variable definitions together:
Task: "Define dark theme CSS variables for background (#0b0f14) in my-textbook/src/css/custom.css"
Task: "Define dark theme CSS variables for text (#e6f4ea) in my-textbook/src/css/custom.css"
Task: "Define dark theme CSS variables for primary color (#00c853) in my-textbook/src/css/custom.css"

# Launch all component styling together:
Task: "Apply dark theme variables to navbar in my-textbook/src/css/custom.css"
Task: "Apply dark theme variables to sidebar in my-textbook/src/css/custom.css"
Task: "Apply dark theme variables to footer in my-textbook/src/css/custom.css"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. **STOP and VALIDATE**: Test User Stories 1 and 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 & 2 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 3 → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---



- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence