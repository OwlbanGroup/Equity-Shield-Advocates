import unittest
from ai_predictive import CorporatePredictiveModel

class TestCorporatePredictiveModel(unittest.TestCase):
    def setUp(self):
        self.model = CorporatePredictiveModel()
        self.model.train_model()

    def test_predict(self):
        prediction = self.model.predict(12)
        self.assertIsInstance(prediction, float)

    def test_train_model(self):
        # Ensure model coefficients are set after training
        self.assertIsNotNone(self.model.model.coef_)

if __name__ == '__main__':
    unittest.main()
