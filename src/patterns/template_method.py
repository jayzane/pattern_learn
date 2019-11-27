"""
模板方法模式：
    父类定义好算法步骤，一些步骤由子类来实现。父类是抽象类，抽象类可以定义具体方法、抽象方法、钩子方法，钩子方法是指
    不做任何事或者有默认行为的方法，抽象方法和钩子方法由子类来实现或者覆盖。
与工厂方法模式区别：
    工厂方法是特殊的模板方法，算法步骤中的对象创建交给子类。
与策略模式区别：
    模板方法使用继承，策略模式使用组合。
    模板方法只有一个算法，子类实现算法某些步骤细节，策略模式是提供多个可替代的算法。
原则:
    8.好莱坞原则
    要我打电话给（调用）你，不要你打电话给我。
    与依赖倒置的区别：
        好莱坞教我们如何创建一个避免依赖的设计，而依赖倒置是教我们在设计里如何避免依赖。
优点：
    1.高层组件不依赖低层组件
缺点：
    1.使用了继承
    2.只存在一个算法，灵活性不够
问题：
    低层组件不可以调用高层组件吗？
    模板方法一定由继承的子类来实现步骤吗？
课题：
    煮咖啡，步骤有烧水、冲泡、倒进杯中、加糖和奶
    煮茶，步骤由烧水、泡茶袋、倒进杯中、加柠檬
"""


class StartCoffee(object):
    def prepare_recipe(self):
        self.boil_water()
        self.brew_coffee_grinds()
        self.pour_in_cup()
        self.add_sugar_and_milk()

    def boil_water(self):
        print('boiling water...')

    def brew_coffee_grinds(self):
        print('brewing coffee grinds...')

    def pour_in_cup(self):
        print('pouring in cup...')

    def add_sugar_and_milk(self):
        print('adding sugar and milk...')


class StartTea(object):
    def prepare_recipe(self):
        self.boil_water()
        self.steep_tee_bag()
        self.pour_in_cup()
        self.add_lemon()

    def boil_water(self):
        print('boiling water...')

    def steep_tee_bag(self):
        print('steeping tee bag...')

    def pour_in_cup(self):
        print('pouring in cup...')

    def add_lemon(self):
        print('adding lemon...')


# 会发现泡咖啡和泡茶有两个步骤是完全一样的，另两个步骤是类似的，能否抽象一下呢？


class CaffeineBeverage(object):
    def prepare_recipe(self):
        print('-- prepare start -- ')
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        # 钩子方法
        if self.custom_want_condiments():
            self.add_condiments()
        print('-- prepare done -- ')

    def boil_water(self):
        print('boiling water...')

    def brew(self):
        """用热水泡咖啡或茶"""
        raise NotImplementedError

    def pour_in_cup(self):
        print('pouring in cup...')

    def add_condiments(self):
        """加调料"""
        raise NotImplementedError

    def custom_want_condiments(self):
        return True


class Coffee(CaffeineBeverage):
    def brew(self):
        print('brewing coffee grinds...')

    def add_condiments(self):
        print('adding sugar and milk...')

    def custom_want_condiments(self):
        _want = input('Want some sugar and milk?(y/n)') == 'y'
        return _want


class Tea(CaffeineBeverage):
    def brew(self):
        print('steeping tee bag...')

    def add_condiments(self):
        print('adding lemon...')

    def custom_want_condiments(self):
        _want = input('Want some lemons?(y/n)') == 'y'
        return _want


def main():
    coffee = Coffee()
    coffee.prepare_recipe()
    tee = Tea()
    tee.prepare_recipe()


if __name__ == '__main__':
    main()
