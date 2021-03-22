import time

import heartrate
import pyramids
import eulerian
import cv2
import numpy as np
import cv2



def processing():
    video=[]
    freq_min = 1
    freq_max = 1.8
    fps = 30

    for i in range(300):
        iimg = cv2.imread('Frames/Frame'+str(i)+'.png')

        video.append(iimg)

    # cv2.imshow('image',video[50])
    # Output img with window name as 'image'

    # Maintain output window utill
    # user presses a key
    cv2.waitKey(0)
    # time.sleep(5)




    # print("processing started")
    # print(str(len(video)) + " initial-framecount")

    lap_video = pyramids.build_video_pyramid(video)
    amplified_video_pyramid = []

    for i, video in enumerate(lap_video):
        # print(i)
        if i == 0 or i == len(lap_video) - 1:
            continue

        # Eulerian magnification with temporal FFT filtering
        # print("Running FFT and Eulerian magnification...")
        result, fft, frequencies = eulerian.fft_filter(video, freq_min, freq_max, fps)
        lap_video[i] += result

        # Calculate heart rate
        # print("Calculating heart rate...")
        heart_rate = heartrate.find_heart_rate(fft, frequencies, freq_min, freq_max)

    # Collapse laplacian pyramid to generate final video
    # print("Rebuilding final video...")
    # amplified_frames = pyramids.collapse_laplacian_video_pyramid(lap_video, self.frame_ct)

    # Output heart rate and final video
    print(heart_rate)
    # print("Displaying final video...")
    # print("processing finished")
    # self.face_detected = False

processing()