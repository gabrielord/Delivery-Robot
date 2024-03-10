#ifndef PARAMETERS_H
#define PARAMETERS_H

#define SERIAL_BAUD 115200
#define SPEED_LEFT 6
#define DIRECTION_LEFT 7

#define SPEED_RIGHT 5
#define DIRECTION_RIGHT 4
//#define MOTOR_PIN 3
//#define DIRECTION_PIN 4
//#define SERVOMOTOR_PIN 6

// Initial angle of the servomotor
#define GAP 7
#define INITIAL_THETA 90+GAP
// Min and max values for servomotor
#define THETA_MIN 80 + GAP
#define THETA_MAX 100 + GAP

#define SPEED_MAX 200
// If DEBUG is set to true, the arduino will send back all the received messages
#define DEBUG false

#endif
