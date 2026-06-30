# TODO: Fix Broad Exception Caught Issues - COMPLETED

## Task

Fix Pylint W0718 "Catching too general exception Exception" warnings in src/api_server.py

## Issues Fixed

- Line 254: get_corporate_structure() - except Exception → (OSError, json.JSONDecodeError)
- Line 301: get_companies_by_sector() - except Exception → (OSError, json.JSONDecodeError)
- Line 345: get_company_by_ticker() - except Exception → (OSError, json.JSONDecodeError)
- Line 442: get_real_assets() - except Exception → (OSError, json.JSONDecodeError)
- health_check() - except Exception → (ValueError, TypeError)
- get_corporate_data() - except Exception → (OSError, json.JSONDecodeError)

## Verification

- Pylint score: 10.00/10
- No remaining "except Exception" found
- Python syntax: OK
