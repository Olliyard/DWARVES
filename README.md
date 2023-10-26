# DWARVES
Collection of files created during our Bachelor's project "DWARVES".
All files within are licensed under Apache 2.0.

## Overview
DWARVES, a **D**uck**W**eed **A**utomatic **R**obot for **V**egetal **E**xperimental **S**election, is an automated robotics and vision system designed to select Duckweed based on growth and color for optimal growth characteristics.
The project is developed together with Center for Quantitative Genetics and Genomics (CQGG) at Aarhus University during the fall semester of 2023.

The repository will function as a collection of all the files created throughout the semester, detailing everything that went into creating a finalized DWARVES system, but will mostly focus on the software development throughout the project.

The main parts of the system are as follows.
* A ``user interface`` to start, stop and adjust the settings for the observation interval and incubators.
* A weighted ``loading zone`` which detects if a duckweed colony has been placed.
* A ``robotic arm`` to pick up the duckweed from the ``loading zone`` and place it in a free incubator slot
* Several ``incubators`` which consists of ``RB lights`` and ``heating elements`` to ensure correct lighting and temperature for the colonies.
* A ``camera`` which will capture images of the duckweed throughout the observation interval and store these for later access.
  
Together, all these parts make up the foundations of DWARVES. It is essential that each element works together in unison, for the prototype to be a success.

## Notes for the Raspberry Pi Zero W
--
The current user and password for the RPi to be used during testing stages will be as follows:
Username: pi
Password: raspberry
ip: raspberrypi.local
