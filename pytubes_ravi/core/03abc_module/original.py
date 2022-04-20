import abc


class CacheBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def set(self, key, val):
        pass


class RedisCache(CacheBase):
    def __init__(self):
        self.cache = {}

    def set(self, key, val):
        self.cache[key] = val


if __name__ == '__main__':
    redis = RedisCache()
