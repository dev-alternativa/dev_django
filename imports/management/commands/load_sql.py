from django.core.management.base import BaseCommand
from django.db import connection
import os
from django.conf import settings
import glob, sqlparse


class Command(BaseCommand):
    help = 'Carrega arquivos SQL iniciais'

    def handle(self, *args, **options):
        sql_dir = os.path.join(settings.BASE_DIR, 'sql')
        sql_files = sql_files = sorted(glob.glob(os.path.join(sql_dir, '*.sql')))

        if not sql_files:
            self.stdout.write(self.style.WARNING('Nenhum arquivo SQL encontrado.'))
            return

        with connection.cursor() as cursor:
            for file_path in sql_files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                    try:
                        # Executa múltiplos comandos SQL separados por ';'
                        for statement in sqlparse.split(sql_content):
                            statement = statement.strip()
                            if statement:
                                cursor.execute(statement)
                        self.stdout.write(self.style.SUCCESS(f'Executado: {os.path.basename(file_path)}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro ao executar {os.path.basename(file_path)}: {e}'))