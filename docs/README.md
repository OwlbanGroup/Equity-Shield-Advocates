# Equity Shield Advocates APP

## Project Overview
Equity Shield Advocates is an application designed to provide structured corporate data and real assets information across various sectors. It includes an API server to serve corporate and real assets data, and an AI component to query and analyze corporate structures.

## Features
- REST API endpoints to access corporate structure, companies by sector, company details by ticker, and real assets data.
- AI component for querying corporate data with simple natural language support.
- Basic unit tests for API and AI components.

## API Endpoints
- `GET /api/corporate-structure`  
  Returns the full corporate structure data grouped by sectors.

- `GET /api/companies/<sector>`  
  Returns the list of companies in the specified sector.  
  Example: `/api/companies/Technology`

- `GET /api/company/<ticker>`  
  Returns details of the company with the specified ticker symbol.  
  Example: `/api/company/MSFT`

- `GET /api/real-assets`  
  Returns the list of real assets under management.

## AI Component Usage
The AI component provides methods to:
- Get list of sectors.
- Get companies by sector.
- Get company details by ticker.
- Query using simple natural language strings like:
  - "companies in Technology"
  - "company with ticker MSFT"

## Testing
- Unit tests cover API endpoints and AI component methods.
- Tests include valid and invalid cases for robustness.

## Future Improvements
- Expand AI capabilities with advanced analytics and natural language processing.
- Add more API endpoints and dynamic data updates.
- Enhance testing coverage and add integration tests.
- Improve documentation and add deployment automation.

## Setup and Running
- Install dependencies from `requirements.txt`.
- Run the API server with `python api_server.py`.
- Run tests with `python -m unittest discover`.
