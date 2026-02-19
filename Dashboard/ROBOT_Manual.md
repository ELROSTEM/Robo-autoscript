# VEX ROBOTC Command Reference Manual

## Drive Base Logic (CRITICAL)
* If the robot is a **2-wheel drive**, use only `leftMotor` and `rightMotor`.
* If the robot is a **4-wheel drive**, you MUST apply all left-side power to BOTH `leftMotor` and `leftrearMotor`. You MUST apply all right-side power to BOTH `rightMotor` and `rightrearMotor`.

## Move Forward
Description: Moves the robot straight forward. All drive motors must be set to a positive value.
Syntax (2-Wheel Example): 
motor[leftMotor] = 50;
motor[rightMotor] = 50;
wait1Msec(1000);

## Move Backward
Description: Reverses the robot in a straight line. All drive motors must be set to a negative value.
Syntax (2-Wheel Example):
motor[leftMotor] = -50;
motor[rightMotor] = -50;
wait1Msec(1000);

## Pivot Turn Left
Description: Spins the robot to the left in place. The left motors go backward (-50), the right motors go forward (50).
Syntax (2-Wheel Example):
motor[leftMotor] = -50;
motor[rightMotor] = 50;
wait1Msec(500);

## Pivot Turn Right
Description: Spins the robot to the right in place. The left motors go forward (50), the right motors go backward (-50).
Syntax (2-Wheel Example):
motor[leftMotor] = 50;
motor[rightMotor] = -50;
wait1Msec(500);

## Stop Motors
Description: Halts all movement immediately.
Syntax (2-Wheel Example):
motor[leftMotor] = 0;
motor[rightMotor] = 0;