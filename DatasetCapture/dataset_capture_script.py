# Hand Data Collection - By: Paulo - Thu Feb 10 2022

import sensor, image, time, tf
from pyb import LED

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

green = LED(2)

# Threshold of hand color
# Adjust as necessary when scene changes
handThreshold = (0, 100, 7, 127, -128, 127)
# (0, 100, 7, 127, -128, 127)
# (67, 100, -3, 29, -128, 127)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()

    green.off()

    detectArea = (20,20,280,200)

    for blob in img.find_blobs([handThreshold], roi=detectArea, pixel_threshold = 300, area_threshold = 5000, merge=True, margin=10):
        green.on()

        # sensor.get_fb().crop(roi=blob.rect())




    print(clock.fps())
