---
layout: default
title: Hardware
description: Rechargable Battery
---




# Power Delivery
We wanted create a rechargeable battery system that would power all the electronics of the circuit and meet the different voltage and current demands of each part. The motivation was to have the system to be modular, portable, and wireless.

## Battery Decision
One of our main concerns for power was also the battery size. We had to estimate and determine the power consumption of the camera, msp, and servo motors and be mindful of how much current is drawn from each voltage source. 
Using the power calculated we could determine the amount of time our device would run with different battery sizes (mA/h). 

We had to consider two issues for **safety**:
1. Consider the safety of the LiPo battery storage 
2. Consider the possibility of having reverse current protection to prevent the servos from damaging the battery when reaching stall torque

As a result, we eventually used Polymer Battery 3.7V 6000mAh, specifically 932-MIKROE-4475.

## Revision 1
<p align="center">
  <img width="460" height="460" src="https://github.com/EE-Emerge/EE-Emerge2022_GestureRecognition/blob/gh-pages/assets/css/power%20first%20iteration.PNG?raw=true">
</p>


As a result, we used the LTC4056 as the main charging IC 
It is a low cost, single-cell, constant-current/ constant-voltage Li-Ion battery charger controller with a programmable termination timer. When combined with a few external components, the LTC4056 forms a very small standalone charger for single cell lithium-ion batteries.
**Safety:** Use the DW01A protection IC to prevent damage or failures caused by overcharge, overdischarge, or overcurrent. 

### Improvements
After developing our projects further, we realized we wanted to make changes to meet our new demands:

1. Implement micro-usb to charge system
1. Implement a way to power the device while charging

## Revision 2
<p align="center">
  <img width="460" height="460" src="https://github.com/EE-Emerge/EE-Emerge2022_GestureRecognition/blob/gh-pages/assets/css/power%20second%20iteration.PNG?raw=true">
</p>
Change: Implemented micro-usb as a way to charge the system
Change: Added LTC4412 Low Loss PowerPath Controller IC 
The LTC4412 controls an external P-channel MOSFET to create a near ideal diode function for power switchover or load sharing. This permits highly efficient OR’ing of multiple power sources for extended battery life and low self-heating
Simply put, it allows us to run the device via a power cable while it is being charged. 

# Hand Movement
We considered two option for the control of fingers:
1. Linear Actuators
2. Servo Motors

We had also ran into the issues of how to control the servos. Initially the Micro Maestro was used as the control but eventually moved to MSP430.

## Our Choice: Servo Motor (Hi Torque MG996R)
The servo motors were chosen as a solution due to size and ability to create a sufficient torque to open and close fingers.

### Linear Actuators and their issues
<p align="center">
  <img width="460" height="460" src="https://github.com/EE-Emerge/EE-Emerge2022_GestureRecognition/blob/gh-pages/assets/css/servo%20motor%20linear%20actuator.PNG?raw=true">
</p>
Linear actuators would've been very ideal and useful in controlling the fingers. They are the best option for straight, smooth, direct control of the fingers. Some could be used to determine how far and the force being applied on the actuator with their support for closed feedback systems.

Although these would be great for more advanced implementations of hands, they aren't ideal for our situation due to a number of issues:
1. Cost
2. Only need to open and close hand (more features than necessary)

## Our Choice: MSP 430 Microcontroller
The MSP430 was chosen as the main control for the servos due to its easy and flexible scripting features, simple UART communication (through Energia IDE), and lower power usage. 

### Micro Maestro 6-Channel USB Servo Controller
The Micro Maestro would have been used to create PWM signals necessary to drive each of the motors and motions individually.
**Advantage:** More fingers could be moved independently versus MSP430's support for 2 channels of PWM signals
**Disadvantage:** Issues getting the board to communicate and interface was more limited than the MSP430.
