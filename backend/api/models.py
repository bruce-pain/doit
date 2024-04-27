from django.db import models

STATUS_CHOICES = [
    ("not_started", "Not Started"),
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
]


class Category(models.Model):
    """
    Category fields:
        name -> category name
    """

    name = models.CharField(max_length=100, blank=False)
    owner = models.ForeignKey(
        "auth.User", related_name="categories", on_delete=models.CASCADE
    )

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "{}".format(self.name)


class Task(models.Model):
    """
    Task fields:
        title -> title or short description of the task
        description -> long description for the task
        time_created -> timestamp for when the task was created
        owner -> User who created the task
        status -> completion status of the task [completed, not_started, in_progress]
        category -> User defined category for grouping tasks
        due_date -> time when the task should be completed
        time_completed -> time when the task is completed
    """

    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        "auth.User", related_name="tasks", on_delete=models.CASCADE
    )
    status = models.CharField(
        default="not_started", choices=STATUS_CHOICES, max_length=15
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    due_date = models.DateTimeField(null=True)
    # time_completed = None

    def __repr__(self):
        return "Task #{}: {}".format(self.id, self.title)

    def __str__(self):
        return "Task #{}: {}".format(self.id, self.title)

    class Meta:
        ordering = ["time_created"]
