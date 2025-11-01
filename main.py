from tkinter import *
from PIL import Image,ImageTk
import mysql.connector
import pickle

fl3=open('sqlunp.dat','rb')
l1=pickle.load(fl3)
fl3.close()

user1=l1[0]
pass1=l1[1]
mydb=mysql.connector.connect(host='localhost',user=user1,password=pass1,database='PMDB3')
cur=mydb.cursor()

fl1=open('gentestid.dat','rb')
gen_testid=pickle.load(fl1)
fl1.close()

l_fr=['f1','f2','f3','f4','f5','fr1','f02','fb1','fb2','fb3','fb4']

def logout():
    for f in l_fr: 
        try:
            globals()[f].destroy()
        except:
            pass
    home()

def backtosdash():
    fb1.destroy()
    fb2.destroy()
    f4.destroy()
    f5.destroy()
    s_dashboard()

def givetest():
    def exam():
        cur.execute('select test_id from tests')
        all_tid=cur.fetchall()
        check_tid=(tstid.get(),)
        if check_tid in all_tid:
            global f02
            f02.destroy() 
            i=0
            marks=0
            def begin_test():
                nonlocal i
                nonlocal marks

                cur.execute(f'select * from {tstid.get()}')
                data5=cur.fetchall()
                if i<data4[2]:
                    global f4
                    f4.destroy()
                    f4=Frame()
                    f4.pack(side=TOP,pady=30)
                    if i!=0:
                        global f5
                        f5.destroy()
                        global f6  
                        f6.destroy()    
                    f5=Frame()
                    f5.pack() 
                    f6=Frame()
                    f6.pack()

                    d=data5[i]
                    Label(f4,text=f'Q{i+1}. {d[1]}',wraplength=750,justify='left',font=('Times New Roman','14')).pack()
                    ansvar=StringVar()
                    ansvar.set('  ')
                    Radiobutton(f4,text='A',variable=ansvar,value='A',font=('Times New Roman','14','bold')).pack(side=LEFT,padx=20,pady=30)
                    Radiobutton(f4,text='B',variable=ansvar,value='B',font=('Times New Roman','14','bold')).pack(side=LEFT,padx=20,pady=30)
                    Radiobutton(f4,text='C',variable=ansvar,value='C',font=('Times New Roman','14','bold')).pack(side=LEFT,padx=20,pady=30)
                    Radiobutton(f4,text='D',variable=ansvar,value='D',font=('Times New Roman','14','bold')).pack(side=LEFT,padx=20,pady=30)
                    response=True
                    def submit1():
                        nonlocal marks,response
                        if ansvar.get()==d[2] and response==True:
                            Label(f6,text='Congratulations! your answer is correct',fg='green',font='Arial 12').pack()
                            marks+=4
                            response=False

                        elif response==True:
                            Label(f6,text=f'Opps! The correct answer is {d[2]}',fg='red',font='Arial 12').pack()
                            marks-=1
                            response=False
                            
                    Button(f5,text='Submit',command=submit1,padx=7,pady=10,font='Arial 12').pack(padx=30,pady=10,side=LEFT)
                    Button(f5,text='Next',command=begin_test,padx=10,pady=10,font='Arial 12').pack(padx=30,pady=10,side=LEFT)
                    i+=1
                elif i==data4[2]:
                    f4.destroy()
                    f5.destroy()
                    f6.destroy()
                    global fb1
                    fb1=Frame()
                    fb1.pack(side=TOP,anchor=E)
                    f4=Frame()
                    f4.pack(pady=30)
                    Button(fb1,text='Back',command=backtosdash,bg='green').pack()
                    Label(f4,text=f'You scored {marks}/{data4[2]*4}',font='Arial 17 bold').pack(pady=30)
                    Label(f4,text='Thank You for giving the test',font='Arial 12',fg='green').pack(pady=60)
                    cur.execute('insert into result values(%s,%s,%s,%s,%s)',(tstid.get(),data4[1],user_name,sname,f'{marks}/{data4[2]*4}'))
                    mydb.commit()
                    f5=Frame()
                    f5.pack()
                    
            global f4
            f4.destroy()
            f4=Frame()
            f4.pack(side=TOP)
            Label(f4,text='Instructions : ',font='Arial 18 bold').pack(padx=30,pady=20)
            cur.execute(f"select * from tests where test_id=\'{tstid.get()}\'")
            data4=cur.fetchone()
            Label(f4,text=f'Test Name : {data4[1]}',font='Arial 14').pack(padx=30,pady=20)
            Label(f4,text=f'Marking Scheme : +4/-1',font='Arial 14').pack(padx=30,pady=20)
            Label(f4,text=f'No. of Questions : {data4[2]}',font='Arial 14').pack(padx=30,pady=20)
            Button(f4,text='Next',command=begin_test,padx=15,pady=10).pack(padx=30,pady=60)
        else:
            f02.destroy()
            f02=Frame()
            f02.pack()
            Label(f02,text='This Test ID does not exist',fg='red').pack()
    f3.destroy()
    fb2.destroy()
    global f4
    f4=Frame()
    f4.pack()
    global f02
    f02=Frame()
    f02.pack()
    Label(f4,text='Enter Test Id : ',font='Arial 16 bold').grid(row=1,column=0,pady=50)
    tstid=StringVar()
    Entry(f4,textvariable=tstid,font='Arial 15').grid(row=1,column=1,pady=50)
    Button(f4,text='Start Test',command=exam,padx=7,pady=10).grid(row=2,column=0)

def giveftest():
    f4.destroy()
    f5.destroy()
    givetest()

def spast_result():
    f3.destroy()
    fb2.destroy()
    global fb1
    fb1=Frame()
    fb1.pack(side=TOP,anchor=E)
    global f4
    f4=Frame()
    f4.pack(anchor=W)
    global f5
    f5=Frame()
    f5.pack()
    Button(fb1,text='Back',command=backtosdash,bg='green').pack()
    Label(f4,text='Past Tests Performance : ',font='forte 25 underline',fg='blue').pack(padx=30,pady=40,side=LEFT)
    cur.execute(f'select test_id,testname,marks from result where username="{user_name}"')
    l3=cur.fetchall()
    if l3==[]:
        Label(f5, text='No data Found',fg='red',font='Arial 16 bold').grid(row=0,column=0,pady=10)
        Label(f5,text='First give a Test to view result',font='Arial 16').grid(row=2,column=0,pady=10)
        Button(f5,text='Give Your First Test',command=giveftest,borderwidth=1,font='Arial 25 bold',fg='indigo').grid(row=3,column=0,pady=20)
    else:
        Label(f5,text='Test ID',font='Arial 15 bold').grid(row=0,column=0,padx=15)
        Label(f5,text='Test Name',font='Arial 15 bold').grid(row=0,column=1,padx=15)
        Label(f5,text='Marks Obtained',font='Arial 15 bold').grid(row=0,column=2,padx=15)
        k=1
        for i in l3:
            Label(f5,text=i[0],font='Arial 13').grid(row=k,column=0,padx=15)
            Label(f5,text=i[1],font='Arial 13').grid(row=k,column=1,padx=15)
            Label(f5,text=i[2],font='Arial 13').grid(row=k,column=2,padx=15)
            k+=1

def s_dashboard():
    fb3.destroy()
    f2.destroy()
    global f3,fb2
    fb2=Frame()
    fb2.pack(side=TOP,anchor=E)
    f3=Frame(highlightbackground="lightgreen",highlightthickness=5)
    f3.pack()
    Button(fb2,text='Logout',command=logout,bg='red',fg='white').pack(padx=10,pady=15)
    Label(f3,text=f'Dashboard :-',font='Forte 28 underline',fg='red').pack(anchor=W,pady=40,padx=60)
    Label(f3,text=f'Name- {sname}         Class- {sclass}',font='Forte 23 ',fg='blue').pack(anchor=W,padx=60)
    Button(f3,text='Give A Test',command=givetest,borderwidth=1,font='Arial 25 bold',fg='indigo').pack(anchor=W,padx=60,pady=25)
    Button(f3,text='Past Test Results',command=spast_result,borderwidth=1,font='Arial 25 bold',fg='indigo').pack(anchor=W,padx=60,pady=25)
    Label(f3,text='                        ').pack(padx=340,pady=10)
   

def s_check():
    cur.execute('select * from students')
    st=cur.fetchall()
    for i in st:
        u=i[0].lower()
        eu=user.get()
        eu=eu.lower()
        if u==eu and i[1]==pswd.get():
            global user_name,sname,sclass
            user_name=user.get()
            sname=i[2]
            sclass=i[3]
            s_dashboard()

def s_login():
    fr1.destroy()
    global f2
    f2=Frame()
    f2.pack(pady=50)
    Label(f2,text='Student Login',font='Forte 28 underline',fg='red').grid(row=0,column=0)
    Label(f2,text='Username : ',font='Arial 23 bold').grid(row=1,column=0,padx=10,pady=20)
    Label(f2,text='Password : ',font='Arial 23 bold').grid(row=2,column=0,padx=10,pady=20)
    global user,pswd
    user=StringVar()
    pswd=StringVar()
    user_entry=Entry(f2,textvariable=user,font='Arial 20')
    user_entry.grid(row=1,column=1)
    pswd_entry=Entry(f2,textvariable=pswd,font='Arial 20',show='*')
    pswd_entry.grid(row=2,column=1)
    Button(f2,text='Login',command=s_check,font='Arial 22 bold',fg='blue',borderwidth=2,border=5).grid(row=4,column=1)

def stu_n_user():
    fr1.destroy()
    def newstudentdata():
        insrt1='insert into students values(%s,%s,%s,%s);'
        vals1=[stu_nuser.get(),stu_npass.get(),stu_nname.get(),stu_nclass.get()]
        global sclass
        sclass=stu_nclass.get()
        global user_name,sname
        user_name=stu_nuser.get()
        sname=stu_nname.get()
        cur.execute(insrt1,vals1)
        mydb.commit()
    def button_s():
        newstudentdata()
        s_dashboard()
    global f2
    f2=Frame()
    f2.pack(pady=30)
    Label(f2,text='Enter following details:',font='Forte 25 underline',fg='blue').grid(row=0,column=0)
    Label(f2,text='Full name : ',font='Arial 20 bold').grid(row=1,column=0,pady=20)
    Label(f2,text='Class : ',font='Arial 20 bold').grid(row=2,column=0,pady=20)
    Label(f2,text='Username : ',font='Arial 20 bold').grid(row=3,column=0,pady=20)
    Label(f2,text='Password : ',font='Arial 20 bold').grid(row=4,column=0,pady=20)
    global stu_nuser,stu_npass,stu_nname,stu_nclass
    stu_nname=StringVar()
    stu_nuser=StringVar()
    stu_nclass=StringVar()
    stu_npass=StringVar()
    stu_nname_entry=Entry(f2,textvariable=stu_nname,font='Arial 20')
    stu_nname_entry.grid(row=1,column=1)
    stu_npass_entry=Entry(f2,textvariable=stu_npass,font='Arial 20')
    stu_npass_entry.grid(row=4,column=1)
    stu_nclass_entry=Entry(f2,textvariable=stu_nclass,font='Arial 20')
    stu_nclass_entry.grid(row=2,column=1)
    stu_nuser_entry=Entry(f2,textvariable=stu_nuser,font='Arial 20')
    stu_nuser_entry.grid(row=3,column=1)
    Button(f2,text='Sign up',command=button_s,font='Arial 22 bold',fg='green',borderwidth=2,border=5).grid(row=5,column=1)

def s_signup():
    f1.destroy()
    global fr1,fb3
    fb3=Frame()
    fb3.pack(side=TOP,anchor=E)
    fr1=Frame()
    fr1.pack(pady=20)
    Button(fb3,text='Back',bg='greenyellow',command=logout).pack(padx=10,pady=5)
    Label(fr1,text='You Are A : ',font='Forte 40 underline',fg='blue').grid(row=0,column=0,pady=30)
    Button(fr1,text='New User',command=stu_n_user,height=3,width=12,font='Arial 15 bold').grid(row=1,column=0,padx=50,pady=70)
    Button(fr1,text='Existing User',command=s_login,height=3,width=12,font='Arial 15 bold').grid(row=1,column=1,padx=50,pady=70)

def backtotdash():
    fb1.destroy()
    f4.destroy()
    f2=Frame()
    f2.pack()
    t_dashboard()

def createtest():
    i=0
    def crtst():
        nonlocal i
        if i==0:
            ins1='insert into tests values(%s,%s,%s)'
            dat1=(testid,test_name.get(),nques.get())
            cur.execute(ins1,dat1)
            mydb.commit()
            cur.execute(f'create table {testid} (Qid int unique not null auto_increment, question text, answer varchar(10), primary key(Qid) );')
            global f5
            f5=Frame()
            f5.pack()
        if i<nques.get():
            global f4
            f4.destroy()
            f4=Frame()
            f4.pack(anchor=NW)
            f5.destroy()
            f5=Frame()
            f5.pack(anchor=NW)
            Label(f4,text=f'Enter Question {i+1} : ').grid(row=1,column=0,padx=30,pady=20)
            qsn=Text(f4,height=7,width=70)
            qsn.grid(row=1,column=1,pady=20)
            Label(f4,text='Option A').grid(row=2,column=0,pady=10)
            Label(f4,text='Option B').grid(row=3,column=0,pady=10)
            Label(f4,text='Option C').grid(row=4,column=0,pady=10)
            Label(f4,text='Option D').grid(row=5,column=0,pady=10)
            A=StringVar()
            B=StringVar()
            C=StringVar()
            D=StringVar()
            Entry(f4,textvariable=A,width=70).grid(row=2,column=1,pady=10)
            Entry(f4,textvariable=B,width=70).grid(row=3,column=1,pady=10)
            Entry(f4,textvariable=C,width=70).grid(row=4,column=1,pady=10)
            Entry(f4,textvariable=D,width=70).grid(row=5,column=1,pady=10)
            Label(f5,text='Enter Answer : ').grid(row=2,column=0,padx=30,pady=20)
            ans=StringVar()
            ans.set('  ')
            Radiobutton(f5,text='A',variable=ans,value='A').grid(row=2,column=1,padx=10,pady=20)
            Radiobutton(f5,text='B',variable=ans,value='B').grid(row=2,column=2,padx=10,pady=20)
            Radiobutton(f5,text='C',variable=ans,value='C').grid(row=2,column=3,padx=10,pady=20)
            Radiobutton(f5,text='D',variable=ans,value='D').grid(row=2,column=4,padx=10,pady=20)
            def ins_val():
                q=qsn.get("1.0","end-1c")+'\n (A)'+A.get()+'\n (B)'+B.get()+'\n (C)'+C.get()+'\n (D)'+D.get()
                ins3=f'insert into {testid} (question,answer) values("{q}","{ans.get()}")'
                cur.execute(ins3)
                mydb.commit()
                crtst()
            Button(f5,text='Next',command=ins_val,padx=20,pady=10).grid(row=3,column=0,padx=30,pady=20)
            i+=1
        elif i==nques.get():
            f4.destroy()
            f5.destroy()
            global fb1
            fb1=Frame()
            fb1.pack(side=TOP,anchor=E)
            f4=Frame()
            f4.pack(anchor=CENTER)
            Button(fb1,text='Home',command=backtotdash,bg='greenyellow').pack(padx=15,pady=7)
            Label(f4,text='Test Created!',font='Arial 16 bold').pack(pady=10)
            Label(f4,text='The test for this test is : ',font='Arial 18 bold').pack(padx=10,pady=10,side=LEFT)
            Label(f4,text=testid,font='Arial 18 bold',bg='lightcyan',padx=10,pady=10).pack(side=LEFT)

    f3.destroy()
    fb2.destroy()
    global f4
    f4=Frame()
    f4.pack(side=LEFT,anchor=NW)
    global gen_testid
    gen_testid+=1
    testid='T'+str(gen_testid)
    
    fl2=open('gentestid.dat','wb')
    pickle.dump(gen_testid,fl2)
    fl2.close()

    Label(f4,text='Enter The Name of Test').grid(row=1,column=0,padx=30,pady=20)
    Label(f4,text='Enter The Number of Questions in Test').grid(row=2,column=0,padx=30,pady=20)
    test_name=StringVar()
    Entry(f4,textvariable=test_name).grid(row=1,column=1,padx=30,pady=20)
    nques=IntVar()
    Entry(f4,textvariable=nques).grid(row=2,column=1,padx=30,pady=20)
    Button(f4,text='Start Creating',command=crtst,padx=10,pady=10).grid(row=3,column=0,padx=30,pady=20)

def result():
    def rslt():
        cur.execute(f'select username,name,marks from result where test_id="{tstid.get()}"')
        l2=cur.fetchall()
        Label(f4,text='Username',font='Arial 12 bold').grid(row=3,column=0)
        Label(f4,text='Name',font='Arial 12 bold').grid(row=3,column=1)
        Label(f4,text='Marks',font='Arial 12 bold').grid(row=3,column=2)
        c=4
        for i in l2:
            Label(f4,text=i[0]).grid(row=c,column=0)
            Label(f4,text=i[1]).grid(row=c,column=1)
            Label(f4,text=i[2]).grid(row=c,column=2)
            c+=1
    f3.destroy()
    fb2.destroy()
    global f4,fb1
    fb1=Frame()
    fb1.pack(side=TOP,anchor=E)
    f4=Frame()
    f4.pack()
    Button(fb1,text='Home',command=backtotdash,bg='springgreen').pack(padx=15,pady=7)
    Label(f4).grid(row=0,column=0,pady=10)
    Label(f4,text='Enter Test Id : ',font='Arial 16 bold').grid(row=1,column=0)
    tstid=StringVar()
    Entry(f4,textvariable=tstid,font='Arial 15').grid(row=1,column=1)
    Button(f4,text='Show Result',command=rslt,padx=7,pady=10).grid(row=2,column=0,pady=30)

def t_dashboard():
    f2.destroy()
    fb3.destroy()
    global f3,fb2
    fb2=Frame()
    fb2.pack(side=TOP,anchor=E)
    f3=Frame(highlightbackground="lightgreen",highlightthickness=5)
    f3.pack(pady=30)
    Button(fb2,text='Logout',command=logout,bg='red',fg='white').pack(padx=10,pady=7)
    Label(f3, text=f'Dashboard :-', font='Forte 28 underline', fg='red').pack(anchor=W, pady=30, padx=60)
    Label(f3, text=f'Name: {tname}        Subject: {tsubject}', font='Forte 23 ', fg='blue').pack(anchor=W, pady=10, padx=60)
    Button(f3,text='Create a Test',command=createtest,borderwidth=1,font='Arial 25 bold',fg='indigo').pack(anchor=W,pady=40,padx=60)
    Button(f3,text='Show Results',command=result,borderwidth=1,font='Arial 25 bold',fg='indigo').pack(anchor=W,padx=50)
    Label(f3,text='                        ').pack(padx=340,pady=100)

def t_check():
    cur.execute('select * from teachers')
    ts=cur.fetchall()
    for i in ts:
        u=i[0].lower()
        eu=user.get()
        eu=eu.lower()
        if u==eu and i[1]==pswd.get():
            global tname,tsubject 
            tname=i[2]
            tsubject=i[3]
            t_dashboard()

def t_login():
    f1.destroy()
    global f2,fb3
    fb3=Frame()
    fb3.pack(side=TOP,anchor=W)
    f2=Frame()
    f2.pack(pady=50)
    Button(fb3,text='Back',bg='green',fg='white',command=logout).pack(padx=10,pady=5)
    Label(f2,text='Teacher Login',font='Forte 28 underline',fg='red').grid(row=0,column=0)
    Label(f2,text='Username : ',font='Arial 23 bold').grid(row=1,column=0,padx=10,pady=20)
    Label(f2,text='Password : ',font='Arial 23 bold').grid(row=2,column=0,padx=10,pady=20)
    global user,pswd
    user=StringVar()
    pswd=StringVar()
    user_entry=Entry(f2,textvariable=user,font='Arial 20')
    user_entry.grid(row=1,column=1)
    pswd_entry=Entry(f2,textvariable=pswd,font='Arial 20',show='*')
    pswd_entry.grid(row=2,column=1)
    Button(f2,text='Login',command=t_check,font='Arial 22 bold',fg='blue',borderwidth=2,border=5).grid(row=4,column=1)

def home():
    global f1,photo1
    f1=Frame()
    f1.pack()
    img1=Image.open('Images\\Logo.png')
    img1=img1.resize((220,180))
    photo1=ImageTk.PhotoImage(img1)
    photo1_label=Label(f1,image=photo1,bg='black')
    photo1_label.pack(pady=20)
    Label(f1,text='Welcome to PrepMaster - The Ultimate Exam Preparation Platform',font='TimesNewRoman 12 bold' ).pack()
    Label(f1,text='Are You A:',font='ArialBlack 18 bold').pack(anchor=W,pady=40,padx=40)
    Button(f1,text='Student',command=s_signup,height=3,width=12,font='Arial 15 bold').pack(side=LEFT,padx=30)
    Button(f1,text='Teacher',command=t_login,height=3,width=12,font='Arial 15 bold').pack(side=LEFT,padx=30)
    

root=Tk()
root.geometry('820x540')
root.title('PrepMaster')
f1=Frame()
f1.pack()
img1=Image.open('Images\\Logo.png')
img1=img1.resize((220,180))
photo1=ImageTk.PhotoImage(img1)
photo1_label=Label(f1,image=photo1,bg='black')
photo1_label.pack(pady=20)
Label(f1,text='Welcome to PrepMaster - The Ultimate Exam Conducting Platform',font='TimesNewRoman 12 bold' ).pack()
Label(f1,text='Are You A:',font='ArialBlack 18 bold').pack(anchor=W,pady=40,padx=40)
Button(f1,text='Student',command=s_signup,height=3,width=12,font='Arial 15 bold').pack(side=LEFT,padx=30)
Button(f1,text='Teacher',command=t_login,height=3,width=12,font='Arial 15 bold').pack(side=LEFT,padx=30)

root.mainloop()
