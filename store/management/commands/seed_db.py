from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Populates database with collections and products."

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Populating database...")
        sql = Path("./sql/seed_store.sql").read_text()

        with connection.cursor() as cursor:
            try:
                cursor.execute(sql)
                self.stdout.write("Done!")
            except Exception:
                self.stdout.write("Data has been already seeded!")
