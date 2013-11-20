from RNA.RNA_Property import *
from RNA.RNA_Structure import *
from RNA.RNA_Keyframe import *
from RNA.RNA_Animation import *
if __name__ == '__main__':
    key1 = RNA_Keyframe(5, RNA_Prop_Float(10))
    key2 = RNA_Keyframe(20, RNA_Prop_Float(21))
    animation = RNA_Animation()
    animation.set(key1)
    animation.set(key2)
    animation.set_end(25)
    prop = RNA_Prop_Float(0)
    prop.set_animation(animation)
    while True:
        prop.step(5)
        print(prop.get())
        input("Enter")
