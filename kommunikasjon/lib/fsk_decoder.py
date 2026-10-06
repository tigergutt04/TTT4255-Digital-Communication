import sys
import numpy as np
from scipy.signal import butter, filtfilt


def bandpass(signal, sample_rate, f0, f1):
    """
    Filtrerer signalet med et båndpassfilter som beholder området rundt
    f0 og f1 og demper frekvenser utenfor dette. 

    Returnerer det filtrerte signalet.
    """
    f_low, f_high = min(f0, f1), max(f0, f1)
    margin = (f_high - f_low) / 2
    nyq = sample_rate / 2
    low  = np.clip((f_low  - margin) / nyq, 1e-6, 1 - 1e-6)
    high = np.clip((f_high + margin) / nyq, 1e-6, 1 - 1e-6)
    b, a = butter(4, [low, high], btype='band')
    return filtfilt(b, a, signal)


def find_sequence(signal, sample_rate, f0, f1, bit_time, sequence):
    """
    Leter etter sequence ved å sammenligne signalets frekvensinnhold
    med den kjente bitsekvensen. 

    Returnerer (start, slutt), der slutt er indeksen rett etter sekvensen.
    Søket har ingen terskel som bekrefter at sekvensen finnes.
    """
    n = int(round(bit_time * sample_rate))
    t = np.arange(n) / sample_rate
    ref0 = np.hanning(n) * np.exp(-2j * np.pi * f0 * t)
    ref1 = np.hanning(n) * np.exp(-2j * np.pi * f1 * t)
    expected = np.asarray(sequence, dtype=float) * 2 - 1
    bit_offsets = np.arange(len(sequence)) * n

    def ratio(starts):
        """
        Sammenligner signalinnholdet ved f0 og f1 i en bitperiode fra
        hver indeks i starts. 
        """
        c = signal[starts[:, None] + np.arange(n)[None, :]]
        c = c - c.mean(axis=1, keepdims=True)
        e0 = np.abs(c @ ref0) ** 2
        e1 = np.abs(c @ ref1) ** 2
        return (e1 / (e0 + e1 + 1e-10)) * 2 - 1

    # Steg 1: grovt søk
    coarse_step = max(1, n // 2)
    coarse_starts = np.arange(0, len(signal) - n + 1, coarse_step)
    coarse_expected = np.repeat(expected, n // coarse_step)
    coarse_corr = np.correlate(ratio(coarse_starts), coarse_expected, mode='valid')
    top3 = np.argsort(coarse_corr)[-3:][::-1]

    # Steg 2: finere søk rundt de beste kandidatene
    fine_step = max(1, n // 124)
    fine_offsets = np.arange(-n // 2, n // 2 + 1, fine_step)
    best_score, best_sample = -np.inf, 0

    for coarse_peak in top3:
        coarse_sample = int(coarse_peak) * coarse_step
        all_starts = np.clip(
            (coarse_sample + fine_offsets[:, None] + bit_offsets[None, :]).flatten(),
            0, len(signal) - n
        )
        scores = ratio(all_starts).reshape(len(fine_offsets), len(sequence)) @ expected
        idx = int(np.argmax(scores))
        if scores[idx] > best_score:
            best_score = scores[idx]
            best_sample = coarse_sample + fine_offsets[idx]

    return int(best_sample), int(best_sample) + len(sequence) * n


def decode_bits(signal, sample_rate, f0, f1, bit_time):
    """
    Deler signalet i blokker på en bitperiode og sammenligner
    signalinnholdet ved f0 og f1. Hver blokk tolkes som 1 hvis
    f1 dominerer, ellers som 0.

    Returnerer en liste med bitverdier. En ufullstendig blokk på slutten
    utelates. Signalet må begynne ved starten av en bitperiode.
    """
    n = int(round(bit_time * sample_rate))
    t = np.arange(n) / sample_rate
    window = np.hanning(n)
    ref0 = window * np.exp(-2j * np.pi * f0 * t)
    ref1 = window * np.exp(-2j * np.pi * f1 * t)

    total = (len(signal) // n) * n
    chunks = signal[:total].reshape(-1, n)
    chunks = chunks - chunks.mean(axis=1, keepdims=True)

    e0 = np.abs(chunks @ ref0) ** 2
    e1 = np.abs(chunks @ ref1) ** 2
    return (e1 > e0).astype(int).tolist()


def fsk_decoder(signal, sample_rate, f0, f1, bit_time,
                start_signal=None, message_length=None):
    """
    Dekoder en FSK-melding fra et signal.

    signal: Måleverdiene fra opptaket.
    sample_rate: Antall målinger per sekund, målt i Hz.
    f0, f1: Frekvensene for bit 0 og bit 1, målt i Hz.
    bit_time: Varigheten av en bit, målt i sek.
    start_signal: Valgfri startsekvens.
    message_length: Valgfritt antall bit i meldingen, uten startsekvensen.
    None betyr at opplysningen ikke er gitt.

    Returnerer bitverdiene som en liste med 0 og 1.
    """
    # Flytt signalet slik at gjennomsnittsverdien blir 0.
    signal = signal - np.mean(signal)

    # ===== OPPGAVE: (skriv her) =====

    # TODO: (1) Filtrer signalet. Dere kan bruke bandpass().
    
    signal = bandpass(signal, sample_rate, f0, f1)

    # TODO: (2) Finn delen av signalet som inneholder meldingen.
    # Dere kan bruke find_sequence() for å finne startsekvens.
    # Hint: find_sequence() returnerer start og slutt i antall samples.
    
    if start_signal is not None:
        _, end = find_sequence(signal, sample_rate, f0, f1, bit_time, start_signal)
        signal = signal[end:]


    # TODO: (3) Dekod meldingen og lagre bitverdiene i variabelen bits.
    # Dere kan bruke decode_bits() og message_length hvis lengden er kjent.
    # Startsekvensen kan tas med, men telles ikke i message_length.
    
    bits = decode_bits(signal, sample_rate, f0, f1, bit_time)
    if message_length is not None:
        bits = bits[:message_length]

    # ===== SLUTT PÅ OPPGAVEN =====

    return bits
