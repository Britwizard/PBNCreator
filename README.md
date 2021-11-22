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



