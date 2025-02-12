from fastapi.testclient import TestClient

from app.main import app


test_client = TestClient(app)


def test_post_paypal_payment_200():
    request_body = {"email": "test@gmail.com", "password": "823fnr828932hf"}
    response = test_client.post("/payment/paypal", json=request_body)
    assert response.status_code == 200
    assert response.json() == {"payment_method": "paypal", "email": "test@gmail.com"}
