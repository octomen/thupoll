from thupoll.telega import components as t_cmp
from thupoll.utils import di


class Components:
    telegram_bot = di.Factory(t_cmp.Components.telegram_bot)
    telegram_hook = di.Factory(t_cmp.Components.telegram_hook)
