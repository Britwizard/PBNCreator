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

In the files created there is also information about the double dummy analysis
