#PBNprinthandlayouts

import os
import tempfile
import datetime
import math
from fpdf import FPDF
#layout limits
left_margin = 8
board_column_width=9
dealer_column_width =12
hands_width = 43
HCP_width =7
dd_width=28
layout_width = left_margin + 2*(board_column_width + dealer_column_width + hands_width + HCP_width + dd_width)
heading_height=4
deal_height=17
top_line=20
line_separation = 4                 # height of each line of hands, HCP 
dd_line_separation = 3              # height of each line of double dummy 
convert_table1={'a':'10','b':'11','c':'12','d':'13'}
HCP_values={'A':4,'K':3,'Q':2,'J':1}
points = ['N','S','E','W']
suit_chars = ['ª','©','¨','§']    # ♠♥♦♣ in Symbol font
dealer_vulnerable_list=['N/None','E/N-S','S/E-W','W/Both','N/N-S','E/E-W','S/Both','W/None','N/E-W','E/Both','S/None','W/N-S','N/Both','E/None','S/N-S','W/E-W']

#remove any existing pdf files in the the temporary directory if possible
# Beware that some of the pdf files in the directory may be used by another process or be inaccessible so
# use a try/except block and ignore any pdf files that cannot be deleted
tempfile_directory = tempfile.gettempdir()
files_in_directory = os.listdir(tempfile_directory)
filtered_files = [file for file in files_in_directory if file.endswith(".pdf")]
for file in filtered_files:
    path_to_file =  os.path.join(tempfile_directory, file)
    try:
        os. remove(path_to_file)
    except:
        continue
    
f = tempfile.mktemp(".pdf")
pdf = FPDF()
def PrintPBNFile(return_heading_data,return_hand_data,return_dd_data, no_of_boards):
    
    Site=return_heading_data['Site']
    Event=return_heading_data['Event']
    PlayDate=return_heading_data['PlayDate']

    pdf.add_page()
    PrintHeadings(Site,Event,PlayDate,pdf)
    Drawlines(pdf,no_of_boards)
    for board_num in range(no_of_boards):
        board_no = board_num+1
        x_origin = left_margin
        if board_no % 2 == 0:  # is number even
             x_origin = left_margin + board_column_width + dealer_column_width + hands_width + HCP_width + dd_width
        y_origin = top_line + heading_height + math.floor(board_num/2)*deal_height
        pdf.set_xy(x_origin,y_origin)
        #Board number
        pdf.set_font("Helvetica", size=16)
        pdf.cell(board_column_width,deal_height,txt=str(board_no),ln=0, align='C')
        #Dealer/Vul
        PrintDealerVul(board_no,pdf,x_origin,y_origin)
        #Hands
        deal=return_hand_data[board_num]
        sorted_hands=PrintHands(deal,pdf,x_origin,y_origin)
        #HCP
        PrintHCP(sorted_hands,pdf,x_origin,y_origin)
        #Double Dummy
        ddtricks=return_dd_data[board_num]
        PrintDoubleDummy(ddtricks,pdf,x_origin,y_origin)
    return(pdf,f)

def PrintDealerVul(board_no,pdf,x_origin,y_origin):
    pdf.set_font("Helvetica", size=8)
    text=dealer_vulnerable_list[int(math.fmod(board_no,16)-1)]
    pdf.set_xy(x_origin+board_column_width,y_origin)
    pdf.cell(dealer_column_width,deal_height,txt=text,ln=0, align='C')

#Calculate HCP list - This is a list containing HCP for suits in the order N,E,S,W
def Calculate_HCP(sorted_hands):
    HCP_list=[]
    for hand in sorted_hands:
        HCP=0
        if hand=='':
            continue
        for card in hand:
            if card.isalpha() and card != 'T':
                HCP+=HCP_values[card]
        HCP_list.append(str(HCP))    
    return(HCP_list)

# layout HCP

def PrintHCP(sorted_hands,pdf,x_origin,y_origin):   
    HCP_list = Calculate_HCP(sorted_hands)
    pdf.set_font("Helvetica", size=9)
   # text=''
    HCP_origin = x_origin + board_column_width + dealer_column_width + hands_width
    for i in range(4):
        pdf.set_xy(HCP_origin,y_origin + (i*line_separation))
        text= HCP_list[i]
        pdf.cell(HCP_width,line_separation, ln=1, txt=text,align='C')    

# This function draws the grid lines on the printed sheets.
def Drawlines(pdf,no_of_boards):
    no_of_rows=int(no_of_boards/2)
    if no_of_boards % 2 !=0 : no_of_rows +=1                #if odd number of boards draw and extra row
    #Horizontal lines
    pdf.line(left_margin,top_line,layout_width,top_line)
    pdf.line(left_margin,top_line+heading_height,layout_width,top_line+heading_height)
    for i in range(no_of_rows):
        i=i+1
        row_y=top_line+heading_height+(deal_height*i)
        pdf.line(left_margin,row_y,layout_width,row_y)
    #Vertical lines
    pdf.line(left_margin,top_line,left_margin,row_y)
    x=left_margin+board_column_width
    pdf.line(x,top_line,x,row_y)
    x=x+dealer_column_width
    pdf.line(x,top_line,x,row_y)
    x=x+hands_width
    pdf.line(x,top_line,x,row_y)
    x=x+HCP_width
    pdf.line(x,top_line,x,row_y)
    x=x+dd_width
    pdf.line(x,top_line,x,row_y)
    x=x+board_column_width
    pdf.line(x,top_line,x,row_y)
    x=x+dealer_column_width
    pdf.line(x,top_line,x,row_y)
    x=x+hands_width
    pdf.line(x,top_line,x,row_y)
    x=x+HCP_width
    pdf.line(x,top_line,x,row_y)
    x=x+dd_width
    pdf.line(x,top_line,x,row_y)

# This function prints out the top heading and the column headings of the printed sheets

def PrintHeadings(Site,Event,PlayDate,pdf):
    text= Site + ":  " + Event  
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200,0,txt=text,border=0,ln=1,align='C')
    
    workdate=PlayDate[0:6] + '20' + PlayDate[6:8]
    d=datetime.datetime.strptime(workdate,"%d.%m.%Y").date()
    text=d.strftime('%d %B %Y')
    pdf.set_font("Helvetica",'B', size=18)
    pdf.cell(200,12,txt=text,border=0,ln=1,align='C')  #cell for play date
    pdf.set_auto_page_break(True, margin = 1.0)
    pdf.set_xy(left_margin,top_line+(heading_height/2))
    for i in range(2):
        pdf.set_font("Helvetica",size = 7)
        pdf.cell(board_column_width,0,txt='Board',ln=0,align='C') # cell for 'Board' heading
        pdf.cell(dealer_column_width,0,txt='Dealer/Vul',ln=0,align='C')
        pdf.set_font("Helvetica",size = 8)
        pdf.cell(hands_width,0,txt='Hands',ln=0,align='C')
        pdf.cell(HCP_width,0,txt='HCP',ln=0,align='C')
        pdf.set_font("Helvetica",size = 7)
        pdf.cell(dd_width,0,txt='Double Dummy',ln=0,align='C')

# This function produces the Hands layout from the 'Deal' line in the pbn file

def PrintHands(deal,pdf,x_origin,y_origin):
    # The deal has quote marks ("") at the start and end - remove these
    dealer = deal[0:1]
    deal=deal[2:]                       # remove dealer and : from hand deal layout
    hands=deal.split()
    pdf.set_font("Helvetica", size=12)
    # deal is ordered from dealer's hand first.  Sort hands in order N,S,E,W
    
    sorted_hands=[None]*4
    if dealer == 'N' :
        sorted_hands[0]=hands[0]
        sorted_hands[1]=hands[2]
        sorted_hands[2]=hands[1]
        sorted_hands[3]=hands[3]
       
    if dealer == 'E' :
        sorted_hands[0]=hands[3]
        sorted_hands[1]=hands[1]
        sorted_hands[2]=hands[0]
        sorted_hands[3]=hands[2]
    if dealer == 'S' :
        sorted_hands[0]=hands[2]
        sorted_hands[1]=hands[0]
        sorted_hands[2]=hands[3]
        sorted_hands[3]=hands[1]
    if dealer == 'W' :
        sorted_hands[0]=hands[1]
        sorted_hands[1]=hands[3]
        sorted_hands[2]=hands[2]
        sorted_hands[3]=hands[0] 
    
    for i in range(4):
        pdf.set_xy(x_origin + board_column_width + dealer_column_width,y_origin+ (line_separation*i))
        suits = sorted_hands[i].split(".")
        point =' ' + points[i] + ': '
        for j in range(4):
            if not point == "":              # print out point(N,S,E,W)
                pdf.set_font("Helvetica", size=9)
                text=point
                pdf.cell(5,line_separation, txt=text, ln=0, align="L")    
            pdf.set_font("Symbol", size=9)
            text = suit_chars[j]
            if j == 1 or j == 2:
                pdf.set_text_color(255,0,0)  # set colour of heart or diamond symbol to red
            else: 
                pdf.set_text_color(0,0,0)
            width=2 
            pdf.cell(width,line_separation, txt=text, ln=0, align="L")  #suit symbol
            pdf.set_font("Helvetica", size=9)
            text=suits[j]
            if text == '': 
                text = '-'
                width = 1
            else:
                width=2*len(text)
            pdf.set_text_color(0,0,0)
            line=0
            if j==3 and i !=3 :line = 1             # print out 4 suits before a new line
            pdf.cell(width,line_separation, txt=text, ln=line, align="L")
            point=''
    return(sorted_hands)



#re-order ddtricks to put NT tricks at end for each player N,E,S,W
def PrintDoubleDummy(ddtricks,pdf,x_origin,y_origin):
    ordered_dd_tricks=[None]*20
    for i in range(4):
        for j in range(5):
            x=i*5+j
            value = ddtricks[x:x+1]
            if j==0:
                ordered_dd_tricks[((i+1)*5)-1]=value
            else:
                ordered_dd_tricks[(i*5)+j-1]=value
    # output the double dummy section for the board
    dd_origin = x_origin + board_column_width + dealer_column_width + hands_width + HCP_width
    pdf.set_xy(dd_origin,y_origin+2)
    pdf.set_font("Courier",size = 7, style='B')
    pdf.cell(dd_width,0,txt='    S  H  D  C NT',ln=0,align='C')
    
    for i in range(4):
        pdf.set_xy(dd_origin,y_origin+((i+1)*dd_line_separation)+1)
        text=" " + points[i]
        for j in range(5):
            char = ordered_dd_tricks[i*5+j]
            if char.isalpha():
                value = convert_table1[char]
            else:
                value=" " + char
            text=text + " " + value
        pdf.set_font("Courier", size=7)
        pdf.cell(dd_width,dd_line_separation,txt=text,ln=0,align='C')

