#include <Arduino.h>

const int BUZZER_PIN = 14;
const int ZERO_HZ = 1200;
const int ONE_HZ = 2200;
const int BIT_DURATION_MS = 200;

const uint8_t START_SIGNAL[] = {1, 1, 0, 0, 1, 1};
const uint8_t STOP_SIGNAL[] = {1, 1, 0, 0, 1, 1};

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
    // Send Barker-startsekvensen før teksten.
    for (uint8_t bit : START_SIGNAL) {
        sendBit(bit);
    }

    while (*message) {
        sendByte(static_cast<uint8_t>(*message));
        ++message;
    }

    for (uint8_t bit : STOP_SIGNAL){
        sendBit(bit);
    }
    noTone(BUZZER_PIN);
}

void setup() {
    pinMode(BUZZER_PIN, OUTPUT);   
}

void loop() {
    sendMessage("Hello");
    delay(2000);

}
