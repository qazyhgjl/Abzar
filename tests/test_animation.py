import unittest
from skeleton.skeleton import Skeleton
from animation.animation_controller import AnimationController
from animation.motion_library import make_motion
from command.parser import Action
class TestAnimation(unittest.TestCase):
 def test_play_and_cancel(self):
  c=AnimationController(Skeleton()); c.play([make_motion(Action('walk',1))]); c.update(.2); self.assertIsNotNone(c.current); c.cancel(); self.assertIsNone(c.current)
if __name__=='__main__': unittest.main()
