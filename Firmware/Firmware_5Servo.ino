#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// =================================================
// 1. HARDWARE CONFIGURATION
// =================================================

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

#define SDA_PIN 21
#define SCL_PIN 22
#define PWM_FREQ 50

#define NUM_SERVOS 5

// =================================================
// 2. SERVO STATES
// =================================================

enum ServoState {
  IDLE,
  CLOSING,
  OPENING
};

struct ServoConfig {
  const char* name;
  char commandID;
  uint8_t channel;

  uint16_t closePulse;
  uint32_t closeTime;

  uint16_t openPulse;
  uint32_t openTime;

  uint16_t stopPulse;
};

struct ServoRuntime {
  ServoState state;
  uint32_t startTime;
};

// =================================================
// 3. SERVO CALIBRATION DATA
// =================================================

ServoConfig servos[NUM_SERVOS] = {

  // Name       ID  CH  Close  Time    Open   Time    Stop

  {"Vang",      'Y', 0, 1800, 50000, 1200, 10000, 1600},

  {"Do",        'R', 1, 1800,  6000, 1200,  2000, 1700},

  {"Xanh la",   'G', 2, 1800, 10000, 1200,  4000, 1700},

  {"Cam",       'O', 3, 2100,  4000, 1200,  4000, 1700},

  {"Nau",       'B', 4, 2100, 10000, 1200,  8000, 1700}
};

ServoRuntime runtimeData[NUM_SERVOS];

// =================================================
// 4. SERIAL COMMAND BUFFER
// =================================================

char commandBuffer[16];
uint8_t commandIndex = 0;

// =================================================
// 5. PWM CONVERSION
// =================================================

uint16_t pulseToTicks(uint16_t pulseUs) {

  return (uint16_t)(
    (uint32_t)pulseUs * 4096UL / 20000UL
  );
}

// =================================================
// 6. SERVO OUTPUT
// =================================================

void writeServo(uint8_t index, uint16_t pulseUs) {

  pwm.setPWM(
    servos[index].channel,
    0,
    pulseToTicks(pulseUs)
  );
}

void stopServo(uint8_t index) {

  writeServo(index, servos[index].stopPulse);

  runtimeData[index].state = IDLE;

  Serial.print(servos[index].name);
  Serial.println(" -> STOP");
}

// =================================================
// 7. START SERVO MOVEMENT
// =================================================

void closeServo(uint8_t index) {

  writeServo(index, servos[index].closePulse);

  runtimeData[index].state = CLOSING;
  runtimeData[index].startTime = millis();

  Serial.print(servos[index].name);
  Serial.println(" -> CLOSING");
}

void openServo(uint8_t index) {

  writeServo(index, servos[index].openPulse);

  runtimeData[index].state = OPENING;
  runtimeData[index].startTime = millis();

  Serial.print(servos[index].name);
  Serial.println(" -> OPENING");
}

// =================================================
// 8. UPDATE EACH SERVO INDEPENDENTLY
// =================================================

void updateServo(uint8_t index) {

  uint32_t currentTime = millis();

  if (runtimeData[index].state == CLOSING) {

    if (currentTime - runtimeData[index].startTime
        >= servos[index].closeTime) {

      stopServo(index);
    }
  }

  else if (runtimeData[index].state == OPENING) {

    if (currentTime - runtimeData[index].startTime
        >= servos[index].openTime) {

      stopServo(index);
    }
  }
}

void updateAllServos() {

  for (uint8_t i = 0; i < NUM_SERVOS; i++) {
    updateServo(i);
  }
}

// =================================================
// 9. CONTROL ALL SERVOS
// =================================================

void closeAll() {

  for (uint8_t i = 0; i < NUM_SERVOS; i++) {
    closeServo(i);
  }
}

void openAll() {

  for (uint8_t i = 0; i < NUM_SERVOS; i++) {
    openServo(i);
  }
}

void stopAll() {

  for (uint8_t i = 0; i < NUM_SERVOS; i++) {
    stopServo(i);
  }
}

// =================================================
// 10. SHOW SERVO STATUS
// =================================================

void showStatus() {

  Serial.println();
  Serial.println("====== SERVO STATUS ======");

  for (uint8_t i = 0; i < NUM_SERVOS; i++) {

    Serial.print(servos[i].name);
    Serial.print(" : ");

    switch (runtimeData[i].state) {

      case IDLE:
        Serial.println("IDLE");
        break;

      case CLOSING:
        Serial.println("CLOSING");
        break;

      case OPENING:
        Serial.println("OPENING");
        break;
    }
  }

  Serial.println("==========================");
}

// =================================================
// 11. PROCESS SERIAL COMMAND
// =================================================

void processCommand(char* command) {

  // Convert lowercase to uppercase
  for (uint8_t i = 0; command[i] != '\0'; i++) {

    if (command[i] >= 'a' && command[i] <= 'z') {
      command[i] -= 32;
    }
  }

  // Global commands
  if (strcmp(command, "ALLC") == 0) {
    closeAll();
    return;
  }

  if (strcmp(command, "ALLO") == 0) {
    openAll();
    return;
  }

  if (strcmp(command, "ALLS") == 0) {
    stopAll();
    return;
  }

  if (strcmp(command, "STATUS") == 0) {
    showStatus();
    return;
  }

  // Individual servo commands
  if (strlen(command) != 2) {
    Serial.println("ERROR: Invalid command");
    return;
  }

  int index = -1;

  for (uint8_t i = 0; i < NUM_SERVOS; i++) {

    if (command[0] == servos[i].commandID) {
      index = i;
      break;
    }
  }

  if (index < 0) {
    Serial.println("ERROR: Servo not found");
    return;
  }

  switch (command[1]) {

    case 'C':
      closeServo(index);
      break;

    case 'O':
      openServo(index);
      break;

    case 'S':
      stopServo(index);
      break;

    default:
      Serial.println("ERROR: Invalid action");
      break;
  }
}

// =================================================
// 12. NON-BLOCKING SERIAL READER
// =================================================

void readSerialCommand() {

  while (Serial.available() > 0) {

    char c = Serial.read();

    if (c == '\n' || c == '\r') {

      if (commandIndex > 0) {

        commandBuffer[commandIndex] = '\0';

        processCommand(commandBuffer);

        commandIndex = 0;
      }
    }

    else {

      if (commandIndex < sizeof(commandBuffer) - 1) {

        commandBuffer[commandIndex++] = c;
      }

      else {

        commandIndex = 0;
        Serial.println("ERROR: Command too long");
      }
    }
  }
}

// =================================================
// 13. SETUP
// =================================================

void setup() {

  Serial.begin(115200);

  Wire.begin(SDA_PIN, SCL_PIN);

  pwm.begin();
  pwm.setPWMFreq(PWM_FREQ);

  delay(10);

  // Initialize all servos
  for (uint8_t i = 0; i < NUM_SERVOS; i++) {

    runtimeData[i].state = IDLE;
    runtimeData[i].startTime = 0;

    writeServo(i, servos[i].stopPulse);
  }

  Serial.println();
  Serial.println("================================");
  Serial.println("     ROBOT HAND - 5 SERVO");
  Serial.println("================================");

  Serial.println("Y C/O/S : Yellow");
  Serial.println("R C/O/S : Red");
  Serial.println("G C/O/S : Green");
  Serial.println("O C/O/S : Orange");
  Serial.println("B C/O/S : Brown");

  Serial.println("--------------------------------");
  Serial.println("ALLC    : Close all fingers");
  Serial.println("ALLO    : Open all fingers");
  Serial.println("ALLS    : Stop all servos");
  Serial.println("STATUS  : Show servo status");
  Serial.println("--------------------------------");
  Serial.println("System READY!");
}

// =================================================
// 14. MAIN LOOP
// =================================================

void loop() {

  readSerialCommand();

  updateAllServos();

}
