from .bone import Bone
from .joint import Joint

class Skeleton:
    def __init__(self):
        self.bones = {}
        self._build()

    def add(self, name, parent, offset, length, limit=1.57):
        bone = Bone(name, parent, offset, length)
        self.bones[name] = bone
        if parent:
            self.bones[parent].children.append(name)
        bone.joint = Joint(name, limit)

    def _build(self):
        self.add('pelvis', None, (0, 1.05, 0), .28)
        self.add('spine', 'pelvis', (0, .28, 0), .35)
        self.add('chest', 'spine', (0, .35, 0), .42)
        self.add('neck', 'chest', (0, .42, 0), .16, .7)
        self.add('head', 'neck', (0, .16, 0), .25, .7)
        for side, x in [('left', -1), ('right', 1)]:
            self.add(f'{side}_clavicle', 'chest', (x*.18, .30, 0), .22, .8)
            self.add(f'{side}_upper_arm', f'{side}_clavicle', (x*.22, 0, 0), .38, 2.6)
            self.add(f'{side}_forearm', f'{side}_upper_arm', (x*.38, 0, 0), .34, 2.7)
            self.add(f'{side}_hand', f'{side}_forearm', (x*.34, 0, 0), .18, 1.4)
            self.add(f'{side}_upper_leg', 'pelvis', (x*.16, -.05, 0), .48, 2.0)
            self.add(f'{side}_lower_leg', f'{side}_upper_leg', (0, -.48, 0), .48, 2.5)
            self.add(f'{side}_foot', f'{side}_lower_leg', (0, -.48, .08), .22, .9)

    def reset(self):
        for bone in self.bones.values(): bone.joint.reset()
