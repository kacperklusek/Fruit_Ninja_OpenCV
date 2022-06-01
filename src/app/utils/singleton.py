from threading import Lock


# TODO - remove link below
# Link to the implementation explanation:
# https://refactoring.guru/pl/design-patterns/singleton/python/example#example-1


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()  # Make it thread-safe

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
