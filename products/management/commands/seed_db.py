from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = (
        "Truncates collections and products tables and populates them with sample data."
    )

    def handle(self, *args, **options):
        self.stdout.write("Populating database...")
        sql = Path("./sql/seed_products.sql").read_text()

        with connection.cursor() as cursor:
            try:
                cursor.execute(sql)
                self.stdout.write("Done!")
            except Exception as e:
                self.stdout.write(f"Error seeding database! {e}")
