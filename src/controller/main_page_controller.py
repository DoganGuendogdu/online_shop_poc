import sys

sys.path.append("..")

from src.view.main_page_view import MainPageView


class MainPageController:
    def __init__(self, main_page_view: MainPageView):
        self.__main_page_view = main_page_view
