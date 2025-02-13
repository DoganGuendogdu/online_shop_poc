import logging

import streamlit as st
from email_validator import validate_email, EmailNotValidError

from ..config import Config


# TODO: Validate user inputs and types.
class PaymentView:
    def __init__(self, config: Config):
        st.subheader("Payment method")
        self.__config = config
        self.__logger = logging.getLogger("payment_view")
        self.__select_payment = st.selectbox("Pick a payment method,", self.__config.payment_methods, index=None)

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

                if not st.session_state.get("apple_id"):
                    self.__logger.debug("'apple_id' is None.")
                    st.warning("Please ensure to provide an Apple ID.")
                    return None

                if not st.session_state["apple_id_password"]:
                    self.__logger.debug("'apple_id_password' is None.")
                    st.warning("Please ensure to provide a password.")
                    return None

                if not self.__validate_email(st.session_state.get("apple_id")):
                    self.__logger.debug("'apple_id' in an invalid email address.")
                    st.warning("Please ensure to provide a valid email address.")
                    return None

                if not self.__validate_apple_pay_password(st.session_state.get("apple_id_password")):
                    self.__logger.debug("Invalid 'apple_pay' password'")
                    st.warning("Please ensure that the provided password has min. 8 and max. 40 digits.")
                    return None

                st.success("Credentials are valid.")
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
                    self.__logger.debug("'paysafe_code' is None.")
                    st.warning("Please provide input for the required fields")
                    return None

                if not self.__validate_paysafe_code(st.session_state["paysafe_code"]):
                    self.__logger.debug("Paysafe code is invalid")
                    st.warning("Please ensure to provide a valid Paysafe code which is 16 digits long.")
                    return None

                st.success("Paysafe code is valid")
                return {
                    "payment_type": "paysafe",
                    "paysafe_code": st.session_state["paysafe_code"]
                }
            return None

    def __render_paypal_payment(self):
        with st.container():
            st.session_state["paypal_username"] = st.text_input("Pleaser enter your PayPal email.")
            st.session_state["paypal_password"] = st.text_input("Please enter your PayPal password.", type="password")
            st.session_state["paypal_button"] = st.button("Pay with PayPal")

            if st.session_state["paypal_button"]:
                # Since Streamlit reruns the whole script from top to bottom everytime a user makes any change,
                # it is necessary to reset the button, so it will not contain a false positive state.
                st.session_state["paypal_button"] = False

                if not st.session_state.get("paypal_username"):
                    self.__logger.debug("'Paypal username' is None.")
                    st.warning("Please provide your Paypal Email.")
                    return None

                if not st.session_state.get("paypal_password"):
                    self.__logger.debug("Paypal password is None.")
                    st.warning("Please provide your PayPal password.")
                    return None

                if not self.__validate_email(st.session_state.get("paypal_username")):
                    self.__logger.debug(
                        f"The provided email: {st.session_state.get('paypal_username')} has an invalid format.")
                    st.warning("Please provide a valid email address.")
                    return None

                if not self.__validate_paypal_password(st.session_state.get("paypal_password")):
                    self.__logger.debug("Invalid password.")
                    st.warning("Please ensure that your provided password is min. 8 and max. 88 digits long.")
                    return None

                st.success("Credentials are valid.")
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

    def __validate_apple_pay_password(self, apple_pay_password: str):
        if len(apple_pay_password) > 40:
            self.__logger.debug("'apple_pay_password' has more than 40 digits.")
            return None
        elif len(apple_pay_password) < 8:
            self.__logger.debug("'apple_pay_password has less than 8 digits.")
            return None
        return apple_pay_password

    def __validate_paysafe_code(self, paysafe_code: str):
        try:
            int(paysafe_code)
        except ValueError:
            return None

        if len(paysafe_code) > 16 or len(paysafe_code) < 16:
            return None
        return paysafe_code

    def __validate_paypal_password(self, paypal_password: str):
        if len(paypal_password) > 88 or len(paypal_password) < 8:
            return None
        return paypal_password

    def __validate_email(self, email: str):
        try:
            email_info = validate_email(email)
            return str(email_info.normalized)
        except EmailNotValidError:
            return None
