#pragma config(Motor,  port2,           rightMotor,    tmotorNormal, openLoop, reversed)
#pragma config(Motor,  port3,           leftMotor,     tmotorNormal, openLoop)

/*
Program Description: This program is a RobotC program

Robot Description: The robot has 2 motors with 4 wheels.
*/

task main()
{
   // 1. dance for 10 seconds
	int time = 0;
	while(time < 10)
	{
		motor[rightMotor] = 50;
		motor[leftMotor] = 50;
		wait1Msec(1000);
		motor[rightMotor] = -50;
		motor[leftMotor] = -50;
		wait1Msec(1000);
		time = time + 1;
	}
   // 2. turn left for 2 seconds
	motor[rightMotor] = 50;
	motor[leftMotor] = -50;
	wait1Msec(2000);

   // 3. Stop
	motor[rightMotor] = 0;
	motor[leftMotor] = 0;
}
