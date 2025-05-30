import time

import pytest

from conftest import browser
from pages.basket_page import BasketPage
from pages.locators import ProductPageLocators
from pages.login_page import LoginPage
from pages.product_page import ProductPage

base_url = "https://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"

class TestUserAddToBasketFromProductPage:

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        link = "https://selenium1py.pythonanywhere.com/accounts/login/"
        page = LoginPage(browser, link)
        page.open()
        email = str(time.time()) + "@fakemail.org"
        password = "bestPasswordInTheWorld123"
        page.register_new_user(email, password)
        page.should_be_authorized_user()

    def test_user_cant_see_success_message(self, browser):
        link = base_url
        page = ProductPage(browser, link)
        page.open()
        assert page.is_not_element_present(
            *ProductPageLocators.SUCCESS_MESSAGE_PRODUCT), "Success message is displayed on product page, but should not be"

    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser):
        link = "https://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0"
        page = ProductPage(browser, link)
        page.open()
        print('===========================')
        page.add_product_to_basket()
        page.solve_quiz_and_get_code()
        page.should_be_success_message_with_product_name()
        page.should_be_success_message_with_price()


@pytest.mark.need_review
@pytest.mark.parametrize(
    'link',
    [
        base_url + "?promo=offer0",
        base_url + "?promo=offer1",
        base_url + "?promo=offer2",
        base_url + "?promo=offer3",
        base_url + "?promo=offer4",
        base_url + "?promo=offer5",
        base_url + "?promo=offer6",
        pytest.param(
          base_url + "?promo=offer7",
          marks=pytest.mark.xfail()
        ),
        base_url + "?promo=offer8",
        base_url + "?promo=offer9"
    ]
)
def test_guest_can_add_product_to_basket(browser, link):
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_success_message_with_product_name()
    page.should_be_success_message_with_price()


@pytest.mark.xfail
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    link = base_url
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket()
    assert page.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE_PRODUCT), "Success message is displayed, but should not be"

@pytest.mark.xfail
def test_message_disappeared_after_adding_product_to_basket(browser):
    link = base_url
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket()
    page.success_message_should_disappear()

def test_guest_cant_see_success_message(browser):
    link = base_url
    page = ProductPage(browser, link)
    page.open()
    page.should_not_be_success_message()

city_and_stars_url = "https://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"

def test_guest_should_see_login_link_on_product_page(browser):
    link = city_and_stars_url
    page = ProductPage(browser, link)
    page.open()
    page.should_be_login_link()

@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
    link = city_and_stars_url
    page = ProductPage(browser, link)
    page.open()
    page.go_to_login_page()

    login_page = LoginPage(browser, browser.current_url)
    login_page.should_be_login_page()

@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    link = city_and_stars_url
    page = ProductPage(browser, link)
    page.open()
    page.go_to_basket_page()

    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_empty_basket()
    basket_page.should_be_text_basket_is_empty()