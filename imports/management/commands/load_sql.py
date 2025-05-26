from django.core.management.base import BaseCommand
from django.db import connection
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Carrega arquivos SQL iniciais'

    def handle(self, *args, **options):
        sql_dir = os.path.join(settings.BASE_DIR, 'sql')
        sql_files = [
            'base_category.sql',
            'base_cnpj_faturamento.sql',
            'base_conta_corrente.sql',
            'base_freight.sql',
            'base_location.sql',
            'base_tax_scenario.sql',
        ]

        with connection.cursor() as cursor:
            for sql_file in sql_files:
                file_path = os.path.join(sql_dir, sql_file)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        sql_content = f.read()
                        cursor.execute(sql_content)
                    self.stdout.write(f'Executado: {sql_file}')