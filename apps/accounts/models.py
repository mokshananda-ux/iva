"""Modelo de usuario personalizado del IVA.

Se usa un `User` propio desde el inicio para evitar migraciones dolorosas
más adelante. La condición de "inscrito" NO es un rol permanente: se calcula
a partir de las matrículas activas (ver `is_enrolled`).
"""
from __future__ import annotations

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Manager que usa el email como identificador principal."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra):
        if not email:
            raise ValueError(_("El email es obligatorio"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email: str, password: str | None = None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        if extra.get("is_staff") is not True:
            raise ValueError(_("El superusuario debe tener is_staff=True"))
        if extra.get("is_superuser") is not True:
            raise ValueError(_("El superusuario debe tener is_superuser=True"))
        return self._create_user(email, password, **extra)


class User(AbstractUser):
    """Usuario basado en email. Mantiene `is_staff` de Django para el panel admin."""

    # Eliminamos username; el login es por email.
    username = None
    email = models.EmailField(_("correo electrónico"), unique=True)

    # Rol docente. Staff administrativo se gestiona con is_staff/grupos.
    is_instructor = models.BooleanField(_("es instructor"), default=False)

    preferred_language = models.CharField(
        _("idioma preferido"), max_length=5, default="es"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        verbose_name = _("usuario")
        verbose_name_plural = _("usuarios")

    def __str__(self) -> str:  # pragma: no cover
        return self.email

    @property
    def is_enrolled(self) -> bool:
        """Inscrito = tiene al menos una matrícula activa.

        Se calcula dinámicamente; nunca es un flag persistente.
        """
        return self.enrollments.filter(status="active").exists()


class Profile(models.Model):
    """Datos extendidos y no críticos del usuario."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    display_name = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    country = models.CharField(max_length=2, blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"Perfil de {self.user.email}"
