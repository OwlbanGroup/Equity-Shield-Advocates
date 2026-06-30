# TODO - System Fixes Implementation

## Phase 1: Security Fixes (CRITICAL)

### Fix 2: Remove Hardcoded API Key

- [x] Update src/api_server.py to remove hardcoded fallback
- [x] API_KEY must now be set via environment variable
- [x] Status: COMPLETED

### Fix 3: Remove Exposed Banking Credentials

- [x] Redact account numbers in get_banking_info()
- [x] Use masked values or remove sensitive data
- [x] Status: COMPLETED

### Fix 1: API Endpoint Path Consistency

- [x] Standardize all endpoints to /api/v1/ prefix
- [x] Update root api_server.py OR remove it
- [x] Status: COMPLETED

## Phase 2: Additional Improvements

### Fix 4: Add Input Validation

- [x] Already implemented in parse_positive_int, parse_optional_float
- [x] Status: COMPLETED

### Fix 5: Fix Root API Server

- [x] Add /health endpoint to root api_server.py
- [x] Add rate limiting
- [x] Remove debug mode
- [x] Status: COMPLETED

## Testing

- [x] Run tests to verify fixes
- [x] Status: COMPLETED
