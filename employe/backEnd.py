import cv2
import os
import numpy as np
from PIL import Image
from mysite.settings import BASE_DIR
# import dlib

detector = cv2.CascadeClassifier(BASE_DIR + '/employe/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
# predictor = dlib.shape_predictor(BASE_DIR + '/employe/shape_predictor_68_face_landmarks.dat')


class FaceRecognition:

    def init(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def faceDetect(self, Entry1, ):
        print("Etape 1")
        face_id = Entry1
        # face_name = Entry2
        # try:
        #     conn.execute('''insert into facedata values ( ?, ?)''', (face_id, face_name))
        #     conn.commit()
        # except sqlite3.IntegrityError:
        #     print("\n ERROR! This id alreeady exists in database!")
        #     print("\n Try agian with new id\n")
        #     exit()
        print("Etape 2")

        cam = cv2.VideoCapture(0)
        print("Etape 3")

        count = 0

        while (True):

            ret, img = cam.read()
            print("Etape 4 while")

            # img = cv2.flip(img, -1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                print("Etape 5 for")

                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1

                # Save the captured image into the datasets folder
                if count < 10:

                    cv2.imwrite(BASE_DIR + '/employe/dataset/User.' + str(face_id) + '.' + str(count) + ".jpg",
                                gray[y:y + h, x:x + w])

                cv2.imshow('Register Face', img)
                print("Etape 6 for")

            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break


        cam.release()
        cv2.destroyAllWindows()

    def trainFace(self):
        print("Etape 7 train")
        # Path for face image database
        path = BASE_DIR + '/employe/dataset'
        print("Etape 8")

        # function to get the images and label data
        def getImagesAndLabels(path):
            print("Etape 9")

            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []

            for imagePath in imagePaths:
                print("Etape 10 for getimage")

                PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
                img_numpy = np.array(PIL_img, 'uint8')

                face_id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_numpy)

                for (x, y, w, h) in faces:
                    print("Etape 11 xywh in faces")
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
            # faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)



                face_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                if (confidence > 100):

                    name = 'Detected'
                    print("Reconnu ")
                    print("confidence", str(confidence), 'Id face ', str(face_id))

                else:
                    print("confidence", str(confidence), 'Id face ', str(face_id))
                    name = "Unknown"
                    print("Non Reconnu ")


                cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

                temperature = self.get_temperature()

                cv2.putText(img, f"Temperature: {temperature} °C", (x + 5, y + h + 25), font, 1, (255, 255, 255), 2)

            cv2.imshow('Detect Face', img)
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break
            if confidence > 70:
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

