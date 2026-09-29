"""
Vis ADC-opptak. Legg .dat-filene i data-mappen.
Velg fil og plottype nedenfor, og kjør: python plot.py i terminalen.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from scipy.signal import periodogram, spectrogram

from lib.raspi_import import raspi_import

# ===== INNSTILLINGER =====

DATA_FILE = "test.dat"      # Filnavn i data-mappen
PLOT_TYPE = "spectrogram"   # Velg "spectrogram" eller "spectrum"
CHANNELS = 1                # Antall kanaler i opptaket
CHANNEL = 0                 # Kanalen som vises. Første kanal har nummer 0.

TIME_START = 0              # Start på utsnittet i sekunder
TIME_END = None             # Slutt i sekunder. None bruker resten av opptaket.
FREQ_MIN = 0                # Laveste frekvens som vises, i Hz
FREQ_MAX = None             # Høyeste frekvens i Hz. None viser hele frekvensområdet.

















def plot_spectrogram(signal, sample_rate, time_start=0.0, frequency_limits=None):
    """
    Viser hvordan frekvensinnholdet endrer seg over tid.

    signal: Måleverdiene fra en kanal i opptaket.
    sample_rate: Antall målinger per sekund, målt i Hz.
    time_start: Tidspunktet utsnittet starter på i det opprinnelige opptaket.
    frequency_limits: Frekvensområdet (min, maks) i Hz. None viser hele området.
    Fargene viser signalstyrken. Funksjonen viser figuren.
    """
    if len(signal) < 2:
        raise ValueError("Det valgte tidsområdet må inneholde minst to måleverdier.")

    # Korte, overlappende utsnitt viser frekvensinnholdet på ulike tidspunkt.
    segment_length = min(1024, len(signal))
    frequencies, times, power = spectrogram(
        signal,
        fs=sample_rate,
        window="hann",
        nperseg=segment_length,
        noverlap=segment_length // 2,
        scaling="spectrum",
        mode="psd",
    )

    plt.figure(figsize=(10, 5))
    plt.pcolormesh(times + time_start, frequencies, power, shading="auto")
    plt.xlim(time_start, time_start + len(signal) / sample_rate)
    plt.ylim(frequency_limits if frequency_limits is not None else (0, sample_rate / 2))
    plt.xlabel("Tid [s]")
    plt.ylabel("Frekvens [Hz]")
    plt.title("Spektrogram")
    plt.colorbar(label="Signalstyrke")
    plt.tight_layout()
    plt.show()


def plot_spectrum(signal, sample_rate, frequency_limits=None):
    """
    Viser frekvensinnholdet i det valgte tidsutsnittet samlet.

    signal: Måleverdiene fra én kanal i opptaket.
    sample_rate: Antall målinger per sekund, målt i Hz.
    frequency_limits: Frekvensområdet (min, maks) i Hz. None viser hele området.
    Toppene viser hvilke frekvenser som dominerer. Funksjonen viser figuren.
    """
    if len(signal) < 2:
        raise ValueError("Det valgte tidsområdet må inneholde minst to måleverdier.")

    frequencies, power = periodogram(
        signal,
        fs=sample_rate,
        window="hann",
        scaling="spectrum",
    )

    plt.figure(figsize=(10, 5))
    plt.plot(frequencies, power)
    plt.xlim(frequency_limits if frequency_limits is not None else (0, sample_rate / 2))
    plt.xlabel("Frekvens [Hz]")
    plt.ylabel("Signalstyrke")
    plt.title("Frekvensspekter")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Finn data-mappen ved siden av denne filen, uansett hvor skriptet startes.
    data_path = Path(__file__).resolve().parent / "data" / DATA_FILE
    sample_period, data = raspi_import(data_path, channels=CHANNELS)
    sample_rate = 1.0 / sample_period
    signal = data[:, CHANNEL]

    if TIME_START < 0 or (TIME_END is not None and TIME_END <= TIME_START):
        raise ValueError("Tidsområdet må starte ved 0 eller senere og slutte etter starten.")

    # Begge plottypene analyserer bare det valgte tidsutsnittet.
    start_sample = int(round(TIME_START * sample_rate))
    end_sample = None if TIME_END is None else int(round(TIME_END * sample_rate))
    signal = signal[start_sample:end_sample]

    max_frequency = sample_rate / 2 if FREQ_MAX is None else FREQ_MAX
    if not 0 <= FREQ_MIN < max_frequency <= sample_rate / 2:
        raise ValueError("Frekvensområdet må ligge mellom 0 og halve sampleraten, med min < maks.")
    frequency_limits = (FREQ_MIN, max_frequency)

    if PLOT_TYPE == "spectrogram":
        plot_spectrogram(
            signal, sample_rate,
            time_start=start_sample / sample_rate,
            frequency_limits=frequency_limits,
        )
    elif PLOT_TYPE == "spectrum":
        plot_spectrum(signal, sample_rate, frequency_limits=frequency_limits)
    else:
        raise ValueError('PLOT_TYPE må være "spectrogram" eller "spectrum".')
