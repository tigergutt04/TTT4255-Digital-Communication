# TTT4255-Digital-Communication

Project in **TTT4255 Electronic System Design** at NTNU.

The goal of the project is to build a simple digital communication system using sound and **Frequency Shift Keying (FSK)**.

The system transmits a digital message from an ESP32 to a Raspberry Pi using two different audio frequencies representing binary `0` and `1`. :chatgpt-content-reference{index="0"}

---

## System overview

The system consists of two main parts:

### Transmitter

The transmitter is built around an ESP32 and a speaker.

The ESP32 converts a digital message into a sequence of bits and transmits the bits using FSK:

- `F0` represents binary `0`
- `F1` represents binary `1`

The speaker converts the electrical signal from the ESP32 into sound. :chatgpt-content-reference{index="1"}

### Receiver

The receiver consists of:

- MAX9814 microphone
- MCP3001 ADC
- Raspberry Pi

The microphone converts the sound into an analog electrical signal. The MCP3001 ADC samples the signal and sends the digital measurements to the Raspberry Pi using SPI. :chatgpt-content-reference{index="2"}

The Raspberry Pi records the signal and decodes the transmitted FSK message. :chatgpt-content-reference{index="3"}

---

## Repository structure

```text
TTT4255-Digital-Communication/
│
├── README.md
├── .gitignore
│
├── esp32/
│   └── sender/
│       └── sender.ino
│
├── raspberry-pi/
│   ├── main.py
│   ├── requirements.txt
│   │
│   ├── c/
│   │   ├── adc_sampler.c
│   │   └── Makefile
│   │
│   └── lib/
│       ├── raspi_import.py
│       └── fsk_decoder.py
│
└── docs/
