from fastapi.testclient import TestClient

from ..src.main import app

test_client = TestClient(app)


def test_invalid_endpoint():
    response = test_client.post("payment/bitcoin", json={"data": "test"})
    assert response.status_code == 404


def test_post_paypal_payment_200():
    request_body = {"email": "test@gmail.com", "password": "823fnr828932hf"}
    response = test_client.post("/payment/paypal", json=request_body)
    assert response.status_code == 200
    assert response.json() == {"payment_method": "paypal", "email": "test@gmail.com"}


def test_post_paypal_payment_invalid_email_422():
    request_body = {"email": "test.com", "password": "823fnr828932hf"}
    response = test_client.post("/payment/paypal", json=request_body)
    assert response.status_code == 422


def test_post_paypal_payment_invalid_password_422():
    request_body = {"email": "olaf@test.com", "password": "123"}
    response = test_client.post("/payment/paypal", json=request_body)
    assert response.status_code == 422


def test_post_master_card_payment_200():
    request_body = {"credit_card_number": 1233123312341235, "expiration_date": "2044-02-05", "cvc": 123,
                    "first_name": "Kaan", "last_name": "KEK"}
    response = test_client.post("payment/master_card", json=request_body)
    assert response.status_code == 200
    assert response.json() == {"payment_method": "credit_card", "credit_card_number": 1233123312341235,
                               "expiration_date": "2044-02-05", "first_name": "Kaan",
                               "last_name": "KEK"}


def test_post_master_card_payment_invalid_cvc_422():
    request_body = {"credit_card_number": 1233123312341235, "expiration_date": "2066-02-05",
                    "cvc": 123892734, "first_name": "Kaan", "last_name": "KEK"}
    response = test_client.post("payment/master_card", json=request_body)
    assert response.status_code == 422


def test_post_master_card_payment_invalid_credit_card_number_422():
    request_body = {"credit_card_number": 3333, "expiration_date": "2066-02-05",
                    "cvc": 123, "first_name": "Kaan", "last_name": "KEK"}
    response = test_client.post("payment/master_card", json=request_body)
    assert response.status_code == 422


def test_post_paysafe_card_payment_200():
    request_body = {"paysafe_code": 2007922397084805}
    response = test_client.post("/payment/paysafe", json=request_body)
    assert response.status_code == 200
    assert response.json() == {"payment_method": "paysafe", "paysafe_code": 2007922397084805}


def test_post_paysafe_card_payment_invalid_paysafe_code_422():
    request_body = {"paysafe_code": 20079223970848053333}
    response = test_client.post("/payment/paysafe", json=request_body)
    assert response.status_code == 422


def test_apple_pay_payment_200():
    request_body = {"apple_id": "test@ot.com", "password": "98feaojfe"}
    response = test_client.post("payment/apple_pay", json=request_body)
    assert response.status_code == 200
    assert response.json() == {"payment_method": "ApplePay", "apple_id": "test@ot.com"}


def test_apple_pay_payment_invalid_email_422():
    request_body = {"apple_id": "test.com", "password": "98feaojfe"}
    response = test_client.post("payment/apple_pay", json=request_body)
    assert response.status_code == 422
