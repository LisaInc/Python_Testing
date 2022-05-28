from selenium import webdriver
from flask_testing import LiveServerTestCase
import time

import server


class TestServer(LiveServerTestCase):
    def create_app(self):
        return server.create_app()

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "http://localhost:5000/"

    def tearDown(self):
        self.driver.quit()

    def test_login_valid_email(self):
        self.driver.get(self.get_server_url())
        assert self.driver.current_url == self.base_url

        button = self.driver.find_element(by="name", value="email")
        button.send_keys("john@simplylift.co")
        signup = self.driver.find_element(by="name", value="submit")
        signup.click()
        assert self.driver.current_url == f"{self.base_url}showSummary"

    def test_login_invalid_email(self):
        self.driver.get(self.base_url)
        button = self.driver.find_element(by="name", value="email")
        button.send_keys("test@test.com")
        signup = self.driver.find_element(by="name", value="submit")
        signup.click()
        assert (
            self.driver.find_element(by="name", value="message").text
            == "Email not found, try again"
        )

    def test_logout(self):
        self.driver.get(self.base_url)
        button = self.driver.find_element(by="name", value="email")
        button.send_keys("john@simplylift.co")
        signup = self.driver.find_element(by="name", value="submit")
        signup.click()
        logout = self.driver.find_element(by="name", value="logout")
        logout.click()
        assert self.driver.current_url == self.base_url

    def test_book_place(self):
        self.driver.get(self.base_url)
        button = self.driver.find_element(by="name", value="email")
        button.send_keys("john@simplylift.co")
        signup = self.driver.find_element(by="name", value="submit")
        signup.click()
        book = self.driver.find_element(by="xpath", value="//ul/li/a")
        book.click()
        assert (
            self.driver.current_url
            == f"{self.base_url}book/Spring%20Festival/Simply%20Lift"
        )

    def test_purchase_place_valid(self):
        self.driver.get(f"{self.base_url}book/Spring%20Festival/Simply%20Lift")
        button = self.driver.find_element(by="name", value="places")
        button.send_keys("1")
        submit = self.driver.find_element(by="name", value="submit")
        submit.click()
        assert self.driver.current_url == f"{self.base_url}purchasePlaces"

    def test_purchase_place_invalid_club_points(self):
        self.driver.get(f"{self.base_url}book/Spring%20Festival/Simply%20Lift")
        button = self.driver.find_element(by="name", value="places")
        button.send_keys("8")
        submit = self.driver.find_element(by="name", value="submit")
        submit.click()
        assert (
            self.driver.find_element(by="name", value="message").text
            == "Your club don't have enought points"
        )
        assert self.driver.current_url == f"{self.base_url}purchasePlaces"

    def test_purchase_place_invalid_max_places(self):
        self.driver.get(f"{self.base_url}book/Spring%20Festival/Simply%20Lift")
        button = self.driver.find_element(by="name", value="places")
        button.send_keys("14")
        submit = self.driver.find_element(by="name", value="submit")
        submit.click()
        assert (
            self.driver.find_element(by="name", value="message").text
            == "You can't book more than 12 places per competition"
        )
        assert self.driver.current_url == f"{self.base_url}purchasePlaces"

    def test_purchase_place_invalid_competition_places(self):
        self.driver.get(f"{self.base_url}book/Test/Simply%20Lift")
        button = self.driver.find_element(by="name", value="places")
        button.send_keys("9")
        submit = self.driver.find_element(by="name", value="submit")
        submit.click()
        assert (
            self.driver.find_element(by="name", value="message").text
            == "There is not enought place in this competition"
        )
        assert self.driver.current_url == f"{self.base_url}purchasePlaces"
