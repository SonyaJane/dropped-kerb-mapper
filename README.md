# Dropped-Kerb Mapper

![Dropped Kerb Mapper mockup images](/readme-files/mock-up.png)

The purpose of Dropped Kerb Mapper is to record the locations of dropped kerbs in the UK. The data gathered will be used by the [Mobility Mapper](https://www.mobilitymapper.co.uk/) platform to generate accessible routes for users of wheeled mobility devices. It will also be used to raise the awareness of the need for well designed and maintained dropped kerbs in the UK, and to help local councils and authorities to understand where they are needed most.

Users can report a dropped kerb by clicking on its location on a map. Optionally, users can upload a photo of the dropped kerb, and classify its condition based on a traffic light system, where:

<table>
  <tr>
    <td><img src="./readme-files/traffic-lights.png" width=75><br></td>
    <td>Red: Dangerous or unusable. <br> Orange: Usable but needs improvement <br> Green: Usable and in good condition.<br> White: A dropped kerb is not present but should be. A wheeler is prevented from entering or exiting the pavement at this point, in order to connect to another section of pavement or road.</td>
  </tr>
</table>

Instructions are provided on how to use the app. Users can see a list of their reports, or view them on a map. There is a contact page that allows a user to ask questions or make suggestions. 

Visit the deployed website [here](https://www.droppedkerbmapper.com/).

## Table of Contents

<insert here>

## User Experience (UX)

### Project Goals

Dropped Kerb Mapper frontend is designed to deliver an intuitive user experience, ensuring that users can report the locations of dropped kerbs in the UK. The primary project goals are: 

- Provide a clean, map-based interface for reporting the precise location of dropped kerbs.  
- Enforce a simple traffic-light condition classification (red/orange/green/blue) together with selectable 'reasons' for the classification choice.  
- Allow optional photo uploads (automatically converted to webp format and compressed) to document each kerb.  
- Require user authentication for creating, editing or deleting reports and tie each report to its creator.  
- Expose an admin dashboard with filtering, search and table views powered by django-tables2 and custom list-filters.  
- Proxy both Ordnance Survey raster tiles and Google Satellite tiles (with session tokens and proper caching headers) for consistent map rendering.  
- Use HTMX and crispy-forms to deliver inline form validation, success/fail partials and real-time map updates.  
- Ensure responsive, accessible design across desktop and mobile devices.  
- Provide a simple contact form and email-confirmation flow (auto-login after confirmation) for a smooth user experience.


## User Goals

1. **Add a dropped kerb location**  
   As a Site User I want to add the location of a dropped kerb by clicking on a map so that I can contribute accurate data to the database.  

2. **Categorise the condition**  
   As a Site User I want to classify the dropped kerb using a traffic-light system so that others know its usability.  

3. **Provide reasons for the classification**  
   As a Site User I want to supply one or more contextual reasons for my condition choice so that I can explain my assessment.  

4. **Upload a photo**  
   As a Site User I want to optionally upload a photo of the dropped kerb so that others can visually verify its condition, and wheelers can judge for themselves if they can use it.

5. **Receive submission confirmation**  
   As a Site User I want to see a success message when my report is saved so that I know my contribution is recorded.  

6. **Register and log in**  
   As a Site User I can register an account and log in so that I can create, view, edit, and delete my own reports.  

7. **Edit a report**  
   As a Site User I want to edit my existing report so that I can correct mistakes or update information.  

8. **Delete a report**  
   As a Site User I want to delete my own report so that I can remove obsolete or erroneous entries.  

9. **View a map of reports**  
   As a Site User I want to see all my reports plotted on an interactive map so that I can visualise their locations.  

10. **Contact support**  
    As a Site User I want to send feedback or questions via a contact form so that I can communicate with the site team.  
  
11. **Filter and search reports (admin)**  
    As a Site Admin I want to filter and search all reports by date, user, location, or condition so that I can manage the data.  

12. **Proxy map tiles**  
    As a user the app should load consistent map tiles so that I see the same Ordnance Survey and Google Satellite imagery.  

## Structure

The structure of the website is shown in the image below. The main page is the map view, where users can add a new report and see their existing reports. The location of existing reports can be changed by dragging its marker on the map. Existing reports can also be viewed as a list on the List Reports page. Both pages provide links to view more detail, and edit the report. The detailed view of the report provides options to edit or delete the report. This structure provides the user with the opportunity to edit and existing report, regargless of how they are viewing it. There is only one route to the option to delete the report to discourage mass deletion, while still enabling the user to remove reports submitted in error.

<img src="./readme-files/app_structure.png">

Note that:

- The header, footer, and navigation menu are the same on all pages.
- Links, buttons and form provide clear feedback to the user.
- Users can add, edit, delete and view their reports after creating an account.
- There is a custom 404 error page.

## Entity Relationship Diagram

The ERD below was created using [Mermaid](https://mermaid.js.org/syntax/entityRelationshipDiagram.html).

This relational database is managed by PostgreSQL with a PostGIS extension for the County and Local Authority Models, which contain the polygons that represent the geographical area as a sequence of longitude and latitude coordinates.

```mermaid
erDiagram
    direction LR
    CUSTOMUSER {
      int id PK
      string username
      bool uses_mobility_device
      bool is_carer
      string mobility_device_type
    }
    REPORT {
      int id PK
      int user_report_number
      decimal latitude
      decimal longitude
      int user_id FK
      int county_id FK
      int local_authority_id FK
      string place_name
      enum condition
      string[] reasons
      string comments
      string photo
      datetime created_at
      datetime updated_at
    }
    COUNTY {
      int id PK
      string county
    }
    LOCALAUTHORITY {
      int id PK
      string local_authority
    }
   
    CUSTOMUSER ||--o{ REPORT : "submits"
    REPORT }o--|| COUNTY : "contains"
    REPORT }o--|| LOCALAUTHORITY : "contains"
```

**CustomUser Model**
Extends Django's AbstractUser to capture accessibility-related user details.

Attributes:

- uses_mobility_device: Indicates whether the user uses a wheeled mobility device.
- is_carer: Indicates whether the user is a carer for someone who uses a wheeled mobility device.
- mobility_device_type: Type of mobility device used by the user or caree.

**County Model**
A geospatial model representing a county boundary. Each instance stores the county's name and its polygon geometry (in WGS84) for spatial lookups (e.g., reverse geocoding a longitude and latitude coordinate to determine which county it falls within).

Attributes:

- county: The human-readable name of the county.
- polygon: The boundary of the county, stored as a MultiPolygon using SRID 4326 (WGS84 latitude/longitude).

**LocalAuthority Model**

A geospatial model representing a local authority boundary. Each instance stores the county's name and its polygon geometry (in WGS84) for spatial lookups (e.g., reverse geocoding a longitude and latitude coordinate to determine which county it falls within).

Attributes:

- local_authority: The human-readable name of the local authority.
- polygon: The boundary of the county, stored as a MultiPolygon using SRID 4326 (WGS84 latitude/longitude).

## Wireframes

Wireframes were created using [Balsamiq](https://balsamiq.com/) to plan the design of the web application.

| Page | Desktop | Mobile |
| --- | --- | --- |
| Home | ![Home desktop wireframe](readme-files/home_desktop.png) | ![Home mobile wireframe](readme-files/home_mobile.png) |
| Instructions | ![Instructions desktop wireframe](readme-files/instructions_desktop.png) | ![Instructions mobile wireframe](readme-files/instructions_mobile.png)  |
| Contact form | ![Contact desktop wireframe](readme-files/contact_desktop.png) | ![Contact mobile wireframe](readme-files/contact_mobile.png) |
| Create an account | ![Create account desktop wireframe](readme-files/create_account_desktop.png) | ![Create account mobile wireframe](readme-files/create_account_mobile.png) |
| Login             | ![Login desktop wireframe](readme-files/login_desktop.png)           | ![Login mobile wireframe](readme-files/login_mobile.png)       |
| Create new report | ![New report desktop wireframe](readme-files/new_report_desktop.png)     | ![New report mobile wireframe](readme-files/new_report_mobile.png)   |
| List reports      | ![List reports desktop wireframe](readme-files/list_reports_desktop.png) | ![List reports mobile wireframe](readme-files/list_reports_mobile.png) |
| Report detail     | ![Report detail desktop wireframe](readme-files/report_detail_desktop.png) | ![Report detail mobile wireframe](readme-files/report_detail_mobile.png) |
| Edit report       | ![Edit report desktop wireframe](readme-files/edit_report_desktop.png)    | ![Edit report mobile wireframe](readme-files/edit_report_mobile.png)   |


## Colour Scheme
![Colour scheme image](assets/readme-files/colour_palette.png)

The primary colour used on the website is burnt orange, which is the same colour used for the app logo. Orange was chosen because it is associated with energy, happiness, and vitality. Since orange lends itself well to other colours found in nature, it is complemented with mango, coffee brown, and a range of shades of khaki green. 

Mango is used for the menu background, button background, and the map search location results panel.

Coffee brown is used for the footer links.

The khaki green adds visual variety, and is used for message alerts, buttons, and the reasons field options.

## Typography

The main font used on the website is Open Sans with Sans Serif as the backup in case the former is not imported successfully. Bitter is used for the headings, as suggested by Figma as a complementary pairing with Open Sans, with Serif as the backup. 

## Features

### General

* Designed from a mobile first perspective.
* Responsive design across all device sizes.
* Hovering over a button or clickable section changes the cursor to a pointer to let the user know it is clickable.
* The base template defines the navbar, menu and footer used on every page of the website.
Navigation bar
Menu
Footer


## Technologies Used

### Languages Used

* [HTML5](https://en.wikipedia.org/wiki/HTML)
* [CSS3](https://en.wikipedia.org/wiki/CSS)
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
* [Python](https://en.wikipedia.org/wiki/Python_(programming_language))


### Libraries and Frameworks

* [Django](https://www.djangoproject.com/) is the web framework.

* [GeoDjango](https://www.djangoproject.com/) is a geographic web framework that builds on top of Django to create GIS (Geographic Information System)-enabled applications. This website uses the following GeoDjango features:
  
  * GIS model field MultiPolygonField for storing the county and local authority boundaries
  * Longitude, Latitude coordinate class Point()
  * Extend Django's ORM with spatial lookup `contains` to find the county that contains a Point.
  * Bulk-load shapefiles using the LayerMapping utility
  * Geo-admin integration

To set up GeoDjango on your computer, start with the [installation instructions](https://docs.djangoproject.com/en/5.2/ref/contrib/gis/install/) to install the requirements, and then move on to the [GeoDjango tutorial](https://docs.djangoproject.com/en/5.2/ref/contrib/gis/tutorial/) for instructions on how to configure the settings in Django.

Note that, under the hood, GeoDjango uses the following geospatial libraries to work with a PostgreSQL database:
* GEOS for fast in-memory geometry operations
* GDAL for reading/writing many geospatial file formats (Shapefile, GeoJSON, KML, etc.)
* PROJ for coordinate transformations

The best way to install these libraries on a Windows machine is to use the [OSGeo4W installer](https://trac.osgeo.org/osgeo4w/). The full set of instructions for Windows can be found [here](https://docs.djangoproject.com/en/5.2/ref/contrib/gis/install/#windows). 

For deployment on Heroku, detailed instructions are given in the [Deployment](#deployment) section. 
 
* [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/) is a CSS library used throughout the website to help with styling and responsiveness.

* [Bootstrap Icons](https://icons.getbootstrap.com/) were imported into the style.css file and used to create a better visual experience for UX purposes. 

* [Google Fonts](https://fonts.google.com) were used throughout the site.

* [Choices.js](https://github.com/Choices-js/Choices) is a JavaScript library used to create a multiselect field for the Report model attribute `reasons`.

* [htmx](https://htmx.org/) is used for rendering partial templates.

* [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/) is a JavaScript library used to create the interactive map on the 'Add Report' page.
  
### Django Packages and Dependencies

* [Django Allauth](https://django-allauth.readthedocs.io/en/latest/) is used for user authentication, registration, and account management.

* [Django Crispy Form](https://django-crispy-forms.readthedocs.io/en/latest/) is used to control the rendering of the forms. 

* [django-tables2](https://django-tables2.readthedocs.io/en/latest/) is used to generate tables (e.g. reports list) with sorting and pagination.

* [WhiteNoise](https://whitenoise.readthedocs.io/en/stable/django.html) is used to serve static files in production with no separate web server needed.

* [Psycopg](https://www.psycopg.org/docs/) is a PostgreSQL/PostGIS database adapter, which means that it is a bridge between Django and the PostgreSQL database.

* [DJ_Databse-URL](https://pypi.org/project/dj-database-url/) is used to parse the DATABASE_URL.

* [Gunicorn](https://gunicorn.org/) is used as Python WSGI HTTP Server for UNIX to support the deployment of Django application.  
  
* [Cloudinary](https://cloudinary.com/) is used as image management solution

### Database Management
* [Azure Database for PostgreSQL](https://azure.microsoft.com/en-gb/products/postgresql/) is used in production.

### Tools and Programs

* [Git](https://git-scm.com) was used for version control by utilizing the Gitpod terminal to commit to Git and Push to GitHub. 

* [GitHub](https://github.com)  
   GitHub was used to store the projects code after being pushed from Git. 

* [Heroku](https://www.heroku.com) is used to deploy the website.

* [Am I Responsive](ami.responsivedesign.is) was used to preview the website across a variety of popular devices.

* [Inkscape](https://inkscape.org/) was used to create the logo. 
  
* [Coolors](https://coolors.co) was used to create the colour palette image.

* [GitHub](https://github.com/) was used as follows:
    - Together with Git for version control and code hosting.
    - This README file serves as the main documentation for the project. 
    - Automatic deployment to Heroku every time the main branch is pushed to.

* [Balsamiq](https://balsamiq.com/) was used to create the wireframes during the design phase of the project.

* [Am I Responsive?](https://ui.dev/amiresponsive) was used to view the responsiveness of the website throughout the development process, and to generate the mockup images used at the top of this README.

* [Chrome DevTools](https://developer.chrome.com/docs/devtools/) was used during the development process to:
    - view how the code renders in a web browser
    - evaluate how the code functions and ensure it behaves as expected
    - test responsiveness
    - debug and refine code

* [W3C Markup Validator](https://validator.w3.org/)
    - W3C Markup Validator was used to validate the HTML code.

* [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)
    - W3C CSS Validator was used to validate the CSS code.

* [JSHint](https://jshint.com/) JavaScript Code Quality Tool was used to validate the JavaScript code.    

* [Favicon.io](https://www.favicon.io/) was used to create the site favicons.

[Back to top ⇧](#dropped-kerb-mapper)

## Testing

The testing documentation can be found [here](https://github.com/).


[Back to top ⇧](#dropped-kerb-mapper)

## Deployment

This website was developed using [Visual Studio Code](https://code.visualstudio.com/), which was then committed and pushed to GitHub using the terminal.

### Deploying on Heroku
To deploy this site to Heroku from its GitHub repository, take following steps:

1. Update the settings.py file:
    * Add 'your_app_name.heroku.com' to ALLOWED_HOSTS. Also add your domain name, if you have one.
    * Add the following to CSRF_TRUSTED_ORIGINS:
        "https://*.your_domain_name",

    Note that the following settings have already been added for deployment:
    * INSTALLED_APPS: 'cloudinary_storage', 'cloudinary',
    * MIDDLEWARE: 'whitenoise.middleware.WhiteNoiseMiddleware'
    * The database engine has been overridden to use GeoDjango's PostGIS backend: 
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
    * CSRF_TRUSTED_ORIGINS: "https://*.azurewebsites.net" "https://*.herokuapp.com",
   * STATIC_ROOT and STATICFILES_DIRS
   * STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

2. In your project root, create a file named Procfile (no extension) with:
   `web: gunicorn dropped_kerb_mapper.wsgi`

3. Push to GitHub
    * Commit all changes.
    * Push your code to your GitHub repository.

4. Create the Heroku App:
    - Log in to Heroku
    - Select New > Create new app
    - Choose a name for your app and select the region.

5. Provision Azure PostgreSQL Database
    * In the Azure Portal, create a new Azure Database for PostgreSQL (Flexible Server recommended).
    * Enable the PostGIS extension on your Azure PostgreSQL instance:
        - Connect to your database (e.g., with psql) and run:  
        ``` bash
        CREATE EXTENSION postgis;
        ```
    * Make sure your Azure PostgreSQL firewall allows connections from Heroku’s IP ranges.
    * Note your database host, name, username, and password.

6. Configure Heroku to Use Azure PostgreSQL
    * In your Heroku app dashboard, go to the 'Settings' tab and click 'Reveal Config Vars'.
    * Add a DATABASE_URL variable in the following format:
    ``` bash
    postgres://<username>:<password>@<host>:5432/<database>?sslmode=require
    ```

7. Add the remaining environment variables:
   * COLLECT
   * Your SECRET_KEY 
   * CLOUDINARY_URL
   * OS_MAPS_API_KEY
   * GOOGLE_MAPS_API_KEY
   * Email settings for your email provider:EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST.
   * GIT_LFS_REPOSITORY

8. Add the Heroku Geo Buildpack to install the GIS libraries GDAL, GEOS and PROJ, which are required for the PostGIS database extension. Go to the CLI by clicking More > Run Console, and enter

    ``` bash
    heroku create --buildpack https://github.com/heroku/heroku-geo-buildpack.git
    ```

9.  Connect Heroku to GitHub
   * In the 'Deploy' tab, connect your Heroku app to your GitHub repository.
   * Select the branch you want to deploy from.

10.  Deploy the App
    * In the 'Deploy' tab, click 'Deploy Branch'.
    * Wait for the build to complete.

11.   Run Migrations and Create Superuser
    * In the Heroku dashboard, go to 'More' > 'Run Console'.
    * Run:
    ``` bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

12.  Upload the County and Local Authority geography data (shapefiles) to the Azure PostgreSQL database
   * Create a fixtures folder in the mapper directory and add the shapefiles to it.
   * Since the shapefiles exceed the GitHub file size limit of 100MB, we use Git Large File Storage (Git LFS) to upload them as follows:
        - Install Git LFS in the repository by running the following command in VS Code:
        ``` bash
        git lfs install
        ```

        - Track the Large Files:
            Tell Git LFS to track your fixture files:
            ``` bash 
            git add mapper/fixtures/counties/
            git add mapper/fixtures/local_authorities/
            ```
            This command creates or updates a file called .gitattributes in your repository.

        - Add and commit the .gitattributes File:
            ``` bash
            git add .gitattributes
            git commit -m "Configure Git LFS for large fixture files"
            ```

        - Add and Commit the Fixture Files:
            Now add your fixture files as usual, then commit and push:
            ``` bash
            git add mapper/fixtures/counties/
            git add mapper/fixtures/local_authorities/
            git commit -m "Add large fixture files with Git LFS"
            git push
            ```    

    * Add the heroku-buildpack-git-lfs buildpack to heroku to download Github Large Files by running the following command in the Heroku CLI:

    ``` bash
    heroku create --buildpack https://github.com/infinitly/heroku-buildpack-git-lfs.git
    ```

    * Now you can add the data to the database via heroku CL, using the load_counties.py and load_local_authorities.py scripts:
  
    ``` bash
    python manage.py load_counties mapper/fixtures/counties/CTYUA_DEC_2024_UK_BFC.shp
    python manage.py load_local_authorities mapper/fixtures/local_authorities/Local_Authority_Districts_Boundaries_UK_BSC.shp
    ```

13. Visit the URL provided by Heroku to see your deployed app.

### Forking the Repository
Forking a GitHub Repository makes a copy of the original repository on your GitHub account, which you can view and/or make changes without affecting the original repository. To fork a repository:

1. Log into [GitHub](https://github.com/login) or [create an account](https://github.com/join).
2. Locate the [GitHub Repository](https://github.com/SonyaJane/dropped-kerb-mapper).
3. At the top of the repository, on the right side of the page, select "Fork"
4. You should now have a copy of the original repository in your GitHub account.

### Creating a Clone

How to run this project within a local IDE, such as VSCode:

1. Log into [GitHub](https://github.com/login) or [create an account](https://github.com/join).
2. Locate the [GitHub Repository](https://github.com/SonyaJane/dropped-kerb-mapper).
3. Under the repository name, click "Clone or download".
4. In the Clone under the HTTPs section, copy the clone URL for the repository.
5. In your local IDE open the terminal.
6. Change the current working directory to the location where you want the cloned directory to be made.
7. Type 'git clone', and then paste the URL you copied in Step 3.

```
git clone https://github.com/SonyaJane/mobility-mapper-frontend
```
8. Press Enter. Your local clone will be created.

Further reading and troubleshooting on cloning a repository from GitHub [here](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/cloning-a-repository)


## Finished Product

| Page | Desktop | Mobile |
| --- | --- | --- |
|

[Back to top ⇧](#dropped-kerb-mapper)

## Future Features



## Credits 

### Content

- All content was written by the developer.

### Media

- Dropped Kerb Mapper logo: Created by the developer in Inkscape
- Home page hero image: Photo taken by the developer.

[Back to top ⇧](#mobility-mapper-frontend)


NOTE
Both the OS map tiles and Google Satellite tiles return a 404 response when a tile does not exist at a given zoom level, but the OS map continues to display the last available tiles while the Google Satellite map does not. This is because MapLibre GL reuses the last available tiles when a tile cannot be fetched. However, the HTTP **response headers** returned by the backend for the 404 response differ between the OS map and Google Satellite tiles. The OS map tiles include caching headers (e.g., Cache-Control) that allow MapLibre GL JS to reuse the last available tiles. The Google Satellite tiles lack these headers, causing MapLibre GL JS to treat the 404 response as a hard failure.
Solution:
Add the appropriate caching headers to a 404 response for the get_google_satellite_tiles view.


Google aerial view 5000 free map views per month
Find the maximum zoom level for satellite imagery at a specific location.
Google Maximum Zoom Imagery service in the Maps JavaScript API (example)
https://developers.google.com/maps/documentation/javascript/maxzoom?_gl=1*udr88s*_up*MQ..*_ga*NTMyNzE0NzAxLjE3NDI4MjI0MDc.*_ga_NRWSTWS78N*MTc0MjgzNDYyMy4zLjAuMTc0MjgzNDYyMy4wLjAuMA..


Use Mapbox Satellite through any of Mapbox's APIs and SDKs with the tileset ID mapbox.satellite.
https://docs.mapbox.com/api/maps/raster-tiles/
Raster Tiles API
750,000 free monthly requests



Customise the Django admin form with some JavaScript so that the reasons field only appears if the condition selected is red or orange.

## Javascript Libraries

MapLibre GL JS for interactive mapping
