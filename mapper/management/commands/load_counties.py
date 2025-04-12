#  Importing shapefile data into the County model
# python manage.py load_counties mapper\fixtures\counties\CTYUA_DEC_2024_UK_BFC.shp
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from mapper.models import County

# Map the model fields to the shapefile fields.
county_mapping = {
    'county': 'CTYUA24NM', # Keys must match model field names, values match shapefile field names.
    'polygon': 'MULTIPOLYGON',  
}

class Command(BaseCommand):
    help = 'Load shapefile data into the County model.'

    def add_arguments(self, parser):
        parser.add_argument('shapefile', type=str, help='The path to the shapefile to import')
        
    def handle(self, *args, **options):
        shapefile_path = options['shapefile']
        self.stdout.write(f"Loading shapefile from {shapefile_path}")

        # Create a LayerMapping instance. Set transform=True if the shapefile's CRS
        # differs from the model's (for example, if your shapefile is in EPSG:27700 and your model is EPSG:4326)
        lm = LayerMapping(County, shapefile_path, county_mapping, transform=True)
        
        # Save the data. Set strict=True to raise errors if there is missing data.
        lm.save(strict=True, verbose=True)
        self.stdout.write(self.style.SUCCESS('Successfully loaded shapefile data into County model.'))