from animation.motion_library import make_motion
from animation.animation_controller import AnimationController
class CommandExecutor:
    def __init__(self, controller): self.controller=controller
    def execute(self, command):
        if command.actions and command.actions[0].type=='stop': self.controller.cancel(); return 'حرکت متوقف شد.'
        self.controller.play([make_motion(a) for a in command.actions]); return 'دستور در صف اجرا قرار گرفت.'
