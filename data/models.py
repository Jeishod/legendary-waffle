from django.db import models


class LifeCycleMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        abstract = True


class User(LifeCycleMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=False, blank=False)
    is_superuser = models.BooleanField(null=False, default=False)
    hashed_password = models.CharField(max_length=255)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"


class Project(LifeCycleMixin):
    title = models.CharField(max_length=50)
    description = models.TextField()
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "projects"


class File(LifeCycleMixin):
    file = models.FileField(upload_to="files/")
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "files"
