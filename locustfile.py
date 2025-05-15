from locust import HttpUser, task, between

class EquityShieldUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def get_corporate_structure(self):
        self.client.get("/api/corporate-structure")

    @task(2)
    def get_real_assets(self):
        self.client.get("/api/real-assets")

    @task(1)
    def get_companies_by_sector(self):
        # Example sector, adjust as needed
        sector = "Technology"
        self.client.get(f"/api/companies/{sector}")

    @task(1)
    def get_company_by_ticker(self):
        # Example ticker, adjust as needed
        ticker = "AAPL"
        self.client.get(f"/api/company/{ticker}")

    @task(1)
    def get_banking_info(self):
        self.client.get("/api/banking-info")
