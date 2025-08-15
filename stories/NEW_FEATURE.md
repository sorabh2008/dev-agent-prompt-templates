# NEW_FEATURE.md – Feature: Add Pet “Favorite Status” Endpoint

## Business Context
Provide a convenient way for clients to check whether a pet is marked as a favorite. This enhances user experience by enabling the UI to display favorite status quickly and reduces unnecessary backend calls.

## Acceptance Criteria
- Endpoint: GET `/pets/:petId/favorite-status`
- Returns JSON `{ petId, isFavorite (boolean), lastUpdated }`
- Requires authentication; respond 401 if missing or invalid auth token
- SLA: P95 < 200ms

## Technical Context
- GitHub Repository: https://github.com/ln-nicolas/petstore-client-ts

## Primary Modules
- `src/apis/petApi.ts` (or equivalent API client file)
- `src/models/Pet.ts` or related model definitions
- `src/services/favoriteService.ts` (new or existing)
- `src/middleware/auth.ts`, if authentication logic lives here

## File Search Keywords
`favorite`
`isFavorite`
`favorite-status`
`petId`
`getFavoriteStatus`

## Implementation Notes
- Reuse existing request configuration and response handling from other pet endpoints (e.g., `getPetById`)
- Add or extend the model (e.g., `PetFavoriteStatus`) and types
- Add unit tests for the new endpoint logic in `petApi` and service layer
- Add integration test where the client simulates an authorized request and validates the response
- Document the new endpoint in the README or OpenAPI schema used by the project

## Done When
- Tests pass (unit+integration)
- Endpoint documented in OpenAPI/README
- CI quality gates pass
