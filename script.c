#pragma config(Motor,  port2,           rightMotor,    tmotorNormal, openLoop, reversed)
#pragma config(Motor,  port3,           leftMotor,     tmotorNormal, openLoop)

/*
Program Description: This program is a RobotC program

Robot Description: The robot has 2 motors with 4 wheels.
*/

task main()
{
   // 1. spin for 2 seconds
	int speed = 50;
	motor[leftMotor] = speed;
	motor[rightMotor] = -speed;
	wait1Msec(2000);
   // 2. go forward
	motor[leftMotor] = speed;
	motor[rightMotor] = speed;
	wait1Msec(2000);

   // 3. Stop
	motor[leftMotor] = 0;
	motor[rightMotor] = 0;
}
