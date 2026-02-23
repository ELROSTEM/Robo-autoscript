# VEX ROBOTC Command Reference Manual

## Drive Base Logic (CRITICAL)
* If the robot is a **2-wheel drive**, use only `leftMotor` and `rightMotor`.
* If the robot is a **4-wheel drive**, you MUST apply all left-side power to BOTH `leftMotor` and `leftrearMotor`. You MUST apply all right-side power to BOTH `rightMotor` and `rightrearMotor`.

### Move Forward
Description: Moves the robot straight forward. All drive motors must be set to a positive value.
Syntax (2-Wheel Example): 
motor[leftMotor] = 50;
motor[rightMotor] = 50;
wait1Msec(1000);

### Move Backward
Description: Reverses the robot in a straight line. All drive motors must be set to a negative value.
Syntax (2-Wheel Example):
motor[leftMotor] = -50;
motor[rightMotor] = -50;
wait1Msec(1000);

### Pivot Turn Left
Description: Spins the robot to the left in place. The left motors go backward (-50), the right motors go forward (50).
Syntax (2-Wheel Example):
motor[leftMotor] = -50;
motor[rightMotor] = 50;
wait1Msec(500);

### Pivot Turn Right
Description: Spins the robot to the right in place. The left motors go forward (50), the right motors go backward (-50).
Syntax (2-Wheel Example):
motor[leftMotor] = 50;
motor[rightMotor] = -50;
wait1Msec(500);

### Stop Motors
Description: Halts all movement immediately.
Syntax (2-Wheel Example):
motor[leftMotor] = 0;
motor[rightMotor] = 0;

## ARM AND MANIPULATOR COMMANDS

### Raise Arm
Description: Moves the robotic arm upward to lift an object.
Syntax:
motor[armMotor] = 60;
wait1Msec(1000);
motor[armMotor] = 0;

### Lower Arm
Description: Moves the robotic arm downward.
Syntax:
motor[armMotor] = -40;
wait1Msec(1000);
motor[armMotor] = 0;

### Grab Object (Close Claw)
Description: Closes the gripper to hold an object. Applies a small amount of continuous power afterward to maintain grip without stalling the motor.
Syntax:
motor[clawMotor] = 50;
wait1Msec(500);
motor[clawMotor] = 15;

### Release Object (Open Claw)
Description: Opens the gripper to drop an object.
Syntax:
motor[clawMotor] = -50;
wait1Msec(500);
motor[clawMotor] = 0;