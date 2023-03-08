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


     

        test_file=self.request.FILES.get('picture')
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


        destination = open(destination_dir+'/'+x+'__'+ test_file.name, 'wb+')

        for chunk in test_file.chunks():
            destination.write(chunk)
        destination.close()
        #so file in test_pic read file and apply face match here
        # add logic here to mark attended
        is_match, member_id =True, '2dd0bb6b-018b-47ea-a3e0-564891248cdb'


        

        # memberID, terminal, dateTime

        if is_match:

            member=Member.objects.get(id=member_id)
            Attendance.objects.create(member=member,terminal_code=terminal_code)

            return Response(
                {
                    "success": True,
                    "id": "sd",
                    "msg": "The attendance marked successfully",
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
