from PySide6.QtCore import QObject, Signal
class AnimationController(QObject):
    changed=Signal(str)
    def __init__(self,skeleton):
        super().__init__(); self.skeleton=skeleton; self.queue=[]; self.current=None; self.elapsed=0; self.paused=False; self.speed=1
    def play(self,clips): self.queue=list(clips); self.current=None; self.elapsed=0; self.paused=False; self._next()
    def _next(self):
        self.current=self.queue.pop(0) if self.queue else None; self.elapsed=0; self.changed.emit(self.current.name if self.current else 'Idle')
    def update(self,dt):
        if self.paused or not self.current:return
        self.elapsed += dt*self.speed; pose=self.current.pose(self.elapsed % self.current.duration)
        for name,bone in self.skeleton.bones.items(): bone.rotation[:]=list(pose.get(name,(0,0,0)))
        if self.elapsed >= self.current.duration*self.current.repetitions:self._next()
    def cancel(self): self.queue=[]; self.current=None; self.skeleton.reset(); self.changed.emit('Idle')
    def toggle_pause(self): self.paused=not self.paused
