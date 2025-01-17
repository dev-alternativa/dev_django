from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Model de gerenciamento de usuário
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Método que efetivamente cria nova instância de usuário e salva no DB
        """
        if not username:
            raise ValueError('Nome de usuário é obrigatório')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        """
        Método para criar um usuário comum, sem privilégios admin
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """
        Método para criar usuario admin
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário precisa ser primeiro Staff, "is_staff=True".')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário precisa ter propriedade "is_superuser=True"')

        return self._create_user(username, password, **extra_fields)


# Model que define os campos que existirão na tabela de user
class CustomUsuario(AbstractUser):

    DEPARTAMENTO_CHOICES = (
        ('FINANCEIRO', 'Financeiro'),
        ('GERENCIA', 'Gerência'),
        ('OPERACIONAL', 'Operacional'),
        ('VENDAS', 'Vendas'),
        ('OUTROS', 'Outros'),
    )

    UNIDADE_CHOICES = (
        ('PIRACICABA', 'Piracicaba'),
        ('VALINHOS', 'Valinhos'),
        ('MANAUS', 'Manaus'),
    )

    email = models.EmailField('E-mail', unique=True, null=True, blank=True)
    contato = models.CharField('Contato', max_length=20)
    departamento = models.CharField('Departamento', max_length=20, choices=DEPARTAMENTO_CHOICES)
    unidade = models.CharField('Unidade', max_length=40, choices=UNIDADE_CHOICES)

    objects = UserManager()

    def __str__(self):
        return self.username
