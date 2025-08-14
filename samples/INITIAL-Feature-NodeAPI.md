# INITIAL.md – Feature: Add Payment Status Endpoint

## Business Context
Add an API endpoint to retrieve payment status for an order. Improves order tracking and reduces support queries.

## Acceptance Criteria
- Endpoint: GET `/payments/:orderId/status`
- Returns JSON `{ orderId, status, lastUpdated }`
- Requires authentication; respond 401 if missing
- SLA: P95 < 200ms

## Primary Modules
- `/routes/payments.js`
- `/controllers/paymentController.js`
- `/services/paymentService.js`
- `/middleware/auth.js`

## File Search Keywords
`payment status`, `orderId`, `paymentService.getStatus`, `/payments/:orderId`

## Implementation Notes
- Reuse validation from `routes/orders.js`
- Add unit tests for controller and service
- Add integration test hitting the route with mock auth

## Done When
- Tests pass (unit+integration)
- Endpoint documented in OpenAPI/README
- CI quality gates pass