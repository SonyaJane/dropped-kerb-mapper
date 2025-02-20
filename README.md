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

**Record a Dropped Kerb (Epic)**: As a Site User I want to add the location of a dropped kerb by clicking on the location on a map, then categorise the dropped kerb using the traffic light classification system, then click the approriate check boxes to provide further details on why that category was selected, and taking a photo so that I can contribute accurate data to the Mobility Mapper platform.

**Acceptance Criteria**

> Interactive Map:
- The user is presented with an interactive map on the submission page.
- The user can click on the map to select the exact location of the dropped kerb.
- A marker is placed on the map at the clicked location to confirm the selection.

> Traffic Light Classification:
- The submission form displays the four traffic light options (red, orange, green, blue) clearly.
- The user is required to select one of the classification options before submitting the report.

> Additional Details via Checkboxes:
- Upon selecting a traffic light category, a set of relevant checkboxes appears with predefined reasons or characteristics explaining the selected category.
- The user can select one or more checkboxes to provide further context.

> Photo Capture/Upload:
- The form provides an option for the user to either capture a new photo using their device’s camera or upload an existing photo.
- The photo field is not required but must accept only valid image formats.

> Form Validation and Submission:
- The form validates that a map location, a traffic light classification, and if a photo has been provided, that is a valid image format.
- If any required field is missing, the user receives clear error messages indicating what needs to be completed.
- Upon successful submission, a confirmation message (or modal) is displayed to the user.

> Data Storage:
- The report submission, including the selected map location, classification, additional checkbox details, and photo, is saved correctly in the database.
- The submission is timestamped and linked to the user’s account for future reference.

**Account registration**: As a Site User I can register an account so that I can add locations of dropped kerbs.
> Given an email a user can register an account.  
> Then the user can log in.  
> When the user is logged in they can add the locations of dropped kerbs (reports).  

**View, edit or delete the location of a dropped kerb**: As a Site User I want to view, edit or delete my reports so that I can correct errors, or update information if the situation changes.

**Acceptance Criteria**

> Given a logged in user, they can modify the information on their reported location  
> Given a logged in user, they can delete their reported location  
> The user can access a list of their submitted dropped kerb reports.
> Each report can be selected to view its information.
> An 'Edit' option is available that allows modification of the location, categories,or photo.
> Changes are validated before being saved.
> The user receives a confirmation message upon successful update.

**Manage reports**: As a Site Admin I can review, verify, update and delete reports so that the dataset is accurate and reliable. 
> An admin dashboard is available listing all new reports.
> Admins can click on a report to view full details, including location, classifications and images.
> A report can be deleted or updated

**View Map of Reported Dropped Kerbs**: As a user, I want to see a map displaying all reported dropped kerbs so that I can understand accessibility challenges in my area.

**Acceptance Criteria**

> A map view plots markers for all reported dropped kerbs.
> The colour of the marker is the given traffic light classification (red, orange, yellow, green, blue)
> Each marker displays a brief summary (photo thumbnail, classification) when clicked.
> Basic map functionalities like zoom and pan are enabled.
> The map updates to reflect new reports in near real-time or via a refresh option.

**Filtering and Searching Data**: As an administrator, I want to filter and search reports by location, date, and sclassification so that I can efficiently manage and analyse the data.

**Acceptance Criteria**

> Admins can filter reports by geographic parameters (e.g., city, postcode) and by date range.
> A severity filter (if applicable) is available to categorize reports based on impact.
> Multiple filters can be applied simultaneously for refined searching.
> The search results are accurate and displayed in a timely manner.

**Sharing and Social Engagement**: As a site administrator, I want to share a report or a map view of dropped kerbs via social media or a shareable link so that I can raise awareness of local accessibility issues.

**Acceptance Criteria**

> A shareable link is generated for individual reports or map views.
> The shareable link includes metadata (such as a preview image and description) for social platforms.
> Social media sharing buttons (if implemented) are available and functional.
> The shared content renders correctly on major social networks.



## Development Log

1. Created local folder "dropped-kerb-mapper"
2. Created "dropped-kerb-mapper" repository on GitHub
3. Initialised repository locally on the command line:
   
   ```
   echo "# dropped-kerb-mapper" >> README.md
    git init
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin https://github.com/SonyaJane/dropped-kerb-mapper.git
    git push -u origin main
    ```

4. Define purpose of the application.
5. Create user stories.
