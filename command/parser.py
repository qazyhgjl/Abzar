import re
from dataclasses import dataclass

DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
ALIASES = {
 'بدو':'run','دویدن':'run','راه برو':'walk','راه بروی':'walk','راه رفتن':'walk',
 'بنشین':'sit','نشستن':'sit','دراز بکش':'lie','درازونشست':'sit_up','دراز و نشست':'sit_up',
 'اسکوات':'squat','اسکات':'squat','شنا':'push_up','پرش':'jump','بپر':'jump',
 'کشش':'stretch','دست چپت را بالا ببر':'arm_raise_left','دست راستت را بالا ببر':'arm_raise_right',
 'سر را به سمت راست بچرخان':'turn_right','سر را به سمت چپ بچرخان':'turn_left',
 'بایست':'stand','ایست':'stand','به دوربین نگاه کن':'look','توقف':'stop','متوقف':'stop'
}
@dataclass
class Action:
    type: str
    duration: float|None = None
    repetitions: int = 1
@dataclass
class Command:
    actions: list
    original: str

class PersianParser:
    def normalize(self, text):
        text = text.translate(DIGITS).replace('ي','ی').replace('ك','ک')
        text = re.sub(r'[،؛,:،]', ' ', text)
        return re.sub(r'\s+', ' ', text.strip().lower())
    def parse(self, text):
        original = text
        text = self.normalize(text)
        if not text: raise ValueError('دستور خالی است.')
        if any(x in text for x in ('توقف','متوقف')): return Command([Action('stop')], original)
        parts = re.split(r'\s*(?:و سپس|بعد از آن|بعدش|بعد)\s*', text)
        actions=[]
        for part in parts:
            duration = self._number_unit(part, ('ثانیه','ثانیه‌ای','دقیقه'))
            reps = self._number_before(part, ('بار','تا','مرتبه')) or 1
            found = None
            for alias, action in sorted(ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
                if alias in part: found=action; break
            if not found: raise ValueError(f'حرکت قابل تشخیص نیست: «{part}»')
            if found == 'stop': return Command([Action('stop')], original)
            if found not in ('sit_up','squat','jump','push_up') and duration is None: duration = 2.0
            actions.append(Action(found, duration, reps))
        return Command(actions, original)
    def _number_before(self, text, words):
        pat = r'(\d+(?:\.\d+)?)\s*(?:'+'|'.join(map(re.escape,words))+')'
        m=re.search(pat,text); return int(float(m.group(1))) if m else None
    def _number_unit(self,text,units):
        pat=r'(\d+(?:\.\d+)?)\s*(?:'+'|'.join(map(re.escape,units))+')'
        m=re.search(pat,text)
        if not m:return None
        value=float(m.group(1)); return value*60 if 'دقیقه' in m.group(0) else value
