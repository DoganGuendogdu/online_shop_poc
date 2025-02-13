from datetime import date

from pydantic import BaseModel
from pydantic import Field, SecretStr, EmailStr
from pydantic import field_validator


class PayPal(BaseModel):
    email: EmailStr = Field(..., example="john.doe@gmail.com")
    # SecretStr ensures that no password is logged or exposed
    # Use syntactic salt 'get_secret_value()' to retrieve password
    password: SecretStr = Field(..., min_length=8, max_length=88)


class MasterCard(BaseModel):
    credit_card_number: int = Field(..., example=9828275081835264)
    expiration_date: date = Field(..., example=date.today())
    # Numbers 100-999, so all 3-digit numbers
    cvc: int = Field(..., example=341)
    first_name: str = Field(..., max_length=40, example="Peter")
    last_name: str = Field(..., max_length=40, example="Lustig")

    @field_validator("credit_card_number")
    def validate_credit_card_number(cls, credit_card_number):
        if len(str(credit_card_number)) > 16:
            raise ValueError("The provided credit card number contains more than 16 digits.")
        elif len(str(credit_card_number)) < 16:
            raise ValueError("The provided credit card number contains less than 16 digits")
        return credit_card_number

    @field_validator("expiration_date")
    def validate_expiration_date(cls, expiration_date: date):
        if expiration_date <= date.today():
            raise ValueError("The provided credit card is invalid since the expiration date has expired.")
        return expiration_date

    @field_validator("cvc")
    def validate_cvc(cls, cvc: int):
        if len(str(cvc)) > 3:
            raise ValueError("The provided cvc number contains more than 3 digits.")
        elif (len(str(cvc))) < 3:
            raise ValueError("The provided cvc number contains less than 3 digits")
        return cvc


class PaySafe(BaseModel):
    paysafe_code: int = Field(..., example=9828275081835264)

    @field_validator("paysafe_code")
    def validate_paysafe_code(cls, paysafe_code: int):
        if len(str(paysafe_code)) > 16:
            raise ValueError("The provided paysafe code contains more than 16 digits.")
        elif len(str(paysafe_code)) < 16:
            raise ValueError("The provided paysafe code contains less than 16 digits")
        return paysafe_code


class ApplePay(BaseModel):
    apple_id: EmailStr = Field(..., example="olaf@outlook.de")
    password: SecretStr = Field(..., min_length=8, max_length=40, example="kndkjansdna82828")
