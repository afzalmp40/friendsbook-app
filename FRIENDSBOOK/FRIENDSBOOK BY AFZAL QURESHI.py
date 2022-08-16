'''FRIENDSBOOK BY AFZAL QURESHI'''

from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import _pickle as pickle
import numpy as np

filename='data/userdata'
window=Tk()

### FADE AWAY main window
def fade_window():
    alpha = window.attributes("-alpha")
    if alpha > 0:
        alpha -= .002
        window.attributes("-alpha", alpha)
        window.after(1, fade_window)
    else:
        window.destroy()

### RED text fade
def text_fade_red(x=0,y=0,start_fading_at=2.5,disappear_at=3.5,text='text here',font="Arial 40 bold",):
    
    global fading_text
    
    interval=int( (disappear_at-start_fading_at)*1000/13 )
    time=[i for i in np.arange(int( start_fading_at*1000 ), int( disappear_at*1000 ),interval) ][::-1]
    
    redlist=[ "#eeee00000000","#ffff00006666","#dddd00001111","#cccc00001111","#bbbb00001111","#aaaa00001111","#999900000000","#888800001111",\
    "#777700002222","#666600003333","#555500004444","#444400005555","#333300007777"] # from bold to light order
    
    shades=redlist[::-1]
    shade_dict={time[i]:shades[i] for i in range( len(shades) )}
    
    for time,shade in shade_dict.items():
        fading_text=canvas1.create_text(x, y, text =text,fill=shade,font=font)
        window.after(time, canvas1.delete, fading_text)

### Email checking
def email_valid(email):    
    if len(email)<5 or not(email.count('@')==1):                   #check length, more than 1 '@''
        return None 
    
    username,domain_extension=email.split('@')  #extract username,domain_extension
    if not( username[0].isalpha() ): #check username start isalpha()
        return None
    if not( username.replace("-", "").replace(".", "").replace("_", "").isalnum()  ):   # print('username problem:',username)
        return None
    if domain_extension.count('.')!=1:           #check for more than 1 '.'
        return None
    if not (domain_extension.replace('.','').isalpha() ):   #check if domain_extension isalpha()
        return None
    
    domain,extension=domain_extension.split('.')        #split domain and extension
    if len(domain)==0:     # check domain length
        return None
    if not( 0<len(extension)<4 ):   # check extension length
        return None
    
    return True

### LOAD userdata from file 
def load_data():
    try:
        #Its important to use binary mode
        with open(filename, 'rb') as dbfile:#pickling always done in binary mode
            db = pickle.load(dbfile)

    except:
        with open(filename, 'wb') as dbfile:
            pickle.dump({},dbfile)
        db={}
    for user in db.values():
        print(user)

load_data()   # load data at the start of program



### SEARCH for a user using a part of fullname 
def search():
    user_to_search=search_name.get().strip().title()
    while '  ' in user_to_search: user_to_search=user_to_search.replace('  ',' ')  #replace all multiple spaces with single space 
    
    if len(user_to_search)<3:
        text_fade_red(x=1000,y=650,start_fading_at=3,disappear_at=4,text='Need bigger\nname to search.',font="Arial 25 ")
        return None
    
    if not(user_to_search.replace(' ','').isalpha()):
        text_fade_red(x=1000,y=640,start_fading_at=3,disappear_at=4,text='No match found',font="Arial 25 ")
        return None
    
    #global matchlist
    matchlist=[]
    
    with open(filename, 'rb') as dbfile:
        db_search=pickle.load(dbfile)
        
    for userdata in db_search.values():
        if user_to_search.lower() in userdata['fullname'].lower():
            matchlist.append(userdata)
            
    if(matchlist):    
        message_search=canvas1.create_text(1000, 640, text='Match found',fill='green',font="Arial 20 bold")
        window.after(3500, canvas1.delete, message_search)
        search_name.set('')
    elif not(matchlist):
        text_fade_red(x=1000,y=640,start_fading_at=3,disappear_at=4,text='No match found',font="Arial 25")
        return None
    
    path='search'
    show_account(matchlist,path)
    

### SIGNIN 
def signin():
    username=login_username.get().strip().lower()
    password=login_password.get()
    
    found={}
    
    with open(filename, 'rb') as dbfile:
        db_signin=pickle.load(dbfile)
    
    for user,userdata in db_signin.items():
        if username == user:
            if userdata['password']==password:
                fullname=userdata['fullname'].upper()
                found=userdata
                message_login=canvas1.create_text(1000, 380, text=f'Welcome back { fullname }!',fill='green',font="Arial 20 bold")
                window.after(6000, canvas1.delete, message_login)
                login_username.set('')
                login_password.set('')
                    
    if not(found):
        text_fade_red(x=1000,y=380,start_fading_at=3,disappear_at=4,text='Invalid details',font="Arial 25",)
        return None
        
    path='signin'
    show_account(found,path)


### Check, Clean and store a new profile
def initialise():    # check new user data and tell various conditions
    
    username=regis_username.get().strip().lower()
    password=regis_password.get()
    password1=regis_password1.get()
    fullname=regis_fullname.get().strip().title()
    phone=regis_phone.get().strip()
    email=regis_email.get().strip()
    description=regis_desc.get(1.0, "end-1c")
    
    while '  ' in fullname: fullname=fullname.replace('  ',' ')     #replace all multiple spaces with single space in fullname
    
    #username check
    if username.replace(' ','').isalpha() or username.replace(' ','').isalnum() or username=='':
        if username=='' or ' ' in username :
            text_fade_red(x=300,y=230,start_fading_at=5,disappear_at=5.5,text='Try a username with only alphanumeric\n characters without spaces.',font="Arial 17")
            return None

        with open(filename, 'rb') as dbfile:
            db_search=pickle.load(dbfile)
            
        if username.lower() in db_search:
            text_fade_red(x=300,y=230,start_fading_at=3,disappear_at=3.5,text='Username already exists.',font="Arial 20")
            return None
        
    #fullname check
    if not fullname:
        text_fade_red(x=300,y=230,start_fading_at=3,disappear_at=4,text='Please enter your full name.',font="Arial 25")
        return None
    
    if not(fullname.replace(' ','').isalpha()):
        text_fade_red(x=300,y=230,start_fading_at=3,disappear_at=4,text='Full name must only be alphabets.',font="Arial 25")
        return None
    
    #passwords check
    if len(password)==0 and len(password1)==0:
        text_fade_red(x=300,y=230,start_fading_at=3,disappear_at=4,text='Please enter a password.',font="Arial 20")
        return None
    
    if len(password)<6 or len(password1)<6 :
        if len(password)>5 or len(password1)>5:    
            if not(password == password1) :
                text_fade_red(x=300,y=230,start_fading_at=3,disappear_at=4,text='Passwords do not match.',font="Arial 20")
                return None 
            
        text_fade_red(x=300,y=230,start_fading_at=3,disappear_at=4,text='\tPassword too small. Size must be atleast 6 characters.',font="Arial 20")
        return None
        
    if len(password)>5 or len(password1)>5:    
        if not(password == password1) :
            text_fade_red(x=300,y=230,start_fading_at=3,disappear_at=4,text='Passwords do not match.',font="Arial 20")
            return None 
    
    #phone number check
    if not(phone.isnumeric()) or len(phone)!=10:
        text_fade_red(x=300,y=230,start_fading_at=3,disappear_at=4,text='Invalid phone number.',font="Arial 20")
        return None 
    
    #email check
    if email_valid(email)!= True:
        text_fade_red(x=300,y=230,start_fading_at=3,disappear_at=4,text='Invalid email.',font="Arial 20")
        return None

    #persuade to add photo
    global regis_image_store
    try:
         type(regis_image_store)
    except:
        message_signup=canvas1.create_text(300, 230,text = 'Would you like to add a photo?',fill='cyan',font="Arial 15 bold")
        window.after(1000, canvas1.delete, message_signup)
        add_photo()
        
    try:
        regis_image_store=regis_image_store.resize((400,400))
    except:
        regis_image_store=None

    count=0
    desc=''
    for word in description.split(' '):
        if count%7==0:
            if word !='\n':
                desc+='\n'
        desc+=word+' '
        count+=1
    
    #create dictionary with user details
    new_user={'username':username , 'fullname':fullname, 'password': password, 'img': regis_image_store, 'phone': phone, 'email':email, 'desc': desc }
    
    #clear data from entry boxes
    regis_username.set('')
    regis_password.set('')
    regis_password1.set('')
    regis_fullname.set('')
    regis_phone.set('')
    regis_email.set('')
    regis_desc.delete("1.0","end")
    del(regis_image_store)
    
    # store the data if all conditions passed
    # read and update database
    with open(filename, 'rb') as dbfile:
        updated_db=pickle.load(dbfile)
    
    updated_db[ new_user['username'] ]=new_user
    
    # Its important to use binary mode
    with open(filename, 'wb') as dbfile:  #pickling always done in binary mode
        pickle.dump(updated_db, dbfile)    # dump database into file via dbfile object
    
    #account creation successful message    
    message_signup=canvas1.create_text(300, 230,text = f'Account creation successful!\nWelcome {fullname}',fill='green',font="Arial 15 bold")
    window.after(6000, canvas1.delete, message_signup)
    
    try:
        window.after(500, canvas1.delete, disp_photo)
    except:
        pass
    
    path='signup'
    show_account(new_user,path)

## show account(s)
def show_account(profile,path):
    if path in ['signup' ,'signin']:
        new_window(profile,path)
    elif path=='search':
        for prof in profile:
            new_window(prof,path)
    

## adding account photo
def add_photo():    
    filename_img = filedialog.askopenfilename(title="Select An Image")

    if filename_img=='':
        return None
    
    global resized_photo
    global disp_photo
    global regis_image_store
    
    regis_image_store= Image.open(filename_img)  # this will be pickled
    
    #resizing and displaying image for reference
    resized_photo= regis_image_store.resize((120,140))   
    resized_photo= ImageTk.PhotoImage(resized_photo)
    disp_photo=canvas1.create_image(280,480,anchor = "nw",image =resized_photo)


## create top window
def new_window(profile,path):
    
    global top
    top=Toplevel()
    top.geometry('900x800')
    top.title(profile['fullname']) 
    top.attributes('-alpha',0.95)
    
    global canvas_top
    #global canvas_top
    canvas_top = Canvas( top, width = 900, height = 800)   # Create Canvas
    canvas_top.pack(fill = "both", expand = True)
    canvas_top.create_image( 0,0,image = bg, anchor = "nw")   # Display image
    canvas_top.create_rectangle(50,50,450,450,fill='light grey')
    
    global show_photo
    global show_disp_photo
    #profile photo
    image= profile['img']  
    if image==None:
        pass
    else:
        show_photo= ImageTk.PhotoImage(image)
        show_disp_photo=canvas_top.create_image(50,50,anchor = "nw",image =show_photo)
    
    global user
    user=profile['username']
    full=profile['fullname']
    phone=profile['phone']
    email=profile['email']
    desc=profile['desc']
    
    #display basic info
    canvas_top.create_text(400,500, text=full,fill="cyan",font="Arial 30 bold")
    canvas_top.create_text(400,540, text='Contact:'+phone,fill="cyan",font="Arial 25 bold")
    canvas_top.create_text(400,580, text='Email:'+email,fill="cyan",font="Arial 25 bold")
    canvas_top.create_text(400,690, text=f'About:{desc}',fill="light yellow",font="Arial 17 bold")
    
    if path =='search':
        Button(top, text='Exit',font="Arial 17 bold", width=6, command=fade_top_window).place(x=660,y=40,height=40, width=100)
        return None
    if path =='signin':
        message=canvas_top.create_text(350, 20, text=f'Welcome back { full }!',fill='green',font="Arial 13 bold")
        top.after(6000, canvas_top.delete, message)
    if path =='signup':
        message=canvas_top.create_text(400, 40, text=f'Welcome to Friendsbook, { full }!',fill='green',font="Arial 13 bold")
        top.after(6000, canvas_top.delete, message)
    
    Button(top, text='Logout',font="Arial 17 bold", width=6, command=fade_top_window).place(x=660,y=40,height=40, width=100)
    Button(top, text='Update\nphoto',font="Arial 17 bold",fg='cyan', width=6, command=update_photo).place(x=550,y=130,height=70, width=150)
    Button(top, text='Delete\nProfile',font="Arial 20 bold",fg='red', width=6, command=delete_profile).place(x=550,y=250,height=70, width=150)
    
    #print user info for signin or signup
    canvas_top.create_text(700,20, text='Signed in as: '+user,fill="yellow",font="Arial 15 italic")
    
### FADE AWAY top window
def fade_top_window():
    alpha = top.attributes("-alpha")
    if alpha > 0:
        alpha -= .002
        top.attributes("-alpha", alpha)
        top.after(1, fade_top_window)
    else:
        top.destroy()
    

## delete profile
def delete_profile():
    with open(filename,'rb') as dbfile:
        db=pickle.load(dbfile)
    if user in db:
        del(db[user])
        
    with open(filename,'wb') as dbfile:
        pickle.dump(db,dbfile)
        
    text_fade_red(x=1050,y=750,start_fading_at=3,disappear_at=4,text='Account deleted!',font="Arial 30")
        
    fade_top_window()

## update account photo
def update_photo():    
    
    global regis_image_1    # required to use in storing userdata
    regis_image_1=None
    
    filename_img = filedialog.askopenfilename(title="Select An Image")
    if filename_img=='':
        return None
    
    regis_image_1= Image.open(filename_img)    # this object will be pickled
    
    global resized_photo_1
    global disp_photo_1

    regis_image_2=regis_image_1.resize((400,400))
    resized_photo_1= ImageTk.PhotoImage(regis_image_2)
    disp_photo_1=canvas_top.create_image(50,50,anchor = "nw",image =resized_photo_1)

    with open(filename, 'rb') as dbfile:
        updated_db=pickle.load(dbfile)

    if user in updated_db:
        updated_db[user]['img']=regis_image_2

    # Its important to use binary mode
    with open(filename, 'wb') as dbfile:  #pickling always done in binary mode
        pickle.dump(updated_db, dbfile)    # dump database into file via dbfile object
            
##########################################################################################################    

'''MAIN'''

# settings of window
window.geometry('1350x850') #in pixel
window.title('FRIENDS BOOK') #give title
window.resizable(0, 0)  # make window non resizeable
window.attributes('-alpha',0.95)

#setting background image
bg = PhotoImage(file = "background.png")       #store image as PhotoImage object
canvas1 = Canvas( window, width = 1350, height = 850)   # Create Canvas
canvas1.pack(fill = "both", expand = True)
canvas1.create_image( 0,0,image = bg, anchor = "nw")   # Display image

'''Title and Logo'''

#create text
canvas1.create_text(640, 60, text = "FRIENDS BOOK",fill="yellow",font="Arial 50 bold")
canvas1.create_text(630, 100, text = "Connecting Humans",fill="yellow",font="Arial 20 italic")

#logo
img1=PhotoImage(file = "like.png")
canvas1.create_image(280,40, image =img1, anchor = "nw")

#exit button
exit_button = Button(text="EXIT",font="Arial 20 bold", width=6, command=fade_window).place(x=1250,y=20,height=30, width=70)

'''SIGNIN '''

#text
canvas1.create_text(900,200,text = '\tSign In',fill='orange',font="Arial 35 bold")
canvas1.create_text(885,250,text = 'Username:',fill='white',font="Arial 22")
canvas1.create_text(885,290,text = 'Password:',fill='white',font="Arial 22")

#input boxes
login_username=StringVar()
login_password=StringVar()
Entry(canvas1,font="Arial 18 ",textvariable=login_username,bg='light grey').place(x=960,y=238,height=30, width=250)
Entry(canvas1,show='*',font="Arial 30 ",textvariable=login_password,bg='light grey').place(x=960,y=278,height=30, width=250)

#Login button
Button(window, text='Login',font="Arial 15 bold", width=6, command=signin).place(x=885,y=320,height=30, width=250)


'''SEARCH profiles'''

#text
canvas1.create_text(900,500,text = '\tSearch profiles',fill='light green',font="Arial 35 bold")
canvas1.create_text(855,550,text = 'Name:',fill='white',font="Arial 22")

#input boxes
search_name=StringVar()
Entry(canvas1,font="Arial 18 ",textvariable=search_name,bg='light grey').place(x=905,y=538,height=30, width=310)

#Search button
Button(window, text='Search',font="Arial 15 bold", width=6,command=search).place(x=885,y=580,height=30, width=250)


'''Create NEW profile'''

canvas1.create_text(310,180,text = 'New Here? Create a profile!',fill='cyan',font="Arial 30 bold")
canvas1.create_text(260,484,text = '''Choose username:
Full Name:
Choose Password:
Reenter Password:
Enter phone number:
Enter email id:

Choose Image



Enter something about yourself:
''',
fill='white',font="Arial 22")


'''INPUT BOXES'''

regis_username=StringVar()
regis_password=StringVar()
regis_password1=StringVar()
regis_fullname=StringVar()
regis_phone=StringVar()
regis_email=StringVar()

#username
Entry(canvas1,font="Arial 18 ",textvariable=regis_username,bg='light grey').place(x=305,y=276,height=25, width=250)
#fullname
Entry(canvas1,font="Arial 18 ",textvariable=regis_fullname,bg='light grey').place(x=203,y=309,height=25, width=352)
#passwords
Entry(canvas1,show='*',font="Arial 25 bold",textvariable=regis_password,bg='light grey').place(x=305,y=342,height=25, width=250)
Entry(canvas1,show='*',font="Arial 25 bold",textvariable=regis_password1,bg='light grey').place(x=305,y=375,height=25, width=250)

#phone number
Entry(canvas1,font="Arial 18 ",textvariable=regis_phone,bg='light grey').place(x=330,y=408,height=25, width=225)
#email
Entry(canvas1,font="Arial 18 ",textvariable=regis_email,bg='light grey').place(x=247,y=441,height=25, width=308)

#description
regis_desc= Text(canvas1, height = 3, width =38, font="Arial 18 italic",bg='light grey')
regis_desc.place(x=56,y=680)#,height=27, width=350)


'''buttons and rectangle'''

#create grey rectangle
canvas1.create_rectangle(280,480,400,620,fill='grey')
#add photo button
Button(window, text='+',font="Arial 30 bold", width=6, command=add_photo).place(x=150,y=545,height=60, width=90)
#create account button
Button(window, text='Create Account',font="Arial 15 bold", width=6, command=initialise).place(x=170,y=780,height=30, width=250)

window.mainloop()