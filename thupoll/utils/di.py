from thupoll.utils import _sentinel


class BaseProvider:
    def __init__(self, provider, **kw):
        self._override = []
        self._provider = provider
        self._kw = kw

    def __call__(self, **kwargs):
        if self._override:
            return self._override[-1](**kwargs)
        return self._run(**kwargs)

    def _run(self, **kwargs):
        raise NotImplementedError

    def override(self, provider: "BaseProvider"):
        self._override.append(provider)

    def reset(self):
        if self._override:
            self._override.pop()

    def update_kw(self, kwargs):
        kw = dict(self._kw)
        kw.update(kwargs)
        return kw


def prepare_providers(kwargs):
    return {k: v() if isinstance(v, BaseProvider) else v
            for k, v in kwargs.items()}


class Factory(BaseProvider):
    def _run(self, **kwargs):
        return self._provider(
            **prepare_providers(self.update_kw(kwargs)))


class Singleton(BaseProvider):
    def __init__(self, provider, **kw):
        super().__init__(provider, **kw)
        self._instance = _sentinel

    def _run(self, **kwargs):
        if self._instance == _sentinel:
            self._instance = self._provider(
                **prepare_providers(self.update_kw(kwargs)))
        return self._instance


class Container:
    @classmethod
    def override(cls, other):
        for k, v in other.__dict__.items():
            if isinstance(v, BaseProvider):
                getattr(cls, k).override(v)
        return other

    @classmethod
    def reset(cls):
        for k, v in cls.__dict__.items():
            if isinstance(v, BaseProvider):
                v.reset()
