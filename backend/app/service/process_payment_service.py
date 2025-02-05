from abc import abstractmethod, ABC
from ..models.payment_methods_model import *


class PaymentMethodStrategy(ABC):
    @abstractmethod
    def get_payment_details(self):
        pass


class PayPalStrategy(PaymentMethodStrategy):
    def __init__(self, paypal_model: PayPalModel):
        self.__paypal_model = paypal_model

    def get_payment_details(self):
        return {
            "payment_method": "paypal",
            **self.__paypal_model.model_dump(exclude={"password"})
        }


class MasterCardStrategy(PaymentMethodStrategy):
    def __init__(self, credit_card_model: MasterCardModel):
        self.__credit_card_model = credit_card_model

    def get_payment_details(self):
        return {
            "payment_method": "credit_card",
            **self.__credit_card_model.model_dump(exclude={"cvc"})
        }


class PaySafeStrategy(PaymentMethodStrategy):
    def __init__(self, paysafe_model: PaySafeModel):
        self.__paysafe_model = paysafe_model

    def get_payment_details(self):
        return {
            "payment_method": "paysafe",
            **self.__paysafe_model.model_dump()
        }


class ApplePayStrategy(PaymentMethodStrategy):
    def __init__(self, apple_pay_model: ApplePayModel):
        self.__apple_pay_model = apple_pay_model

    def get_payment_details(self):
        return {
            "payment_method": "ApplePay",
            **self.__apple_pay_model.model_dump(exclude={"password"})
        }



class Payment(PaymentMethodStrategy):
    def __init__(self):
        self.__payment_method_strategy = None
        # self.__buyer_protection = None

    def set_payment_method(self, payment_method_strategy: PaymentMethodStrategy):
        self.__payment_method_strategy = payment_method_strategy

    # def set_seller_protection_for_buyer(self, buyer_protection: BuyerProtectionStrategy):
    #     self.__buyer_protection = buyer_protection

    def get_payment_details(self):
        return self.__payment_method_strategy.get_payment_details()

    # def print_seller_protection_for_buyer(self):
    #     self.__buyer_protection.print_seller_protection_for_buyer()
