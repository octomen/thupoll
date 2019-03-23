def generate_invite_link(host, token):
    """
    Simple generate link.
    :param host: link to thupoll host
    :param token: user token
    :return:
    """
    return "{host}/login?token={token}".format(
        host=host,
        token=token
    )
