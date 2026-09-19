import unittest
from skeleton.skeleton import Skeleton
class TestSkeleton(unittest.TestCase):
 def test_hierarchy_and_reset(self):
  s=Skeleton(); self.assertIn('head',s.bones); self.assertIn('head',s.bones['neck'].children); s.bones['head'].set_rotation(0,9); self.assertLessEqual(s.bones['head'].rotation[0],.7); s.reset(); self.assertEqual(s.bones['head'].rotation,[0,0,0])
if __name__=='__main__': unittest.main()
