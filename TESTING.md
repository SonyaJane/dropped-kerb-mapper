## Testing User Stories

1. **Add a dropped kerb location**  
   As a Site User I want to add the location of a dropped kerb by clicking on a map so that I can contribute accurate data to the database.  

   **Acceptance Criteria**  
   - An interactive map is displayed on the submission page.  
   - Clicking on the map places a marker at the chosen point.  
   - The latitude and longitude of the marker are captured in the form.  

2. **Categorise the condition**  
   As a Site User I want to classify the dropped kerb using a traffic-light system so that others know its usability.  
   **Acceptance Criteria**  
   - The form shows a dropdown box with five options: None (default), Red, Orange, Green, or White.  
   - One option can be selected.  

3. **Provide reasons for the classification**  
   As a Site User I want to supply one or more contextual reasons for my condition choice so that I can explain my assessment.  
   **Acceptance Criteria**  
   - If the user selects Red or Orange, a dropdown list appears with relevant reasons or characteristics explaining the selected category.  
   - The user can select multiple reasons to provide context.

4. **Upload a photo**  
   As a Site User I want to optionally upload a photo of the dropped kerb so that others can visually verify its condition, and wheelers can judge for themselves if they can use it.
   **Acceptance Criteria**  
   - The form accepts image files (jpg, png, webp).  
   - Uploaded images are converted to WebP and compressed.  
   - Photo upload is optional but validated if provided. 

5. **Receive submission confirmation**  
   As a Site User I want to see a success message when my report is saved so that I know my contribution is recorded.  
   **Acceptance Criteria**  
   - On valid submission, an HTMX partial confirms success inline.  
   - The new marker appears on the map without a full page reload.  

6. **Register and log in**  
   As a Site User I can register an account and log in so that I can create, view, edit, and delete my own reports.  
   **Acceptance Criteria**  
   - Users sign up with email and password.  
   - Email confirmation link auto-confirms and logs the user in.  

7. **Edit a report**  
   As a Site User I want to edit my existing report so that I can correct mistakes or update information.  
   **Acceptance Criteria**  
   - The edit form is pre-populated with the original data.  
   - On valid update, a success message displays and redirects to detail view.  

8. **Delete a report**  
   As a Site User I want to delete my own report so that I can remove obsolete or erroneous entries.  
   **Acceptance Criteria**  
   - Only the owner or a superuser may delete.  
   - After deletion, the user is redirected to the reports list with a success message.  

9. **View a map of reports**  
   As a Site User I want to see all my reports plotted on an interactive map so that I can visualise their locations.  
   **Acceptance Criteria**  
   - Markers are colour-coded by condition.  
   - Clicking a marker shows a summary popup with thumbnail and condition.

10. **Contact support**  
    As a Site User I want to send feedback or questions via a contact form so that I can communicate with the site team.  
    **Acceptance Criteria**  
    - The contact page shows a form asking name, email, and message.  
    - On valid submission, emails are sent to the admin and a confirmation to the user.  
    - A success message displays on the contact page.  
  
11. **Filter and search reports (admin)**  
    As a Site Admin I want to filter and search all reports by date, user, location, or condition so that I can manage the data.  
    **Acceptance Criteria**  
    - The django admin interface provides sidebar filters for condition, reasons, user, and date.  
    - A search box allows keyword lookup in reasons and comments.  

12. **Proxy map tiles**  
    As a user the app should load consistent map tiles so that I see the same Ordnance Survey and Google Satellite imagery.  
    **Acceptance Criteria**  
    - OS raster tiles are served via the `/os_tiles/…/` endpoint with caching headers.  
    - Google satellite tiles use a valid session token and return proper cache controls on 404.  
