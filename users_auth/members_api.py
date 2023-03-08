from rest_framework import viewsets, mixins, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users_auth.models import Member
from authatt.settings import BASE_DIR
import os


import face_recognition




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




        test_file=self.request.FILES.get('picture')
        destination_dir = str(BASE_DIR)+'/media/test_pic_val/'


        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        destination_img = destination_dir+'/'+ test_file.name
        destination = open(destination_img, 'wb+')

        for chunk in test_file.chunks():
            destination.write(chunk)
        destination.close()

        # image validator
        firstface1 = face_recognition.load_image_file(destination_img)
        first_face_encoding = face_recognition.face_encodings(firstface1)
        n_faces = len(first_face_encoding)

        if(not n_faces==1):
            print('Ignoring Face Feed for ', destination_img)
            return Response(
            {
                "success": False,
                "msg": "Cannot add member. Please change Image.",
                'n-faces': n_faces
            },
            status=status.HTTP_201_CREATED,
            )
            
                    

        member = serializer.save()

        return Response(
            {
                "success": True,
                "id": member.id,
                "msg": "The member added successfully",
            },
            status=status.HTTP_201_CREATED,
        )
