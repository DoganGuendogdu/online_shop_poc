import streamlit as st

from app.config import Config


# TODO: Do not return a value if a selected payment method is not ready yet.
# TODO: Validate user inputs
class PaymentView:
    def __init__(self, config: Config):
        st.subheader("Payment method")
        self.__config = config
        self.__select_payment = st.selectbox("Pick payment method", self.__config.get_payment_methods(),
                                             index=None)

    def get_payment_input_data(self):
        if self.__select_payment == "paypal":
            get_paypal_data = self.__get_paypal_input_data()

            if get_paypal_data:
                return get_paypal_data
        elif self.__select_payment == "master_card":
            credit_card_data = self.__get_master_card_input_data()

            if credit_card_data:
                return credit_card_data
        elif self.__select_payment == "paysafe":
            paysafe_card_data = self.__get_paysafe_card_input_data()

            if paysafe_card_data:
                return paysafe_card_data
        elif self.__select_payment == "apple_pay":
            apple_pay_data = self.__get_apple_pay_input_data()

            if apple_pay_data:
                return apple_pay_data
        else:
            return None

    def __get_paypal_input_data(self) -> dict:
        with st.form(key="paypal_form"):
            paypal_user_name = st.text_input("Pleaser enter your PayPal user name.")
            paypal_password = st.text_input("Please enter your PayPal password.", type="password")
            pay_button = st.form_submit_button("Pay")

            if pay_button:
                if all([paypal_user_name, paypal_password]):
                    return {
                        "payment_type": "paypal",
                        "paypal_user_name": paypal_user_name,
                        "paypal_password": paypal_password
                    }

    def __get_master_card_input_data(self) -> dict:
        with st.form(key="master_card_form"):
            credit_card_number = st.text_input("Please enter your credit card number.", key=int)
            expiration_date = st.date_input("Please enter the expiration date of your credit card.")
            cvc_number = st.text_input("Please enter your digit CVC number.", max_chars=3)
            first_name = st.text_input("Please enter your first name.")
            last_name = st.text_input("Please enter your last name.")
            pay_button = st.form_submit_button("Pay")

            if pay_button:
                if all([credit_card_number, expiration_date, cvc_number, first_name, last_name]):
                    return {
                        "payment_type": "master_card",
                        "credit_card_number": credit_card_number,
                        "expiration_date": expiration_date,
                        "cvc_number": cvc_number,
                        "first_name": first_name,
                        "last_name": last_name
                    }

    def __get_paysafe_card_input_data(self) -> dict:
        with st.form(key="paysafe_form"):
            paysafe_code = st.text_input("Please enter your Paysafe card code.", max_chars=16)
            pay_button = st.form_submit_button("Pay")

            if pay_button:
                if paysafe_code:
                    return {
                        "payment_type": "paysafe",
                        "paysafe_code": paysafe_code
                    }

    def __get_apple_pay_input_data(self) -> dict:
        with st.form(key="apple_pay_form"):
            apple_id = st.text_input("Please enter your Apple ID.")
            apple_id_password = st.text_input("Please enter your Apple ID password", type="password")
            pay_button = st.form_submit_button("Pay")

            if pay_button:
                if all([apple_id, apple_id_password]):
                    return {
                        "payment_type": "apple_pay",
                        "apple_id": apple_id,
                        "apple_id_password": apple_id_password
                    }
