import time
from dataclasses import dataclass

@dataclass
class Clock:
    """
    1.0	    1 Sekunde Realzeit = 1 Spielsekunde (Echtzeit-Modus)
    10.0	1 Sekunde Realzeit = 10 Spielsekunden
    *60.0	1 Sekunde Realzeit = 1 Spielminute → 🌗 realistischer Tagesverlauf
    3600.0	1 Sekunde Realzeit = 1 Spielstunde → kompletter Tag in 24 Sekunden
    0.0	Pause - Zeit steht still    
    """
    start_real_time: float = time.time()
    tick_rate: float = 60.0  # 1 Sekunde Realtime = 1 Spielminute
    offset_ticks: int = 0

    def now(self) -> int:
        elapsed = time.time() - self.start_real_time
        return self.offset_ticks + int(elapsed * self.tick_rate)

    def get_time(self) -> dict:
        ticks = self.now()
        day = ticks // 1440
        hour = (ticks % 1440) // 60
        minute = ticks % 60
        return {"day": day, "hour": hour, "minute": minute}

    def get_formatted_time(self) -> str:
        t = self.get_time()
        return f"Tag {t['day']}, {t['hour']:02d}:{t['minute']:02d}"

    def pause(self):
        self.offset_ticks = self.now()
        self.start_real_time = time.time()
        self.tick_rate = 0

    def resume(self, tick_rate=60.0):
        self.start_real_time = time.time()
        self.tick_rate = tick_rate