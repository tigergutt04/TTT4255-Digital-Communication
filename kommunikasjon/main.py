"""
Fullfør TODO-ene her og i fsk_decoder() i lib/fsk_decoder.py.
"""

import subprocess
from pathlib import Path

from lib.fsk_decoder import fsk_decoder
from lib.raspi_import import raspi_import

# ===== INNSTILLINGER =====

# TODO: (1) Tilpass innstillingene til meldingen dere sender.
F0 = 500          # Frekvens for bit 0 i Hz
F1 = 4000          # Frekvens for bit 1 i Hz
BIT_TIME = 0.02    # 20 ms per bit, samme som BIT_DURATION_MS i ESP32-koden

# Barker-13: +1 blir bit 1, -1 blir bit 0. Sendes foran hver melding.
START_SIGNAL = [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
MESSAGE_LENGTH = 40            # "Hello": 5 byte, uten Barker-startsekvensen

DURATION = 15                 # Opptakslengde i sekunder
OUTPUT_FILE = 'recording.bin'  # Filen opptaket lagres i

SAMPLE_RATE = 31250  # Hz, IKKE ENDRE.

# ===== OPPTAK OG INNLESING =====   

num_samples = int(DURATION * SAMPLE_RATE)
base_dir = Path(__file__).resolve().parent
sampler_dir = base_dir / 'c'
output_path = base_dir / OUTPUT_FILE

# Bygg sampleren i riktig mappe, uansett hvor Python-skriptet startes.
subprocess.run(['make'], cwd=sampler_dir, check=True)
subprocess.run(
    ['sudo', str(sampler_dir / 'adc_sampler'), str(num_samples), str(output_path)],
    check=True,
)

# Les opptaket. sample_period er tiden mellom målingene i sekunder.
sample_period, data = raspi_import(output_path, channels=1)
sample_rate = 1.0 / sample_period   # Antall målinger per sekund
signal = data[:, 0]                 # Hent målingene fra første kanal

# ===== OPPGAVE: (skriv her) =====

# TODO: (2) Kall fsk_decoder() og lagre resultatet i bits.
# Se parameterbeskrivelsene i funksjonen.
bits = fsk_decoder(signal, sample_rate, F0, F1, BIT_TIME, start_signal=START_SIGNAL, message_length=MESSAGE_LENGTH)

# TODO: (3) Skriv ut bits og sammenlign med meldingen dere sendte.
print(bits)
# ===== SLUTT PÅ OPPGAVE =====
