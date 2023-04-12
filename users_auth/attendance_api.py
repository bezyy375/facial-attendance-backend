from rest_framework import viewsets, mixins, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# import uuid
import os
import datetime


from users_auth.models import Attendance, Member

from authatt.settings import BASE_DIR

import numpy as np
import face_recognition
import cv2

from users_auth.members_api import image_resize


'''
#Disabling pre-training
known_face_encodings = []
known_face_names = []
known_face_regions = []

face_locations = []
face_encodings = []
face_names = []
path = 'media/member'

filenames=os.listdir(path)
for filename in filenames:
    

    print('Feeding',filename )
    try:
    # if (True):
        if len(known_face_names)<70:
            second_image = path + "/" + filename
            firstface1 = face_recognition.load_image_file(second_image)
            first_face_encoding = face_recognition.face_encodings(firstface1)[0]
            known_face_encodings.append(first_face_encoding)
            # name = os.path.splitext(filename)[0]
            known_face_names.append(filename)
            known_face_regions.append(str(dir))


            
    except:
        print('Exception Raised in Feeding!!')
        pass
print(known_face_names)
print(known_face_regions)
'''


# Create your views here.
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "member", "terminal_code", "date_time"]
        read_only_field = ["id"]


class AttendanceViewSet(ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Attendance.objects.all()

    def create(self, request, *args, **kwargs):

        test_file = self.request.FILES.get('picture')
        terminal_code = request.data['terminal_code']

        print(test_file)

        x = datetime.datetime.now()
        x = str(x)
        x = x.replace(":", "__")
        x = x.replace(".", "__")
        x = x.replace("-", "__")

        destination_dir = str(BASE_DIR)+'/media/test_pic/'+terminal_code

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        destination_img = destination_dir+'/'+x+'__' + test_file.name
        destination = open(destination_img, 'wb+')

        for chunk in test_file.chunks():
            destination.write(chunk)
        destination.close()

        print("Before Loading image file")
        unknown_image = face_recognition.load_image_file(destination_img)

        print("Before Loading image encodings")
        unknown_encoding = face_recognition.face_encodings(unknown_image)

        n_faces = len(unknown_encoding)
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

        print("AFTER unknown_encoding", destination_img)
        unknown_encoding = unknown_encoding[0]

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
                    second_image = path + "/" + filename
                    firstface1 = face_recognition.load_image_file(second_image)
                    first_face_encoding = face_recognition.face_encodings(
                        firstface1)

                    if (not len(first_face_encoding) == 1):
                        print('Ignoring Face Feed for ', second_image)
                        continue

                    first_face_encoding = first_face_encoding[0]

                    known_face_encodings.append(first_face_encoding)
                    # name = os.path.splitext(filename)[0]
                    known_face_names.append(filename)
                    known_face_regions.append(str(dir))

            except Exception as e:
                print('Exception Raised in Feeding!!', e)
                pass
        print(known_face_names)
        print(known_face_regions)

        def getresult(first_image):
            first_image = str(first_image)

            folder = 'media/test_pic'
            print("IN SYSTem", first_image)

            first_image = first_image.replace(")", "")
            first_image = first_image.replace("(", "")

            c = 23
            print("AFTER", first_image)
            try:
                # if(True):

                print("Before Loading image file")
                # unknown_image = face_recognition.load_image_file(first_image)
                unknown_image = cv2.imread(first_image)

                # Convert the image from RGB color (which OpenCV uses) to BGR color (which face_recognition uses)
                # bgr_unknown_image = unknown_image[:, :, ::-1]
                bgr_unknown_image = cv2.cvtColor(
                    unknown_image, cv2.COLOR_BGR2RGB)

                # Image resizing
                image_resize(
                    cv2.imread(unknown_image), width=500)

                print("Before Loading image encodings")
                unknown_encoding = face_recognition.face_encodings(bgr_unknown_image)[
                    0]

                print("AFTER unknown_encoding", first_image)

                '''
                frame=cv2.imread(first_image)
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                print('After Resizing')


                
                test_face_locations = face_recognition.face_locations(small_frame)
                print('After Face Locations')

                unknown_encoding = face_recognition.face_encodings(small_frame, test_face_locations)
                '''

                results = face_recognition.compare_faces(
                    known_face_encodings, unknown_encoding)
                print('/n/nMatching Results:\n', results, '\n\n')

                if True in results:
                    first_match_index = results.index(True)
                    founname = known_face_names[first_match_index]
                    print("UserID", founname)
                    return True, founname.split('.')[0]

            except Exception as e:
                print('Exception Raised in Recognition!!', e)
                pass

            return False, 'Member Not Found!'

        # so file in test_pic read file and apply face match here
        # add logic here to mark attended
        is_match, member_id = getresult(destination_img)

        # memberID, terminal, dateTime

        if is_match:

            member = Member.objects.get(id=member_id)
            Attendance.objects.create(
                member=member, terminal_code=terminal_code)

            return Response(
                {
                    "success": True,
                    "id": member_id,
                    "msg": "The attendance marked successfully",
                    "member":  {"id": member.id, "name": member.name, "organization": member.organization.name, },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "msg": "No Member found to mark  attendance",
            },
            status=status.HTTP_404_NOT_FOUND,
        )
