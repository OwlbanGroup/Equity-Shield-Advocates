# TODO - System Fixes Implementation

## Phase 1: Security Fixes (CRITICAL)

### Fix 2: Remove Hardcoded API Key
- [ ] Update src/api_server.py to remove hardcoded fallback
- [ ] Update tests/test_api_server.py to use env var or accept for testing
- [ ] Status: PENDING

### Fix 3: Remove Exposed Banking Credentials
- [ ] Redact account numbers in get_banking_info()
- [ ] Use masked values or remove sensitive data
- [ ] Status: PENDING

### Fix 1: API Endpoint Path Consistency
- [ ] Standardize all endpoints to /api/v1/ prefix
- [ ] Update root api_server.py OR remove it
- [ ] Status: PENDING

## Phase 2: Additional Improvements

### Fix 4: Add Input Validation
- [ ] Already implemented in parse_positive_int, parse_optional_float

### Fix 5: Fix Root API Server
- [ ] Add /health endpoint to root api_server.py
- [ ] Add rate limiting
- [ ] Remove debug mode
- [ ] Status: PENDING

## Testing
- [ ] Run tests to verify fixes
- [ ] Status: PENDING
