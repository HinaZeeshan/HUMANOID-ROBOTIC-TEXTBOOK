# Actionable Tasks: Humanoid Robotics Textbook & RAG Chatbot

This document lists the actionable, dependency-ordered tasks required to implement the feature as described in `spec.md` and `plan.md`.

## Implementation Strategy

The implementation will follow a phased approach, prioritizing foundational setup and then delivering user stories as independently testable increments. The MVP (Minimum Viable Product) is the completion of User Story 1 and User Story 2, which delivers the core educational content and the interactive RAG chatbot.

## Phase 1: Project Setup

These tasks initialize the project structure.

- [x] T001 Initialize a Docusaurus project in the `./docs` directory.
- [x] T002 Create a directory for the backend service at `./backend`.
- [x] T003 Initialize a Python project with FastAPI in `./backend` and add a placeholder `main.py`.
- [x] T004 Create a directory for automation scripts at `./scripts`.
- [x] T005 Create a directory for test assets at `./tests`.
- [x] T006 Update the `.gitignore` file to exclude common Python and Node.js artifacts.

## Phase 2: Foundational Implementation

These tasks establish the core components required by multiple user stories.

- [] T007 Configure the basic Docusaurus site settings in `docs/docusaurus.config.js` (e.g., site title, theme).
- [ ] T008 [P] Implement the mock API endpoint `POST /api/v1/chat` in `backend/main.py` that returns a hardcoded response.
- [x] T009 [P] Create the basic structure for the GitHub Actions deployment workflow in `.github/workflows/deploy.yml`.

## Phase 3: User Story 1 - Learn Humanoid Robotics Core Concepts

**Goal**: Students can understand the fundamental concepts and pipeline of building a humanoid robot system.
**Independent Test**: Review the textbook content for clarity, correctness, and completeness across all core modules.

- [x] T010 [US1] Create placeholder Markdown files for 8 chapters in `docs/docs/`.
- [x] T011 [P] [US1] Write the content for Chapter 1 (ROS 2) in `docs/docs/01-ros2-basics.md`.
- [x] T012 [P] [US1] Write the content for Chapter 2 (URDF) in `docs/docs/02-urdf-models.md`.
- [x] T013 [P] [US1] Write the content for Chapter 3 (Digital Twin) in `docs/docs/03-digital-twins.md`.
- [x] T014 [P] [US1] Write the content for Chapter 4 (NVIDIA Isaac) in `docs/docs/04-nvidia-isaac.md`.
- [x] T015 [P] [US1] Write the content for Chapter 5 (Vision-Language-Action) in `docs/docs/05-vla-models.md`.
- [x] T016 [P] [US1] Write the content for the remaining chapters in `docs/docs/`.

## Phase 4: User Story 3 - Access Practical Steps for Building Systems

**Goal**: Students can use practical guidance and code to build system components.
**Independent Test**: Follow the practical steps and run the provided code examples for each module to verify they work as described.

- [x] T017 [P] [US3] Add runnable code examples for ROS 2 to `docs/docs/01-ros2-basics.md`.
- [x] T018 [P] [US3] Add runnable code examples for URDF to `docs/docs/02-urdf-models.md`.
- [x] T019 [P] [US3] Add runnable code examples for Isaac Sim to `docs/docs/04-nvidia-isaac.md`.

## Phase 5: User Story 2 - Interact with RAG Chatbot

**Goal**: Students can ask questions and receive relevant, accurate answers from an embedded RAG chatbot.
**Independent Test**: Query the RAG chatbot for chapter-specific information and verify the accuracy and relevance of its responses.

- [ ] T020 [US2] Implement the RAG ingestion script in `scripts/ingest_content.py` to read markdown files and upload them to the Vertex AI RAG Corpus.
- [ ] T021 [US2] Run the ingestion script to populate the RAG corpus with the chapter content.
- [ ] T022 [US2] Implement the full backend logic for `POST /api/v1/chat` in `backend/main.py` to query the Vertex AI RAG service.
- [x] T023 [US2] Create the frontend `ChatKit` component in React at `docs/src/theme/Chatbot.tsx`.
- [ ] T024 [US2] Implement the API call from the `Chatbot.js` component to the backend `/api/v1/chat` endpoint.
- [x] T025 [US2] Add the `Chatbot.tsx` component to the main Docusaurus layout at `docs/src/theme/Layout.js`.

## Phase 6: User Story 4 - Access Docusaurus-Deployed Textbook

**Goal**: Students can access the textbook online via a reliably deployed Docusaurus site.
**Independent Test**: Access the deployed site and verify all content and the chatbot render and function correctly.

- [x] T026 [US4] Finalize the GitHub Actions workflow in `.github/workflows/deploy.yml` to build and deploy the Docusaurus site to GitHub Pages.
- [ ] T027 [US4] Trigger the deployment workflow and verify the site is live and functional at the target GitHub Pages URL.

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T028 Create the "golden dataset" of Q&A pairs for accuracy testing in `tests/golden_dataset.jsonl`.
- [ ] T029 Create an automated test script in `tests/evaluate_accuracy.py` to measure chatbot performance against the golden dataset and report the accuracy score.
- [ ] T030 Review all content for style, consistency, and correctness.
- [ ] T031 Implement the "Retry/Suggest alternatives" error handling UI in the `Chatbot.js` component.

## Dependencies & Parallel Execution

- **User Story Dependency Graph**:
  - `(Setup) -> (Foundational)`
  - `(Foundational) -> [US1, US2, US3, US4]`
  - `[US2] -> [US1, US3]` (The chatbot is most useful once there is content to ingest)
  - `[US4] -> [US1, US2, US3]` (Deployment is the final step)
- Minor change to trigger deployment workflow.
- **Parallel Opportunities**:
  - **Content Creation**: Tasks for writing different chapters ([US1], [US3]) can be done in parallel (`T011` through `T019`).
  - **UI/Backend Split**: The frontend `ChatKit` component (`T023`) can be developed in parallel with the backend API (`T022`), using the mock from `T008` as the interface.