import json
import os

from django.core.management.base import BaseCommand
from imdb import settings

from imdb.api.models import IMDB

filepath = settings.BASE_DIR + '/imdb/api/src/imdb_db.json'

class Command(BaseCommand):
    help = 'Transfer imdb data from json file to db.'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filePath', type=str, default=filepath,
                            help='Transfer imdb data from json file to db')

    def handle(self, *args, **options):
        # Reading scan results from the json file
        file_path = os.path.normpath(options['filePath'])
        file = open(file_path, 'r')
        imdb_content = json.load(file)
        file.close()

        # Get the latest scan date from the AWS SSM Parameter Store.
        
        # invalid_records_obj = IMDB.objects.filter(scan_date__date=latest_scan_date, is_scan_valid=True)
        # invalid_records_obj.update(is_scan_valid=False)

        for content in imdb_content:

            new_imdb_account = IMDB(
                                    name_director=content.get("name", '') + content.get("director", ''),
                                    name=content.get("name", ''),
                                    director=content.get("director", ''),
                                    imdb_score=content.get("imdb_score"),
                                    popularity_99=content.get("99popularity"),
                                    genre=content.get("genre", list()),
                                )
            new_imdb_account.save()

        return         
