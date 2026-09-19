from dataclasses import dataclass, field
import math

@dataclass
class Bone:
    name: str
    parent: str | None
    offset: tuple
    length: float
    children: list = field(default_factory=list)
    joint: object = None
    rotation: list = field(default_factory=lambda: [0.0, 0.0, 0.0])

    def set_rotation(self, axis, value):
        value = max(-self.joint.limit, min(self.joint.limit, value))
        self.rotation[axis] = value
