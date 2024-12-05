from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Model de gerenciamento de usuário
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Método que efetivamente cria nova instância de usuário e salva no DB
        """
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Método para criar um usuário comum, sem privilégios admin
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Método para criar usuario admin
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário precisa ser primeiro Staff, "is_staff=True".')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário precisa ter propriedade "is_superuser=True"')

        return self._create_user(email, password, **extra_fields)


# Model que define os campos que existirão na tabela de user
class CustomUsuario(AbstractUser):

    DEPARTAMENTO_CHOICES = (
        ('FINANCEIRO', 'Financeiro'),
        ('GERENCIA', 'Gerência'),
        ('OPERACIONAL', 'Operacional'),
        ('VENDAS', 'Vendas'),
    )

    UNIDADE_CHOICES = (
        ('PIRACICABA', 'Piracicaba'),
        ('VALINHOS', 'Valinhos'),
        ('MANAUS', 'Manaus'),
    )

    email = models.EmailField('E-mail', unique=True)
    contato = models.CharField('Contato', max_length=20)
    departamento = models.CharField('Departamento', max_length=20, choices=DEPARTAMENTO_CHOICES)
    unidade = models.CharField('Unidade', max_length=40, choices=UNIDADE_CHOICES)

    is_staff = models.BooleanField('Membro da equipe', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'contato']

    def __str__(self):
        return self.email

    objects = UserManager()
