"""
Fullfør TODO-ene her og i fsk_decoder() i lib/fsk_decoder.py.
"""

import subprocess

from lib.fsk_decoder import fsk_decoder
from lib.raspi_import import raspi_import

# ===== INNSTILLINGER =====

# TODO: (1) Tilpass innstillingene til meldingen dere sender.
F0 = 1200          # Frekvens for bit 0 i Hz
F1 = 2200          # Frekvens for bit 1 i Hz
BIT_TIME = 0.2     # Varighet per bit i sekunder

START_SIGNAL = [1, 1, 1, 0, 1]  # Bitsekvens som markerer meldingens start
MESSAGE_LENGTH = None          # Antall bit uten startsekvens, eller None hvis ukjent

DURATION = 15                 # Opptakslengde i sekunder
OUTPUT_FILE = 'recording.bin'  # Filen opptaket lagres i

SAMPLE_RATE = 31250  # Hz, IKKE ENDRE.

# ===== OPPTAK OG INNLESING =====

num_samples = int(DURATION * SAMPLE_RATE)
subprocess.run(
    ['sudo', './c/adc_sampler', str(num_samples), OUTPUT_FILE],
    check=True,
)

# Les opptaket. sample_period er tiden mellom målingene i sekunder.
sample_period, data = raspi_import(OUTPUT_FILE, channels=1)
sample_rate = 1.0 / sample_period   # Antall målinger per sekund
signal = data[:, 0]                 # Hent målingene fra første kanal

# ===== OPPGAVE: (skriv her) =====

# TODO: (2) Kall fsk_decoder() og lagre resultatet i bits.
# Se parameterbeskrivelsene i funksjonen.

# TODO: (3) Skriv ut bits og sammenlign med meldingen dere sendte.

# ===== SLUTT PÅ OPPGAVE =====
