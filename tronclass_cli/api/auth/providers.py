from tronclass_cli.api.auth.zjuam import ZjuamAuthProvider

_auth_providers = {'zju': ZjuamAuthProvider}


def get_auth_provider(name):
    return _auth_providers[name]
