from thupoll.telega import components as t_cmp
from thupoll.utils import Factory


class Components:
    telegram_bot = Factory(t_cmp.Components.telegram_bot)
    telegram_hook = Factory(t_cmp.Components.telegram_hook)
