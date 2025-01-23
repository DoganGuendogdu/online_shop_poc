from src.controller.main_page_controller import MainPageController
from src.controller.process_payment_controller import ProcessPaymentController
from src.view.main_page_view import MainPageView
from src.view.process_payment_view import ProcessPaymentView


def main():
    main_page_view = MainPageView()
    main_page_controller = MainPageController(main_page_view)

    process_payment_view = ProcessPaymentView()
    process_payment_controller = ProcessPaymentController(process_payment_view)
    process_payment_controller.process_payment()


if __name__ == "__main__":
    main()
