'''
#PBN_Generator
#Version 1 - Initial Version
#Version 2 - Add printing
#Version 3 - Add Settings to menu
#Version 4 - Add option to settings to reject boards with no hand having more than 11 HCP
#Version 5 - Open pdf file in default application.
'''
# Public imported modules
from tkinter import *    # this does not load all of tkinter - it does not load the ttk modules or messagebox for instance
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkcalendar import DateEntry
import datetime
import win32api
import win32print
import os,sys
# Private imported modules
import PBNPrintHandRecords as pbnp
import PBNMakefiles as makefiles

# This function is called when the Generate Files button is clicked to 
# validate the data entered on the window,generate the pbn files and print out the sheets.
def GenFiles():
    global passedout
    site = site_field.get()
    event = event_field.get()
    if event == ''or  site=='': 
        messagebox.showerror(title="Error",message="You must enter the Site and Event.")
        return
    
    startdatestring = startdate_field.get()
    enddatestring = enddate_field.get()
    
    start_date = datetime.datetime.strptime(startdatestring,'%d/%m/%Y')
    end_date = datetime.datetime.strptime(enddatestring,'%d/%m/%Y')
    if end_date < start_date:
        messagebox.showerror(title="Error",message="The end date is less than the start date.")
        dayofweek_field.current(0)
        return
    day_of_week = dayofweek_field.get()
    if day_of_week == '':
        messagebox.showerror(title="Error",message="Day of week not specified.")
        return
        
    boards = boards_field.get()
    if not boards.isnumeric():
        messagebox.showerror("Error","Invalid number of boards")
        return
    no_of_boards =int(boards)
    if no_of_boards > 32 or no_of_boards < 1:
        messagebox.showerror("Error","Number of boards outside limits")
        return    

    
    if pdf_file.get() > 0:
        Pdf_file=True
    else:
        Pdf_file=False
    
    day_found=False
    # advance date from start date until day of week is reached.    
    current_date=start_date
    while current_date <= end_date:
        weekday=(current_date.strftime("%A"))
        if weekday==day_of_week: 
            day_found=True
            break
        # Advancing current date by one day
        current_date += datetime.timedelta(days=1)
    if day_found is False:                         # No bridge sessions between start and end date
        messagebox.showerror("Error","Insufficient days between start and end date")
        return
    
    # Get the folder for the pbn files
    folder_path=filedialog.askdirectory()
    if folder_path=='':
        messagebox.showerror("Error","Please select a folder for pbn files.\nTo do this click Generate button again.")
        return
    
    directory_label.configure(text = "Generating Files in: " + folder_path)
    
    no_of_days=int(abs((end_date - current_date).days))
    if no_of_days == 0:
        pb_increment = 100
    else:
        pb_increment = abs(100/(no_of_days/7))                # increment of progress bar required for each week between start and end date

    while current_date <= end_date:
        # Create the PBN file for the given date and return headings, hand and double dummy data for printing
        return_heading_data,return_hand_data,return_dd_data=makefiles.CreatePBNfile(folder_path,current_date,no_of_boards,event,site,passedout) # generate the pbn file
        if return_heading_data['Event']=='X':            # if an error occured when trying to open the PBN file an X is place in the Event name
            messagebox.showerror("Error","pbn file already exists - generation abandoned")
            return
        if Pdf_file:
            pdf,f=pbnp.PrintPBNFile(return_heading_data,return_hand_data,return_dd_data, no_of_boards) #create pdf file to print out all the deals
            
        current_date+= datetime.timedelta(days=7)                   #advance to the following week
        mainwindow.update_idletasks()
        pb1['value'] += pb_increment

    if Pdf_file:
        pdf.output(f) # write the data to a pdf file.
        os.startfile(f)  # open the pdf file in default pdf application (Normally Adobe Acrobat) 
        
    messagebox.showwarning("Success","File generation complete")
    sys.exit(0)
# END OF PROGRAM EXECUTION

# Get default settings if they have been set up
def GetSettings():
    global passedout
    site=''
    event=''
    boards=''
    appdata=os.getenv('LOCALAPPDATA')
    folder_path= os.path.join(appdata,"PBNCreator")
    settingsfileName="PBNCreator_Settings.txt"
    filename=os.path.join(folder_path,settingsfileName)
    if os.path.exists(filename):
        file= open(filename,"r")
        settings=file.read()
        settingslist = settings.split('¬')
        if len(settingslist) != 4:
            messagebox.showerror("Invalid Settings File: " + settingsfileName)
            exit()
        site = settingslist[0]
        event = settingslist[1]
        boards= settingslist[2]
        passedout=settingslist[3]
    return(site,event,boards,passedout)
#Enter default settings for the Event, Site and Number of boards 

def settings():
    
    
    settingswin=Toplevel(mainwindow)
    settingswin.title("Settings")
    
    settingswin.iconbitmap("PBNCreator.ico")
    settingswin.geometry("350x230")
    settingssite_label=Label(settingswin,text="Site Name:")
    settingssite_label.place(x=20, y=30)
    settingssite_field=Entry(settingswin,width=30)
    settingssite_field.place(x=130,y=30)

    settingsevent_label=Label(settingswin,text="Event Name:")
    settingsevent_label.place(x=20, y=70)
    settingsevent_field=Entry(settingswin,width=30)
    settingsevent_field.place(x=130,y=70)

    settingsboards_label=Label(settingswin,text="Number of boards:")
    settingsboards_label.place(x=20, y=110)
    settingsboards_field=Entry(settingswin,width=3)
    settingsboards_field.place(x=130,y=110)
    passed_out=IntVar()
    settingspassed_out_field=Checkbutton(settingswin,text="Reject boards where no hand has more than 11 points",variable=passed_out)
    settingspassed_out_field.place(x=20, y=150)

    OKbutton=Button(settingswin,text="OK",width=7,command=lambda:settingsOK(settingswin,settingssite_field.get(),\
        settingsevent_field.get(),settingsboards_field.get(), passed_out.get()))
    OKbutton.place(x=50,y=190)

    Cancelbutton=Button(settingswin,text="Cancel",width=7,command=lambda:settingswin.destroy())
    Cancelbutton.place(x=110,y=190)
    site,event,boards,passedout= GetSettings()
    settingssite_field.insert(0,site)
    settingsevent_field.insert(0,event)
    settingsboards_field.insert(0,boards)
    if passedout =='1':settingspassed_out_field.select()
# OK button clicked in Settings window - save settings in a file and put settings onto window
    
def settingsOK(settingswin,site,event,boards,passed_out):
    global passedout
    passedout = str(passed_out)
    settings=site+"¬"+event+"¬"+boards+"¬"+passedout
    appdata=os.getenv('LOCALAPPDATA')
    Folder_name="PBNCreator"
    folder_path = os.path.join(appdata,Folder_name)
    if not  os.path.exists(folder_path):
       os.mkdir(folder_path)
    settingsfileName="PBNCreator_Settings.txt"
    filename=os.path.join(folder_path,settingsfileName)
    if os.path.exists(filename):
        os.remove(filename)
    file = open(filename,"w")
    file.write(settings)
    file.close()
    settingswin.destroy()
    
    site_field.delete(0,END)
    event_field.delete(0,END)
    boards_field.delete(0,END)

    event_field.insert(0,event)
    boards_field.insert(0,boards)
    site_field.insert(0,site)  
# The help window
def Help():
    Helpwin=Toplevel(mainwindow)    
    Helpwin.title("Help")
    Helpwin.geometry("700x660")
    Helptext = Text(Helpwin,height=38, width=85)
    Helptext.tag_configure('normal',font=("Arial",12))
    Helptext.tag_configure('big',font=("Verdana",16,'bold'))
    Helptext.insert(END,"\n   How to use PBNGenerator\n\n",'big')
    Helptext.insert(END,"   1. Create a folder into which the pbn deal files are to be stored.\n\n","normal")
    Helptext.insert(END,"   2. Start up PBNGenerator app.\n\n","normal")
    Helptext.insert(END,"   3. If this is the first time the app has been used: \n\n","normal")
    Helptext.insert(END,"      \u25CF Call up Settings from the 'Edit' menu.\n\n","normal")
    Helptext.insert(END,"      \u25CF Enter the default Site, Event and number of boards to be dealt.\n\n","normal")
    Helptext.insert(END,"      \u25CF Click OK to save.\n\n","normal")
    Helptext.insert(END,"   4. Select the start and end dates for which weekly files are to be generated. You can click\n \
       on the downarrow next to the date to bring up a calendar.\n\n","normal")
    Helptext.insert(END,"   5. Select the day of the week on which the bridge session is to be played.\n\n","normal")
    Helptext.insert(END,"   6. If you want printed sheets showing the hand records for each of the pbn files select\n      'Print Sheets'.\n\n","normal")
    Helptext.insert(END,"   7. Click the 'Generate' button.  A 'Select Folder' window will open. Select the folder\n \
       created in step 1 and click OK.\n\n","normal")
    Helptext.insert(END,"      That's it - the files will be generated and sheets printed to the default printer.\n\n","normal")
    Helptext.insert(END,"      The names of the files will be in the form 'YYMMDD.pbn' where the playing date is DDMMYYY.\n\n","normal")
    Helptext.insert(END,"      To produce pbn files for more than one day in the week, change the event and repeat the\n \
       above process from step 5 but choose a different weekday.\n\n","normal")
    Helptext.insert(END,".\n\n","normal")
    Helptext.pack()
    Closebutton=Button(Helpwin,text="Close",width=7,command=lambda:Helpwin.destroy())
    Closebutton.pack(side = BOTTOM, pady =10)

def About():
    Aboutwin=Toplevel(mainwindow)
    Aboutwin.title('About')
    LabelVariable=StringVar()
    TextLabel=Label(Aboutwin, textvariable=LabelVariable, justify=LEFT, width=35, wraplength=200)
    TextLabel.pack()
    LabelVariable.set("\n\n  PBN Generator is a program developed by Peter Ellington in the Python Programming Language.\n\n \
  The purpose of the program is to generate files in Portable Bridge Notation suitable for dealing on a dealing \
machine. The files, that have a file extension of 'pbn', can also be uploaded to a website along with the results \
of a duplicate bridge session so that hands can be displayed on-line.\n\n \
                      Version 1.0\n\n \
                          2021\n\n")

mainwindow=Tk()
mainwindow.title("Generate Dealing Files")
mainwindow.geometry("400x430")
mainwindow.resizable(False,False)
passed_out=IntVar()  # option variable = 1 if board with no hand have more than 11 HCP is to be rejected
passedout = str(passed_out)
mainwindow.iconbitmap("PBNCreator.ico")

site_label=Label(mainwindow,text="Site Name:")
site_label.place(x=20, y=30)
site_field=Entry(mainwindow,width=30)
site_field.place(x=130,y=30)

event_label=Label(mainwindow,text="Event Name:")
event_label.place(x=20, y=70)
event_field=Entry(mainwindow,width=30)
event_field.place(x=130,y=70)

boards_label=Label(mainwindow,text="Number of boards:")
boards_label.place(x=20, y=110)
boards_field=Entry(mainwindow,width=3)
boards_field.place(x=130,y=110)
#Set up fields with default settings
site,event,boards,passedout= GetSettings()
event_field.insert(0,event)
boards_field.insert(0,boards)
site_field.insert(0,site)
startdate_label=Label(mainwindow,text = "Start Date:")
startdate_label.place(x=20, y=150)
startdate_field= DateEntry(mainwindow, width=11, locale='en_GB', background='darkblue',foreground='white', borderwidth=2)
startdate_field.place(x=130,y=150)

enddate_label=Label(mainwindow,text = "End Date:")
enddate_label.place(x=20, y=190)
enddate_field= DateEntry(mainwindow, width=11, locale='en_GB', background='darkblue',foreground='white', borderwidth=2)
enddate_field.place(x=130,y=190)

daysofweek=["","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
dayofweek_label=Label(mainwindow,text="Day of the week:")
dayofweek_label.place(x=20, y=230)
dayofweek_field=ttk.Combobox(mainwindow,values=daysofweek,width=11)
dayofweek_field.place(x=130,y=230)

pdf_file=IntVar()
print_checkbox = Checkbutton(mainwindow,text='PDF File?',variable=pdf_file) 
print_checkbox.place(x=130,y=270)

Generate_button = Button(mainwindow, text="Generate Files", command=GenFiles,width=11)
Generate_button.place(x=130,y=310)
Generate_button['state']=NORMAL

directory_label=Label(mainwindow,text="")
directory_label.place(x=20, y=350)
pb1 = ttk.Progressbar(mainwindow, orient=HORIZONTAL, length=200, mode='determinate')
pb1.place(x=70, y=390)
# Set up Settings menu
menubar=Menu(mainwindow)
Editmenu=Menu(menubar,tearoff=0)
Editmenu.add_command(label="Settings",command=settings)
Editmenu.add_command(label="Exit",command=mainwindow.quit)
menubar.add_cascade(label="Edit",menu=Editmenu)
Helpmenu=Menu(menubar,tearoff=0)
Helpmenu.add_command(label="PBGenerator Help",command=Help)
Helpmenu.add_command(label="About PBGenerator",command=About)
menubar.add_cascade(label="Help",menu=Helpmenu)

mainwindow.config(menu=menubar)
site_field.focus()
mainwindow.mainloop()