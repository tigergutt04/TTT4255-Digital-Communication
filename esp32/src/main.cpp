#include <Arduino.h>

const int BUZZER_PIN = 25;
const int ZERO_HZ = 500;
const int ONE_HZ = 4000;
const int BIT_DURATION_MS = 20;

void sendBit(bool bit) {
    tone(BUZZER_PIN, bit ? ONE_HZ : ZERO_HZ);
    delay(BIT_DURATION_MS);
}

void sendByte(uint8_t value) {
    // Send the most significant bit first.
    for (int i = 7; i >= 0; --i) {
        sendBit((value >> i) & 1);
    }
}

void sendMessage(const char* message) {
    while(*message) {
        sendByte(static_cast<uint8_t>(*message));
        ++message;
    }
    noTone(BUZZER_PIN);
}

void setup() {
    pinMode(BUZZER_PIN, OUTPUT);   
}

void loop() {
    sendMessage("Hi");
    delay(2000);
}
