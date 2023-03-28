import face_recognition
import cv2
from random import randint
import numpy as np
# from PIL import Image, ImageDraw


def getColor():
    r = randint(128, 255)
    g = randint(128, 255)
    b = randint(128, 255)
    rand_color = (r, g, b)
    return rand_color


destination_img = './images/salman.jpeg'

firstface1 = face_recognition.load_image_file(destination_img)


face_landmarks_list = face_recognition.face_landmarks(firstface1)

face_locations = face_recognition.face_locations(firstface1)

first_face_encoding = face_recognition.face_encodings(firstface1)

n_faces = len(first_face_encoding)

print(n_faces, face_locations)


img = cv2.imread(destination_img)


colors = {"chin": (0, 0, 255),
          "left_eyebrow": (0, 255, 0),
          "right_eyebrow": (0, 255, 0),
          #   "right_eyebrow": (254, 182, 189),
          "nose_bridge": (134, 153, 137),
          "nose_tip": (222, 137, 212),
          "left_eye": (255, 0, 0),
          "right_eye": (255, 0, 0),
          #   "right_eye": (177, 231, 245),
          "top_lip": (233, 223, 158),
          "bottom_lip": (233, 223, 158),
          #   "bottom_lip": (174, 177, 200)
          }


for facePart in face_landmarks_list[0]:
    # print(facePart)
    color = getColor()
    # print('\"'+facePart+'\":', color, ',')
    color = colors[facePart]
    facePartPoints = face_landmarks_list[0][facePart]
    for point in facePartPoints:
        # print(point)
        img = cv2.circle(img, point, radius=1, color=color, thickness=2)
    # print('\n')


cv2.imwrite('./images/resut.png', img)


# pil_image = Image.fromarray(cv2.imread(destination_img))

# d = ImageDraw.Draw(pil_image)


# print(face_landmarks_list[0]['left_eyebrow'])

# d.polygon(face_landmarks_list[0]['left_eyebrow'],)
# pil_image.save("./images/resut2.png")


img = cv2.imread(destination_img)


for facePart in face_landmarks_list[0]:
    color = colors[facePart]
    facePartPoints = face_landmarks_list[0][facePart]

    pts = np.array(facePartPoints,
                   np.int32)
    pts = pts.reshape((-1, 1, 2))
    img = cv2.polylines(img, [pts],
                        not facePart == 'chin', color, 2)

cv2.imwrite('./images/resut2.png', img)


img = cv2.imread(destination_img)

top, right, bottom, left = face_locations[0]
start_point = (left, top)
end_point = (right, bottom)


img = cv2.rectangle(img, start_point, end_point, (0, 0, 255), 2)


cv2.imwrite('./images/resut3.png', img)


cropped_face = img[top:bottom, left:right]

cv2.imwrite('./images/resut4.png', cropped_face)


print(first_face_encoding[0].shape)
