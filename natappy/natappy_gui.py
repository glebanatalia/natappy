import tkinter
from tkinter import Tk,StringVar,N,E,W,S,Listbox,MULTIPLE,END,Entry,VERTICAL,FALSE,Spinbox,Label
from tkinter import ttk
from tkinter import messagebox
import natappy as nat
from natappy import create_report
import traceback
from os.path import expanduser
import datetime
from datetime import date, timedelta
home = expanduser("~")
from instagram.client import InstagramAPI
from idlelib.ToolTip import *
import textwrap
import compet as comp
import time
import openpyxl
import campcomp
import pandas
import pickle
 
info= {'blogpost':{},'comptags':[],'competition':[],'campaign':'','brandname':'','excludetags':[],'bloggers': [],'tags': [], 'format': None , 'platforms': [],'fromdate':[],'todate':[],'replies':False,'retweets':False,'blogposts':[]}  

passwords=[line.split('=')[1].split('\'')[1] for line in open('%s/Desktop/natappy/passwords/passwords.rtf' %home,'r') if '=' in line]
#==============================================================================
# interface
#==============================================================================
api = InstagramAPI(access_token=passwords[3],client_id=passwords[1], client_secret=passwords[2])

def username_to_id_ig(username):
    return '123456789'     
     
     
def add_blogger_to_excel(blogger):
    wb = openpyxl.load_workbook('%s/Desktop/natappy/bloggers.xlsx' %home)
    sheet = wb.get_sheet_by_name('Bloggers')
    #position=sheet.get_highest_row()
    position=sheet.max_row
    print ('highest row',position)
    blogger=blogger.split(',')
    counter=0
    for column in ['A','B','C','D','F','G']:
            sheet[str(column)+str(position+1)]=blogger[counter]
            sheet['E'+str(position+1)] = '123456789'
            counter+=1
    wb.save('%s/Desktop/natappy/bloggers.xlsx' %home)
   
add_buttons=[]
def first_window(root,info=info):  
    variablefb=StringVar()
    variableig=StringVar()
    variabletw=StringVar() 
    variablebl=StringVar()
    compvariablefb=StringVar()
    compvariableig=StringVar()
    compvariabletw=StringVar() 
    replies=StringVar()
    retweets=StringVar()          

    def next_():    
        info['platforms']=[chkbox.get() for chkbox in [variablefb,variableig,variabletw,variablebl] if chkbox.get()!='no']  
        info['retweets']=True if retweets.get()=='True' else False
        info['replies']=True if replies.get()=='True' else False
        info['competition']=[chkbox.get() for chkbox in [compvariablefb,compvariableig,compvariabletw] if chkbox.get()!='no']  
        second_window(root,info=info)
        
    def back():      
        root.destroy()
        root.quit()
        
    def active_next():
        send.state(['!disabled','active'])

    def question(info=info):

        if variabletw.get()=='Twitter':
            additional_button3 = ttk.Checkbutton(c, text='Include retweets', variable=retweets,onvalue='True',offvalue='False')
            additional_button3.grid(column=0, row=5, sticky=(N,W,E),padx=50, pady=5)
            add_buttons.append(additional_button3)
            additional_button4 = ttk.Checkbutton(c, text='Include replies', variable=replies,onvalue='True',offvalue='False')
            additional_button4.grid(column=0, row=6, sticky=(N,W,E),padx=50, pady=5) 
            add_buttons.append(additional_button4)
        if variabletw.get()=='no': 
            add_buttons[0].grid_forget()
            add_buttons[1].grid_forget()
            del add_buttons[:] 
        send.state(['!disabled','active'])
   
    c = ttk.Frame(root)
    c.grid(column=0, row=0, sticky=(N,W,E,S))
        
    background_image=tkinter.PhotoImage(file='%s/Desktop/natappy/images/new.gif' %home)
    background_label = tkinter.Label(c, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
 
    root.grid_columnconfigure(0, weight=3)
    root.grid_rowconfigure(0,weight=3)
    
    g0 = ttk.Checkbutton(c, text='Blogs', variable=variablebl,onvalue='Blogs', offvalue='no',command=active_next)
    g0.grid(column=0, row=1, sticky=(N,W,E,S),padx=20, pady=(20,10))   
                                  
    g1 = ttk.Checkbutton(c, text='Facebook', variable=variablefb,onvalue='Facebook', offvalue='no',command=active_next)
    g1.grid(column=0, row=2, sticky=(N,W,E,S),padx=20, pady=10)    

    g2 = ttk.Checkbutton(c, text='Instagram', variable=variableig,onvalue='Instagram',offvalue='no',command=active_next)
    g2.grid(column=0, row=3, sticky=(N,W,E,S),padx=20, pady=10)

    g3 = ttk.Checkbutton(c, text='Twitter', variable=variabletw,onvalue='Twitter',offvalue='no',command=question)
    g3.grid(column=0, row=4, sticky=(N,W,E),padx=20, pady=(10,20))
    
#    compg1 = ttk.Checkbutton(c, text='collect competition entries', variable=compvariablefb,onvalue='Facebook', offvalue='no',command=active_next)
#    compg1.grid(column=1, row=2, sticky=(N,W,E,S),padx=20, pady=10)    

    compg2 = ttk.Checkbutton(c, text='collect competition entries', variable=compvariableig,onvalue='Instagram',offvalue='no',state= 'disabled')
    compg2.grid(column=1, row=3, sticky=(N,W,E,S),padx=20, pady=10)

    compg3 = ttk.Checkbutton(c, text='collect competition entries', variable=compvariabletw,onvalue='Twitter',offvalue='no')
    compg3.grid(column=1, row=4, sticky=(N,W,E,S),padx=20, pady=(10,20))
    
    send = ttk.Button(c, text='Next',command=next_, state='disabled',default='active')
    send.grid(column=3,row=7, pady=20,sticky=E,padx=(2,20))

    close = ttk.Button(c, text='Quit', command=back, default='active',state='active')
    close.grid(column=2, row=7, pady=20,sticky=E)
                
    c.grid_columnconfigure(0, weight=1)
    c.grid_rowconfigure(5, weight=1)
    
    a={'Facebook':variablefb,'Instagram':variableig,'Twitter':variabletw,'Blogs':variablebl}    
    b={'Facebook':compvariablefb,'Instagram':compvariableig,'Twitter':compvariabletw} 
    for platform in a.keys():
        if platform in info['platforms']:
            a[platform].set(platform)
            active_next()
        else:
            a[platform].set('no') 
    for platform in b.keys():
        if platform in info['competition']:
            b[platform].set(platform)
            active_next()
        else:
            b[platform].set('no') 
    
    if 'Twitter' in info['platforms']:
        include_replies = ttk.Checkbutton(c, text='Include replies', variable=replies,onvalue='True',offvalue='False')
        include_replies.grid(column=0,sticky=(W,S), row=9,padx=(70,0), pady=(5,5))
        include_retweets = ttk.Checkbutton(c, text='Include retweets', variable=retweets,onvalue='True',offvalue='False')
        include_retweets.grid(column=0, sticky=(W,S), row=8,padx=(70,0), pady=(20,5))
        if info['replies']==True:             
            replies.set('True')
        if info['retweets']==True:        
            retweets.set('True')   

       
    root.title('1/5 Select Media')
    root.geometry('640x330+440+200')



def second_window(root,info):
    def next_step(): 
        idxs = lbox.curselection()  
        for blogger in idxs:
            name = bloggers()[blogger]
            if name not in info['bloggers']:            
                info['bloggers'].append(name)  
        if 'Blogs' in info['platforms']:
            blog_posts(root,info)
        else:
            third_window(root,info)
        
    def cantfind(info=info):
        idxs = lbox.curselection()  
        for blogger in idxs:
            name = bloggers()[blogger]
            if name not in info['bloggers']:            
                info['bloggers'].append(name)  
        add_blogger(info=info)       
          
    def active_next(*args):
        send.state(['!disabled','active'])  
                
    def back():
        idxs = lbox.curselection()  
        for blogger in idxs:
            name = bloggers()[blogger]
            if name not in info['bloggers']:            
                info['bloggers'].append(name)  
        first_window(root,info=info)
        
    c = ttk.Frame(root,padding=(5,0,0,0))
    c.grid(column=0, row=0, sticky=(N,W,E,S))
    
    background_image=tkinter.PhotoImage(file='%s/Desktop/natappy/images/moon.gif' %home)
    background_label = tkinter.Label(c, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    root.grid_columnconfigure(0, weight=3)
    root.grid_rowconfigure(0,weight=3)
    
    lbox = Listbox(c,selectmode=MULTIPLE)
    lbox.grid(column=0, row=1, rowspan=11,columnspan=7, sticky=(N,W,S),padx=(10,10),pady=(1,1),ipadx=75)
    
    yscroll = ttk.Scrollbar(command=lbox.yview, orient=VERTICAL)
    yscroll.grid(row=0, column=0, padx=(0,10),sticky=(N,W,S))
    
    lbox.configure(yscrollcommand=yscroll.set) 
   
    for blogger in bloggers():
        lbox.insert(END, blogger)            
        lbox.bind("<<ListboxSelect>>")
                     
    lbox.yview_scroll(40, 'units')
         
    cantfind =ttk.Button(c, text='Add new bloggers',command=cantfind)
    cantfind.grid(column=4, row=1,padx=(10,0),sticky=(N,S,E,W),pady=(20,10))

    send = ttk.Button(c, text='Next', command=next_step,default='active',state='disabled')
    send.grid(column=6, row=11, sticky=E,pady=20,padx=(2,20))    
  
    close = ttk.Button(c, text='Back', command=back, default='active')
    close.grid(column=5, row=11,sticky=S+E,pady=20,padx=2)
    
    lbox.bind('<<ListboxSelect>>', active_next)   
    
    if info['bloggers']:
        for blogger in info['bloggers']:
            i=bloggers().index(blogger)
            lbox.selection_set(i)
        active_next()
   
    for i in range(len(bloggers()),2):
        lbox.itemconfigure(i, background='#f0f0ff')
 
    c.grid_columnconfigure(0, weight=1)
    c.grid_rowconfigure(5, weight=1)    
       
    root.title('2/5 Select bloggers')
    root.geometry('680x550+300+40')
  

def add_blogger(info=info): 
    to_write=[]

    def adding_bloggers(info=info):        
        for entry in connections.keys(): 
            entrydata=[]
            print (entry.get())
            if len(entry.get())<=1:
                name='nothing'
            else:
                name=entry.get()
            entrydata.append(name)
            for connected in connections[entry]:
                if connected.get()=='':
                    entrydata.append('nothing')
                else:
                    entrydata.append(connected.get())  
                                 
            if entrydata!=['nothing','nothing','nothing','nothing','nothing','nothing']:           
                to_write.append(str(','.join([name for name in entrydata])+'\n')) 
        screennames=sum(map(lambda x:0 if x.split(',')[0]=='nothing' else 1,to_write))
        print (to_write)
        print (screennames)
        if to_write and screennames==len(to_write) :    
            file=open('%s/Desktop/natappy/bloggers.txt' %home,'a') 
            file.writelines(to_write) 
            file.close() 
            print (to_write)
            counter=0
            for el in to_write:
                print (counter,el)
                add_blogger_to_excel(el)   
                counter+=1                 
            second_window(root=root,info=info)
        elif to_write and screennames!=len(to_write):
            messagebox.showerror('Give me screen name','Screen name is required!')
    
    def back(info=info):       
            second_window(root=root,info=info)       

    c = ttk.Frame(root)
    c.grid(column=0, row=0, sticky=(N,W,E,S))
          
    background_image=tkinter.PhotoImage(file='%s/Desktop/natappy/images/followers.gif' %home)
    background_label = tkinter.Label(c, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    root.grid_columnconfigure(0, weight=3)
    root.grid_rowconfigure(0,weight=3)
  
    close = ttk.Button(c, text='Back', command=back, default='active')
    close.grid(column=4, row=12, sticky=W+E,padx=(0,2),pady=40)
    close = ttk.Button(c, text='Add bloggers', command=adding_bloggers, default='active')
    close.grid(column=5, row=12, sticky=W+E,padx=(2,20),pady=40)
            
    screen_name = ttk.Label(c, text="Screen name. Required")
    screen_name.grid(column=0, row=1, padx=(10,0), pady=20) 
    tip1 = ListboxToolTip(screen_name, textwrap.wrap('Name that will be shown in report. It might be whatever, but it can not contains commas.  ',25))    
     
    link_name = ttk.Label(c, text="Facebook link name")
    link_name.grid(column=1, row=1, padx=(0,0), pady=20) 
    tip2 = ListboxToolTip(link_name,textwrap.wrap("Name shown in facebook link ex. https://www.facebook.com/blogger_link_name. If link name is in format link_name-somenumbers then please, provide numbers instead of name",23))
       
    t1 = Entry(c, width=20)
    t1.grid(column=0, row=2, sticky=W, padx=(30,2), pady=(2,2)) 
    t2 = Entry(c, width=20)
    t2.grid(column=0, row=4, sticky=W, padx=(30,2), pady=(2,2)) 
    t3 = Entry(c, width=20)
    t3.grid(column=0, row=6, sticky=W, padx=(30,2), pady=(2,2)) 
    t4 = Entry(c, width=20)
    t4.grid(column=0, row=8, sticky=W, padx=(30,2), pady=(2,2)) 
    t5 = Entry(c, width=20)
    t5.grid(column=0, row=10, sticky=W, padx=(30,2), pady=(2,2)) 
     
    ct1 = Entry(c, width=20)
    ct1.grid(column=1, row=2, sticky=W, padx=(2,2), pady=(2,2)) 
    ct2 = Entry(c, width=20)
    ct2.grid(column=1, row=4, sticky=W, padx=(2,2), pady=(2,2)) 
    ct3 = Entry(c, width=20)
    ct3.grid(column=1, row=6, sticky=W, padx=(2,2), pady=(2,2)) 
    ct4 = Entry(c, width=20)
    ct4.grid(column=1, row=8, sticky=W, padx=(2,2), pady=(2,2)) 
    ct5 = Entry(c, width=20)
    ct5.grid(column=1, row=10, sticky=W, padx=(2,2), pady=(2,2)) 
    
    instagram_name = ttk.Label(c, text="Instagram link name")
    instagram_name.grid(column=2, row=1, padx=(0,0), pady=20)  
    tip3 = ListboxToolTip(instagram_name, textwrap.wrap("Name shown in instagram link Ex. https://www.instagram.com/lydiaemillen/ link_name=lydiaemillen",25))
    
    bt1 = Entry(c, width=20)
    bt1.grid(column=2, row=2, sticky=W, padx=(2,2), pady=(2,2)) 
    bt2 = Entry(c, width=20)
    bt2.grid(column=2, row=4, sticky=W, padx=(2,2), pady=(2,2)) 
    bt3 = Entry(c, width=20)
    bt3.grid(column=2, row=6, sticky=W, padx=(2,2), pady=(2,2)) 
    bt4 = Entry(c, width=20)
    bt4.grid(column=2, row=8, sticky=W, padx=(2,2), pady=(2,2)) 
    bt5 = Entry(c, width=20)
    bt5.grid(column=2, row=10, sticky=W, padx=(2,2), pady=(2,2)) 
    
    twitter_name = ttk.Label(c, text="Twitter link name")
    twitter_name.grid(column=3, row=1, padx=(0,10), pady=5)   
    tip4 = ListboxToolTip(twitter_name, ["Copy Paste name", "shown in twitter link Ex.", "twitter.com/TimeOutLondon",  "link_name=TimeOutLondon"])    
    
    dt1 = Entry(c, width=20)
    dt1.grid(column=3, row=2, sticky=W, padx=(2,2), pady=(2,2)) 
    dt2 = Entry(c, width=20)
    dt2.grid(column=3, row=4, sticky=W, padx=(2,2), pady=(2,2)) 
    dt3 = Entry(c, width=20)
    dt3.grid(column=3, row=6, sticky=W, padx=(2,2), pady=(2,2)) 
    dt4 = Entry(c, width=20)
    dt4.grid(column=3, row=8, sticky=W, padx=(2,2), pady=(2,2)) 
    dt5 = Entry(c, width=20)
    dt5.grid(column=3, row=10, sticky=W, padx=(2,2), pady=(2,2)) 
    
        
    dtw1 = Entry(c, width=20)
    dtw1.grid(column=4, row=2, sticky=W, padx=(2,2), pady=(2,2)) 
    dtw2 = Entry(c, width=20)
    dtw2.grid(column=4, row=4, sticky=W, padx=(2,2), pady=(2,2)) 
    dtw3 = Entry(c, width=20)
    dtw3.grid(column=4, row=6, sticky=W, padx=(2,2), pady=(2,2)) 
    dtw4 = Entry(c, width=20)
    dtw4.grid(column=4, row=8, sticky=W, padx=(2,2), pady=(2,2)) 
    dtw5 = Entry(c, width=20)
    dtw5.grid(column=4, row=10, sticky=W, padx=(2,2), pady=(2,2)) 
    
    a1 = Entry(c, width=20)
    a1.grid(column=5, row=2, sticky=W, padx=(2,20), pady=(2,2)) 
    a2 = Entry(c, width=20)
    a2.grid(column=5, row=4, sticky=W, padx=(2,20), pady=(2,2)) 
    a3 = Entry(c, width=20)
    a3.grid(column=5, row=6, sticky=W, padx=(2,20), pady=(2,2)) 
    a4 = Entry(c, width=20)
    a4.grid(column=5, row=8, sticky=W, padx=(2,20), pady=(2,2)) 
    a5 = Entry(c, width=20)
    a5.grid(column=5, row=10, sticky=W, padx=(2,20), pady=(2,2)) 
    
    website = ttk.Label(c, text="Website")
    website.grid(column=4, row=1, padx=(0,0), pady=20) 
    
    views = ttk.Label(c, text="Unique Users p/m")
    views.grid(column=5, row=1, padx=(0,0), pady=20) 

    connections={t1:[ct1,bt1,dt1,dtw1,a1],t2:[ct2,bt2,dt2,dtw2,a2],t3:[ct3,bt3,dt3,dtw3,a3],t4:[ct4,bt4,dt4,dtw4,a4],t5:[ct5,bt5,dt5,dtw5,a5]}

    root.title('New blogger')
    root.geometry('1100x400+100+100')
 
def tags_info():
        return 'Tags are not case sensitive. Application sees posts\'s texts as a sequence of characters and does not recognize words. Therefore Ex. searching for tag \'stiler\' would also return posts with tag \'@stilercom\' as it contains part \'stiler\' too. To get accurate results, please avoid using too short tags'

def screenname_to_website(blogger):
    a=pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' %home)
    b=pandas.DataFrame(a)
    return list(b[b['Blogger']==blogger]['URL'])[0]   

def website_to_screenname(website):
    a=pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' %home)
    b=pandas.DataFrame(a)
    return list(b[b['URL']==website]['Blogger'])[0]   



def process_link(link,bloggers):
    websites=[screenname_to_website(blogger) for blogger in bloggers]
    
    for website in websites:
        if 'www.' in website:
            if website.split('.')[1] in link:
                return website_to_screenname(website)
        else:
            if website.split('/')[2].split('.')[0] in link:
                return website_to_screenname(website)
    return ''
    

def blog_posts(root,info):  
   
    def next_window():
        for blogger in info['bloggers']:
            info['blogpost'][blogger]=[]
        if info['platforms']==['Blogs'] and [entry.get() for entry in entries]==['', '', '', '', '', '', '', '', '', '', '', '', '']:
            for blogger in info['bloggers']:                
                info['blogpost'][blogger].append(screenname_to_website(blogger))
        for entry in entries:
            
            if entry.get() and entry.get() not  in info['blogpost'].values() :
                info['blogpost'][process_link(entry.get(),info['bloggers'])].append(entry.get())
                
        print (info['blogpost'])
        third_window(root=root,info=info)

    def back(info=info):  
        for blogger in info['bloggers']:
            info['blogpost'][blogger]=[]
        for entry in entries:
            if entry.get() and entry.get() not  in info['blogpost'].values() :
                info['blogpost'][process_link(entry.get(),info['bloggers'])].append(entry.get())   
        second_window(root=root,info=info)

    
    def active_next(*args):
        send.state(['!disabled','active'])  

    c = ttk.Frame(root)
    c.grid(column=0, row=0, sticky=(N,W,E,S))

    root.grid_columnconfigure(0, weight=3)
    root.grid_rowconfigure(0,weight=3)

    send = ttk.Button(c, text='Next', command=next_window, default='active')#,state='disabled')
    send.grid(column=2, row=15,sticky=(E),pady=0,padx=2)    
   
    close = ttk.Button(c, text='Back', command=back, default='active')
    close.grid(column=1, row=15,pady=0,padx=2)
   

    t1 = Entry(c, width=60)
    t1.grid(column=0, row=1, sticky=W, padx=(20,70),pady=(30,5)) 
    t1.bind("<Button-1>", active_next)
    t2 = Entry(c, width=60)
    t2.grid(column=0, row=2, sticky=W, padx=(20,0),pady=(5,5))
    t2.bind("<Button-1>", active_next)
    t3 = Entry(c, width=60)
    t3.grid(column=0, row=3, sticky=W, padx=(20,0),pady=5) 
    t3.bind("<Button-1>", active_next)
    t4 = Entry(c, width=60)
    t4.grid(column=0, row=4, sticky=W, padx=(20,0),pady=5) 
    t4.bind("<Button-1>", active_next)
    t5 = Entry(c, width=60)
    t5.grid(column=0, row=5, sticky=W, padx=(20,0),pady=5)
    t5.bind("<Button-1>", active_next)
    t6 = Entry(c, width=60)
    t6.grid(column=0, row=7, sticky=W, padx=(20,0),pady=5)
    t6.bind("<Button-1>", active_next)
    t7 = Entry(c, width=60)
    t7.grid(column=0, row=8, sticky=W, padx=(20,0),pady=(5)) 
    t7.bind("<Button-1>", active_next)
    ct1 = Entry(c, width=60)
    ct1.grid(column=0, row=9, sticky=W, padx=(20,0),pady=(5)) 
    ct1.bind("<Button-1>", active_next)
    ct2 = Entry(c, width=60)
    ct2.grid(column=0, row=10, sticky=W, padx=(20,0),pady=(5))
    ct2.bind("<Button-1>", active_next)
    ct3 = Entry(c, width=60)
    ct3.grid(column=0, row=11, sticky=W, padx=(20,0),pady=5) 
    ct3.bind("<Button-1>", active_next)
    ct4 = Entry(c, width=60)
    ct4.grid(column=0, row=12, sticky=W, padx=(20,0),pady=5) 
    ct4.bind("<Button-1>", active_next)
    ct5 = Entry(c,width=60)
    ct5.grid(column=0, row=13, sticky=W, padx=(20,0),pady=5)
    ct5.bind("<Button-1>", active_next)
    ct6 = Entry(c, width=60)
    ct6.grid(column=0, row=14, sticky=W, padx=(20,0),pady=5)
    ct6.bind("<Button-1>", active_next)

    entries=[t1,t2,t3,t4,t5,t6,t7,ct1,ct2,ct3,ct4,ct5,ct6]


    if info['tags']:
        a=list(zip(entries,info['tags']))    
        for tag in a:
            tag[0].insert(0,tag[1])
        active_next()

    if info['blogpost']:
        links=[]
        for el in info['blogpost'].keys():
            for link in info['blogpost'][el]:
               links+=link
        a=list(zip(entries,links))    
        for link in a:
            link[0].insert(0,link[1])
        active_next()
   
    root.title('Enter Blog Posts URLs')
    root.geometry('800x550+440+200')

         
def third_window(root,info):  
    store0,store1,store2,store3,store4,store5=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
   
    def next_window():
        for entry in entries:
            if entry.get() and entry.get() not  in info['tags'] :
                info['tags'].append(str(entry.get()).encode('ascii', 'ignore').decode('utf-8'))
        for entry2 in entries2:
            if entry2.get() and entry2.get() not in info['excludetags']:
                info['excludetags'].append(str(entry2.get()).encode('ascii', 'ignore').decode('utf-8'))  
        for el in compentries:
            if  competriesvar[el].get():
                   if connections[el].get() not in info['comptags']:
                       info['comptags'].append( connections[el].get())
        fourth_window(root=root,info=info)

    def back(info=info):  
        for entry in entries:
            if entry.get() and entry.get() not  in info['tags'] :
                info['tags'].append(str(entry.get()).encode('ascii', 'ignore').decode('utf-8'))
        for entry2 in entries2:
            if entry2.get() and entry2.get() not in info['excludetags']:
                info['excludetags'].append(str(entry2.get()).encode('ascii', 'ignore').decode('utf-8'))   
        for el in compentries:
            if competriesvar[el].get():
                if connections[el].get() not in info['comptags']:
                    info['comptags'].append( connections[el].get())  
        if info['blogpost']:
            blog_posts(root=root,info=info)
        else:
            second_window(root=root,info=info)

    
    def active_next(*args):
        send.state(['!disabled','active'])  
        
    def clear_c1(*args):
            c1.delete(0,END)
    def clear_c2(*args):
            c2.delete(0,END)
    def clear_c3(*args):
            c3.delete(0,END)
              
    c = ttk.Frame(root)
    c.grid(column=0, row=0, sticky=(N,W,E,S))
            
    background_image=tkinter.PhotoImage(file='%s/Desktop/natappy/images/man.gif' %home)
    background_label = tkinter.Label(c, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    root.grid_columnconfigure(0, weight=3)
    root.grid_rowconfigure(0,weight=3)

    send = ttk.Button(c, text='Next', command=next_window, default='active',state='disabled')
    send.grid(column=4, row=22,pady=(50,50),padx=(2,30))    
   
    close = ttk.Button(c, text='Back', command=back, default='active')
    close.grid(column=3, row=22,sticky=E,pady=(50,50),padx=2)
   
    t1 = Entry(c, width=20)
    t1.grid(column=1, row=1, sticky=W, padx=(20,0),pady=(30,5)) 
    t1.bind("<Button-1>", active_next)
    t2 = Entry(c, width=20)
    t2.grid(column=1, row=2, sticky=W, padx=(20,0),pady=(5,5))
    t2.bind("<Button-1>", active_next)
    t3 = Entry(c, width=20)
    t3.grid(column=1, row=3, sticky=W, padx=(20,0),pady=5) 
    t3.bind("<Button-1>", active_next)
    t4 = Entry(c, width=20)
    t4.grid(column=1, row=4, sticky=W, padx=(20,0),pady=5) 
    t4.bind("<Button-1>", active_next)
    t5 = Entry(c, width=20)
    t5.grid(column=1, row=5, sticky=W, padx=(20,0),pady=5)
    t5.bind("<Button-1>", active_next)
    t6 = Entry(c, width=20)
    t6.grid(column=1, row=6, sticky=W, padx=(20,0),pady=5)
    t6.bind("<Button-1>", active_next)
#    t7 = Entry(c, width=80)
#    t7.grid(column=1, row=7, sticky=W, padx=(20,0),pady=5) 
#    t7.bind("<Button-1>", active_next)
#    t8 = Entry(c, width=80)
#    t8.grid(column=1, row=8, sticky=W, padx=(20,0),pady=5)
#    t8.bind("<Button-1>", active_next)
#    t9 = Entry(c, width=80)
#    t9.grid(column=1, row=9, sticky=W, padx=(20,0),pady=5) 
#    t9.bind("<Button-1>", active_next)
#    t10 = Entry(c, width=80)
#    t10.grid(column=1, row=10, sticky=W, padx=(20,0),pady=5) 
#    t10.bind("<Button-1>", active_next)
#    t11 = Entry(c, width=80)
#    t11.grid(column=1, row=11, sticky=W, padx=(20,0),pady=5)
#    t11.bind("<Button-1>", active_next)
#    t12 = Entry(c, width=80)
#    t12.grid(column=1, row=12, sticky=W, padx=(20,0),pady=5)
#    t12.bind("<Button-1>", active_next)
#    t13 = Entry(c, width=80)
#    t13.grid(column=1, row=13, sticky=W, padx=(20,0),pady=5) 
#    t13.bind("<Button-1>", active_next)
#    t14 = Entry(c, width=80)
#    t14.grid(column=1, row=14, sticky=W, padx=(20,0),pady=5)
#    t14.bind("<Button-1>", active_next)
#    t15 = Entry(c, width=80)
#    t15.grid(column=1, row=15, sticky=W, padx=(20,0),pady=5) 
#    t15.bind("<Button-1>", active_next)
#    t16 = Entry(c, width=80)
#    t16.grid(column=1, row=16, sticky=W, padx=(20,0),pady=5) 
#    t16.bind("<Button-1>", active_next)
#    t17 = Entry(c, width=80)
#    t17.grid(column=1, row=17, sticky=W, padx=(20,0),pady=5)
#    t17.bind("<Button-1>", active_next)
#    t18 = Entry(c, width=80)
#    t18.grid(column=1, row=18, sticky=W, padx=(20,0),pady=5)
#    t18.bind("<Button-1>", active_next)
#    t19 = Entry(c, width=80)
#    t19.grid(column=1, row=19, sticky=W, padx=(20,0),pady=5)
#    t19.bind("<Button-1>", active_next)
#    t20 = Entry(c, width=80)
#    t20.grid(column=1, row=20, sticky=W, padx=(20,0),pady=5)
#    t20.bind("<Button-1>", active_next)
#    t21 = Entry(c, width=80)
#    t21.grid(column=1, row=21, sticky=W, padx=(20,0),pady=5) 
#    t21.bind("<Button-1>", active_next)
#    t22 = Entry(c, width=80)
#    t22.grid(column=1, row=22, sticky=W, padx=(20,0),pady=5)
#    t22.bind("<Button-1>", active_next)
#    t23 = Entry(c, width=80)
#    t23.grid(column=1, row=23, sticky=W, padx=(20,0),pady=5) 
#    t23.bind("<Button-1>", active_next)
#    t24 = Entry(c, width=80)
#    t24.grid(column=1, row=24, sticky=W, padx=(20,0),pady=5) 
#    t24.bind("<Button-1>", active_next)
#    t25 = Entry(c, width=80)
#    t25.grid(column=1, row=25, sticky=W, padx=(20,0),pady=5)
#    t25.bind("<Button-1>", active_next)
#    t26 = Entry(c, width=80)
#    t26.grid(column=1, row=26, sticky=W, padx=(20,0),pady=5)
#    t26.bind("<Button-1>", active_next)
#    

    

    
    c1 = Entry(c, width=23)
    c1.grid(column=2, row=4, sticky=W, padx=(10,20),pady=(5,5)) 
    c1.bind("<Button-1>", clear_c1)
    
    c2 = Entry(c, width=23)
    c2.grid(column=2, row=5, sticky=W, padx=(10,20),pady=(5,5)) 
    c2.bind("<Button-1>", clear_c2)
    
    c3 = Entry(c, width=23)
    c3.grid(column=2, row=6, sticky=W, padx=(10,20),pady=(5,6)) 
    c3.bind("<Button-1>", clear_c3)
    
    g1 = ttk.Checkbutton(c, variable=store0,command=active_next)
    g1.grid(column=0, row=1, sticky=(W),padx=(20,0), pady=(25,6))
    
    g2 = ttk.Checkbutton(c,  variable=store1,command=active_next)
    g2.grid(column=0, row=2, sticky=(W),padx=(20,0), pady=6)

    g3 = ttk.Checkbutton(c,  variable=store2,command=active_next)
    g3.grid(column=0, row=3, sticky=(W),padx=(20,0), pady=6)

    g4 = ttk.Checkbutton(c, variable=store3,command=active_next)
    g4.grid(column=0, row=4, sticky=(W),padx=(20,0), pady=6)

    g5 = ttk.Checkbutton(c,  variable=store4,command=active_next)
    g5.grid(column=0, row=5, sticky=(W),padx=(20,0), pady=6)

    g6 = ttk.Checkbutton(c, variable=store5,command=active_next)
    g6.grid(column=0, row=6, sticky=(W),padx=(20,0), pady=6)
    
    connections={g1:t1,g2:t2,g3:t3,g4:t4,g5:t5,g6:t6}
    entries2=[c1,c2,c3]
    entries=[t1,t2,t3,t4,t5,t6]
    compentries=[g1,g2,g3,g4,g5,g6]
    competriesvar={g1:store0,g2:store1,g3:store2,g4:store3,g5:store4,g6:store5}
    
    if info['tags']:
        a=list(zip(entries,info['tags']))    
        for tag in a:
            tag[0].insert(0,tag[1])
        active_next()
        
    if info['excludetags']:
        a=list(zip(entries2,info['excludetags']))    
        for tag in a:
            tag[0].insert(0,tag[1])
    else:        
        c1.insert(END,'Exclude tag')
        c2.insert(END,'Exclude tag')
        c3.insert(END,'Exclude tag')
        


    root.title('3/5 Tags')
    root.geometry('650x420+440+200')

def fourth_window(root,info):
    store = StringVar()           
    
    def next_window(root=root,info=info):
        info['format']=store.get()
        fifth_window(root=root,info=info)
        info['brandname']=brand.get()
        info['campaign']=campaign.get()
  
    def back(info=info): 
        third_window(root=root,info=info)
    
        
    def active_next(*args):
        send.state(['!disabled','active'])  
       
    c = ttk.Frame(root)
    c.grid(column=0, row=0, sticky=(N,W,E,S))
    
    background_image=tkinter.PhotoImage(file='%s/Desktop/natappy/images/road.gif' %home)
    background_label = tkinter.Label(c, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    root.grid_columnconfigure(0, weight=3)
    root.grid_rowconfigure(0,weight=3)
                     

    g2 = ttk.Radiobutton(c, text='Full Report', variable=store,value='Full',command=active_next)
    g2.grid(column=1, row=2, sticky=(N,W,E,S),padx=20, pady=20)
    
    g4 = ttk.Radiobutton(c, text='Quick Report', variable=store,value='Quick',command=active_next)
    g4.grid(column=1, row=4, sticky=(N,W,E,S),padx=20, pady=20)

    w = Label(c, text="First Page Title")
    w.grid(column=1, row=5 , sticky=(S,W), padx=(20,5),pady=(5,0))
    
    brand = Entry(c, width=20)
    brand.grid(column=1, row=6 , sticky=W, padx=(20,5),pady=(5,0)) 
    
    campaign = Entry(c, width=20)
    campaign.grid(column=2, row=6 , sticky=W, padx=(5,70),pady=(5,0)) 
    
    send = ttk.Button(c, text='Next',command=next_window, default='active',state='disabled')
    send.grid(column=3,row=7, pady=20,sticky=E,padx=(2,20))

    close = ttk.Button(c, text='Back', command=back, default='active')
    close.grid(column=2, row=7, pady=20,sticky=E)
    
    if info['format']:
        store.set(info['format'])            
        active_next()
    
    c.grid_columnconfigure(0, weight=1)
    c.grid_rowconfigure(5, weight=1)

    root.title('4/5 Format')
    root.geometry('550x400+440+200')

def number_to_month(number):
    months={'January':'01','February':'02','March':'03','April':'04','May':'05','June':'06','July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}
    return dict((value, key) for key, value in months.items())[number] 

def fifth_window(root,info):
    s=ttk.Style()
    s.configure('nat.TFrame',background="white")
    fromdayvar=StringVar()
    frommonthvar=StringVar()
    fromyearvar=StringVar()
    todayvar=StringVar()
    tomonthvar=StringVar()
    toyearvar=StringVar()
          
    def back(info=info):
        info['fromdate']=[int(fromyear.get()),(month_to_number(frommonth.get())),int(fromday.get())]
        info['todate']=[int(toyear.get()),(month_to_number(tomonth.get())),int(today.get())]
        fourth_window(root=root,info=info)
    
    def info_completed(info=info):
      
        info['fromdate']=[int(fromyear.get()),(month_to_number(frommonth.get())),int(fromday.get())]
        info['todate']=[int(toyear.get()),(month_to_number(tomonth.get())),int(today.get())]
        pickle.dump(info, open('{home}/Desktop/natappy/pickle/info.pickle'.format(home=home), 'wb'))
        try:
            root.withdraw()
            print('info=', info)
            if not info['competition']:
                nat.create_report(info['bloggers'],info['platforms'],info['tags'],info['format'],info['fromdate'],info['todate'],info['replies'],info['retweets'],info['excludetags'],info['brandname'],info['campaign'],info['blogpost'])
                root.withdraw()
                messagebox.showinfo("Report completed", 'Details: \n Report: {format} \n Media: {platform2} \n Tags: {tags2} \n Bloggers: {bloggers2} \n Report completed'.format(tags2=' '.join([tag for tag in info['tags']]), platform2=' '.join([platform for platform in info['platforms']]), bloggers2 = ' '.join([blogger for blogger in info['bloggers']]), **info), parent=c)
            else:
                campcomp.campaign_competition(info['blogpost'],info['comptags'],info['competition'],info['campaign'],info['brandname'],info['excludetags'],info['bloggers'],info['tags'],info['format'],info['platforms'],info['fromdate'],info['todate'],info['replies'],info['retweets'],info['blogposts'])
                #comp.competreport(info['competition'],info['comptags'],info['fromdate'],info['bloggers'],info['todate'],info['settings'],info['format'],info['brandname'],info['campaign']) 
                root.withdraw()
                messagebox.showinfo("Report completed", 'Details: \n Report: {format} \n Media: {platform2} \n Tags: {tags2} \n Bloggers: {bloggers2} \n Report completed'.format(tags2=' '.join([tag for tag in info['tags']]), platform2=' '.join([platform for platform in info['platforms']]), bloggers2 = ' '.join([blogger for blogger in info['bloggers']]), **info), parent=c)
        except Exception as e:
            info = 'Exception: {e}'.format(e=e)
            print(info+'\nExiting now')            
            messagebox.showinfo("Error", info)            
        root.quit()
    
    def month_to_number(month):
       return int({'January':'01','February':'02','March':'03','April':'04','May':'05','June':'06','July':'07','August':'08','September':'09','October':10,'November':11,'December':12}[month])
       
    c = ttk.Frame(root,style='nat.TFrame')
    c.grid(column=0, row=0, sticky=(N,W,E,S))
    
    background_image=tkinter.PhotoImage(file='%s/Desktop/natappy/images/palms.gif' %home)
    background_label = tkinter.Label(c, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    root.grid_columnconfigure(0, weight=3)
    root.grid_rowconfigure(0,weight=3)
                         
    fromlbl = ttk.Label(c, text="From:",anchor=E,width=0)
    fromlbl.grid(column=0, row=0, padx=20, pady=(20,4),sticky=(N,W,S,E))
    
    tolbl = ttk.Label(c, text="To:",anchor=E,width=0)
    tolbl.grid(column=0, row=2,padx=20, pady=(20,4),sticky=(N,W,S,E))
    
    fromday = Spinbox(c,values=[i for i in range(1,32)],width=5,textvariable=fromdayvar)
    fromday.grid(column=0, row=1, sticky=W,padx=(20,10), pady=0)
    
    
    frommonth = Spinbox(c,values=['January','February','March','April','May','June','July','August','September','October','November','December'],textvariable=frommonthvar,width=11)
    frommonth.grid(column=1, row=1, sticky=W,padx=(10,20), pady=0)
    
    fromyear=Spinbox(c,values=[2014,2015,2016],width=5,textvariable=fromyearvar)
    fromyear.grid(column=2, row=1, sticky=W,padx=(20,20), pady=0)
    
    today = Spinbox(c,values=[i for i in range(1,32)],width=5,textvariable=todayvar)
    today.grid(column=0, row=3, sticky=W,padx=(20,10), pady=0)
    
    tomonth = Spinbox(c,values=['January','February','March','April','May','June','July','August','September','October','November','December'],width=11,textvariable=tomonthvar)
    tomonth.grid(column=1, row=3, sticky=W,padx=(10,20), pady=0)
    
    toyear=Spinbox(c,values=[2014,2015,2016],width=5,textvariable=toyearvar)
    toyear.grid(column=2, row=3, sticky=W,padx=(20,20), pady=0)
    
    send = ttk.Button(c, text='Create Report',command=info_completed, default='active')
    send.grid(column=3,row=6, pady=20,sticky=E,padx=(2,20))
    
    close = ttk.Button(c, text='Back',command=back,default='active')
    close.grid(column=2, row=6, pady=20,sticky=E)
            
    c.grid_columnconfigure(0, weight=1)
    c.grid_rowconfigure(5, weight=1)
    
    if info['fromdate']:
        if len(str(info['fromdate'][1]))==1:
            month= '0'+str(info['fromdate'][1])
        else:
            month= str(info['fromdate'][1])
        fromdayvar.set(info['fromdate'][2]) 
        frommonthvar.set(number_to_month(month))
        fromyearvar.set(info['fromdate'][0]) 
    else:
        fromdayvar.set((date.today() - timedelta(days=7)).day)
        if len(str((date.today() - timedelta(days=7)).month))==1:
            month='0'+(str((date.today() - timedelta(days=7)).month))
        else:
            month=(str((date.today() - timedelta(days=7)).month))
        frommonthvar.set (number_to_month(month))
        fromyearvar.set((date.today() - timedelta(days=7)).year)
    
    if info['todate']:
        if len(str(info['todate'][1]))==1:
            month= '0'+str(info['todate'][1])
        else:
            month= str(info['todate'][1])
        todayvar.set(info['todate'][2]) 
        tomonthvar.set(number_to_month(month)) 
        toyearvar.set(info['todate'][0]) 
    else:
        todayvar.set(datetime.datetime.now().day)
        if len(str(datetime.datetime.now().month))==1:
            month='0'+str(datetime.datetime.now().month)
        else:
            month=str(datetime.datetime.now().month)
        tomonthvar.set(number_to_month(month))
        toyearvar.set(datetime.datetime.now().year)

    root.title('5/5 Date Range')
    root.geometry('550x400+440+200')
    
def bloggers():
    bloggers=sorted([blogger for blogger in pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' %home)['Blogger'] if type(blogger) is not float])
    return bloggers   

if __name__ == '__main__':
    root=Tk()   
    root.resizable(width=FALSE, height=FALSE) 
    first_window(root)
  
    root.mainloop()

