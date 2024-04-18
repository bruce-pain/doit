from rest_framework import serializers

from api.models import Task, Category


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
    )

    class Meta:
        model = Task
        fields = [
            "url",
            "id",
            "title",
            "description",
            "time_created",
            "status",
            "category",
            "due_date",
        ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="task-detail",
        read_only=True,
    )

    class Meta:
        model = Category
        fields = ["url", "id", "name", "tasks"]
