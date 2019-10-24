"""
装饰者模式:
    动态的将责任附加到对象上，不采用继承进行拓展
原则：
    5.对拓展开放，对修改关闭（开闭原则）
优点：
    1.不同于继承的另一种方式来拓展
    2.对调用者是透明的
缺点：
    1.出产生很多装饰者小类, 只是相互连接方式不同，而不是属性，数量多了也会增加复杂度
    2.针对具体类的类型编程会有问题
课题：
    对为茶饮添加各种配料(套娃)
    beverage 饮料 grass jelly 仙草冻 2.00 coffee jelly 咖啡冻 3.00 coconut jelly 椰果 3.50 pudding 布丁 3.00
"""

from src.utils import start_end


class StartBeverage(object):
    description = 'unknown'

    def cost(self):
        raise NotImplementedError

    def get_description(self):
        return self.description


class StartBubbleTeaWithGrass(StartBeverage):
    """珍珠奶茶加仙草冻"""
    description = 'bubble tea, grass'

    def cost(self):
        return 15.00 + 2.00


class StartBubbleTeaWithCoffee(StartBeverage):
    """珍珠奶茶加咖啡冻"""
    description = 'bubble tea, coffee'

    def cost(self):
        return 15.00 + 3.00


class StartBubbleTeaWithCoconut(StartBeverage):
    """珍珠奶茶加咖啡冻"""
    description = 'bubble tea, coconut'

    def cost(self):
        return 15.00 + 3.50


class StartBubbleTeaWithPudding(StartBeverage):
    """珍珠奶茶加布丁"""
    description = 'bubble tea, pudding'

    def cost(self):
        return 15.00 + 3.50


class StartFruitTeaWithGrass(StartBeverage):
    """果茶加仙草冻"""
    description = 'fruit tea, grass'

    def cost(self):
        return 10.00 + 2.00


class StartFruitTeaWithCoffee(StartBeverage):
    """果茶加咖啡冻"""
    description = 'fruit tea, coffee'

    def cost(self):
        return 10.00 + 3.00


class StartFruitTeaWithCoconut(StartBeverage):
    """果茶加椰果"""
    description = 'fruit tea, coconut'

    def cost(self):
        return 10.00 + 3.50


class StartFruitTeaWithPudding(StartBeverage):
    """果茶加布丁"""
    description = 'fruit tea, pudding'

    def cost(self):
        return 10.00 + 3.50


# 类真多
# 怎么减少呢?
# 解决1，将Beverage类添加调料设置和取得的方法
class MidBeverage(object):
    description = 'unknown'
    base_cost = 0

    def __init__(self):
        self.grass = None
        self.coffee = None
        self.coconut = None
        self.pudding = None

    def has_grass(self):
        return True if self.grass else False

    def set_grass(self):
        self.grass = True

    def has_coffee(self):
        return True if self.coffee else False

    def set_coffee(self):
        self.coffee = True

    def has_coconut(self):
        return True if self.coconut else False

    def set_coconut(self):
        self.coconut = True

    def has_pudding(self):
        return True if self.pudding else False

    def set_pudding(self):
        self.pudding = True

    def cost(self):
        total_cost = self.base_cost
        if self.has_grass():
            total_cost += 2.00
        if self.has_coffee():
            total_cost += 3.00
        if self.has_coconut():
            total_cost += 3.50
        if self.has_pudding():
            total_cost += 3.00
        return total_cost

    def get_description(self):
        description = self.description
        if self.has_grass():
            description = description + ', grass'
        if self.has_coffee():
            description = description + ', coffee'
        if self.has_coconut():
            description = description + ', coconut'
        if self.has_pudding():
            description = description + ', pudding'
        return description


class MidBubbleTea(MidBeverage):
    description = 'bubble tea'
    base_cost = 15.00


# 怎么这么多条件判断，而且我要双份椰果怎么办?
# 解决2，使用装饰者模式

class BubbleTea(StartBeverage):
    description = 'bubble tea'

    def cost(self):
        return 15.00


class FruitTea(StartBeverage):
    description = 'bubble tea'

    def cost(self):
        return 15.00


class CondimentDecorator(StartBeverage):
    def get_description(self):
        """需要重写这个方法"""
        raise NotImplementedError

    # ide会提示要实现这个方法，但是这个类也是抽象类
    # def cost(self):
    #     raise NotImplementedError


class Grass(CondimentDecorator):

    def __init__(self, beverage):
        self.beverage = beverage

    def get_description(self):
        return self.beverage.get_description() + ', grass'

    def cost(self):
        return self.beverage.cost() + 2.00


class Coffee(CondimentDecorator):

    def __init__(self, beverage):
        self.beverage = beverage

    def get_description(self):
        return self.beverage.get_description() + ', coffee'

    def cost(self):
        return self.beverage.cost() + 3.00


class Coconut(CondimentDecorator):

    def __init__(self, beverage):
        self.beverage = beverage

    def get_description(self):
        return self.beverage.get_description() + ', coconut'

    def cost(self):
        return self.beverage.cost() + 3.50


class Pudding(CondimentDecorator):

    def __init__(self, beverage):
        self.beverage = beverage

    def get_description(self):
        return self.beverage.get_description() + ', pudding'

    def cost(self):
        return self.beverage.cost() + 3.00


@start_end
def mid_main():
    beverage = MidBubbleTea()
    beverage.set_grass()
    beverage.set_coconut()
    print('%s ￥%s' % (beverage.get_description(), beverage.cost()))


@start_end
def end_main():
    # 双份椰果加仙草的珍珠奶茶
    beverage = BubbleTea()
    print('%s ￥%s' % (beverage.get_description(), beverage.cost()))
    beverage = Grass(beverage)
    beverage = Coconut(beverage)
    beverage = Coconut(beverage)
    print('%s ￥%s' % (beverage.get_description(), beverage.cost()))


if __name__ == '__main__':
    mid_main()
    end_main()
