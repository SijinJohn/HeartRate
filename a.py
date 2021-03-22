import cv2
import time
path = "videos/PETS09-S1-L1-View001.avi"

# define a video capture object
vid = cv2.VideoCapture(path)

while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    start_time = time.time()
    # Display the resulting frame
    # cv2.imshow('frame', frame)

    green_channel = frame[:, :, 1]
    cv2.imshow('frame_green', green_channel)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("FPS: ", 1.0 / (time.time() - start_time))
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
