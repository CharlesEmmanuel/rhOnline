import cv2
import os
import numpy as np
from PIL import Image
from mysite.settings import BASE_DIR
import dlib

detector = cv2.CascadeClassifier(BASE_DIR + '/employe/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
predictor = dlib.shape_predictor(BASE_DIR + '/employe/shape_predictor_68_face_landmarks.dat')


class FaceRecognition:

    def init(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def faceDetect(self, Entry1):
        face_id = Entry1
        cam = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1

                # Use dlib to detect facial landmarks
                # dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
                # shape = predictor(gray, dlib_rect)

                # Extract the eye landmarks (approximate regions)
                # left_eye_points = np.array([(shape.part(i).x, shape.part(i).y) for i in range(36, 42)])
                # right_eye_points = np.array([(shape.part(i).x, shape.part(i).y) for i in range(42, 48)])

                # Check if eyes are open (you can define your own criteria based on eye movement)
                # left_eye_open = self.are_eyes_open(left_eye_points)
                # right_eye_open = self.are_eyes_open(right_eye_points)

                # if not (left_eye_open and right_eye_open):
                    # If one or both eyes are closed, skip face registration
                    # cv2.putText(img, "Eyes Closed", (x + 5, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    # continue

                # Assuming you have a function to read temperature from the temperature sensor
                # temperature = self.get_temperature()

                # Display temperature on the screen
                # cv2.putText(img, f"Temperature: {temperature} °C", (x + 5, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                # Save the captured image into the datasets folder
                cv2.imwrite(BASE_DIR + '/employe/dataset/User.' + str(face_id) + '.' + str(count) + ".jpg",
                            gray[y:y + h, x:x + w])

                cv2.imshow('Register Face', img)

            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
            elif count >= 30:
                break

        cam.release()
        cv2.destroyAllWindows()

    def trainFace(self):
        # Path for face image database
        path = BASE_DIR + '/employe/dataset'

        # function to get the images and label data
        def getImagesAndLabels(path):

            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []

            for imagePath in imagePaths:

                PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
                img_numpy = np.array(PIL_img, 'uint8')

                face_id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_numpy)

                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(face_id)

            return faceSamples, ids

        print("\n Training faces. It will take a few seconds. Wait ...")
        faces, ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.save(BASE_DIR + '/employe/trainer/trainer.yml')  # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))

    def recognizeFace(self):
        recognizer.read(BASE_DIR + '/employe/trainer/trainer.yml')
        cascadePath = BASE_DIR + '/employe/haarcascade_frontalface_default.xml'
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        confidence = 0

        # Retriving names from database
        # data = conn.execute('''select * from facedata''')
        # for x in data:
        #     names.append(x[1])

        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)

        # Define min window size to be recognized as a face
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                face_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                if (confidence < 100):
                    name = 'Detected'
                else:
                    name = "Unknown"

                cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

                temperature = self.get_temperature()

                cv2.putText(img, f"Temperature: {temperature} °C", (x + 5, y + h + 25), font, 1, (255, 255, 255), 2)

            cv2.imshow('Detect Face', img)
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break
            if confidence > 50:
                break

        print("\n Exiting Program")
        cam.release()
        cv2.destroyAllWindows()

        return face_id

    def are_eyes_open(self, eye_landmarks):
        eye_height = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        eye_open_threshold = 0.2
        return eye_height > eye_open_threshold

    def get_temperature(self):
        return round(np.random.uniform(36.0, 37.5), 1)

