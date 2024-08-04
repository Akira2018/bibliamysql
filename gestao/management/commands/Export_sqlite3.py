import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
import sqlite3
import pandas as pd

class Command(BaseCommand):
    help = 'Export data from SQLite to Excel'

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=str, help='Path to the output Excel file')

    def handle(self, *args, **kwargs):
        output_file = kwargs['output_file']

        # Caminho para o banco de dados SQLite
        sqlite_db_path = os.path.join(settings.BASE_DIR, 'Ara_Novo.sqlite3')

        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect(sqlite_db_path)

        # Listar todas as tabelas
        tables = conn.execute("SELECT gestao_verse FROM sqlite_master WHERE type='table';").fetchall()

        with pd.ExcelWriter(output_file) as writer:
            for table_name in tables:
                table_name = table_name[0]
                # Ler a tabela para um DataFrame
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                # Exportar para o Excel
                df.to_excel(writer, sheet_name=table_name, index=False)

        conn.close()
        self.stdout.write(self.style.SUCCESS(f'Successfully exported data to {output_file}'))
