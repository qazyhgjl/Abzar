import unittest
from command.parser import PersianParser
class TestParser(unittest.TestCase):
 def setUp(self): self.p=PersianParser()
 def test_persian_duration(self): self.assertEqual(self.p.parse('۳۰ ثانیه بدو').actions[0].duration,30)
 def test_repetitions(self): self.assertEqual(self.p.parse('5 بار اسکوات انجام بده').actions[0].repetitions,5)
 def test_sequence(self): self.assertEqual([x.type for x in self.p.parse('۲۰ ثانیه راه برو و بعد بنشین').actions],['walk','sit'])
 def test_empty(self):
  with self.assertRaises(ValueError): self.p.parse('')
if __name__=='__main__': unittest.main()
