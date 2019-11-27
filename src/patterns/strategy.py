"""
策略模式:
    定义一算法族，算法可以相互替换，算法的改变不影响调用的客户
原则:
    1.将变化和不变化部分独立开来，封装变化（开闭原则）
    2.针对接口而不是实现编程，接口就是超类，超类包括接口和抽象类，会用到多态特性
    3.多用组合少用继承
优点：
    1.封装了变化，变化不影响原有系统
    2.管理算法族，避免多重条件转移语句
缺点：
    1.可能会产生很多策略类
    2.客户需要了解所有策略，并自行决定选择哪一个
课题：
    对鸭子的行为进行拓展
"""
import abc


class StartDuck(object):
    display_name = 'normal'

    def quack(self):
        """鸭子叫"""
        print('ga ga ga...')

    # 解决1,添加的方法
    def fly(self):
        """飞"""
        print('flying by wings.')

    def display(self):
        print('I am a %s duck.' % self.display_name)


class StartGreenHeadDuck(StartDuck):
    display_name = 'green-head'


class StartRedHeadDuck(StartDuck):
    display_name = 'red-head'


class StartRubberDuck(StartDuck):
    """橡胶鸭，可以发出声响，但是不能飞"""
    display_name = 'rubber'


# 问题1,现在需要添加多种飞行行为，鸭叫行为
# 解决1,在StartDuck中添加fly方法
# 会发现，所有鸭子都会飞了，橡胶鸭也能飞了!
# 解决2,将fly变成接口
# 代码无法复用，需在很多鸭子里写重复飞行代码

class FlyMixin(abc.ABC):
    @abc.abstractmethod
    def fly(self):
        pass


class MidDuck(object):
    display_name = 'normal'

    def quack(self):
        """鸭子叫"""
        print('ga ga ga...')

    def display(self):
        print('I am a %s duck.' % self.display_name)


class MidGreenHeadDuck(MidDuck, FlyMixin):
    display_name = 'green-head'

    def fly(self):
        print('flying by wings.')


class MidRedHeadDuck(MidDuck, FlyMixin):
    display_name = 'red-head'

    def fly(self):
        print('flying by wings.')


class MidRubberDuck(MidDuck):
    display_name = 'rubber'

    def fly(self):
        print('cannot fly')


# 解决3，封装变化，将鸭子的飞行和叫的行为分开，并且针对接口编程
# 问题2，如何动态的添加行为
# 解决4，为Duck添加setter方法，其实python可以对属性进行再赋值
class EndDuck(object):
    display_name = 'normal'

    def __init__(self):
        self.quack_behavior = None
        self.fly_behavior = None

    def display(self):
        print('I am a %s duck.' % self.display_name)

    def perform_fly(self):
        self.fly_behavior.fly()

    def set_quack_behavior(self, quack_behavior):
        self.quack_behavior = quack_behavior

    def set_fly_behavior(self, fly_behavior):
        self.fly_behavior = fly_behavior


class QuackMixin(abc.ABC):
    @abc.abstractmethod
    def quark(self):
        pass


class FlyMixin(abc.ABC):
    @abc.abstractmethod
    def fly(self):
        pass


class QuackGaGa(QuackMixin):
    def quark(self):
        print('ga ga ga...')


class QuackGuaGua(QuackMixin):
    def quark(self):
        print('gua gua gua...')


class FlyWithWings(FlyMixin):
    def fly(self):
        print('flying with wings.')


class FlyWithRocket(FlyMixin):
    def fly(self):
        print('flying with Rocket.')


class FlyNoWay(FlyMixin):
    def fly(self):
        print('flying no ways.')


class EndGreenHeadDuck(EndDuck):
    display_name = 'green-head'

    def __init__(self):
        # TODO(jayzane): 不使用具体实现
        super().__init__()
        self.quack_behavior = QuackGaGa()
        self.fly_behavior = FlyWithWings()


class EndRedHeadDuck(EndDuck):
    display_name = 'red-head'

    def __init__(self):
        super().__init__()
        self.quack_behavior = QuackGaGa()
        self.fly_behavior = FlyWithWings()


class EndRubberDuck(EndDuck):
    display_name = 'rubber'

    def __init__(self):
        super().__init__()
        self.quack_behavior = QuackGuaGua()
        self.fly_behavior = FlyNoWay()


if __name__ == '__main__':
    green_duck = EndGreenHeadDuck()
    red_duck = EndRedHeadDuck()
    rubber_duck = EndRubberDuck()

    green_duck.perform_fly()
    red_duck.perform_fly()
    rubber_duck.perform_fly()

    fly_rocket = FlyWithRocket()
    green_duck.set_fly_behavior(fly_rocket)
    green_duck.perform_fly()
