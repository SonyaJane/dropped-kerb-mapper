# Dropped-Kerb Mapper

The purpose of this web application is to enable users to record the location of dropped kerbs in the UK. The data gathered will be used by the [Mobility Mapper](https://www.mobilitymapper.co.uk/) platform to generate accessible routes for users of wheeled mobility devices.

Users are able to rate the dropped kerb using a traffic light system, where:

<table>
  <tr>
    <td><img src="./readme-files/traffic-lights.png" width=75><br></td>
    <td>Red: Dangerous or unusable. <br> Orange: Usable but needs improvement <br> Green: Usable and in good condition.<br> Blue: A dropped kerb is not present but should be. A wheeler is prevented from entering or exiting the pavement at this point, in order to connect to another section of pavement or road.</td>
  </tr>
</table>


## User Stories

**Add the location of a Dropped Kerb**

As a Site User I want to add the location of a dropped kerb by clicking on the location on a map, so that I can contribute accurate data to the Dropped-Kerb database.

**Acceptance Criteria**

- The user is presented with an interactive map on the submission page.
- The user can click on the map to select the exact location of the dropped kerb.
- A marker is placed on the map at the clicked location to confirm the selection.


**Categorise the condition of the Dropped Kerb**

As a Site User I want to categorise the dropped kerb using the traffic light classification system, so that I can record its usability for wheelers based on its condition.

**Acceptance Criteria**

- The submission form displays the four traffic light options (red, orange, green, blue) clearly.
- The user is required to select one of the classification options before submitting the report.


**Explain why a condition category was selected**

As a Site User I want to provide my reasons for selecting a condition category, so that I can explain my choice and provide a clearer picture of the state of the dropped kerb.

**Acceptance Criteria**
- Upon selecting a traffic light category, a set of relevant checkboxes appears with predefined reasons or characteristics explaining the selected category.
- The user can select one or more checkboxes to provide further context.


**Upload photos of the dropped kerb**
As a Site User I want to upload photos of the dropped kerb so wheelers can judge for themselves if they can use it or not.

**Acceptance Criteria**
- The form provides an option for the user to either capture a new photo using their device’s camera or upload an existing photo.
- The photo field is not required but must accept only valid image formats.


**Recieve a confirmation that my submission was successful**
As a site user I would like to receive confirmation that my submission of a dropped kerb record was complete and saved successfully, so that I can be sure that my contributions are being added to the database.

**Acceptance Criteria**

- The form validates that a map location, a traffic light classification, and if a photo has been provided, that is a valid image format.
- If any required field is missing, the user receives clear error messages indicating what needs to be completed.
- Upon successful submission, a confirmation message (or modal) is displayed to the user.


**Dropped Kerb Reports saved successfully**
As the owner of the website I would like confimration that reports are being successfully saved and stored in the database, so that I can be certain that we are receiving and storing the data corrrectly.

**Acceptance Criteria**
- The report submission, including the selected map location, classification, additional checkbox details, and photo, is saved correctly in the database.
- The submission is timestamped and linked to the user’s account for future reference.

---

**Account registration**

As a Site User I can register an account so that I can add locations of dropped kerbs.

**Acceptance Criteria**
1. Given an email a user can register an account.  
2. Then the user can log in.  
3. When the user is logged in they can add the locations of dropped kerbs (reports).  

---

**View, edit or delete the location of a dropped kerb**

As a Site User I want to view, edit or delete my reports so that I can correct errors, or update information if the situation changes.

**Acceptance Criteria**

1. Given a logged in user, they can modify the information on their reported location  
2. Given a logged in user, they can delete their reported location  
3. The user can access a list of their submitted dropped kerb reports.
4. Each report can be selected to view its information.
5. An 'Edit' option is available that allows modification of the location, categories,or photo.
6. Changes are validated before being saved.
7. The user receives a confirmation message upon successful update.

---

**Manage reports**

As a Site Admin I can review, verify, update and delete reports so that the dataset is accurate and reliable. 

**Acceptance Criteria**

1. An admin dashboard is available listing all new reports.
2. Admins can click on a report to view full details, including location, classifications and images.
3. A report can be deleted or updated

---

**View Map of Reported Dropped Kerbs**

As a user, I want to see a map displaying all reported dropped kerbs so that I can see which kerbs have been reported, and understand accessibility challenges in my area.

**Acceptance Criteria**

1. A map view plots markers for all reported dropped kerbs.
2. The colour of the marker is the given traffic light classification (red, orange, yellow, green, blue)
3. Each marker displays a brief summary (photo thumbnail, classification) when clicked.
4. Basic map functionalities like zoom and pan are enabled.
5. The map updates to reflect new reports in near real-time or via a refresh option.

---

**Filtering and Searching Data**

As an administrator, I want to filter and search reports by location, date, and classification so that I can efficiently manage and analyse the data.

**Acceptance Criteria**

1. Admins can filter reports by geographic parameters and by date range.
2. A traffic light filter is available to categorise reports.
3. Multiple filters can be applied simultaneously for refined searching.
4. The search results are accurate and displayed in a timely manner.

---

**Sharing and Social Engagement**

As a site administrator, I want to share a report or a map view of dropped kerbs via social media or a shareable link so that I can raise awareness of local accessibility issues.

**Acceptance Criteria**

1. A shareable link is generated for a map view of the reports.
2. The shareable link includes metadata (such as a preview image and description) for social platforms.
3. Social media sharing buttons are available and functional.
4. The shared content renders correctly on major social networks.

## Entity Relationship Diagram

<img src="./readme-files/Entity_Relationship_Diagram.svg">


## Development Log

1. Created local folder "dropped-kerb-mapper"
2. Created "dropped-kerb-mapper" repository on GitHub
3. Initialised repository locally on the command line
4. Define purpose of the application.
5. Created user stories.
6. Created a Project board in Github for the user stories
7. Created a user story template
8. Added user stories to Project board
9. Create wireframes
10. Create Entity Relationship Diagram
11. Create a virtual environment using venv, and activate it:
    ```
    python -m venv .venv
    .venv\Scripts\activate
    ```
12. Create .gitignore file and add .venv/
13. Install Django
    ```
    pip install django
    ```
14. Add the packages to the requirements file using pip.
    ```
    pip freeze local > requirements.txt
    ```
15. Create a new project named dropped_kerb_mapper using the Django built-in function from the django-admin command-line utility. The dot at the end to signifies the current directory.
    ```
    django-admin startproject dropped_kerb_mapper .
    ```
16. Create a new app named mapper using the Django built-in function from the manage.py file.
    ```
    python manage.py startapp mapper
    ```
17. Add the new app to the list of installed apps in the settings.py file.
18. In the mapper/views.py file, create a view function called my_mapper
19. In dropped_kerb_mapper/urls, import the view function my_mapper.
20. Add the new path 'mapper/' into the urlpatterns.
21. Run the server in a browser window to test the code.
    ```
    python manage.py runserver
    ```
22. Deploy app to [Heroku](https://dashboard.heroku.com/apps). Create a new Heroku app with the unique name (dropped-kerb-mapper) hosted on a cloud server in Europe. No Django static file collection will be required yet during the build, so in Settings under reveal the config vars we added a key of DISABLE_COLLECTSTATIC with a value of 1.
23. Create Procfile and declare the dropped_kerb_mapper project as a web process with the command to execute it. web: gunicorn codestar.wsgi
24. the dropped_kerb_mapper/settings.py file, set the DEBUG constant to False and add ['.azurewebsites.net', '127.0.0.1'] to the ALLOWED_HOSTS list.
25. Commit to Github
26.  Deploy to Azure Web Apps. Open app to open the webpage and append /mapper to the URL in the browser bar to see the text "Hello, mappers".
28.  Create a PostgreSQL database on Azure (Azure Database for PostgreSQL Flexible Server)
29. Install the two packages required to connect to your PostgreSQL database. Then add them to the requirements file:
```
pip install dj-database-url psycopg2
```
30.  Create env.py at the top level of the project and add it to .gitignore.
31.  Connect the Django app to the Azure Database by setting the value of the DATABASE_URL constant.
    
``` Python
import os
os.environ.setdefault(
    "DATABASE_URL", 
    "postgres://username:password@yourserver.postgres.database.azure.com:5432/your_database?sslmode=require")
```

and in settings.py add

``` Python
import os
import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}
```

and connect the settings.py file to the env.py file:

```
if os.path.isfile('env.py'):
    import env
```
32. create database tables with Django's migrate command.
33. create a superuser with admin access to our database:
```
python manage.py createsuperuser
```
34.  Set a secret key as an environment variable in the env.py file, and modify the settings.py file to retrieve the new SECRET_KEY from the environment variables.
```
SECRET_KEY = os.environ.get("SECRET_KEY")
```
35.  Add a new SECRET_KEY as an environment variable on Azure Web Apps.
36.  Create models in /mapper/models.py based on the Entity Relationship Diagram.
37.  In mapper/admin.py file, import the models and register them to allow us to create, update and delete reports from the admin panel. 
38.  In the codestar/settings.py file and add the CSRF_TRUSTED_ORIGINS. This is a list of the trusted origins for requests to add content to the database from the admin dashboard.
``` Python
CSRF_TRUSTED_ORIGINS = [
    "https://*.azurewebsites.net",
    "http://127.0.0.1:8000"
]
```
39. Delete Reasons model and replace with a MultiSelectField in the Report model.
    ```
    pip install django-multiselectfield
  ```

40. Add meta classes to models.
41. Create urls.py for Mapper app.
42. Delete my_mapper views import from the dropped_kerb_mapper urls.py file, and add include to imported functions. Replace the existing mapper/ url pattern with a new empty string pattern, so Django now looks in the mapper app URL file for any blog urlpatterns:
``` Python
path('', include('mapper.urls'), name='mapper-urls'),
```
43. Create a templates directory in the mapper app, with another directory nested within, named mapper.
44. In this new mapper/templates/mapper directory, create a new HTML file named report_list.html.
45. Create a class-based view in the mapper/views.py file named ReportList that inherits from the generic.ListView class to display all the reports.
46. In blog/urls.py import the views file and path. Add a urlpattern for the ReportList class-based view named home.
47. Add Summernote for admin.
48. The MultiSelectField, 'reasons', stores its data as a comma‑separated string in the database. However, Django’s built‑in filtering in the admin cant parse that string, so I had to create a custom admin filter using Django’s SimpleListFilter class to filter the queryset based on whether a particular allowed reason is present in the field.
49. Create custom code to import a csv file into Django and create Report model instances.
50. Create project level templates folder and add a base.html file.
51. Create reports.html template to show a list of all the existing reports.
52. Install whitenoise package to create staticfiles for deployment.
53. Create a view for a single report.
54. Create Azure blob storage account.
55. Install the Python packages required to connect to the Azure blob storage: 
```
pip install django-storages azure-storage-blob
```
We will use the built‑in Azure backend from django‑storages with our account name, key, and container. 
56. Add 'storages' to INSTALLED_APPS in the settings.py file.
57. Add the following environment variables to the local .env file (and in the Azure environment):
``` python
os.environ.setdefault("AZURE_STORAGE_ACCOUNT", "<blob_storage_account_name>")
os.environ.setdefault("AZURE_STORAGE_KEY", "<corresponding_account_key>")
os.environ.setdefault("AZURE_CONTAINER", "container_name")
os.environ.setdefault("AZURE_SSL", "True")  # Enforces secure connections.
```
and in settings.py:
``` python
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = os.environ.get("AZURE_STORAGE_ACCOUNT")
AZURE_ACCOUNT_KEY = os.environ.get("AZURE_STORAGE_KEY")
AZURE_CONTAINER = os.environ.get("AZURE_CONTAINER")
AZURE_SSL = os.environ.get("AZURE_SSL")
```
58.  Add regular user authentication using the Python package AllAuth, including email confirmation. pip install django-allauth
59.  Add a report form. Install the two packages django-crispy-forms and crispy-bootstrap.
60.  Azure blob storage was timing out when uploading large images, so I had to create a custom class in \dropped-kerb-mapper\mapper\storage.py and change the settings to use it. The custom class extends the AzureStorage class from django-storages and overrides the default timeout setting (20 secs).
61.  This didnt solve the timmeout issue, so Im going to try Cloudinary instead.
62.  Remove photos model and add photos field to Report model.
63. Convert uploaded photos to webp format and reduce size < 5Mb
64. Add signals to delete photos from cloud storage when deleted in app
65. Change reports list to only those created by the user, but view all for a super user.
66. Create page with reports pinned on a map. Use Ordnance Survey map tiles with MapLibre GL JS Javascript library. Set up a proxy view in Django that fetches the tile images using a secret API key in env.py and then serve them to the client so the client-side code never sees the API key.
67. Add Google satellite tiles. Requires a cahced session token so install a persistant cache backend: django-redis

NOTE
Both the OS map tiles and Google Satellite tiles return a 404 response when a tile does not exist at a given zoom level, but the OS map continues to display the last available tiles while the Google Satellite map does not. This is because MapLibre GL reuses the last available tiles when a tile cannot be fetched. However, the HTTP **response headers** returned by the backend for the 404 response differ between the OS map and Google Satellite tiles. The OS map tiles include caching headers (e.g., Cache-Control) that allow MapLibre GL JS to reuse the last available tiles. The Google Satellite tiles lack these headers, causing MapLibre GL JS to treat the 404 response as a hard failure.
Solution:
Add the appropriate caching headers to a 404 response for the get_google_satellite_tiles view.




Now any model field that uses file storage (like an ImageField) will automatically save files to the Azure Blob container.


could use Ordnance Survey – Open Names

Google aerial view 5000 free map views per month
Find the maximum zoom level for satellite imagery at a specific location.
Google Maximum Zoom Imagery service in the Maps JavaScript API (example)
https://developers.google.com/maps/documentation/javascript/maxzoom?_gl=1*udr88s*_up*MQ..*_ga*NTMyNzE0NzAxLjE3NDI4MjI0MDc.*_ga_NRWSTWS78N*MTc0MjgzNDYyMy4zLjAuMTc0MjgzNDYyMy4wLjAuMA..


Use Mapbox Satellite through any of Mapbox's APIs and SDKs with the tileset ID mapbox.satellite.
https://docs.mapbox.com/api/maps/raster-tiles/
Raster Tiles API
750,000 free monthly requests

1.  Create a home page that tells you about the web app.



Customise the Django admin form with some JavaScript so that the reasons field only appears if the classification selected is red or orange.

## Javascript Libraries

MapLibre GL JS for interactive mapping
