from typing import Any
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Resets sequence in the database."

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("Reseting sequence...", ending="\n")
        sql = Path("./sql/sequence_reset.sql").read_text()

        with connection.cursor() as cursor:
            cursor.execute(sql)

        self.stdout.write("Done!", ending="")
