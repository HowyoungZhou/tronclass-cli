import requests
import rsa
from bs4 import BeautifulSoup

from tronclass_cli.api.auth import AuthProvider, AuthError

PUB_KEY_URL = 'https://zjuam.zju.edu.cn/cas/v2/getPubKey'
LOGIN_URL = 'https://zjuam.zju.edu.cn/cas/login'


def rsa_encrypt(message, pub_key):
    key_length = rsa.common.byte_size(pub_key.n)
    payload = rsa.transform.bytes2int(message)
    cypher = rsa.core.encrypt_int(payload, pub_key.e, pub_key.n)
    return rsa.transform.int2bytes(cypher, key_length)


class ZjuamAuthProvider(AuthProvider):
    desc = 'ZJU Unified Identity Authentication'

    def __init__(self, session):
        super().__init__()
        self.session = session

    def get_pub_key(self):
        pub = self.session.get(PUB_KEY_URL).json()
        n = int(pub['modulus'], base=16)
        e = int(pub['exponent'], base=16)
        return rsa.PublicKey(n, e)

    def login(self, username: str, password: str):
        res = self.session.get(LOGIN_URL).text
        soup = BeautifulSoup(res, 'lxml')
        execution = soup.findAll('input', attrs={'name': 'execution'})[0]['value']

        pub_key = self.get_pub_key()
        encrypted_pass = rsa_encrypt(password.encode(), pub_key).hex()

        form = {
            'username': username,
            'password': encrypted_pass,
            'authcode': '',
            'execution': execution,
            '_eventId': 'submit'
        }
        self.session.post(LOGIN_URL, data=form)
        cookies = self.session.cookies
        if '_pc0' not in cookies:
            raise AuthError()
        return self.session
