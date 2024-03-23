from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Resets sequence in the database."

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Reseting sequence...")
        sql = Path("./sql/sequence_reset.sql").read_text()

        with connection.cursor() as cursor:
            cursor.execute(sql)

        self.stdout.write("Done!")
