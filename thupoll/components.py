import dependency_injector.containers as containers
import dependency_injector.providers as providers

from thupoll.telega.components import Components as TComponents


class Components(containers.DeclarativeContainer):
    telegram_bot = providers.Factory(TComponents.telegram_bot)
    telegram_hook = providers.Factory(TComponents.telegram_hook)
