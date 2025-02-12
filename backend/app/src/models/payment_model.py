from abc import abstractmethod, ABC
from ..entities.payments import *


class PaymentStrategy(ABC):
    @abstractmethod
    def get_payment_details(self):
        pass


class PayPalStrategy(PaymentStrategy):
    def __init__(self, paypal: PayPal):
        self.__paypal_model = paypal

    def get_payment_details(self):
        return {
            "payment_method": "paypal",
            **self.__paypal_model.model_dump(exclude={"password"})
        }


class MasterCardStrategy(PaymentStrategy):
    def __init__(self, credit_card: MasterCard):
        self.__credit_card_model = credit_card

    def get_payment_details(self):
        return {
            "payment_method": "credit_card",
            **self.__credit_card_model.model_dump(exclude={"cvc"})
        }


class PaySafeStrategy(PaymentStrategy):
    def __init__(self, paysafe: PaySafe):
        self.__paysafe_model = paysafe

    def get_payment_details(self):
        return {
            "payment_method": "paysafe",
            **self.__paysafe_model.model_dump()
        }


class ApplePayStrategy(PaymentStrategy):
    def __init__(self, apple_pay: ApplePay):
        self.__apple_pay_model = apple_pay

    def get_payment_details(self):
        return {
            "payment_method": "ApplePay",
            **self.__apple_pay_model.model_dump(exclude={"password"})
        }



class PaymentModel(PaymentStrategy):
    def __init__(self):
        self.__payment_strategy = None
        # self.__buyer_protection = None

    def set_payment_method(self, payment_strategy: PaymentStrategy):
        self.__payment_strategy = payment_strategy

    # def set_seller_protection_for_buyer(self, buyer_protection: BuyerProtectionStrategy):
    #     self.__buyer_protection = buyer_protection

    def get_payment_details(self):
        return self.__payment_strategy.get_payment_details()

    # def print_seller_protection_for_buyer(self):
    #     self.__buyer_protection.print_seller_protection_for_buyer()
