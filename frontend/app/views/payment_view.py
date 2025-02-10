import logging

import streamlit as st
from app.config import Config


# TODO: Validate user inputs and types.
class PaymentView:
    def __init__(self, config: Config):
        st.subheader("Payment method")
        self.__config = config
        self.__logger = logging.getLogger("payment_view")
        self.__select_payment = st.selectbox("Pick payment method", self.__config.payment_methods, index=None)

        self.__initialize_state_elements()

    def handle_payment(self):
        if self.__select_payment == "Paysafe":
            return self.__render_paysafe_payment()
        elif self.__select_payment == "Master Card":
            return self.__render_master_card_payment()
        elif self.__select_payment == "ApplePay":
            return self.__render_apple_pay_payment()
        elif self.__select_payment == "PayPal":
            return self.__render_paypal_payment()
        else:
            self.__logger.debug(
                f"Can not process payment method. Payment method '{self.__select_payment}' does not exist")

    def __render_master_card_payment(self):
        with st.container():
            st.session_state["credit_card_number"] = st.text_input("Please enter your credit card number.")
            st.session_state["expiration_date"] = st.date_input("Please enter the expiration date of your credit card.")
            st.session_state["cvc_number"] = st.text_input("Please enter your CVC number.", max_chars=3)
            st.session_state["first_name"] = st.text_input("Please enter your first name.")
            st.session_state["last_name"] = st.text_input("Please enter your last name.")
            st.session_state["master_card_pay_button"] = st.button("Pay with MasterCard")

            if st.session_state["master_card_pay_button"]:
                # Reset button state to prevent false positives
                st.session_state["master_card_pay_button"] = False

                # Check if all required fields have been provided
                if not all([
                    st.session_state.get("credit_card_number"),
                    st.session_state.get("expiration_date"),
                    st.session_state.get("cvc_number"),
                    st.session_state.get("first_name"),
                    st.session_state.get("last_name")
                ]):
                    self.__logger.debug(
                        "Cannot return 'MasterCard' credentials. One or more required fields are missing."
                    )
                    st.warning("Please provide input for all required fields.")
                    return None

                return {
                    "payment_type": "master_card",
                    "credit_card_number": st.session_state["credit_card_number"],
                    "expiration_date": st.session_state["expiration_date"],
                    "cvc_number": st.session_state["cvc_number"],
                    "first_name": st.session_state["first_name"],
                    "last_name": st.session_state["last_name"]
                }

            return None

    def __render_apple_pay_payment(self):
        with st.container():
            st.session_state["apple_id"] = st.text_input("Please enter your Apple ID.")
            st.session_state["apple_id_password"] = st.text_input("Please enter your password.", type="password")
            st.session_state["apple_pay_button"] = st.button("Pay with Apple Pay")

            if st.session_state["apple_pay_button"]:
                # Since Streamlit reruns the whole script from top to bottom everytime a user makes any change,
                # it is necessary to reset the button, so it will not contain a false positive state.
                st.session_state["apple_pay_button"] = False

                # Check if all required fields have been provided.
                if not all([
                    st.session_state.get("apple_id"),
                    st.session_state.get("apple_id_password")
                ]):
                    self.__logger.debug(
                        "Can not return 'apple_pay' credentials. Either 'apple_id' or 'password' is None.")
                    st.warning("Please provide input for the required fields")
                    return None

                return {
                    "payment_type": "apple_pay",
                    "apple_id": st.session_state.get("apple_id"),
                    "apple_id_password": st.session_state.get("apple_id_password")
                }

            return None

    def __render_paysafe_payment(self):
        with st.container():
            st.session_state["paysafe_code"] = st.text_input("Pleaser enter your PaySafe code.", type="password")
            st.session_state["paysafe_button"] = st.button("Pay with Paysafe")

            if st.session_state["paysafe_button"]:
                # Since Streamlit reruns the whole script from top to bottom everytime a user makes any change,
                # it is necessary to reset the button, so it will not contain a false positive state.
                st.session_state["paysafe_button"] = False

                # Check if all required fields have been provided.
                if not st.session_state.get("paysafe_code"):
                    self.__logger.debug("Can not return 'paysafe' credentials. 'paysafe_code' is None.")
                    st.warning("Please provide input for the required fields")
                    return None

                return {
                    "payment_type": "paysafe",
                    "paysafe_code": st.session_state["paysafe_code"]
                }

            return None

    def __render_paypal_payment(self):
        with st.container():
            st.session_state["paypal_username"] = st.text_input("Pleaser enter your PayPal user name.")
            st.session_state["paypal_password"] = st.text_input("Please enter your PayPal password.", type="password")
            st.session_state["paypal_button"] = st.button("Pay with PayPal")

            if st.session_state["paypal_button"]:
                # Since Streamlit reruns the whole script from top to bottom everytime a user makes any change,
                # it is necessary to reset the button, so it will not contain a false positive state.
                st.session_state["paypal_button"] = False

                # Check if all required fields have been provided.
                if not all([st.session_state.get("paypal_username"), st.session_state.get("paypal_password")]):
                    self.__logger.debug(
                        "Can not return 'paypal' credentials. Either 'paypal_username' or 'paypal_password' is None.")
                    st.warning("Please provide input for the required fields")
                    return None

                return {
                    "payment_type": "paypal",
                    "paypal_username": st.session_state["paypal_username"],
                    "paypal_password": st.session_state["paypal_password"]
                }

            return None

    def __initialize_state_elements(self):
        # PayPal fields.
        if "paypal_username" not in st.session_state:
            st.session_state["paypal_username"] = ""
        if "paypal_password" not in st.session_state:
            st.session_state["paypal_password"] = ""
        if "paypal_button" not in st.session_state:
            st.session_state["paypal_button"] = False

        # Paysafe fields.
        if "paysafe_code" not in st.session_state:
            st.session_state["paysafe_code"] = ""
        if "paysafe_button" not in st.session_state:
            st.session_state["paysafe_button"] = None

        # Apple Pay fields.
        if "apple_id" not in st.session_state:
            st.session_state["apple_id"] = ""
        if "apple_id_password" not in st.session_state:
            st.session_state["apple_id_password"] = ""
        if "apple_pay_button" not in st.session_state:
            st.session_state["apple_pay_button"] = None

        # Master Card fields.
        if "credit_card_number" not in st.session_state:
            st.session_state["credit_card_number"] = ""
        if "expiration_date" not in st.session_state:
            st.session_state["expiration_date"] = None
        if "cvc_number" not in st.session_state:
            st.session_state["cvc_number"] = ""
        if "first_name" not in st.session_state:
            st.session_state["first_name"] = ""
        if "last_name" not in st.session_state:
            st.session_state["last_name"] = ""
        if "master_card_pay_button" not in st.session_state:
            st.session_state["master_card_pay_button"] = False
