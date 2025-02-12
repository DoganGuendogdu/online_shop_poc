from ..views.main_page_view import MainPageView


class MainPageController:
    def __init__(self, main_page_view: MainPageView):
        self.__main_page_view = main_page_view

    def show_main_page(self):
        self.__main_page_view.show_main_page()
