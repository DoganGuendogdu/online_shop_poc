from config import Config
from controller.main_page_controller import MainPageController
from controller.payment_controller import PaymentController
from service.payment_service import PaymentService
from views.main_page_view import MainPageView
from views.process_payment_view import PaymentView


def main():
    config = Config()

    main_page_view = MainPageView()
    main_page_controller = MainPageController(main_page_view)
    main_page_controller.show_main_page()

    payment_view = PaymentView(config)
    payment_service = PaymentService()
    payment_controller = PaymentController(payment_view, payment_service)

    payment_controller.get_payment_input_data()


if __name__ == "__main__":
    main()
