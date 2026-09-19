from dataclasses import dataclass
import math
@dataclass
class MotionClip:
    name: str
    duration: float
    frames: list
    repetitions: int=1
    def pose(self,t):
        if not self.frames:return {}
        t=max(0,min(self.duration,t)); a,b=self.frames[0],self.frames[-1]
        for i in range(len(self.frames)-1):
            if self.frames[i][0] <= t <= self.frames[i+1][0]: a,b=self.frames[i],self.frames[i+1]; break
        f=0 if b[0]==a[0] else (t-a[0])/(b[0]-a[0]); result={}
        keys=set(a[1])|set(b[1])
        for k in keys:
            va=a[1].get(k,(0,0,0)); vb=b[1].get(k,(0,0,0)); result[k]=tuple(va[j]+(vb[j]-va[j])*f for j in range(3))
        return result

def make_motion(action):
    t=action.duration or {'sit_up':2,'squat':2,'push_up':2,'jump':1.2}.get(action.type,2)
    r=action.repetitions
    z={}; pi=math.pi
    if action.type in ('run','walk'):
        amp=.65 if action.type=='run' else .35; z={'left_upper_leg':(0,amp,0),'right_upper_leg':(0,-amp,0),'left_upper_arm':(0,-amp,0),'right_upper_arm':(0,amp,0)}
    elif action.type in ('squat','sit_up','push_up'): z={'left_upper_leg':(-.9,0,0),'right_upper_leg':(-.9,0,0),'spine':(-.5,0,0)}
    elif action.type=='arm_raise_left': z={'left_upper_arm':(0,0,-1.4)}
    elif action.type=='arm_raise_right': z={'right_upper_arm':(0,0,1.4)}
    elif action.type=='turn_left': z={'neck':(0,-.7,0)}
    elif action.type=='turn_right': z={'neck':(0,.7,0)}
    elif action.type=='jump': z={'left_upper_leg':(.3,0,0),'right_upper_leg':(.3,0,0)}
    elif action.type=='stand' or action.type=='look': z={}
    elif action.type=='stretch': z={'left_upper_arm':(0,0,-1.1),'right_upper_arm':(0,0,1.1)}
    return MotionClip(action.type,t,[(0,{}),(t/2,z),(t,{})],r)
