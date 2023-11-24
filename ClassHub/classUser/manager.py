from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, Enrollment_no, password=None, **extra_fields):
        if not Enrollment_no:
            raise ValueError("Enrollment Number is required")

        extra_fields["email"] = self.normalize_email(extra_fields["email"])
        user = self.model(Enrollment_no=Enrollment_no, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, Enrollment_no, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(Enrollment_no, password, **extra_fields)
