# Contributing to MCP Gateway

We love your input! We want to make contributing to MCP Gateway as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

### Prerequisites

- Node.js 18+
- Python 3.13+
- Docker & Docker Compose
- Git

### Quick Setup

```bash
git clone https://github.com/your-username/mcp-gateway.git
cd mcp-gateway
./setup.sh
```

### Manual Setup

1. **Install dependencies:**
   ```bash
   npm run install:all
   ```

2. **Set up environment:**
   ```bash
   cp packages/frontend/env.example packages/frontend/.env
   cp packages/backend/env.example packages/backend/.env
   # Edit .env files with your configuration
   ```

3. **Start development:**
   ```bash
   npm run dev
   ```

## Code Style

### Frontend (React/TypeScript)

- Use **TypeScript** for all new code
- Follow **ESLint** and **Prettier** configurations
- Use **functional components** with hooks
- Implement **proper error boundaries**
- Write **accessible** components

```bash
# Lint frontend code
cd packages/frontend
npm run lint

# Format code
npm run format
```

### Backend (Python/FastAPI)

- Follow **PEP 8** style guide
- Use **Black** for code formatting
- Use **isort** for import sorting
- Add **type hints** for all functions
- Write **docstrings** for all public functions

```bash
# Format backend code
cd packages/backend
black .
isort .

# Type checking
mypy .
```

## Testing

### Frontend Tests

```bash
cd packages/frontend
npm test
npm run test:coverage
```

### Backend Tests

```bash
cd packages/backend
pytest
pytest --cov=. --cov-report=html
```

### Integration Tests

```bash
# Start all services
docker-compose -f docker-compose.full.yml up -d

# Run integration tests
npm run test:integration
```

## Commit Messages

We follow the [Conventional Commits](https://conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools

### Examples

```
feat(chat): add support for file attachments

fix(auth): resolve token refresh issue on page reload

docs(readme): update installation instructions

style(frontend): format components with prettier

refactor(backend): extract OpenAPI parsing logic

perf(api): optimize database queries for service listing

test(integration): add end-to-end chat flow tests

chore(deps): update React to v18.2.0
```

## Issue Reporting

### Bug Reports

When filing a bug report, please include:

1. **Clear title** describing the issue
2. **Steps to reproduce** the problem
3. **Expected behavior**
4. **Actual behavior**
5. **Environment details** (OS, browser, versions)
6. **Screenshots** if applicable
7. **Error logs** from browser console or server logs

### Feature Requests

When requesting a feature, please include:

1. **Clear description** of the feature
2. **Use case** and why it's needed
3. **Proposed solution** if you have one
4. **Alternative solutions** you've considered
5. **Additional context** or screenshots

## Architecture Guidelines

### Frontend Architecture

```
src/
├── components/     # Reusable UI components
├── pages/         # Route components
├── hooks/         # Custom React hooks
├── services/      # API clients and external services
├── types/         # TypeScript type definitions
├── utils/         # Utility functions
└── __tests__/     # Test files
```

### Backend Architecture

```
packages/backend/
├── gateway_server.py      # Main FastAPI app
├── mcp_client_manager.py  # MCP client logic
├── openapi_mcp_generator.py # OpenAPI conversion
├── models/               # Data models
├── services/            # Business logic
├── utils/              # Utility functions
└── tests/             # Test files
```

### Design Principles

1. **Separation of Concerns**: Keep business logic separate from presentation
2. **Single Responsibility**: Each module should have one reason to change
3. **Dependency Inversion**: Depend on abstractions, not concretions
4. **DRY**: Don't repeat yourself
5. **KISS**: Keep it simple, stupid
6. **YAGNI**: You ain't gonna need it

## API Design Guidelines

### RESTful Endpoints

- Use **nouns** for resource names
- Use **HTTP methods** appropriately
- Return **consistent** error responses
- Include **proper** HTTP status codes
- Use **pagination** for large datasets

### Request/Response Format

```json
{
  "data": {
    // Response data
  },
  "meta": {
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 100
    }
  },
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Invalid input data",
      "field": "email"
    }
  ]
}
```

## Security Guidelines

### Authentication

- Always validate **JWT tokens**
- Implement **proper CORS** policies
- Use **HTTPS** in production
- Store **secrets** securely

### Input Validation

- **Validate** all user inputs
- **Sanitize** data before database operations
- Use **Pydantic models** for API validation
- Implement **rate limiting**

### Error Handling

- **Never expose** internal errors to users
- **Log** security-related events
- Use **generic** error messages for security issues
- Implement **proper** exception handling

## Documentation

### Code Documentation

- Write **clear** and **concise** comments
- Document **complex** business logic
- Include **examples** in docstrings
- Keep documentation **up-to-date**

### API Documentation

- Use **OpenAPI/Swagger** specifications
- Include **request/response** examples
- Document **error codes** and meanings
- Provide **authentication** details

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release notes
- [ ] Tag the release
- [ ] Deploy to staging
- [ ] Verify staging deployment
- [ ] Deploy to production
- [ ] Announce the release

## Community

### Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Getting Help

- **Documentation**: Check the README and inline docs
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Chat**: Join our Discord server (if available)

## Recognition

Contributors who make significant contributions will be recognized in:

- The README.md file
- Release notes
- Project documentation
- Special contributor badges

## Questions?

Don't hesitate to ask questions! We're here to help:

- Open an issue with the "question" label
- Start a discussion on GitHub
- Reach out to maintainers directly

Thank you for contributing to MCP Gateway! 🚀
