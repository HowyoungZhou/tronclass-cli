import requests
import rsa
from bs4 import BeautifulSoup

PUB_KEY_URL = 'https://zjuam.zju.edu.cn/cas/v2/getPubKey'
LOGIN_URL = 'https://zjuam.zju.edu.cn/cas/login'


def get_pub_key(session):
    pub = session.get(PUB_KEY_URL).json()
    n = int(pub['modulus'], base=16)
    e = int(pub['exponent'], base=16)
    return rsa.PublicKey(n, e)


def rsa_encrypt(message, pub_key):
    key_length = rsa.common.byte_size(pub_key.n)
    payload = rsa.transform.bytes2int(message)
    cypher = rsa.core.encrypt_int(payload, pub_key.e, pub_key.n)
    return rsa.transform.int2bytes(cypher, key_length)


def login(user_id: str, password: str):
    session = requests.session()
    res = session.get(LOGIN_URL).text
    soup = BeautifulSoup(res, 'lxml')
    execution = soup.findAll('input', attrs={'name': 'execution'})[0]['value']

    pub_key = get_pub_key(session)
    encrypted_pass = rsa_encrypt(password.encode(), pub_key).hex()

    form = {
        'username': user_id,
        'password': encrypted_pass,
        'authcode': '',
        'execution': execution,
        '_eventId': 'submit'
    }
    session.post(LOGIN_URL, data=form)
    cookies = session.cookies
    if '_pc0' not in cookies:
        raise Exception('failed to login')
    return cookies
