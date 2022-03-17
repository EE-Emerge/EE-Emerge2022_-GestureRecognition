# Hand Recognition - By: Paulo - Thu Feb 10 2022

import sensor, image, time, tf
from pyb import LED

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

green = LED(2)

# Threshold of hand
# Adjust as necessary in Tools>>Machine Vision>>Threshold Editor when scene changes
handThreshold = (0, 100, 7, 127, -128, 127)
# (0, 100, 7, 127, -128, 127)
# (67, 100, -3, 29, -128, 127)

# This is the training model implemented by EdgeImpulse, change the file name if necessary
net = tf.load("trained.tflite", load_to_fb=True)
labels = [l.rstrip('\n') for l in open("labels.txt")]


clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()

    green.off()

    detectArea = (20,20,280,200)
    img.draw_rectangle(detectArea, color = (0,255,0), thickness = 1)
    img.draw_string(30, 20, "Detect Area", mono_space=False)

    #scores = net.classify(img, roi = detectArea)[0].output()
    #label = labels[scores.index(max(scores))]
    #img.draw_string(0, 10, label, mono_space=False)


    for blob in img.find_blobs([handThreshold], roi=detectArea, x_stride=5, y_stride=5, pixel_threshold = 500, area_threshold = 7000, merge=True, margin=10):
        #img.draw_rectangle(blob.rect(), color = (255,0,0), thickness = 2)
        img.draw_string(0, 0, "Hand Detected", (255,165,0), mono_space=False)
        #green.on()

        scores = net.classify(img, roi=blob.rect())[0].output()
        label = labels[scores.index(max(scores))]

        img.draw_string(0, 10, label, mono_space=False)





    print(clock.fps())
