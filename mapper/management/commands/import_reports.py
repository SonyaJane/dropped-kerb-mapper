import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from mapper.models import Report

# python manage.py import_reports mapper/fixtures/equal_footing_reports.csv
class Command(BaseCommand):
    help = 'Import CSV data into the Report model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        try:
            with open(csv_file, newline='', encoding='utf-8-sig') as f: # 'utf-8-sig' to handle BOM
                reader = csv.DictReader(f)
                for row in reader:
                    # csv file has columns matching the model fields.
                    try:
                        # Assume the CSV column 'user' contains a username.
                        user = User.objects.get(username=row['user'])
                    except User.DoesNotExist:
                        user = None

                    # Create a new Report instance. Make sure your CSV columns align with your model fields.
                    report = Report.objects.create(
                        latitude=row['latitude'],
                        longitude=row['longitude'],
                        classification=row['classification'],
                        comments=row.get('comments', ''),
                        user=user,
                    )
                    # If the CSV provides reasons as a comma-separated string,
                    # set the MultiSelectField value accordingly.
                    if 'reasons' in row and row['reasons'].strip():
                        reasons_list = [r.strip() for r in row['reasons'].split(',')]
                        report.reasons = reasons_list
                    report.save()

                self.stdout.write(self.style.SUCCESS('Successfully imported CSV data.'))
        except FileNotFoundError:
            raise CommandError(f'File "{csv_file}" does not exist')
