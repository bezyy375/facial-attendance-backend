from rest_framework import viewsets, mixins, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users_auth.models import Attendance


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
        # add logic here to mark attended
        return Response(
            {
                "success": True,
                "id": "sd",
                "msg": "The attendance marked successfully",
            },
            status=status.HTTP_201_CREATED,
        )
