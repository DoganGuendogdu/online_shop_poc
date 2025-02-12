import logging

from config import Config
from app.src.controller.main_page_controller import MainPageController
from app.src.controller.payment_controller import PaymentController
from app.src.service.payment_service import PaymentService
from app.src.views.main_page_view import MainPageView
from app.src.views.payment_view import PaymentView


def main():
    logging.basicConfig(level=logging.INFO)

    config = Config()

    main_page_view = MainPageView()
    main_page_controller = MainPageController(main_page_view)
    main_page_controller.show_main_page()

    payment_view = PaymentView(config)
    payment_service = PaymentService(config)
    payment_controller = PaymentController(payment_view, payment_service)
    payment_controller.call_payment_api()


if __name__ == "__main__":
    main()
