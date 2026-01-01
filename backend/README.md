---
title: Humanoid Robotics Book Agent
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Humanoid Robotics Textbook Backend Agent

This is the backend API for the Humanoid Robotics Textbook RAG agent.

## Configuration

This Space requires the following Secret Environment Variables to be set in the Settings tab:

- `COHERE_API_KEY`: Your Cohere API key.
- `NEON_DATABASE_URL`: Connection string for your Neon Postgres database.
- `QDRANT_URL`: URL for your Qdrant vector database.
- `QDRANT_API_KEY`: API key for Qdrant.

## API Documentation

Once running, the API documentation is available at `/docs` (Swagger UI) or `/redoc`.
