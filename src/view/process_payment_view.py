import streamlit as st

from src.config import Config


class ProcessPaymentView:
    def __init__(self, config: Config):
        st.subheader("Payment method")
        self.__config = config
        self.__select_payment = st.selectbox("Pick payment method", self.__config.get_payment_methods(),
                                             index=None)

    def get_payment_method_credentials(self):
        if self.__select_payment == "PayPal":
            get_paypal_data = self.__get_paypal_data()

            if get_paypal_data:
                return get_paypal_data
        elif self.__select_payment == "Credit card":
            credit_card_data = self.__get_credit_card_data()

            if credit_card_data:
                return credit_card_data
        elif self.__select_payment == "Paysafe":
            paysafe_card_data = self.__get_paysafe_card_data()

            if paysafe_card_data:
                return paysafe_card_data
        elif self.__select_payment == "ApplePay":
            apple_pay_data = self.__get_apple_pay_data()

            if apple_pay_data:
                return apple_pay_data
        else:
            return None

    def __get_paypal_data(self) -> dict:
        with st.container():
            paypal_user_name = st.text_input("Pleaser enter your PayPal user name.")
            paypal_password = st.text_input("Please enter your PayPal password.", type="password")
            pay_button = st.button("Pay", type="primary")

            if pay_button:
                if all([paypal_user_name, paypal_password]):
                    return {"payment_type": "PayPal",
                            "paypal_user_name": paypal_user_name,
                            "paypal_password": paypal_password}

    def __get_credit_card_data(self) -> dict:
        with st.container():
            credit_card_number = st.text_input("Please enter your credit card number.", key=int)
            expiration_date = st.date_input("Please enter the expiration date of your credit card.")
            cvc_number = st.text_input("Please enter your digit CVC number.", max_chars=3)
            first_name = st.text_input("Please enter your first name.")
            last_name = st.text_input("Please enter your last name.")
            pay_button = st.button("Pay", type="primary")

            if pay_button:
                if all([credit_card_number, expiration_date, cvc_number, first_name, last_name]):
                    return {
                        "payment_type": "Credit card",
                        "credit_card_number": credit_card_number,
                        "expiration_date": expiration_date,
                        "cvc_number": cvc_number,
                        "first_name": first_name,
                        "last_name": last_name}

    def __get_paysafe_card_data(self) -> dict:
        with st.container():
            paysafe_code = st.text_input("Please enter your Paysafe card code.", max_chars=16)
            pay_button = st.button("Pay", type="primary")

            if pay_button:
                if paysafe_code:
                    return {
                        "payment_type": "PaySafe",
                        "paysafe_code": paysafe_code}

    def __get_apple_pay_data(self) -> dict:
        with st.container():
            apple_id = st.text_input("Please enter your Apple ID.")
            apple_id_password = st.text_input("Please enter your Apple ID password", type="password")
            pay_button = st.button("Pay", type="primary")

            if pay_button:
                if all([apple_id, apple_id_password]):
                    return {"payment_type": "Apple Pay",
                            "apple_id": apple_id,
                            "apple_id_password": apple_id_password}
