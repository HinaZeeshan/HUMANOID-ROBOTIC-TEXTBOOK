# Testing Strategy

This document outlines the testing strategy for the Humanoid Robotics Textbook project.

## Testing Philosophy

The project follows a comprehensive testing approach to ensure:
- Reliability of the RAG system
- Accuracy of content retrieval
- Performance under load
- Correct handling of cross-module queries
- Proper integration between components

## Test Categories

### Unit Tests
Located in `backend/tests/unit/`

Test individual functions and classes in isolation:
- RAG service methods
- Content service methods
- Utility functions
- Data models

**Example unit test structure:**
```python
def test_rag_service_index_content():
    # Test indexing content in the RAG system
    pass

def test_content_service_create_module():
    # Test creating a module in the content service
    pass
```

### Integration Tests
Located in `backend/tests/integration/`

Test interactions between multiple components:
- API endpoints with database
- RAG service with vector database
- Content service with data models
- Cross-module query functionality

**Example integration test:**
```python
def test_rag_query_endpoint():
    # Test the full RAG query flow from API to response
    pass
```

### Contract Tests
Located in `backend/tests/contract/`

Test API contracts and ensure backward compatibility:
- API request/response schemas
- Error handling
- Status codes
- Endpoint availability

### Frontend Tests
Located in `my-textbook/src/__tests__/`

Test React components and frontend functionality:
- Chatbot component rendering
- API integration
- User interactions
- State management

## Testing Frameworks

### Backend
- **pytest**: Primary testing framework
- **pytest-asyncio**: For async tests
- **pytest-mock**: For mocking dependencies
- **requests-mock**: For API endpoint testing
- **factory-boy**: For test data generation

### Frontend
- **Jest**: JavaScript testing framework
- **React Testing Library**: Component testing
- **Cypress**: End-to-end testing (planned)

## Test Data

### Fixtures
Test fixtures are located in `backend/tests/fixtures/`:
- Sample textbook content
- Mock API responses
- Test users and sessions
- Sample queries and expected responses

### Test Content
Realistic textbook content is used for testing:
- Sample ROS 2 code examples
- Simulation configurations
- AI model definitions
- Cross-module workflow examples

## Running Tests

### Backend Tests
```bash
# Run all tests
cd backend
python -m pytest

# Run unit tests only
python -m pytest tests/unit/

# Run integration tests only
python -m pytest tests/integration/

# Run with coverage
python -m pytest --cov=src/

# Run specific test file
python -m pytest tests/unit/test_rag_service.py
```

### Frontend Tests
```bash
# Run all frontend tests
cd my-textbook
npm test

# Run tests in watch mode
npm test -- --watch

# Run end-to-end tests (when implemented)
npm run test:e2e
```

## Test Coverage Goals

### Backend
- **Minimum 80%** code coverage
- **100%** coverage for critical RAG functionality
- **90%** coverage for API endpoints
- **95%** coverage for data models

### Frontend
- **Minimum 70%** component coverage
- **100%** coverage for critical user interactions
- **90%** coverage for API integration components

## CI/CD Integration

Tests are integrated into the CI/CD pipeline:
- Unit tests run on every commit
- Integration tests run on pull requests
- Contract tests run before deployment
- Performance tests run periodically

## Performance Testing

### Load Testing
- Simulate multiple concurrent users
- Test RAG query performance under load
- Measure response times for different query types

### Stress Testing
- Test system behavior under high load
- Verify memory usage patterns
- Check for resource leaks

### Endurance Testing
- Long-running tests to identify memory leaks
- Consistency checks over extended periods
- Database connection stability

## Test Scenarios

### RAG System Tests
1. **Basic Query**: Simple content retrieval
2. **Cross-module Query**: Multi-module content retrieval
3. **Context Filtering**: Module-specific queries
4. **Performance**: Query response times
5. **Edge Cases**: Empty queries, very long queries

### Content Management Tests
1. **Module Creation**: Creating new textbook modules
2. **Content Indexing**: Proper indexing of new content
3. **Content Updates**: Updating existing content
4. **Search Accuracy**: Relevance of search results

### Frontend Integration Tests
1. **Chatbot Functionality**: Full conversation flow
2. **API Integration**: Proper API communication
3. **Error Handling**: Graceful error responses
4. **Cross-module Detection**: Proper query classification

## Mocking Strategy

### External Services
- Mock Cohere API calls during testing
- Mock Qdrant vector database operations
- Mock external authentication services

### Database Operations
- Use in-memory database for tests
- Mock database connections
- Use test database for integration tests

## Test Data Management

### Seeding
- Automated test data seeding
- Consistent test data across environments
- Clean-up after each test run

### Test Isolation
- Each test runs in isolation
- Database state reset between tests
- Clean environment for each test run

## Quality Gates

### Before Merge
- All unit tests must pass
- Integration tests must pass
- Coverage must meet minimum thresholds
- No security vulnerabilities

### Before Release
- All tests must pass
- Performance benchmarks must be met
- Security scans must pass
- Manual QA sign-off

## Test Maintenance

### Regular Reviews
- Monthly test suite review
- Update tests with feature changes
- Remove obsolete tests
- Optimize slow tests

### Documentation
- Keep test documentation up to date
- Document test scenarios
- Maintain test data descriptions
- Update testing procedures

This testing strategy ensures the reliability and quality of the Humanoid Robotics Textbook project while maintaining high standards for educational content accuracy and system performance.