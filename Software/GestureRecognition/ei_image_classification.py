import sensor, image, time, os, tf, uos, gc

# determine the most repeated value
def most_frequent(List):
    return max(set(List), key = List.count)

# Setting up the sensors
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QQCIF) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
sensor.set_auto_whitebal(False) # Turn off white balance.
sensor.set_auto_gain(False)
sensor.set_auto_exposure(False)
clock = time.clock() # Tracks FPS.

# Initialize variables
net = None
labels = None
TRIGGER_THRESHOLD = 5
frame_count = 0
mostLikelyIndex = -1
label_list = []
current_prediction_index = 0
enableBackgroundBlend = False
BG_UPDATE_FRAMES = 50

if not "temp" in os.listdir(): os.mkdir("temp") # Make a temp directory

# Takes a picture to subtract background on launch
print("About to save background image...")
sensor.skip_frames(time = 2000) # Give the user time to get ready.
sensor.snapshot().save("temp/bg.bmp")
print("Saved background image - Now frame differencing!")

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading (File from EdgeImpulse)
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    print(e)
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

# Loading Labels for the training model
try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

clock = time.clock()

while(True):
    clock.tick()

    img = sensor.snapshot()
    
    frame_count += 1
    # Unused but capable of learning small changes in background 
    if enableBackgroundBlend  and frame_count > BG_UPDATE_FRAMES:
        frame_count = 0
        img.blend("temp/bg.bmp", alpha=(256-BG_UPDATE_BLEND))
        img.save("temp/bg.bmp")

    # Replace the image with the "abs(NEW-OLD)" frame difference.
    img.difference("temp/bg.bmp")
    # Convert the difference grayscale into a binary image
    img.binary([(50, 255)])

    # default settings just do one detection... change them to search the image...
    for obj in net.classify(img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
        print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
        img.draw_rectangle(obj.rect())
        # This combines the labels and confidence values into a list of tuples
        predictions_list = list(zip(labels, obj.output()))
        mostLikelyIndex = 0

        # determine the modt likely index every frame
        for i in range(len(predictions_list)):
            if predictions_list[mostLikelyIndex][1] < predictions_list[i][1]:
                mostLikelyIndex = i
        label_list.append(mostLikelyIndex)
        
        # uses the mostLikelyIndex to write on screen when connected to a display or computer
        img.draw_string(0, 0, predictions_list[mostLikelyIndex][0], color = (255, 0, 0), scale = 2,
                        mono_space = False, char_rotation = 0, char_hmirror = False, char_vflip = False,
                        string_rotation = 0, string_hmirror = False, string_vflip = False)

        # prints out to serial terminal all the expected values
        for i in range(len(predictions_list)):
            print("%s = %f" % (predictions_list[i][0], predictions_list[i][1]))

    print(clock.fps(), "fps")
