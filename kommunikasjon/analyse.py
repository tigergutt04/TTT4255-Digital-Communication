import numpy as np
from lib.raspi_import import raspi_import

sp, data = raspi_import('recording.bin', channels=1)
fs = 1.0 / sp
s = data[:, 0] - data[:, 0].mean()

w = int(0.05 * fs)                      # 50 ms-vinduer
f = np.fft.rfftfreq(w, 1 / fs)
rows = []
for k in range(len(s) // w):
    seg = s[k * w:(k + 1) * w]
    sp_ = np.abs(np.fft.rfft(seg * np.hanning(w)))
    rows.append((k * w / fs, f[sp_.argmax()], sp_.max()))

mx = max(r[2] for r in rows)
for t, fr, a in rows:
    if a > 0.2 * mx:
        print(f"{t:6.2f} s  {fr:6.0f} Hz  styrke {a / mx:4.2f}")
