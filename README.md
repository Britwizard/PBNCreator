# PBNCreator
PBNCreator is a Windows based application written in Python.
The purpose of the app is to:
- Create files in Portable Bridge Notation (pbn) which are used to deal boards that are used in the playing card game of duplicate bridge.
- To produce a .pdf file that gives details of the boards and open this file in Adobe Acrobat so that it may be printed.

Boards contain all 52 cards of a pack of playing cards in 4 'hands' of 13 cards. A physical board looks like this:

![image](https://user-images.githubusercontent.com/93732783/142861642-13919e7b-91b9-4312-881e-d521fe2f93de.png)

The app repeatedly randomly shuffles and deals the 4 hands and adds details to a file in a fixed notation to make up a single board.
Up to 30 boards may be created in a single pbn file.
The pbn files are created in a folder and have the file extension '.pbn'.

pbn files are used by automatic card dealing machines to deal physical boards and playing cards.  There are a number of different dealing machines:

![image](https://user-images.githubusercontent.com/93732783/142860123-12acc832-2839-4477-8d41-b2257a661bc0.png)

![image](https://user-images.githubusercontent.com/93732783/142861223-381224f9-b64b-4412-8573-5e10002a0f3d.png)

The pbn file, as well as containing information about the hands to be dealt has additional information:

- The site name: that is the place where the game of duplicate bridge is to be played.
- The event name: that could be something like 'Monday afternoon' or 'Social Pairs' or 'Individual Tourney'
- The playing date

In the files created there is also information about the double dummy analysis which gives the number of tricks that can be made by a dealer in each of the suit or in no trumps.  The algorithm used is the Bo Haglund double dummy solver available as open source in Afwas/python-dd.   (A slight problem was found with this code in that it used a Python function os.path.abspath() that caused the code to fail when converted into an exe with pyinstaller.  For this reason the opensource ddstable.py code was copied into a local file PBNdds.py and the code that used this function was recoded in a different way.)


## Features
The features of PBNCreator are:
1. Specify a Site Name, Event Name and the number of boards to be generated in each PBN file
2. Choose a range of dates between which a single PBN file will be generated at the rate of one per week.
3. Specify the weekday on which the bridge session is to be played.
4. Specify a folder (directory) into which the PBN files are to be saved.  File names are of the form YYMMDD.pbn where the playing date of the bridge session is DD/MM/YYYY.  E.g. the file named  211101.pbn would have a playing date of 01/11/2021.
4. Optionally select to produce a pdf file of the boards in the set of pbn files.  For each of the PBN files a single page is formatted showing all the boards in the file. For each board it shows the board number, the dealer and vulnerability, the hands, the high card points for each hand and the double dummy analysis indicating makeable tricks by each player in each suit and no trumps.  The pdf file is created as a temporary file that is opened in Adobe Acrobat at the end of the file generation so that it may be saved or printed.
5. The ability to set up a default Site Name, Event Name, number of boards and an option to reject any board where no hand has more than 11 points (such hands are likely to be passed out during the bidding and as such they may be undesirable.

## Operation
When the program starts  for the first time the following window will be displayed:

![image](https://user-images.githubusercontent.com/93732783/143018989-c41dd117-ab77-4a1c-9382-85d6563f438d.png)

Click on the ‘Edit’ menu and select ‘Settings’.  The following window is displayed:

![image](https://user-images.githubusercontent.com/93732783/143019129-60e65301-6a93-44ba-87c3-ea249538c599.png)


Enter the default Site Name, Event Name, Number of boards and make a choice of whether to reject boards where no hand has more than 11 points- for example:

![image](https://user-images.githubusercontent.com/93732783/143019221-3e6cde9b-8c52-464b-a208-b666fee3fbfd.png)

The number of boards must be greater than 1 and less than 31 otherwise an error will be given.
Click the OK button. The Settings window will close and the original window will appear as:

![image](https://user-images.githubusercontent.com/93732783/143019285-9dab104f-669a-4a4d-91e6-f0ccbd831fd8.png)


The Site Name, Event Name and number of boards are filled in from the settings.
You now need to set up the Start and End Dates.  Clicking on down arrow button ˅ on the date field will give a calendar as shown in the following figure:

![image](https://user-images.githubusercontent.com/93732783/143020105-0cc805f4-d5be-49a9-9747-b8bd6927b06e.png)


This can be used to select a date.  The End date must be at least 7 days greater than the Start date.
From the Day of the week selection list choose the weekday for which the pbn file is to be generated:

![image](https://user-images.githubusercontent.com/93732783/143020226-dca46440-a141-4c7e-8fc1-94f65cf43fba.png)


Click the PDF file? checkbox if you want a file.  If this checkbox is not clicked then pdf file is not produced but the pbn files are still created:

![image](https://user-images.githubusercontent.com/93732783/143020387-a686a9db-5793-46bc-ac6a-a99720597096.png)

Click the ‘Generate File’ button and the following Select Folder window is opened:

![image](https://user-images.githubusercontent.com/93732783/143020512-fb048e69-b56a-4e83-80b3-770e90cea355.png)


Select a previously created folder into which the pbn files are to be stored or create a new folder for the files using the New folder facility. When the ‘Select Folder’ button is clicked the pbn file generation will begin.  
When all the pbn files have been generated  then if the PDF File?  checkbox  has been selected the pdf file will open in the default application for viewing pdf files. This is usually Adobe Acrobat.  The user can then print this file, that contains as many pages as there are pbn files, to their chosen printer or save it to a file of their own. 
A typical page printout of a 30 board PBN file will appear as follows:

![image](https://user-images.githubusercontent.com/93732783/143021457-09d61d3d-d303-4567-b956-aca2e289bf7a.png)




