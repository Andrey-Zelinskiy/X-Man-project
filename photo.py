import cv2
import os
import numpy
from PIL import Image

# Не вызывается
recognizer = cv2.face.LBPHFaceRecognizer_create()


def initFC():
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    return faceCascade


def initRC():
    faces, ids = get_images_and_labels(".\\faces")
    recognizer.train(faces, numpy.array(ids))
    recognizer.write('face.yml')
    recognizer.read('face.yml')


# Не вызывается
def get_images_and_labels(path):
    faceCascade = initFC()
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    images = []
    labels = []
    for image_path in imagePaths:
        image_pil = Image.open(image_path).convert('L')
        image = numpy.array(image_pil, 'uint8')
        nbr = int(os.path.split(image_path)[-1].split(".")[1])
        faces = faceCascade.detectMultiScale(image)
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
    return images, labels

# Добавление фото. Принимает: 1) ID, 2) путь к фото


def takePhoto(face_id, path):
    faceCascade = initFC()
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        for count in range(10):
            cv2.imwrite("faces/user." + str(face_id) + "." +
                        str(count) + ".jpg", gray[y:y + h, x:x + w])
    initRC()


# Распознавание принимает 1)путь к фоткеб 2)Словарь id+Name
def recognize(path):
    faceCascade = initFC()
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces1 = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(10, 10),
    )
    id = 1
    for (x, y, w, h) in faces1:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # if (confidence < 100):

        #     name = names[id]
        #     confidence = "  {0}%".format(round(100 - confidence))
        # else:
        #     name = "unknown"
        #     confidence = "  {0}%".format(round(100 - confidence))
        # print(name + ": " + confidence)
    return id
