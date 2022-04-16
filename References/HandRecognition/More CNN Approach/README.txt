**Alternative to Edge-Impulse**

Tensorflow's gesture classification example:
https://github.com/tensorflow/examples/tree/master/lite/examples/gesture_classification/web


-- Run index.html from "examples-master/lite/examples/gesture_classfication/web"

-- Collect picture samples and train the model

-- Three files will be downloaded: models.json, model.weights.bin, and labels.text

-- To convert the model to tflite, follow and run the steps here: 
https://colab.research.google.com/github/tensorflow/examples/blob/master/lite/examples/gesture_classification/ml/tensorflowjs_to_tflite_colab_notebook.ipynb

-- You will upload models.json and model.weights.bin when prompted.

-- Finishing all the steps from the conversion will give you model.tflite

-- Put the model.tflite and labels.txt in the camera

*The camera will not run again because there is not enough ram. However, assuming that everything worked fine, then this process makes things easier because we are using pretrained models that work really well if the camera just have enough ram. We might be able to reuse this model for the project if we can just change the name of the gestures from the index.html and labels.txt. Also, if you can figure out a way to reduce the picture sample resolution from 224*224 to 128*128 which is the minimum it might work, but I don't know how to.

The base model specification is listed here. They said size and width can be "varied", but I have no idea how.
https://github.com/tensorflow/examples/blob/master/lite/examples/gesture_classification/web/README.md