---
layout: default
title: Software
description: OpenMV Camera and MSP430 Logic for Gesture Recognition
---

# How was the Gesture Recognition Processed?

## OpenMV Camera
The gesture recognition of our project is centered around the use of an OpenMV camera and a training model from EdgeImpulse. It starts by taking picture of the background using it as a basis for background subtraction. After determining the difference of the current image and the background image, a binary filter was used to more cleanly define the hand shape. The conversion to binary images had solved multiple issues such as providing smaller image sizes, circumventing skin color issues, etc. Afterwards, the image is classified by the training model we have on the SD card and thus, we have our detection of an open, closed, and blank state. The state is then communicated to the MSP430 through UART.
<video src="https://github.com/EE-Emerge/EE-Emerge2022_GestureRecognition/blob/gh-pages/assets/css/SoftwareDemo.mov" controls="controls" style="max-width: 730px;">
</video>


## MSP430

The control for the motors is based on the MSP430 from TI. The microcontroller receives the state of the camera through UART and uses that to determine which rotation the motor should be in. The rotation of the motor is controlled through Pulse Width Modulation(PWM). The Energia IDE was used as an alternative to Code Composer Studio due to its simpler nature.

# Justifications
## OpenMV Camera

The decision to use the OpenMV camera was founded in multiple reasons. We wanted to have an easy to use implementation of computer vision. Having python as an interface for the camera made rapid prototyping more convenient. An added benefit to using the OpenMV camera was their emphasis on supporting machine learning through the use of Convolution Neural Networks(CNN).

## MSP430

The use of the MSP430 was the result of a desire to divide the logic of the motors from the camera due to the memory constraints and allows for more segmented logic. This also makes it easier to connect to a driver board so that potentially in the future, individual finger control could be implemented.
