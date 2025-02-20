# Dropped-Kerb Mapper

The purpose of this web application is to enable users to record the location of dropped kerbs in the UK. The data gathered will be used by the [Mobility Mapper](https://www.mobilitymapper.co.uk/) platform to generate accessible routes for users of wheeled mobility devices.

Users are able to rate the dropped kerb using a traffic light system, where:

<table>
  <tr>
    <td><img src="./readme-files/traffic-lights.png" width=75><br><br></td>
    <td>Red: Dangerous or unusable. <br> Orange: Usable but needs improvement <br> Green: Usable and in good condition.<br> Blue: A dropped kerb is not present but should be. A wheeler is prevented from entering or exiting the pavement at this point, in order to connect to another section of pavement or road.</td>
  </tr>
</table>


## User Stories

**View comments**: As a Site User / Admin I can view comments on an individual post so that I can read the conversation  
> **AC1** Given one or more user comments the admin can view them.  
> **AC2** Then a site user can click on the comment thread to read the conversation.

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
