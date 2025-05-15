# Equity Shield Advocates

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

## Setup and Running
- Install dependencies from `requirements.txt` using `pip install -r requirements.txt`.
- Run the API server with `python src/api_server.py`.
- Run tests with `python -m unittest discover`.

## Deployment
- The project uses Gunicorn as the WSGI server, configured in the `Procfile` with the command: `web: gunicorn wsgi:app`.
- CI/CD pipeline is configured in `.github/workflows/ci-cd.yml` to run tests and lint on push to main branch.
- Deployment automation commands need to be added to the CI/CD pipeline for full automation.

### Deployment Instructions

#### Prerequisites

- Docker installed on your system
- Alternatively, Python 3.11+ and pip installed for local deployment

#### Docker Deployment

1. Build the Docker image:

```bash
docker build -t equity-shield-advocates .
```

2. Run the Docker container:

```bash
docker run -d -p 8000:8000 --name equity-shield-advocates equity-shield-advocates
```

3. The API will be accessible at `http://localhost:8000`.

#### Local Deployment without Docker

1. Install dependencies:

```bash
pip install -r config/requirements.txt
```

2. Run the app using gunicorn:

```bash
gunicorn wsgi:app --bind 0.0.0.0:8000 --workers 4
```

3. The API will be accessible at `http://localhost:8000`.

#### Notes

- The app uses Waitress in `wsgi.py` for production serving if run directly.
- The `Procfile` is configured for deployment on platforms like Heroku using gunicorn.
- Ensure the `data/` directory is included in your deployment environment as it contains required JSON data files.
pip install -r config/requirements.txt
docker run -d -p 8000:8000 --name equity-shield-advocates equity-shield-advocates

## Testing
- Unit tests cover API endpoints and AI component methods.
- Tests include valid and invalid cases for robustness.
- Run tests using `python -m unittest discover`.

## Future Improvements
- Add deployment automation commands to the CI/CD pipeline.
- Perform full end-to-end testing including UI and integration.
- Enhance documentation and add deployment instructions.
- Expand AI capabilities with advanced analytics and natural language processing.

## Contact
For questions or collaboration, contact the Owlban Group at [contact@owlbangroup.com](mailto:contact@owlbangroup.com).
