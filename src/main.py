from config import Config
from controller.main_page_controller import MainPageController
from controller.process_payment_controller import ProcessPaymentController
from view.main_page_view import MainPageView
from view.process_payment_view import ProcessPaymentView



def main():
    config = Config()

    main_page_view = MainPageView()
    main_page_controller = MainPageController(main_page_view)

    process_payment_view = ProcessPaymentView(config)
    process_payment_controller = ProcessPaymentController(process_payment_view)
    process_payment_controller.process_payment()


if __name__ == "__main__":
    main()
