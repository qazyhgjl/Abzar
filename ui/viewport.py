from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
import math
class Viewport(QOpenGLWidget):
    def __init__(self,skeleton,controller):
        super().__init__(); self.skeleton=skeleton; self.controller=controller; self.mode='X-Ray'; self.yaw=0; self.pitch=8; self.zoom=-3.8; self.last=None
    def initializeGL(self): glClearColor(.015,.025,.05,1); glEnable(GL_DEPTH_TEST); glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    def resizeGL(self,w,h): glViewport(0,0,w,h); glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluPerspective(45,w/max(1,h),.1,100); glMatrixMode(GL_MODELVIEW)
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT); glLoadIdentity(); glTranslatef(0,-1.05,self.zoom); glRotatef(self.pitch,1,0,0); glRotatef(self.yaw,0,1,0); self._grid(); self._body()
    def _grid(self):
        glColor4f(.05,.3,.35,.35); glBegin(GL_LINES)
        for i in range(-10,11): glVertex3f(i/3,0,-3);glVertex3f(i/3,0,3);glVertex3f(-3,0,i/3);glVertex3f(3,0,i/3)
        glEnd()
    def _body(self):
        # Procedural capsules/lines are generated from the hierarchical offsets.
        glLineWidth(4); glColor4f(.1,.85,1,.95)
        for b in self.skeleton.bones.values():
            if not b.parent: continue
            p=self._pos(b.parent); q=(p[0]+b.offset[0],p[1]+b.offset[1],p[2]+b.offset[2])
            glBegin(GL_LINES); glVertex3f(*p);glVertex3f(*q);glEnd(); glPointSize(8); glBegin(GL_POINTS);glVertex3f(*q);glEnd()
        glColor4f(.15,.65,1,.18); glLineWidth(14)
        for b in self.skeleton.bones.values():
            if b.parent:
                p=self._pos(b.parent);q=(p[0]+b.offset[0],p[1]+b.offset[1],p[2]+b.offset[2]);glBegin(GL_LINES);glVertex3f(*p);glVertex3f(*q);glEnd()
    def _pos(self,name):
        b=self.skeleton.bones[name]; p=(0,0,0) if not b.parent else self._pos(b.parent); return tuple(p[i]+b.offset[i] for i in range(3))
    def mousePressEvent(self,e): self.last=e.position()
    def mouseMoveEvent(self,e):
        if self.last and e.buttons() & Qt.LeftButton: d=e.position()-self.last; self.yaw+=d.x();self.pitch+=d.y();self.last=e.position();self.update()
    def wheelEvent(self,e): self.zoom+=e.angleDelta().y()/120*.25; self.update()
