#pragma config(Motor,  port2,           rightMotor,    tmotorNormal, openLoop, reversed)
#pragma config(Motor,  port3,           leftMotor,     tmotorNormal, openLoop)

/*
Program Description: This program is a RobotC program

Robot Description: The robot has 2 motors with 4 wheels.
*/

task main()
{
   // 1. go forward for 1 seccond
  motor[rightMotor] = 50;
  motor[leftMotor] = 50;
  wait1Msec(1000);
   // 2. spin for 3 seconds


   // 3. Stop


