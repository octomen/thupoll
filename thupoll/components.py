import dependency_injector.containers as containers
import dependency_injector.providers as providers

from thupoll.telegram import factories


class Components(containers.DeclarativeContainer):
    telegram_bot = providers.Singleton(factories.telegram_bot_factory)
    telegram_hook = providers.Singleton(
        factories.telegram_hook_factory, bot=telegram_bot)
