# vpc-get-high-scores-image

This tool will pull data and create high score images for PinUP Popper to display when a mapped button is pressed. This brings the VPC High Scores onto your cab. It can update on startup of your cab and when entering and exiting the table.

**CAUTION: Please make sure you backup your PinUP Popper DB before making these changes!!!**

## **Adding VPS Id to table(s) in PinUP Popper**

1. This tool requires the use of the VPS ID from <https://virtualpinballspreadsheet.github.io/> (hereby known as VPS). The easiest way to add the VPS Id to a table is through the import process via PinUP Popper.

You can see the VPS Id for a table in the image below:
![image](vps_id_location.png)

**1a.** Download an updated version of the puplookup.csv from VPS to the PinUPSystem folder from: <https://virtualpinballspreadsheet.github.io/export>

**1b.** You now need to import data for each new table so it picks up the VPS ID into the field you configured in Pinup Popper Lookup settings tab in the Game Manager (add VPS-ID to the field).

## **Setup the batch file to run on Windows startup**

1. Using <https://github.com/emb417/vpc-get-high-scores-image/releases>, download the following files to the `C:\Pinball\PinUPSystem\LAUNCH` folder (**IMPORTANT: BE AWARE THE LAUNCH FOLDER MIGHT BE IN A DIFFERENT LOCATION IF YOU HAVE USED BALLER INSTALLER**).

2. Open `POPMENU_GetHighScoresForAllTables.bat` and edit line 3 to conform to your field.
   - Example: `"%_curloc%\vpc-get-high-scores-image.exe" "True" "" "CUSTOM3" "%_ParentFolderName%" "%_ParentFolderName%\POPmedia\Visual Pinball X\Other2" "10" ""`
     - **You will need change the CUSTOM3 field above to match the field you have chosen to house the VPS Id in Step 1 - 1b**

3. Create a shortcut to `POPMENU_GetHighScoresForAllTables.bat`

4. Copy the shortcut to your Windows startup folder

## **Setup scripts to run the vpc-get-high-scores-image.exe on Launch and Close of the table**

1. Pinup Popper Setup > Popper Setup Tab > Emulators > Visual Pinball X > Launch Setup Tab
   - Paste the following at the end of 1. **Launch Script** and 2. **Close Script**:
     - `START /min "" "[STARTDIR]LAUNCH\vpc-get-high-scores-image.exe" "False" "[CUSTOM3]" "CUSTOM3" "C:\Pinball\PinUPSystem" "C:\Pinball\PinUPSystem\POPMedia\Visual Pinball X\Other2" "10" ""`
       - **You will need change the CUSTOM3 fields above to match the field you have chosen to house the VPS Id in Step 1 - 1b**
2. Save and Close

## **Enable Display to Show Other2**

1. Pinup Popper Setup > Popper Setup Tab > GlobalConfig button > Displays tab
   - Set `Other 2` = `Active Hidden`
2. Save

3. Pinup Popper Setup > Popper Setup Tab > Screens / Themes button

4. In Pup Pack Editor
   - Change Mode field of `Other` to `ForcePop`
5. Click "Save PuP-Pack" button

## **Configure and Place the Other Display**

1. On the same "PuP Editor" screen, click "Configure Display/Locations" button

2. On the "PinUP Player DIsplays" window, click on `Other2` in the "Select Screen" list

3. Adjust this display to your liking. This will be the display for the high scores.
   - Suggestions for main playfield screen:
     - Rotation: `270`
     - Width: `700` (or `350`)
     - Height: `1172` (or `586`)
     - Default State: `off`
4. Click "Save Settings" button

5. Close "PuP Pack Editor" window

## **Configure key in PinUP Popper to display Other2 (the high score image)**

1. On "PinUP Popper Setup" window, click "Controller Setup" button

2. Assign key press to `Show Other` entry

3. Click "Close" button

4. On "PinUP Popper Setup" window, click "Exit Setup" button

## **Test Getting High Scores**

1. Navigate to the C:\Pinball\PinUPSystem\LAUNCH folder

2. Run `POPMENU_GetHighScoresForAllTables.bat`
   You should see a command window start executing and pulling down the images...
   You should also be able to check your `C:\Pinball\PinUPSystem\POPMedia\Visual Pinball X\Other2` folder to see the high score images being created.

3. Run PinUP Popper

4. Navigate to a table

5. Press button to display Other2 that you set in step #19.

## **Refreshing All High Scores While in PinUP Popper**

1. Get to the Operator Menu in PinUP Popper

2. Scroll to Custom Scripts

3. Press GetHighScoresForAllTables
