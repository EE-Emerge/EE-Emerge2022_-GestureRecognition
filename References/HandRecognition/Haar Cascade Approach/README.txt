**Alternative to CNN because the camera does not have enough RAM**

Source for Opencv-master: https://github.com/Aravindlivewire/Opencv
Source for Openmv-master: https://github.com/openmv/openmv

OpenCV is used to create Haar Cascade algorithms, which is then converted to cascade files for use in OpenMV.

-- To convert to cascade files for OpenMV, use "cascade_convert.py".
	-- You can either use WSL or a windows command prompt. In the terminal, go to the directory where the "cascade_convert.py" and the xml file you want to convert, then enter the command: "python3 cascade_convert.py example.xml"

-- Copy/paste the converted ".cascade" file to the camera storage.

-- You can test if it is working by using OpenMV's face detection example and editing LINE 28: 

face_cascade = image.HaarCascade("frontalface", stages=25)


to -----> hand_cascade = image.HaarCascade("example.cascade", stages=25)

You might want to use all stages for better accuracy but "slower process" by changing the line to:

hand_cascade = image.HaarCascade("example.cascade")

I don't know how to use openCV for creating Haar Cascades yet. It might be something you can look at.