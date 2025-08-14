# CLAUDE.md – Coding Conventions & Agent Rules

## General
- Use conventional commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`
- PR must include tests, docs update, and pass CI

## JavaScript/TypeScript
- Style: Prettier + ESLint (airbnb/base)
- Naming: camelCase; Components PascalCase
- Avoid `any`; prefer explicit types
- Do not block event loop in request handlers

## React
- Co-locate component, styles, tests
- Prefer function components + hooks
- State mgmt: Redux Toolkit or Context + reducers
- Use React Testing Library for UI tests

## Node.js API
- Layered: routes → controllers → services → data
- Validate inputs at the edge (Joi/zod)
- Centralized error handler; never throw plain strings
- Use async/await with try/catch

## Java (Spring Boot & Microservices)
- Structure: controller → service → repository; or hexagonal (ports/adapters)
- Use constructor injection; avoid field injection
- Annotate transactions at service layer
- Handle N+1 via fetch joins or entity graphs
- Tests: JUnit5 + Testcontainers for integration

## Apollo GraphQL
- Schema-first (`typeDefs`), resolvers thin
- Use DataLoader to prevent N+1
- Validate args; sanitize inputs
- Separate queries vs mutations resolvers

## Security
- Enforce auth/roles at edge (middleware/interceptor/context)
- Sanitize inputs; escape output
- Secrets via env/secret manager; never commit secrets

## Performance
- Targets (default): API P95 < 300ms, DB queries P95 < 50ms
- Add caching where beneficial; measure first
- Log correlation IDs for tracing

## Testing
- Pyramid: unit > integration > e2e
- Coverage on changed lines ≥ 80%
- Include negative tests (error paths, validation)
- Snapshot tests sparingly; prefer assertions

## Agent Rules
- Start with story template keywords → locate files via path hints
- Limit refactors to scope; separate PR if needed
- Update CHANGELOG and docs
- Provide migration guide for any breaking change