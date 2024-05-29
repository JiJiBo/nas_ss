BLACKLIST = set()


def add_token_to_blacklist(token: str):
    BLACKLIST.add(token)


def is_token_in_blacklist(token: str):
    return token in BLACKLIST