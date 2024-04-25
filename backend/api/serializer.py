from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import Task, Category


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(
        many=True, view_name="task-detail", read_only=True
    )
    categories = serializers.HyperlinkedRelatedField(
        many=True, view_name="category-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "tasks", "categories"]


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = [
            "url",
            "id",
            "title",
            "description",
            "owner",
            "time_created",
            "status",
            "category",
            "due_date",
        ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    tasks = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="task-detail",
        read_only=True,
    )

    class Meta:
        model = Category
        fields = ["url", "id", "name", "owner", "tasks"]
