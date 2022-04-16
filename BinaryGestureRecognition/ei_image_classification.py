# Edge Impulse - OpenMV Image Classification Example

import sensor, image, time, os, tf, uos, gc

def most_frequent(List):
    return max(set(List), key = List.count)

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QQCIF) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
sensor.set_auto_whitebal(False) # Turn off white balance.
sensor.set_auto_gain(False)
sensor.set_auto_exposure(False)
clock = time.clock() # Tracks FPS.

net = None
labels = None
TRIGGER_THRESHOLD = 5
low_threshold = (20, 50)
high_threshold = (205, 255)
grayscale_thres = (170, 255)
BG_UPDATE_FRAMES = 50 # How many frames before blending.
BG_UPDATE_BLEND = 30 # How much to blend by... ([0-256]==[0.0-1.0]).
enableBackgroundBlend = False


if not "temp" in os.listdir(): os.mkdir("temp") # Make a temp directory

print("About to save background image...")
sensor.skip_frames(time = 2000) # Give the user time to get ready.
sensor.snapshot().save("temp/bg.bmp")
print("Saved background image - Now frame differencing!")

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    print(e)
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

clock = time.clock()

frame_count = 0
mostLikelyIndex = -1
label_list = []
current_prediction_index = 0

while(True):
    clock.tick()

    img = sensor.snapshot()

    frame_count += 1
    if enableBackgroundBlend  and frame_count > BG_UPDATE_FRAMES:
        frame_count = 0
        # Blend in new frame. We're doing 256-alpha here because we want to
        # blend the new frame into the backgound. Not the background into the
        # new frame which would be just alpha. Blend replaces each pixel by
        # ((NEW*(alpha))+(OLD*(256-alpha)))/256. So, a low alpha results in
        # low blending of the new image while a high alpha results in high
        # blending of the new image. We need to reverse that for this update.
        img.blend("temp/bg.bmp", alpha=(256-BG_UPDATE_BLEND))
        img.save("temp/bg.bmp")

    #if frame_count > 40:
    #    frame_count = 0
    #    current_prediction_index = most_frequent(label_list)
    #    label_list = []

    # Performance using bilateral goes down significantly
    #img.bilateral(3, color_sigma=0.1, space_sigma=1)

    # Replace the image with the "abs(NEW-OLD)" frame difference.
    img.difference("temp/bg.bmp")
    #value = img.get_histogram().get_threshold().value()
    img.binary([(50, 255)])
    #img.binary([(0, value)])
    #img.erode(2)
    #img.dilate(1)

    hist = img.get_histogram()
    # This code below works by comparing the 99th percentile value (e.g. the
    # non-outlier max value against the 90th percentile value (e.g. a non-max
    # value. The difference between the two values will grow as the difference
    # image seems more pixels change.
    diff = hist.get_percentile(0.99).l_value() - hist.get_percentile(0.90).l_value()
    triggered = diff > TRIGGER_THRESHOLD


    # default settings just do one detection... change them to search the image...
    for obj in net.classify(img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
        print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
        img.draw_rectangle(obj.rect())
        # This combines the labels and confidence values into a list of tuples
        predictions_list = list(zip(labels, obj.output()))
        mostLikelyIndex = 0

        for i in range(len(predictions_list)):
            if predictions_list[mostLikelyIndex][1] < predictions_list[i][1]:
                mostLikelyIndex = i
        label_list.append(mostLikelyIndex)
        img.draw_string(0, 0, predictions_list[mostLikelyIndex][0], color = (255, 0, 0), scale = 2,
                        mono_space = False, char_rotation = 0, char_hmirror = False, char_vflip = False,
                        string_rotation = 0, string_hmirror = False, string_vflip = False)

        for i in range(len(predictions_list)):
            print("%s = %f" % (predictions_list[i][0], predictions_list[i][1]))

    print(clock.fps(), "fps")
