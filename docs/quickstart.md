# Quickstart Guide

Get up and running with the Humanoid Robotics Textbook project in minutes.

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- A Cohere API key
- Git for version control

## Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd humanoid-robotic-textbook
```

### 2. Set up the backend
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file to add your Cohere API key and other configuration
```

### 3. Set up the frontend
```bash
# Navigate to the textbook directory
cd ../my-textbook

# Install Node.js dependencies
npm install
```

## Running the Application

### 1. Start the backend server
```bash
# From the backend directory
cd backend
python -m src.api.main
```
The backend will start on `http://localhost:8000`

### 2. Start the frontend
```bash
# From the textbook directory
cd my-textbook
npm start
```
The frontend will start on `http://localhost:3000`

### 3. Build the RAG index
```bash
# In a new terminal, from the project root
cd scripts
python build-rag-index.py
```

## Using the Application

### Textbook Content
Browse the complete textbook at `http://localhost:3000`, organized into 5 modules:
1. ROS 2 Basics
2. Digital Twin Simulation
3. AI-Robot Brain
4. Vision-Language-Action Systems
5. Capstone Project

### Chatbot
- Use the floating chatbot button on any textbook page to ask questions
- The chatbot will provide context-aware responses based on the current module
- For cross-module queries, ask about workflows that span multiple concepts

### Advanced Chat Interface
Visit `http://localhost:3000/chat` for the advanced interface with:
- Module filtering options
- Source visibility
- Quick suggestion buttons
- Detailed attribution

## Key Features

### Cross-Module Queries
Ask questions that span multiple modules, such as:
- "How does voice command flow to robot navigation?"
- "How do I integrate ROS 2 with Gazebo simulation?"
- "Explain the complete perception-action loop"

### Context-Aware Responses
The chatbot adapts to the current textbook module:
- On ROS 2 pages: Get ROS-specific answers
- On simulation pages: Get Gazebo/Unity-specific answers
- On AI pages: Get Isaac/Nav2-specific answers

### Source Attribution
All responses include sources from the textbook content, showing you exactly where the information comes from.

## Troubleshooting

### Backend not starting
- Ensure all environment variables are set in `.env`
- Verify your Cohere API key is valid
- Check that required services (PostgreSQL, Qdrant) are running

### Frontend not connecting to backend
- Verify the backend is running on port 8000
- Check that the frontend is configured to connect to the correct backend URL
- Look for CORS errors in browser console

### Chatbot not responding
- Confirm the RAG index has been built
- Verify content files exist and are properly formatted
- Check backend logs for errors

## Next Steps

- Explore all 5 textbook modules
- Try asking cross-module questions in the chatbot
- Visit the advanced chat interface for more features
- Contribute to the project by adding more content or features