import requests
from BeautifulSoup import BeautifulSoup
import getpass

class CsdnHandler():
    """Csdn operator"""
    def __init__(self):
        self.sess = requests.Session()

    def login(self):
        username = raw_input('username: ')
        password = getpass.getpass('password: ')
        url = 'https://passport.csdn.net/account/login'
        html = self.sess.get(url).text
        soup = BeautifulSoup(html)

        lt = self.get_element_value(soup, 'name', 'lt')
        execution = self.get_element_value(soup, 'name', 'execution')
        _eventId = self.get_element_value(soup, 'name', '_eventId')

        data = {
                'username' : username,
                'password' : password,
                'lt' : lt,
                'execution' : execution,
                '_eventId' : _eventId
                }

        response = self.sess.post(url, data)

        return self.is_login_success(response)

    @staticmethod
    def get_element_value(soup, element_name, element_value):
        element = soup.find(attrs={element_name : element_value})
        if element is None:
            return None
        return element.get('value', None)

    @staticmethod
    def is_login_success(response):
        if response.status_code != 200:
            return False
        return -1 != response.content.find('lastLoginIP')
