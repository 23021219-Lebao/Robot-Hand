#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

void servoControl(int pulse) {
    int ticks = pulse * 4096 / 20000;
    pwm.setPWM(0, 0, ticks);
}

void setup() {
    Wire.begin(21, 22);
    pwm.begin();
    pwm.setPWMFreq(50);
}

void loop() {
    servoControl(1800);
    delay(4000);

    servoControl(1600);
    delay(2000);

    servoControl(1200);
    delay(5000);
}
