"""
适配器模式：
    将一个接口转化为另一个接口，以符合客户的期望。
外观模式：
    为一个子系统的一群接口提供一个简化的统一接口
适配器模式和外观模式的区别：
    两者意图不同，适配器就是为了转化接口，而外观是为了简化接口
适配器模式和装饰者模式的区别：
    装饰者会提供自己的新的行为
原则：
    7.最少知识（Law of Demeter）,只和你密友谈话
    几个调用对象方法的指导方针:
        1.自身
        2.作为参数的对象
        3.方法内实例化的对象
        4.对象的属性对象
    反例：station = Station();station.get_thermometer().get_temperature()
        调用了方法实例化对象的方法生成的对象
课题：
    用鸭子接口使用火鸡类；使用一套音响系统
"""
from src.utils import start_end


class Duck(object):

    def quack(self):
        raise NotImplementedError

    def fly(self):
        raise NotImplementedError


class Turkey(object):
    def gobble(self):
        raise NotImplementedError

    def fly(self):
        raise NotImplementedError


class RedHeadTurkey(Turkey):
    def gobble(self):
        print('red head turkey gobble...')

    def fly(self):
        print('red head fly...')


# 客户只会使用鸭子接口，但是又想用火鸡类
class TurkeyAdapter(object):
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def quack(self):
        self.adaptee.gobble()

    def fly(self):
        """5次火鸡飞行才当1次鸭子飞"""
        for i in range(5):
            self.adaptee.fly()


# Adapter可以适配多个类吗？
class MultiAdapter(object):
    def __init__(self, adaptee_one, adaptee_two):
        self.adaptee_one = adaptee_one
        self.adaptee_two = adaptee_two

    def action_one(self):
        self.adaptee_one.action_one_a()
        self.adaptee_two.action_one_b()


# 有较多的类组成的系统
# 比如一套音响视听系统，有cd机、投影仪、屏幕、功放甚至还有爆米花机
# 启动它，需要打开投影仪，打开屏幕，打开cd机，放入cd碟片，打开功放，设置音量，最后再做爆米花，安心挺音乐吧！
# 如何简单调用它？
class CDPlayer(object):
    def on(self):
        print('cd player on...')

    def off(self):
        print('cd player off...')

    def set_cd(self, cd):
        print('cd player set cd to %s...' % cd)


class Projector(object):
    def on(self):
        print('projector on...')

    def off(self):
        print('projector off...')


class Screen(object):
    def on(self):
        print('screen on...')

    def off(self):
        print('screen off...')


class Amplifier(object):
    def on(self):
        print('amplifier on...')

    def off(self):
        print('amplifier off...')

    def set_volume(self, volume):
        print('amplifier set volume %s...' % volume)


class PopcornPopper(object):
    def on(self):
        print('popcorn popper on...')

    def off(self):
        print('popcorn popper off...')


# 使用外观模式
class Facade(object):
    def __init__(self, projector, screen, cd_player, amplifier, popcorn):
        self.projector = projector
        self.screen = screen
        self.cd_player = cd_player
        self.amplifier = amplifier
        self.popcorn = popcorn

    def start(self):
        self.projector.on()
        self.screen.on()
        self.cd_player.on()
        self.cd_player.set_cd('CD1')
        self.amplifier.on()
        self.amplifier.set_volume(10)
        self.popcorn.on()
        print('enjoy it..')


# 如果使用命令模式会怎样？
# 使用命令组，会产生非常多的命令类。命令模式有统一的接口，例如execute()，但是外观模式没有，仅做简化命令。

@start_end
def duck_main():
    """客户调用"""
    turkey = RedHeadTurkey()
    adapter = TurkeyAdapter(turkey)
    adapter.quack()
    adapter.fly()


@start_end
def facade_main():
    projector = Projector()
    screen = Screen()
    cd_player = CDPlayer()
    amplifier = Amplifier()
    popcorn = PopcornPopper()
    facade = Facade(projector, screen, cd_player, amplifier, popcorn)
    facade.start()


if __name__ == '__main__':
    duck_main()
    facade_main()
