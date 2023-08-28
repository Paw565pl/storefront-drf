from typing import Any
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Populates database with collections and products."

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("Populating database...", ending="\n")
        sql = Path("./sql/seed_store.sql").read_text()

        with connection.cursor() as cursor:
            cursor.execute(sql)

        self.stdout.write("Done!", ending="")
