"""
简单工厂(非模式):
    根据参数返回不同的实例
工厂方法模式:
    定义创建对象接口，子类决定如何实例化
抽象工厂模式：
    定义创建产品族的接口，每个产品创建会用到工厂方法模式
原则：
    6.依赖倒置, 依赖抽象而不是具体类，不能让高层组件依赖低层组件，高层是由低层定义其行为的类
课题：
    开宜宾燃面的加盟店
    流程：备: prepare，煮: boil，添: add，装: plate,
    配料: 水面:noodles，芽菜: sprout，香料: spice，辣椒: pepper，蔬菜: vegetables 肉：meat
    燃面种类：素燃(veges ranmian noodles)，荤燃(meat ranmian noodles)
"""
from src.utils import start_end


class StartNoodles(object):
    def prepare(self):
        print('preparing...')

    def boil(self):
        print('boiling...')

    def add(self):
        print('adding...')

    def plate(self):
        print('plating...')


class StartVegesRanmianNoodles(StartNoodles):
    pass


class StartMeatRanmianNoodles(StartNoodles):
    pass


class StartStore(object):
    def order(self, type_str):
        noodles = None
        if type_str == 'veges':
            noodles = StartVegesRanmianNoodles()
        elif type_str == 'meat':
            noodles = StartMeatRanmianNoodles()
        noodles.prepare()
        noodles.boil()
        noodles.add()
        noodles.plate()


# 使用简单工厂
class SimpleNoodlesFactory(object):
    def create(self, type_str):
        noodles = None
        if type_str == 'veges':
            noodles = StartVegesRanmianNoodles()
        elif type_str == 'meat':
            noodles = StartMeatRanmianNoodles()
        return noodles


class SimpleFactoryStore(object):
    def __init__(self, factory):
        self.factory = factory

    def order(self, type_str):
        print('prepare from %s' % self.factory)
        noodles = self.factory.create(type_str)
        noodles.prepare()
        noodles.boil()
        noodles.add()
        noodles.plate()


# 如果开了宜宾，成都两家店，会怎么做?
class YibinStyleVegesRanmianNoodles(StartNoodles):
    pass


class YibinStyleMeatRanmianNoodles(StartNoodles):
    pass


class ChenduStyleVegesRanmianNoodles(StartNoodles):
    pass


class ChenduStyleMeatRanmianNoodles(StartNoodles):
    pass


class YibinNoodlesFactory(object):
    def create(self, type_str):
        noodles = None
        if type_str == 'veges':
            noodles = YibinStyleVegesRanmianNoodles()
        elif type_str == 'meat':
            noodles = YibinStyleMeatRanmianNoodles()
        return noodles

    def __str__(self):
        return 'Yibin Factory'


class ChenduNoodlesFactory(object):
    def create(self, type_str):
        noodles = None
        if type_str == 'veges':
            noodles = ChenduStyleVegesRanmianNoodles()
        elif type_str == 'meat':
            noodles = ChenduStyleMeatRanmianNoodles()
        return noodles

    def __str__(self):
        return 'Chendu Factory'


# 如果加盟店想有自己的流程呢？比如有的煮的硬一点，有的煮得软一点。将加盟店和创建燃面捆绑起来同时又保持弹性。
# 这就需要将create放回store，但是将create抽象

class FactoryMethodStore(object):

    def order(self, type_str):
        """这里还是各个店采用了统一的流程实现"""
        noodles = self.create(type_str)
        noodles.prepare()
        noodles.boil()
        noodles.add()
        noodles.plate()

    def create(self, type_str):
        raise NotImplementedError


class MidYibinStore(FactoryMethodStore):
    def create(self, type_str):
        noodles = None
        if type_str == 'veges':
            noodles = YibinStyleVegesRanmianNoodles()
        elif type_str == 'meat':
            noodles = YibinStyleMeatRanmianNoodles()
        return noodles


class MidChenduStore(FactoryMethodStore):
    def create(self, type_str):
        noodles = None
        if type_str == 'veges':
            noodles = ChenduStyleVegesRanmianNoodles()
        elif type_str == 'meat':
            noodles = ChenduStyleMeatRanmianNoodles()
        return noodles


# 现在各个店同一种原料，有不同差异，比如宜宾的辣椒比成都辣椒辣，现在需要控制原料
# 配料: 水面:noodles，芽菜: sprout，香料: spice，辣椒: pepper，蔬菜: vegetables 肉：meat
class IngredientFactory(object):
    def create_noodles(self):
        raise NotImplementedError

    def create_sprout(self):
        raise NotImplementedError

    def create_spice(self):
        raise NotImplementedError

    def create_pepper(self):
        raise NotImplementedError

    def create_vegetables(self):
        raise NotImplementedError

    def create_meat(self):
        raise NotImplementedError


class YibinIngredientFactory(IngredientFactory):
    def create_noodles(self):
        return 'Yibin noodles'

    def create_sprout(self):
        return 'Yibin sprout'

    def create_spice(self):
        return 'Yibin spice'

    def create_pepper(self):
        return 'Yibin pepper'

    def create_vegetables(self):
        return 'Yibin vegetables'

    def create_meat(self):
        return 'Yibin meat'


class ChenduIngredientFactory(IngredientFactory):
    def create_noodles(self):
        return 'Chendu noodles'

    def create_sprout(self):
        return 'Chendu sprout'

    def create_spice(self):
        return 'Chendu spice'

    def create_pepper(self):
        return 'Chendu pepper'

    def create_vegetables(self):
        return 'Chendu vegetables'

    def create_meat(self):
        return 'Chendu meat'


class Noodles(object):
    noodles = None
    sprout = None
    spice = None
    pepper = None
    vegetables = None
    meat = None

    def prepare(self):
        raise NotImplementedError

    def boil(self):
        print('boiling...')

    def add(self):
        print('adding...')

    def plate(self):
        print('plating...')


class VegesRanmianNoodles(Noodles):
    def __init__(self, factory):
        # 原料工厂
        self.factory = factory

    def prepare(self):
        noodles = self.factory.create_noodles()
        sprout = self.factory.create_sprout()
        spice = self.factory.create_spice()
        pepper = self.factory.create_pepper()
        vegetables = self.factory.create_vegetables()
        result = f'{noodles}, {sprout}, {spice}, {pepper}, {vegetables}'
        print(f'preparing {result} ...')
        return result


class MeatRanmianNoodles(Noodles):
    def __init__(self, factory):
        # 原料工厂
        self.factory = factory

    def prepare(self):
        noodles = self.factory.create_noodles()
        sprout = self.factory.create_sprout()
        spice = self.factory.create_spice()
        pepper = self.factory.create_pepper()
        meat = self.factory.create_meat()
        result = f'{noodles}, {sprout}, {spice}, {pepper}, {meat}'
        print(f'preparing {result} ...')
        return result


class YibinStore(FactoryMethodStore):
    def create(self, type_str):
        ingredient_factory = YibinIngredientFactory()
        noodles = None
        if type_str == 'veges':
            noodles = VegesRanmianNoodles(ingredient_factory)
        elif type_str == 'meat':
            noodles = MeatRanmianNoodles(ingredient_factory)
        return noodles


class ChenduStore(FactoryMethodStore):
    def create(self, type_str):
        ingredient_factory = ChenduIngredientFactory()
        noodles = None
        if type_str == 'veges':
            noodles = VegesRanmianNoodles(ingredient_factory)
        elif type_str == 'meat':
            noodles = MeatRanmianNoodles(ingredient_factory)
        return noodles


@start_end
def start_main():
    store = StartStore()
    store.order('veges')


@start_end
def simple_facroty_main():
    """从两家店点餐"""
    yibin_factory = YibinNoodlesFactory()
    yibin_store = SimpleFactoryStore(yibin_factory)
    yibin_store.order('veges')

    chengdu_factory = ChenduNoodlesFactory()
    cheng_du_store = SimpleFactoryStore(chengdu_factory)
    cheng_du_store.order('veges')


@start_end
def factory_method_main():
    yibin_store = MidYibinStore()
    yibin_store.order('veges')
    chendu_store = MidChenduStore()
    chendu_store.order('veges')


@start_end
def end_main():
    yibin_store = YibinStore()
    yibin_store.order('veges')
    chendu_store = ChenduStore()
    chendu_store.order('veges')


if __name__ == '__main__':
    start_main()
    simple_facroty_main()
    factory_method_main()
    end_main()
