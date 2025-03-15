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
27.  Create models in /mapper/models.py based on the Entity Relationship Diagram.



## Javascript Libraries

MapLibre GL JS for interactive mapping
