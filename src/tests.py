import threading


def module_singleton_task():
    from src.patterns.singleton import module_singleton
    obj = module_singleton
    print(obj)


def test_module_singleton():
    for i in range(10):
        t = threading.Thread(target=module_singleton_task)
        t.start()


if __name__ == '__main__':
    test_module_singleton()
