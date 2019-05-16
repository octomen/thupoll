def generate_invite_link(host, token):
    """
    Simple generate link.
    :param host: link to thupoll host
    :param token: user token
    :return:
    """
    # TODO remove hard-code-link
    return "http://thupoll.liinda.ru?token={token}".format(
        host=host,
        token=token
    )
