from __future__ import annotations

from django.core.management.base import BaseCommand, CommandParser
from main.grist import GristClient
from main.models import GristConfig


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--grist-config",
            required=True,
            type=str,
            help="UUID of the grist config we want to process",
            action="store",
            nargs="?",
        )

    def handle(self, *args, **options):
        try:
            config: GristConfig = GristConfig.objects.get(id=options["grist_config"])
        except GristConfig.DoesNotExist:
            self.stdout.write(self.style.ERROR("Config not found for the given UUID"))
            return 1

        if not config.enabled:
            self.stdout.write(self.style.ERROR("Config is not enabled"))
            return 1

        grist_client = GristClient.from_config(config)

        response = grist_client.get_tables()
        for table in response["tables"]:
            if table["id"] == config.table_id:
                self.stdout.write(
                    self.style.ERROR(f"Table {config.table_id} already exists, aborting...")
                )
                return

        # create a new table
        # fetch all projects from recoco
        # fill the new table with the projects
        # register the table ID in the config record
        # trash the previous table
