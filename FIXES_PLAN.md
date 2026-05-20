# System Weaknesses Fixes Plan

## Fixes to Implement

### 1. API Endpoint Path Mismatch (CRITICAL)

- **Problem**: Dashboard calls `/api/v1/*` but API serves `/api/*`
- **Fix**: Update `src/api_server.py` to use `/api/v1/` prefix

### 2. Remove Hardcoded Credentials

- **Problem**: API key hardcoded in source
- **Fix**: Use environment variable `API_KEY` from `os.getenv()`

### 3. Remove Exposed Banking Credentials

- **Problem**: Bank account numbers returned in API response
- **Fix**: Replace with masked/redacted info or remove entirely

### 4. Add Input Validation

- **Problem**: No sanitization on numeric inputs
- **Fix**: Add try/except with proper validation

### 5. Fix Root API Server

- **Problem**: No /health endpoint, no rate limiting, debug mode
- **Fix**: Add health endpoint, security improvements

### 6. Update Dashboard API URLs

- **Problem**: Dashboard uses wrong paths (already fixed by server change)

## Progress

- [ ] Fix 1: Add /v1/ prefix to API endpoints
- [ ] Fix 2: Remove hardcoded API key
- [ ] Fix 3: Remove banking credentials exposure
- [ ] Fix 4: Add input validation
- [ ] Fix 5: Fix root api_server.py
