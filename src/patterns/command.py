"""
命令模式:
    将请求封装成对象，可以将请求参数化其他对象，同时支持撤销操作。队列、日志也可用。
课题：
    一块可编程遥控器，有几号插槽，一个号有一对，对应开和关，需要接入不同产商的机器。
"""

from src.utils import start_end


# 写一个打开电灯和关闭电灯的命令

class CommandMixin(object):
    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError


class LightOnCommand(CommandMixin):
    def __init__(self, light):
        self.light = light

    def execute(self):
        # 不直接实现细节，通过接受者light做处理，更加对调用者和接收者解耦
        self.light.on()

    def undo(self):
        self.light.off()

    def __str__(self):
        return 'light on'


class LightOffCommand(CommandMixin):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.off()

    def undo(self):
        self.light.on()

    def __str__(self):
        return 'light off'


# 添加撤销会记录上一次操作


class Light(object):
    """厂商类"""

    def on(self):
        print('light on..')

    def off(self):
        print('light off..')


class SimpleRemoteControl(object):
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def press(self):
        print('press...')
        self.command.execute()


# 所有插槽的遥控器的实现

class NoCommand(CommandMixin):
    """不做任何操作的命令，用于初始化遥控器"""

    def execute(self):
        return

    def undo(self):
        return

    def __str__(self):
        return 'no command'


class RemoteControl(object):
    def __init__(self, slot_count=2):
        self.slot_count = slot_count
        no_command = NoCommand()
        self.on_commands = [no_command] * slot_count
        self.off_commands = [no_command] * slot_count
        # 前一个命令用于undo操作
        self.pre_command = None

    def set_command(self, slot, on_command, off_command):
        self.on_commands[slot] = on_command
        self.off_commands[slot] = off_command

    def press_on(self, slot):
        print('slot %s press on..' % slot)
        self.on_commands[slot].execute()
        self.pre_command = self.on_commands[slot]

    def press_off(self, slot):
        print('slot %s press off..' % slot)
        self.off_commands[slot].execute()
        self.pre_command = self.off_commands[slot]

    def press_undo(self):
        print('press undo..')
        self.pre_command.undo()

    def __str__(self):
        to_string = []
        for i in range(self.slot_count):
            to_string.append('[slot %s]: %s, %s' % (i, self.on_commands[i], self.off_commands[i]))
        return '\n'.join(to_string)


# 实现播放音响CD

class Stereo(object):
    def on(self):
        print('stereo on...')

    def off(self):
        print('stereo off...')

    def set_cd(self):
        print('stereo set cd')

    def set_volume(self, volume):
        print('stereo set volume to %s' % volume)


class StereoOnCommand(CommandMixin):
    def __init__(self, stereo):
        self.stereo = stereo

    def execute(self):
        self.stereo.on()
        self.stereo.set_cd()
        self.stereo.set_volume(12)

    def undo(self):
        self.stereo.off()

    def __str__(self):
        return 'stereo on'


class StereoOffCommand(CommandMixin):
    def __init__(self, stereo):
        self.stereo = stereo

    def execute(self):
        self.stereo.off()

    def undo(self):
        self.stereo.on()
        self.stereo.set_cd()
        self.stereo.set_volume(12)

    def __str__(self):
        return 'stereo off'


# 使用组合命令
class MacroCommand(CommandMixin):
    def __init__(self, commands):
        self.commands = commands

    def execute(self):
        for command in self.commands:
            command.execute()

    def undo(self):
        for command in self.commands[::-1]:
            command.undo()


@start_end
def simple_main():
    # 接收者
    light = Light()
    light_on_cmd = LightOnCommand(light)
    light_off_cmd = LightOffCommand(light)
    # 调用者
    control = SimpleRemoteControl()
    control.set_command(light_on_cmd)
    control.press()
    control.set_command(light_off_cmd)
    control.press()


@start_end
def remote_main():
    light = Light()
    light_on_cmd = LightOnCommand(light)
    light_off_cmd = LightOffCommand(light)
    stereo = Stereo()
    stereo_on_cmd = StereoOnCommand(stereo)
    stereo_off_cmd = StereoOffCommand(stereo)

    control = RemoteControl()
    control.set_command(0, light_on_cmd, light_off_cmd)
    print(control)
    control.set_command(1, stereo_on_cmd, stereo_off_cmd)
    print(control)
    control.press_on(0)
    control.press_on(1)
    control.press_off(0)
    control.press_off(1)


@start_end
def remote_with_undo_main():
    light = Light()
    light_on_cmd = LightOnCommand(light)
    light_off_cmd = LightOffCommand(light)
    stereo = Stereo()
    stereo_on_cmd = StereoOnCommand(stereo)
    stereo_off_cmd = StereoOffCommand(stereo)

    control = RemoteControl()
    control.set_command(0, light_on_cmd, light_off_cmd)
    control.set_command(1, stereo_on_cmd, stereo_off_cmd)
    control.press_on(0)
    control.press_on(1)
    control.press_undo()
    control.press_off(0)
    control.press_off(1)
    control.press_undo()


@start_end
def macro_main():
    light = Light()
    light_on_cmd = LightOnCommand(light)
    light_off_cmd = LightOffCommand(light)
    stereo = Stereo()
    stereo_on_cmd = StereoOnCommand(stereo)
    stereo_off_cmd = StereoOffCommand(stereo)
    on_cmds = [light_on_cmd, stereo_on_cmd]
    off_cmds = [light_off_cmd, stereo_off_cmd]
    macro_on_cmd = MacroCommand(on_cmds)
    macro_off_cmd = MacroCommand(off_cmds)
    control = RemoteControl()
    control.set_command(0, macro_on_cmd, macro_off_cmd)
    control.press_on(0)
    control.press_off(0)
    control.press_undo()


if __name__ == '__main__':
    simple_main()
    remote_main()
    remote_with_undo_main()
    macro_main()
