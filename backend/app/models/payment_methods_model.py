from datetime import datetime

from pydantic import BaseModel, Field, SecretStr, EmailStr


class PayPalModel(BaseModel):
    email: EmailStr = Field(..., example="john.doe@gmail.com")
    # SecretStr ensures that no password is logged or exposed
    # Use syntactic salt 'get_secret_value()' to retrieve password
    password: SecretStr = Field(..., min_length=8, max_length=88)


class MasterCardModel(BaseModel):
    credit_card_number: int = Field(..., ge=0000000000000000, le=9999999999999999, example=9828275081835264)
    expiration_date: datetime = Field(..., example=datetime.now())
    # Numbers 100-999, so all 3-digit numbers
    cvc: int = Field(..., ge=100, le=999, example=123)
    first_name: str = Field(..., max_length=40, example="Peter")
    last_name: str = Field(..., max_length=40, example="Lustig")


class PaySafeModel(BaseModel):
    paysafe_code: int = Field(..., ge=0000000000000000, le=9999999999999999, example=9828275081835264)


class ApplePayModel(BaseModel):
    apple_id: EmailStr = Field(..., example="olaf@outlook.de")
    password: SecretStr = Field(..., min_length=8, max_length=40, example="kndkjansdna82828")
