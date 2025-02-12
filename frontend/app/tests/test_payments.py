import unittest
from unittest.mock import patch, Mock

from ..src.config import Config
from ..src.service.payment_service import PaymentService


class TestPaymentMethods(unittest.TestCase):

    # 'requests.post' is the actual object/service which will be mocked.
    @patch("requests.post")
    def test_paysafe_payment(self, mock_post):
        # Create the service which will use the mocked API.
        config = Config()
        payment_service = PaymentService(config)

        # Create a mock object with:
        # 1. The expected value to be returned
        # 2. The expected status code returned
        mock = Mock()
        mock.json.return_value = {"payment_method": "paysafe", "paysafe_code": 2007922397084805}
        mock.status_code = 200

        # Assign the created Mocking object to the mocked service
        # Essentially, the mocked object reflects the behaviour of the API
        # So, 'mock_post' is the post request to the API where the mocked object reflects its behaviour
        mock_post.return_value = mock

        url = "http://backend-fastapi-api:1111/payment/paysafe"

        # Call the API service. Here, the internal post request will be mapped to the mocked object.
        result = payment_service.post_payment({"payment_type": "paysafe", "paysafe_code": 4444444444444444})

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {"payment_method": "paysafe", "paysafe_code": 2007922397084805})

        mock_post.assert_called_with(url, json={'paysafe_code': 4444444444444444})

    @patch("requests.post")
    # Mock the API. Assume that API exists.
    def test_apple_pay_payment(self, mock_post):
        config = Config()
        payment_service = PaymentService(config)

        # Create Mock object with return value and status code.
        mock = Mock()
        mock.json.return_value = {"payment_method": "ApplePay", "apple_id": "test@gmail.com"}
        mock.status_code = 200

        # Assign Mock object to the actual Post request
        # So, here the Post request is mocked
        mock_post.return_value = mock

        # Call the service with input data
        result = payment_service.post_payment(
            {"payment_type": "apple_pay", "apple_id": "test@gmail.com", "apple_id_password": "jhdsajfkajsfh"})

        # API status code
        self.assertEqual(result.status_code, 200)

        # API response
        self.assertEqual(result.json(), {"payment_method": "ApplePay", "apple_id": "test@gmail.com"})

        # API endpoint and request body
        mock_post.assert_called_with("http://backend-fastapi-api:1111/payment/apple_pay",
                                     json={"apple_id": "test@gmail.com", "password": "jhdsajfkajsfh"})

    @patch("requests.post")
    def test_paypal_payment(self, mock_post):
        mock = Mock()
        mock.json.return_value = {"payment_method": "paypal", "email": "dogan@test.com"}
        mock.status_code = 200

        mock_post.return_value = mock

        payment_service = PaymentService(Config())

        response = payment_service.post_payment(
            {"payment_type": "paypal", "paypal_username": "dogan@test.com", "paypal_password": "adjashdjashdaj"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"payment_method": "paypal", "email": "dogan@test.com"})
        mock_post.assert_called_with("http://backend-fastapi-api:1111/payment/paypal",
                                     json={"email": "dogan@test.com", "password": "adjashdjashdaj"})

    @patch("requests.post")
    def test_master_card_payment(self, mock_post):
        mock = Mock()
        mock.json.return_value = {"payment_method": "credit_card",
                                  "credit_card_number": 1233123312341235,
                                  "expiration_date": "2025-09-12",
                                  "first_name": "Klaus",
                                  "last_name": "Otto"
                                  }
        mock.status_code = 200

        mock_post.return_value = mock

        payment_service = PaymentService(config=Config())
        response = payment_service.post_payment(
            {"payment_type": "master_card", "credit_card_number": 1233123312341235, "expiration_date": "2025-09-12",
             "cvc_number": 123, "first_name": "Klaus", "last_name": "Otto"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"payment_method": "credit_card", "credit_card_number": 1233123312341235,
                                           "expiration_date": "2025-09-12", "first_name": "Klaus", "last_name": "Otto"})
        mock_post.assert_called_with("http://backend-fastapi-api:1111/payment/master_card",
                                     json={"credit_card_number": 1233123312341235, "expiration_date": "2025-09-12",
                                           "cvc": 123, "first_name": "Klaus", "last_name": "Otto"})

    if __name__ == "__main__":
        unittest.main()
