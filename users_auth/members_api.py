from rest_framework import viewsets, mixins, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users_auth.models import Member


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
        member = serializer.save()

        return Response(
            {
                "success": True,
                "id": member.id,
                "msg": "The member added successfully",
            },
            status=status.HTTP_201_CREATED,
        )
