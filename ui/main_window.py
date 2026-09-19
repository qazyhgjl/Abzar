from PySide6.QtWidgets import *
from PySide6.QtCore import QTimer, Qt
from .viewport import Viewport
from skeleton.skeleton import Skeleton
from command.parser import PersianParser
from command.executor import CommandExecutor
from animation.animation_controller import AnimationController
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('شبیه‌ساز حرکت انسان | Offline AI'); self.resize(1400,850); self.setStyleSheet('QMainWindow,QWidget{background:#07111d;color:#d9f7ff} QPushButton,QLineEdit,QComboBox{background:#10283a;border:1px solid #1e7180;padding:8px;color:#d9f7ff} QTextEdit{background:#06101a;border:1px solid #195365;color:#d9f7ff}')
        self.skeleton=Skeleton(); self.controller=AnimationController(self.skeleton); self.parser=PersianParser(); self.executor=CommandExecutor(self.controller); self.viewport=Viewport(self.skeleton,self.controller)
        self.chat=QTextEdit(); self.chat.setReadOnly(True); self.input=QLineEdit(); self.input.setPlaceholderText('دستور فارسی را وارد کنید؛ مانند: ۳۰ ثانیه بدو و بعد بنشین')
        send=QPushButton('ارسال'); send.clicked.connect(self.submit); self.input.returnPressed.connect(self.submit); stop=QPushButton('توقف'); stop.clicked.connect(self.stop); pause=QPushButton('مکث / ادامه'); pause.clicked.connect(self.controller.toggle_pause)
        mode=QComboBox(); mode.addItems(['X-Ray','Skeleton','Transparent Skin','Muscles','Skin','Joint Debug']); mode.currentTextChanged.connect(lambda x:setattr(self.viewport,'mode',x))
        side=QVBoxLayout(); side.addWidget(QLabel('کنترل دستورات فارسی'));side.addWidget(self.chat);side.addWidget(mode);side.addWidget(self.input);side.addWidget(send);side.addWidget(stop);side.addWidget(pause);side.addStretch()
        root=QHBoxLayout();root.addWidget(self.viewport,4); panel=QWidget();panel.setLayout(side);root.addWidget(panel,1); central=QWidget();central.setLayout(root);self.setCentralWidget(central)
        self.statusBar().showMessage('آماده | Offline | بدون API خارجی'); self.controller.changed.connect(lambda x:self.statusBar().showMessage('حرکت فعلی: '+x))
        self.timer=QTimer(self); self.timer.timeout.connect(self.tick); self.timer.start(16)
    def submit(self):
        text=self.input.text().strip()
        if not text:return
        self.chat.append('شما: '+text); self.input.clear()
        try: c=self.parser.parse(text); self.chat.append('تفسیر: '+', '.join(a.type for a in c.actions)); self.chat.append(self.executor.execute(c))
        except ValueError as e:self.chat.append('خطا: '+str(e))
    def stop(self): self.controller.cancel(); self.chat.append('سیستم: همه حرکات متوقف شد.')
    def tick(self): self.controller.update(.016); self.viewport.update()
