import unittest
from RNA.RNA_Property import *
from RNA.RNA_Structure import *
from RNA.RNA_Keyframe import *
from RNA.RNA_Animation import *

class TestRNA(unittest.TestCase):
    # Basic Tests
    def test_intprop(self):
        prop = RNA_Prop_Int(0)
        self.assertEqual(prop.get(),0)
    def test_boolprop(self):
        prop = RNA_Prop_Bool(True)
        self.assertTrue(prop.get())
    def test_floatprop(self):
        prop = RNA_Prop_Float(0.0)
        self.assertEqual(prop.get(),0.0)
    def test_stringprop(self):
        prop = RNA_Prop_String('')
        self.assertEqual(prop.get(),'')
    # END Basic Tests

    # Animation Tests
    def test_animation1(self):
        key1 = RNA_Keyframe(0, RNA_Prop_Int(0))
        key2 = RNA_Keyframe(20,RNA_Prop_Int(20))
        animation = RNA_Animation()
        animation.set(key1)
        animation.set(key2)
        animation.set_end(21)
        prop = RNA_Prop_Int(0)
        prop.set_animation(animation)

        val_list = list(range(22))
        val_list[21] = 20
        while prop.get_time() < 21:
            prop.step()
            self.assertEqual(prop.get(), val_list[prop.get_time()])
    # END Animation Tests
if __name__ == '__main__':
    unittest.main()
    #    key1 = RNA_Keyframe(5, RNA_Prop_Float(10))
    #    key2 = RNA_Keyframe(20, RNA_Prop_Float(21))
    #    animation = RNA_Animation()
    #    animation.set(key1)
    #    animation.set(key2)
    #    animation.set_end(25)
    #    prop = RNA_Prop_Float(0)
    #    prop.set_animation(animation)
    #    while True:
    #        prop.step(5)
    #        print(prop.get())
    #        input("Enter")
