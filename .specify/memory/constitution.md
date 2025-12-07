# Physical AI & Humanoid Robotics – Unified Book with Embedded RAG Chatbot Constitution

## Core Principles

### I. Technical Accuracy
All robotics, AI, and implementation details must be technically accurate and verifiable.

### II. Educational Clarity
Content must be clear and accessible for intermediate-to-advanced AI/robotics learners.

### III. Full Reproducibility
All code, simulations, and deployment steps must be fully reproducible.

### IV. Strict Adherence to Specified Tools and Architecture
All development must strictly follow the defined tools and architectural patterns.

## Key Standards

- All technical explanations backed by official documentation (ROS 2, NVIDIA Isaac, Gazebo, etc.)
- Every code snippet must be complete, runnable, and tested
- Docusaurus site must build and deploy cleanly to GitHub Pages
- RAG chatbot uses only: OpenAI Agents/ChatKit, FastAPI, Neon Postgres, Qdrant Cloud (free tier)
- Chatbot must support whole-book queries and selected-text-only queries
- Zero broken links, working live demos where applicable

## Constraints

- Cover all 4 modules exactly as specified (ROS 2 → Gazebo/Unity → NVIDIA Isaac → VLA + Capstone)
- Use only Spec-Kit Plus + Claude Code for content generation
- Fully responsive Docusaurus design
- RAG index built from final book markdown only (no external sources)
- Deployment: GitHub Pages (book) + free-tier hosting (FastAPI backend)

## Success Criteria

- Book successfully deployed and accessible on GitHub Pages
- RAG chatbot embedded and fully functional in the live book
- Chatbot accurately answers questions using full context and selected text only
- All code examples run without modification in standard environments
- 100% module coverage with working capstone integration example

## Governance
Constitution supersedes all other practices; Amendments require documentation, approval, migration plan

All PRs/reviews must verify compliance; Complexity must be justified; Use CLAUDE.md for runtime development guidance

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
