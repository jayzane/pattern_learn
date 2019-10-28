"""
单例模式：
    一个类只有一个对象，并提供全局访问点
优点：
    1.提高性能
    2.严格控制客户怎样访问类实例
缺点：
    1.扩展困难
    2.违背单一职责，既充当工厂角色，又充当产品角色
python的几种实现方式:
    1.1 工厂方法
    1.2 工厂方法，加锁
    1.3 工厂方法，加锁, 优化
    2.使用模块, 线程安全的
    3.装饰器，也有线程问题
    4.使用__new__, 也有线程问题 
    5.metaclass, 也有线程问题 
"""
import threading
import time
from src.utils import start_end


class BaseSingleton(object):
    """
    工厂方法
    """
    instance = None

    def __init__(self):
        # 加入io体验多线程的问题
        time.sleep(0.1)

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance


def base_task():
    obj = BaseSingleton.get_instance()
    print(obj)


# 多线程是否有问题？

class BaseLockSingleton(object):
    instance = None
    instance_lock = threading.Lock()

    def __init__(self):
        # 加入io体验多线程的问题
        time.sleep(0.1)

    @classmethod
    def get_instance(cls):
        with cls.instance_lock:
            if not cls.instance:
                cls.instance = cls()
        return cls.instance


def base_lock_task():
    obj = BaseLockSingleton.get_instance()
    print(obj)


# 每次get_instance都有加锁，有性能问题，如何解决？
class BaseLockOptSingleton(object):
    instance = None
    instance_lock = threading.Lock()

    def __init__(self):
        # 加入io体验多线程的问题
        time.sleep(0.1)

    @classmethod
    def get_instance(cls):
        """如果有了，直接返回，没有才加锁获取，并且在锁中再判断一次"""
        if not cls.instance:
            with cls.instance_lock:
                if not cls.instance:
                    cls.instance = cls()
        return cls.instance


def base_lock_opt_task():
    obj = BaseLockOptSingleton.get_instance()
    print(obj)


class ModuleSingleton(object):
    """模块"""

    def __init__(self):
        time.sleep(0.1)


module_singleton = ModuleSingleton()


def singleton_decorator(cls):
    """装饰器"""
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


@singleton_decorator
class DecoratorSingleton(object):
    def __init__(self):
        time.sleep(0.1)


def decorator_task():
    obj = DecoratorSingleton()
    print(obj)


class NewSingleton(object):
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = object.__new__(cls)
        return cls.instance


class SingletonMetaclass(type):
    def __call__(cls, *args, **kwargs):  # 这里的cls为楼下的MetaclassSingleton
        print('cls is %s' % cls)
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonMetaclass, cls).__call__(*args, **kwargs)
        return cls.instance


class MetaclassSingleton(metaclass=SingletonMetaclass):
    pass


@start_end
def base_main():
    for i in range(10):
        t = threading.Thread(target=base_task)
        t.start()


@start_end
def base_lock_main():
    for i in range(10):
        t = threading.Thread(target=base_lock_task)
        t.start()


@start_end
def base_lock_opt_main():
    for i in range(10):
        t = threading.Thread(target=base_lock_opt_task)
        t.start()


@start_end
def new_main():
    singleton_1 = NewSingleton()
    singleton_2 = NewSingleton()
    print(singleton_1)
    print(singleton_2)


@start_end
def decorator_main():
    # singleton_1 = DecoratorSingleton()
    # singleton_2 = DecoratorSingleton()
    # print(singleton_1)
    # print(singleton_2)
    for i in range(10):
        t = threading.Thread(target=decorator_task)
        t.start()


@start_end
def metaclass_main():
    singleton_1 = MetaclassSingleton()
    singleton_2 = MetaclassSingleton()
    print(singleton_1)
    print(singleton_2)


if __name__ == '__main__':
    base_main()
    base_lock_main()
    base_lock_opt_main()
    decorator_main()
    new_main()
    metaclass_main()
