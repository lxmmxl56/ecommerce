import logging
import uuid

import requests

from acceptance_tests.api import EnrollmentApiClient
from acceptance_tests.config import (ENABLE_AUTO_AUTH, APP_SERVER_URL, LMS_PASSWORD, LMS_EMAIL, LMS_URL,
                                     BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, ECOMMERCE_API_SERVER_URL,
                                     ECOMMERCE_API_SIGNING_KEY)
from acceptance_tests.pages import LMSLoginPage
from ecommerce_api_client.client import EcommerceApiClient


log = logging.getLogger(__name__)


class LoginMixin(object):
    def setUp(self):
        super(LoginMixin, self).setUp()
        self.lms_login_page = LMSLoginPage(self.browser)

    def login(self):
        if ENABLE_AUTO_AUTH:
            self.login_with_auto_auth()
        else:
            self.login_with_lms()

    def login_with_auto_auth(self):
        url = '{}/test/auto_auth/'.format(APP_SERVER_URL)
        self.browser.get(url)

    def login_with_lms(self, email=None, password=None, course_id=None):
        """ Visit LMS and login. """
        email = email or LMS_EMAIL
        password = password or LMS_PASSWORD

        # Note: We use Selenium directly here (as opposed to Bok Choy) to avoid issues with promises being broken.
        self.lms_login_page.browser.get(self.lms_login_page.url(course_id))  # pylint: disable=not-callable
        self.lms_login_page.login(email, password)


class LogoutMixin(object):
    def logout(self):
        url = '{}/accounts/logout/'.format(APP_SERVER_URL)
        self.browser.get(url)


class LmsUserMixin(object):
    password = 'edx'

    def create_lms_user(self, username=None, password=None, email=None):
        username = username or ('auto_auth_' + uuid.uuid4().hex[0:20])
        password = password or 'edx'
        email = email or '{}@example.com'.format(username)

        url = '{host}/auto_auth?no_login=true&username={username}&password={password}&email={email}'.format(
            host=LMS_URL, username=username, password=password, email=email)
        auth = None

        if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
            auth = (BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD)

        requests.get(url, auth=auth)

        return username, password, email


class EnrollmentApiMixin(object):
    def setUp(self):
        super(EnrollmentApiMixin, self).setUp()
        self.enrollment_api_client = EnrollmentApiClient()

    def assert_user_enrolled(self, username, course_id, mode='honor'):
        status = self.enrollment_api_client.get_enrollment_status(username, course_id)
        self.assertDictContainsSubset({'is_active': True, 'mode': mode}, status)


class EcommerceApiMixin(object):
    @property
    def ecommerce_api_client(self):
        return EcommerceApiClient(ECOMMERCE_API_SERVER_URL, ECOMMERCE_API_SIGNING_KEY, self.username, self.email)

    def assert_order_created_and_completed(self):
        orders = self.ecommerce_api_client.get_orders()
        self.assertGreater(len(orders), 0, 'No orders found for the user!')

        # TODO Validate this is the correct order.
        order = orders[0]

        self.assertEqual(order['status'], 'Complete')
