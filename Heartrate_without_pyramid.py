#####--------This is eulerian heart beat with commented laplacian pyramid
#####--------Output seems to be good. Not sure of accuracy.
import cv2
import numpy as np
import heartrate
import pyramids
import eulerian
from kthread import *

class monitor():
    def __init__(self):
        faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt0.xml")
        cap = cv2.VideoCapture(0)
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))
        print(self.fps)
        self.video_frames = []
        face_rects = ()
        self.frame_count = 0
        self.heart_rate=0
        self.frame_ct=0
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        self.frame_limit=50
        self.freq_min = 1
        self.freq_max = 1.8
        self.face_detected=False
        self.thread_end=True
        self.v1=[]

        while cap.isOpened():
            self.frame_count += 1
            # print(frame_count)
            ret, img = cap.read(0)

            frame = cv2.putText(img,str(self.heart_rate//1)+" "+str(self.face_detected), org, font,
                                fontScale, color, thickness, cv2.LINE_AA)
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            roi_frame = img

            # Detect face
            if len(self.video_frames) == 0:
                face_rects = faceCascade.detectMultiScale(gray, 1.3, 5)


            # Select ROI

            if len(face_rects) > 0:
                # print("Length of face greater than1")
                self.face_detected=True
                for (x, y, w, h) in face_rects:
                    roi_frame = img[y:y + h, x:x + w]
                if roi_frame.size != img.size:
                    roi_frame = cv2.resize(roi_frame, (500, 500))
                    frame = np.ndarray(shape=roi_frame.shape, dtype="float")
                    frame[:] = roi_frame * (1. / 255)

                    self.video_frames.append(frame)
                    cv2.imshow("data", frame)
                    if ((len(self.video_frames)==400) and (self.thread_end==True)):
                        print(str(len(self.video_frames)) + " rawdata-framecount")
                        self.frame_count = 0
                        self.face_detected=False
                        print("process-call")
                        self.v1 = self.video_frames
                        # processing_thread = KThread(target=self.processing(self.v1))
                        processing_thread = KThread(target=self.processing, args=(self.v1,))
                        processing_thread.start()
                        print("process-call-complete")
                        # print("50-----completed")
                        # self.processing()

                        #return video_frames, frame_count, fps
            if len(self.video_frames) == 400:
                self.frame_count = 0

    def processing(self,video):

        print("processing started")
        self.thread_end=False
        print(str(len(video))+" initial-framecount")
        # lap_video = pyramids.build_video_pyramid(video)
        amplified_video_pyramid = []

        for i, vide in enumerate(video):
            # print(i)
            if i == 0 or i == len(video) - 1:
                continue

            # Eulerian magnification with temporal FFT filtering
            # print("Running FFT and Eulerian magnification...")
            result, fft, frequencies = eulerian.fft_filter(vide, self.freq_min, self.freq_max, self.fps)
            # lap_video[i] += result

            # Calculate heart rate
            # print("Calculating heart rate...")
            self.heart_rate = heartrate.find_heart_rate(fft, frequencies, self.freq_min, self.freq_max)
            # print(self.heart_rate)
        # Collapse laplacian pyramid to generate final video
        # print("Rebuilding final video...")
        # amplified_frames = pyramids.collapse_laplacian_video_pyramid(lap_video, self.frame_ct)

        # Output heart rate and final video
            print("Heart rate: ", self.heart_rate, "bpm")
            # print("Displaying final video...")
            print("processing finished")
            self.thread_end = True
            self.video_frames.clear()
            self.v1.clear()
            self.frame_count=0
            self.face_detected = False


obj=monitor()
# obj()