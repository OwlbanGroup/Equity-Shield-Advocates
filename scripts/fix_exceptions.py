#!/usr/bin/env python3
"""Script to fix broad exception caught issues in api_server.py."""

FILE_PATH = (
    'c:/Users/bizle/OneDrive/bsean4890@gmail.com/.github/'
    'Equity-Shield-Advocates/Equity-Shield-Advocates/src/api_server.py'
)

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: health_check - except Exception -> except (ValueError, TypeError)
old = (
    'except Exception as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Health check failed")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
new = (
    'except (ValueError, TypeError) as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Health check failed")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
content = content.replace(old, new)

# Fix 2: get_corporate_data - except Exception -> except (OSError, json.JSONDecodeError)
old = (
    'except Exception as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Error in get_corporate_data")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
new = (
    'except (OSError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Error in get_corporate_data")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
content = content.replace(old, new)

# Fix 3: get_corporate_structure
old = (
    'except Exception as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Error in get_corporate_structure")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
new = (
    'except (OSError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Error in get_corporate_structure")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
content = content.replace(old, new)

# Fix 4: get_companies_by_sector
old = (
    'except Exception as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Error in get_companies_by_sector")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
new = (
    'except (OSError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Error in get_companies_by_sector")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
content = content.replace(old, new)

# Fix 5: get_company_by_ticker
old = (
    'except Exception as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Error in get_company_by_ticker")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
new = (
    'except (OSError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Error in get_company_by_ticker")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
content = content.replace(old, new)

# Fix 6: get_real_assets
old = (
    'except Exception as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Error in get_real_assets")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
new = (
    'except (OSError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive fallback\n'
    '        logger.exception("Error in get_real_assets")\n'
    '        return json_error(HTTP_500, ERROR_INTERNAL_SERVER, str(exc))'
)
content = content.replace(old, new)

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixes applied successfully!')
