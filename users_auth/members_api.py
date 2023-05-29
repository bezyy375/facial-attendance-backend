from rest_framework import viewsets, mixins, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users_auth.models import Member
from authatt.settings import BASE_DIR
import os
import cv2
import numpy as np

import face_recognition


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


# Create your views here.
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["id", "name", "picture", "organization"]
        read_only_field = ["id"]


class MemberViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Member.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        test_file = self.request.FILES.get('picture')
        destination_dir = str(BASE_DIR)+'/media/test_pic_val/'

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        destination_img = destination_dir+'/' + test_file.name
        if (len(destination_img.split('.')) == 1):
            destination_img = destination_img+".png"
        destination = open(destination_img, 'wb+')

        for chunk in test_file.chunks():
            destination.write(chunk)
        destination.close()

        cv2.imwrite(destination_img, image_resize(
            cv2.imread(destination_img), width=500))

        # image validator
        firstface1 = face_recognition.load_image_file(destination_img)
        first_face_encoding = face_recognition.face_encodings(firstface1)
        n_faces = len(first_face_encoding)

        if (n_faces == 0):
            return Response(
                {
                    "success": False,
                    "msg": "Invalid Image. Found no face in image.",
                    "n_faces": n_faces
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        elif (n_faces > 1):
            return Response(
                {
                    "success": False,
                    "msg": "Invalid Image. Found multiple faces in image.",
                    "n_faces": n_faces
                },
                status=status.HTTP_412_PRECONDITION_FAILED,
            )

        known_face_encodings = []
        known_face_names = []
        known_face_regions = []

        face_locations = []
        face_encodings = []
        face_names = []
        path = 'media/member'

        filenames = os.listdir(path)
        for filename in filenames:

            print('Feeding', filename)
            if ('.DS_Store' in filename):
                continue
            try:
                # if (True):
                if len(known_face_names) < 70:
                    feed_image_path = path + "/" + filename
                    feed_image = face_recognition.load_image_file(
                        feed_image_path)
                    feed_image_encoding = face_recognition.face_encodings(
                        feed_image)

                    if (not len(feed_image_encoding) == 1):
                        print('Ignoring Face Feed for ', feed_image_path)
                        continue

                    known_face_encodings.append(feed_image_encoding[0])
                    # name = os.path.splitext(filename)[0]
                    known_face_names.append(filename)
                    known_face_regions.append(str(dir))

            except Exception as e:
                print('Exception Raised in Feeding!!', e)
                pass

        results = face_recognition.compare_faces(
            known_face_encodings, first_face_encoding[0])
        print('/n/nMatching Results:\n', results, '\n\n')

        if True in results:

            first_match_index = results.index(True)
            founname = known_face_names[first_match_index]
            userIDFound = founname.split('.')[0]
            # print("UserID", founname, userIDFound)

            member = Member.objects.get(id=userIDFound)

            return Response(
                {
                    "success": False,
                    "msg": "Member Already registered. (ID: {t_memberID}, Name:{t_memberName}) ".format(t_memberID=member.id, t_memberName=member.name),
                    "member":  {"id": member.id, "name": member.name, "organization": member.organization.name, },
                },
                status=status.HTTP_412_PRECONDITION_FAILED,
            )

        member = serializer.save()

        # storing images
        createdMemberID = str(member.id)
        # createdMemberID = 'af5fbc8d-e13d-4738-a12c-e700b8c8f1ff'
        destination_dir = str(BASE_DIR)+'/media/member/'+createdMemberID+'/'
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        originalImagePath = destination_dir+'original.png'
        faceBoundaryImagePath = destination_dir+'face_boundary.png'
        faceLMsImagePath = destination_dir+'face_landmarks.png'
        faceCroppedImagePath = destination_dir+'face_cropped.png'

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

        # Original Image
        cv2.imwrite(originalImagePath, cv2.imread(destination_img))

        # Face Locations/Bounding Box
        img = cv2.imread(destination_img)
        face_locations = face_recognition.face_locations(firstface1)
        top, right, bottom, left = face_locations[0]
        start_point = (left, top)
        end_point = (right, bottom)
        img = cv2.rectangle(img, start_point, end_point, (0, 0, 255), 2)
        cv2.imwrite(faceBoundaryImagePath, img)

        # Cropped Face
        cropped_face = img[top:bottom, left:right]
        cv2.imwrite(faceCroppedImagePath, cropped_face)

        # Face Landmarks
        img = cv2.imread(destination_img)
        face_landmarks_list = face_recognition.face_landmarks(firstface1)

        for facePart in face_landmarks_list[0]:
            color = colors[facePart]
            facePartPoints = face_landmarks_list[0][facePart]

            pts = np.array(facePartPoints,
                           np.int32)
            pts = pts.reshape((-1, 1, 2))
            img = cv2.polylines(img, [pts],
                                not facePart == 'chin', color, 2)
        cv2.imwrite(faceLMsImagePath, img)

        destination_dir = 'http://127.0.0.1:9001/media/member/' + \
            str(member.id)+'/'

        return Response(
            {
                "success": True,
                "id": member.id,
                "msg": "The member added successfully",
                "inter_photos_dir": destination_dir
            },
            status=status.HTTP_201_CREATED,
        )
