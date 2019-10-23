"""
观察者模式:
    定义对象间一对多依赖，当对象改变时，依赖者会受到通知并自动更新
原则:
    4.交互对象，采用松耦合
优点：
    1.观察者和被观察者建立了松耦合
    2.通知统一管理，广播通信
    3.表示层和数据逻辑层分离，稳定的消息更新机制，抽象了更新接口
缺点：
    1.观察者过多，会费时
    2.循环依赖问题会崩溃
    3.没法知道观察者是怎么变化的，只知道变化了
课题:
    天气数据更新，同步到公告板，公告板可拓展
总结:
    1.封装变化：主题状态在变，观察者数目和类型在变，改变观察者而不用改变主题
    2.针对接口而不是实现：主题和观察者都使用了接口
    3.多用组合：多个观察者组合进主题中而不是继承
"""
from src.utils import start_end


class StartWeatherData(object):
    """
    问题：
        1.针对具体实现而不是接口
        2.新的公告板会修改代码，没有封装变化
        3.无法运行时动态添加公告板
    """

    def __init__(self):
        self.temperature = None
        self.humidity = None
        self.pressure = None

    def measure_changed(self):
        temperature = self.get_temperature()
        humidity = self.get_humidity()
        pressure = self.get_pressure()
        current = StartCurrent()
        statistics = StartStatistics()
        forecast = StartForecast()
        current.update(temperature, humidity, pressure)
        statistics.update(temperature, humidity, pressure)
        forecast.update(temperature, humidity, pressure)

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def get_pressure(self):
        return self.pressure

    def set_changed(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.measure_changed()


class StartCurrent(object):
    def update(self, temperature, humidity, pressure):
        print(f'Current Codition: temperature:{temperature}, humidity:{humidity}, pressure:{pressure}')

    def __str__(self):
        return 'Current'


class StartStatistics(object):
    def update(self, temperature, humidity, pressure):
        print(f'Statistics: temperature:{temperature}, humidity:{humidity}, pressure:{pressure}')

    def __str__(self):
        return 'Statistics'


class StartForecast(object):
    def update(self, temperature, humidity, pressure):
        print(f'Forecast: temperature:{temperature}, humidity:{humidity}, pressure:{pressure}')

    def __str__(self):
        return 'Forecast'


# 这次不采用abc模块
class SubjectMixin(object):
    def add_observer(self, observer):
        raise NotImplementedError

    def delete_observer(self, observer):
        raise NotImplementedError

    def notify_observers(self):
        raise NotImplementedError


class EndWeatherData(SubjectMixin):
    def __init__(self):
        self.observers = []
        # 通过参数调节通知频率，避免风吹草动都通知过去
        self.changed = False
        self.temperature = None
        self.humidity = None
        self.pressure = None

    def add_observer(self, observer):
        self.observers.append(observer)
        print(f'{observer} added')

    def delete_observer(self, observer):
        self.observers.remove(observer)
        print(f'{observer} deleted')

    def notify_observers(self):
        if self.changed:
            temperature = self.get_temperature()
            humidity = self.get_humidity()
            pressure = self.get_pressure()
            for observer in self.observers:
                # 观察者都实现了update接口，并且采取了被push方式
                # 如果采取pull方式，则将被观察者对象传过去，让观察者调用其getter方法
                observer.update(temperature, humidity, pressure)
            self.changed = False

    def measure_changed(self):
        self.notify_observers()

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def get_pressure(self):
        return self.pressure

    def set_changed(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.changed = True
        self.measure_changed()


@start_end
def start_main():
    weather = StartWeatherData()
    weather.set_changed(1, 2, 3)
    weather.set_changed(10, 20, 30)
    weather.set_changed(100, 200, 300)


@start_end
def end_main():
    weather = EndWeatherData()
    current = StartCurrent()
    statistics = StartStatistics()
    forecast = StartForecast()
    weather.add_observer(current)
    weather.add_observer(statistics)
    weather.add_observer(forecast)

    weather.set_changed(1, 2, 3)
    weather.set_changed(10, 20, 30)
    weather.set_changed(100, 200, 300)
    weather.delete_observer(forecast)
    weather.set_changed(1000, 2000, 3000)


if __name__ == '__main__':
    start_main()
    end_main()
