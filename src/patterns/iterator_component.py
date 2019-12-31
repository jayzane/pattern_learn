"""
迭代器与组合模式
迭代器：
    提供一种办法遍历所有元素，而不需知道它们的组织方式
组合：
    树状结构的组织方式，元素又可以是组合
原则:
    9.单一职责原则：一个类应该只有一个引起它变化的原因
"""
from src.utils import start_end


class Array(object):

    def __init__(self):
        self.array = []
        self.val = None

    def add(self, val):
        self.array.append(val)

    def print(self):
        print('item is %s' % self.val)


class FirstIteratorMixin(object):
    def has_next(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError


class FirstMenu(Array, FirstIteratorMixin):

    def has_next(self):
        try:
            self.val = self.array.pop()
        except IndexError:
            return False
        else:
            return True

    def next(self):
        return self.val


class PyMenu(Array):
    """python style"""

    def __next__(self):
        try:
            self.val = self.array.pop()
        except IndexError:
            raise StopIteration
        else:
            return self

    def __iter__(self):
        return self

    def add(self, val):
        self.array.append(val)


class ComponentMixin(object):
    """接口方式而不用抽象类是因为没有需要继承的行为"""

    def print(self):
        raise NotImplementedError

    def get_child(self, i):
        raise NotImplementedError


class MenuItem(ComponentMixin):
    def __init__(self, val):
        self.val = val

    def print(self):
        print('item is %s' % self.val)


class ComponentMenu(Array, ComponentMixin):
    def print(self):
        for node in self.array:
            node.print()

    def get_child(self, i):
        return self.array[i]

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.val = self.array.pop()
        except IndexError:
            raise StopIteration
        else:
            return self.val


@start_end
def first_main():
    menu = FirstMenu()
    menu.add('c')
    menu.add('b')
    menu.add('a')
    while menu.has_next():
        menu.print()


@start_end
def py_main():
    menu = PyMenu()
    menu.add('c')
    menu.add('b')
    menu.add('a')
    for m in menu:
        m.print()


@start_end
def main():
    menu = ComponentMenu()
    for l in ['a', 'b', 'c']:
        item = MenuItem(l)
        menu.add(item)
    menu_child = ComponentMenu()
    for l in ['a1', 'b1', 'c1']:
        item = MenuItem(l)
        menu_child.add(item)
    menu.add(menu_child)
    for m in menu:
        m.print()


if __name__ == '__main__':
    first_main()
    py_main()
    main()
