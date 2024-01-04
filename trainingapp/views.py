from django.shortcuts import render,redirect
from trainingapp.models import CustomUser,department,alldetails,trainees,trainers,trainerAttendence,traineeAttendence,trainerLeave,traineeLeave,tasks,submittedTask,schedule,TrainerNotifications,TraineeNotifications
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from datetime import datetime
import os
from django.urls import reverse
# Create your views here.
def index(request):
    return render(request,'index.html')
def loginpage(request):
    return render(request,'login.html')
def loginuser(request):
    if request.method == 'POST':
        user=request.POST['username']
        pwd=request.POST['password']
        usr1=auth.authenticate(username=user, password=pwd)
        if usr1 is not None:
            if usr1.user_type == '1':
                login(request,usr1)
                return redirect('adminhome')
            elif usr1.user_type == '2':
                auth.login(request,usr1)
                return redirect('trainerHome')
            elif usr1.user_type == '3':
                auth.login(request,usr1)
                return redirect('traineeHome')
        else:
            messages.info(request,'Invalid Username or Password!. Try again')
            return redirect('loginpage')
    else:
        return redirect('loginpage')
def about(request):
    return render(request,'about.html')
def trainerReg(request):
    existing_emails = list(CustomUser.objects.values_list('email', flat=True))
    usernames = CustomUser.objects.values_list('username', flat=True)
    phones=alldetails.objects.values_list('phone', flat=True)
    dep=department.objects.all()
    return render(request,'trainerReg.html',{'dept':dep,'existing_emails': existing_emails,'usernames':usernames,'phone':phones})
def Regtrainer(request):
    phones=alldetails.objects.values_list('phone', flat=True)
    if request.method == 'POST':
        try:
            fname=request.POST['fname']
            lname=request.POST['lname']
            user=request.POST['username']
            email=request.POST['email']
            phone=request.POST['contact']
            joind=request.POST['jdate']
            gen=request.POST['std_gender']
            image=request.FILES.get('profile')
            doc=request.FILES.get('files')
            sel=request.POST['sel']
            dep=department.objects.get(id=sel)
            us=request.POST['text']
            status=request.POST['status']
            password='dummy'
            if CustomUser.objects.filter(username__iexact=user).exists():
                messages.info(request,'This username already exists!!')
                return redirect('trainerReg')
            elif alldetails.objects.filter(phone__exact=phone).exists():
                messages.info(request,'Phone number Already exists!!')
                return redirect('trainerReg')
            elif len(phone) != 10:
                messages.info(request,'Phone Number Must Have 10 Digits!!')
                return redirect('trainerReg')
            elif CustomUser.objects.filter(email__iexact=email).exists():
                messages.info(request,'Email Already exists!!')
                return redirect('trainerReg')
            else:
                usr=CustomUser.objects.create_user(first_name=fname,last_name=lname,username=user,email=email,password=password,user_type=us)
                usr.save()

                det=alldetails(gender=gen,Join_Date=joind,phone=phone,Image=image,Docs=doc,status=status,dep=dep,user=usr)
                det.save()
                trainer=trainers(user=usr,details=det)
                trainer.save()
                subject='Thankyou for register with us'
                message2= 'Kindly wait for the admin approval of your profile'
                send_mail(subject,message2,settings.EMAIL_HOST_USER,[email])
                messages.info(request,'Account created.Kindly wait for admin approval.')
                return redirect('trainerReg')
        except:
            messages.info(request,'Fill all required Information!!')
            return redirect('trainerReg')
    return redirect('trainerReg')
def traineeReg(request):
    existing_emails = list(CustomUser.objects.values_list('email', flat=True))
    usernames = CustomUser.objects.values_list('username', flat=True)
    phones=alldetails.objects.values_list('phone', flat=True)
    dep=department.objects.all()
    return render(request,'traineeReg.html',{'dept':dep,'existing_emails': existing_emails,'usernames':usernames,'phone':phones})
def Regtrainee(request):
    if request.method == 'POST':
        try:
            fname=request.POST['fname']
            lname=request.POST['lname']
            user=request.POST['username']
            email=request.POST['email']
            phone=request.POST['contact']
            joind=request.POST['jdate']
            gen=request.POST['std_gender']
            image=request.FILES.get('profile')
            doc=request.FILES.get('files')
            sel=request.POST['sel']
            dep=department.objects.get(id=sel)
            us=request.POST['text']
            status=request.POST['status']
            password='dummy'
            if CustomUser.objects.filter(username__iexact=user).exists():
                messages.info(request,'This username already exists!!')
                return redirect('traineeReg')
            elif alldetails.objects.filter(phone__exact=phone).exists():
                messages.info(request,'Phone number Already exists!!')
                return redirect('traineeReg')
            elif len(phone) != 10:
                messages.info(request,'Phone Number Must Have 10 Digits!!')
                return redirect('traineeReg')
            elif CustomUser.objects.filter(email__iexact=email).exists():
                messages.info(request,'Email Already exists!!')
                return redirect('traineeReg')
            else:
                usr=CustomUser.objects.create_user(first_name=fname,last_name=lname,username=user,email=email,password=password,user_type=us)
                usr.save()

                det=alldetails(gender=gen,Join_Date=joind,phone=phone,Image=image,Docs=doc,status=status,dep=dep,user=usr)
                det.save()
                trainee=trainees(user=usr,details=det)
                trainee.save()
                subject='Thankyou for register with us'
                message2= 'Kindly wait for the admin approval of your profile'
                send_mail(subject,message2,settings.EMAIL_HOST_USER,[email])
                messages.info(request,'Account created.Kindly wait for admin approval.')
                return redirect('traineeReg')
        except:
            messages.info(request,'Fill all required Information!!')
            return redirect('traineeReg')
    return redirect('traineeReg')

# adminsection----------------------------------------------------------------------------------
@login_required(login_url='loginpage')
def adminhome(request):
    count=alldetails.objects.filter(status='pending').count()
    tr=trainers.objects.all().count()
    st=trainees.objects.all().count()
    de=department.objects.all().count()
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    return render(request,'admin/adminHome.html',{'num':count,'tr':tr,'st':st,'dep':de,'a':a})
@login_required(login_url='loginpage')
def admin_approve(request,a):
    user=CustomUser.objects.get(id=a)
    det=alldetails.objects.get(user_id=a)
    import random
    password = ''.join(random.choices('0123456789', k=6))
    user.set_password(password)
    user.save()
    det.status='approved'
    det.save()
    subject='Your account approved'
    message2= 'Username:'+user.username+'\n'+'Password:'+password+'\n'+'You can login now..'
    send_mail(subject,message2,settings.EMAIL_HOST_USER,[user.email])
    messages.info(request,'approved'+' '+user.first_name)
    return redirect('approvalpage')
@login_required(login_url='loginpage')
def admin_reject(request,a):
    user=CustomUser.objects.get(id=a)
    det=alldetails.objects.get(user_id=a)
    if len(det.Image)>0:
        os.remove(det.Image.path)
    if len(det.Docs)>0:
        os.remove(det.Docs.path)
    det.delete()
    det.user.delete()
    subject='Your account Rejected!!!'
    message2= 'Sorry! Your Account Rejected by manager.'
    send_mail(subject,message2,settings.EMAIL_HOST_USER,[user.email])
    messages.info(request,'Rejected'+' '+user.first_name)
    return redirect('approvalpage')
@login_required(login_url='loginpage')
def addnewtr(request):
    existing_emails = list(CustomUser.objects.values_list('email', flat=True))
    usernames = CustomUser.objects.values_list('username', flat=True)
    phones=alldetails.objects.values_list('phone', flat=True)
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    count=alldetails.objects.filter(status='pending').count()
    return render(request,'admin/addtrainer.html',{'num':count,'a':a,'existing_emails': existing_emails,'usernames':usernames,'phone':phones})
@login_required(login_url='loginpage')
def newtrainer(request):
    if request.method == 'POST':
        try:
            fname=request.POST['fname']
            lname=request.POST['lname']
            user=request.POST['username']
            email=request.POST['email']
            phone=request.POST['contact']
            joind=request.POST['jdate']
            gen=request.POST['std_gender']
            image=request.FILES.get('profile')
            doc=request.FILES.get('files')
            us=request.POST['text']
            import random
            password = ''.join(random.choices('0123456789', k=6))
            if CustomUser.objects.filter(username__iexact=user).exists():
                messages.info(request,'This username already exists!!')
                return redirect('addnewtr')
            elif alldetails.objects.filter(phone__exact=phone).exists():
                messages.info(request,'Phone number Already exists!!')
                return redirect('addnewtr')
            elif len(phone) != 10:
                messages.info(request,'Phone Number Must Have 10 Digits!!')
                return redirect('addnewtr')
            elif CustomUser.objects.filter(email__iexact=email).exists():
                messages.info(request,'Email Already exists!!')
                return redirect('addnewtr')
            else:
                usr=CustomUser.objects.create_user(first_name=fname,last_name=lname,username=user,email=email,password=password,user_type=us)
                usr.save()

                det=alldetails(gender=gen,Join_Date=joind,phone=phone,Image=image,Docs=doc,status='Approved',user=usr)
                det.save()
                trainer=trainers(user=usr,details=det)
                trainer.save()
                subject='Welcome to KnowledgeWorks'
                message2= 'Your Account has been created by trainee manager.'+'\n'+'Your Username:'+' '+user+'\n'+'Password:'+' '+password
                send_mail(subject,message2,settings.EMAIL_HOST_USER,[email])
                messages.info(request,'New trainer'+' '+fname+' '+'Added')
                return redirect('viewtrainer')
        except:
            messages.info(request,'Fill all required Information!!')
            return redirect('addnewtr')
    return redirect('addnewtr')
@login_required(login_url='loginpage')
def viewattend(request):
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    count=alldetails.objects.filter(status='pending').count()
    tr=trainers.objects.all()
    return render(request,'admin/viewattendence.html',{'trainer':tr,'num':count,'a':a})
@login_required(login_url='loginpage')
def viewattend1(request):
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    count=alldetails.objects.filter(status='pending').count()
    tr=trainees.objects.all()
    return render(request,'admin/viewtraineeattend.html',{'trainer':tr,'num':count,'a':a})
@login_required(login_url='loginpage')
def getattend(request):
    if request.method == 'POST':
        from_date_str = request.POST.get('from')
        to_date_str = request.POST.get('to')
        sel=request.POST['sel']
        tr=trainers.objects.get(id=sel)
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
        details = trainerAttendence.objects.filter(trainer=tr,date__range=[from_date_str, to_date_str])
        return render(request,'admin/attendence.html',{'details':details,'from':from_date,'to':to_date,'tr':tr})
    return redirect('viewattend')
@login_required(login_url='loginpage')
def getattend2(request):
    if request.method == 'POST':
        from_date_str = request.POST.get('from')
        to_date_str = request.POST.get('to')
        sel=request.POST['sel']
        tr=trainees.objects.get(id=sel)
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
        details = traineeAttendence.objects.filter(trainee=tr,date__range=[from_date_str, to_date_str])
        return render(request,'admin/attendence.html',{'details':details,'from':from_date,'to':to_date,'tr':tr})
    return redirect('viewattend1')
@login_required(login_url='loginpage')
def removeT(request,a):
    te=alldetails.objects.get(user_id=a)
    if te.user.user_type == '2':
        if len(te.Image)>0:
            os.remove(te.Image.path)
        if len(te.Docs)>0:
            os.remove(te.Docs.path)
        te.delete()
        te.user.delete()
        messages.info(request,'Trainer Removed')
        return redirect('viewtrainer')
    else:
        if len(te.Image)>0:
            os.remove(te.Image.path)
        if len(te.Docs)>0:
            os.remove(te.Docs.path)
        te.delete()
        te.user.delete()
        messages.info(request,'Trainee Removed')
        return redirect('viewtrainee')
@login_required(login_url='loginpage')
def trainerattend(request):
    count=alldetails.objects.filter(status='pending').count()
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    return render(request,'admin/trainerattend.html',{'num':count,'a':a})
@login_required(login_url='loginpage')
def leaveA(request):
    count=alldetails.objects.filter(status='pending').count()
    t1=trainerLeave.objects.filter(status='pending')
    t2=traineeLeave.objects.filter(status='pending')
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    return render(request,'admin/leaveReq.html',{'num':count,'trainer':t1,'trainee':t2,'a':a})
@login_required(login_url='loginpage')
def leave_approve1(request,a):
    l=trainerLeave.objects.get(id=a)
    l.status='Approved'
    l.save()
    n=TrainerNotifications(trainer=l.trainer,notify='Your leave Approved',link=reverse('leaveR'))
    n.save()
    messages.info(request,'Trainer leave Approved')
    return redirect(leaveA)
@login_required(login_url='loginpage')
def leave_approve2(request,a):
    l=traineeLeave.objects.get(id=a)
    l.status='Approved'
    l.save()
    n=TraineeNotifications(trainee=l.trainee,notify='Your leave Approved',link=reverse('leaveR'))
    n.save()
    messages.info(request,'Trainee leave Approved')
    return redirect(leaveA)
@login_required(login_url='loginpage')
def leave_reject1(request,a):
    l=trainerLeave.objects.get(id=a)
    l.status='Rejected'
    l.save()
    n=TrainerNotifications(trainer=l.trainer,notify='Your leave Rejected',link=reverse('leaveR'))
    n.save()
    messages.info(request,'Trainer leave Rejected')
    return redirect(leaveA)
@login_required(login_url='loginpage')
def leave_reject2(request,a):
    l=traineeLeave.objects.get(id=a)
    l.status='Rejected'
    l.save()
    n=TraineeNotifications(trainee=l.trainee,notify='Your leave Rejected',link=reverse('leaveR'))
    n.save()
    messages.info(request,'Trainee leave Rejected')
    return redirect(leaveA)
@login_required(login_url='loginpage')
def assignD(request):
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    count=alldetails.objects.filter(status='pending').count()
    return render(request,'admin/assignD.html',{'num':count,'a':a})
@login_required(login_url='loginpage')
def assignT(request):
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    user=trainees.objects.all()
    tr=trainers.objects.all()
    count=alldetails.objects.filter(status='pending').count()
    return render(request,'admin/assignT.html',{'num':count,'user':user,'dep':tr,'a':a})
@login_required(login_url='loginpage')
def batch(request,a):
    if request.method == 'POST':
        traine=trainees.objects.get(id=a)
        sel=request.POST['sel']
        trainer=trainers.objects.get(id=sel)
        traine.trainer=trainer
        traine.save()
        msg='You are assigned to the trainer-'+' '+trainer.user.first_name
        n=TraineeNotifications(trainee=traine,notify=msg,link=reverse('traineeHome'))
        n.save()
        msg2='New trainee'+' '+traine.user.first_name+' '+'assigned to you.'
        n1=TrainerNotifications(trainer=trainer,notify=msg2,link=reverse('manageTrainee'))
        n1.save()
        return redirect('assignT')
    return redirect('assignT')
@login_required(login_url='loginpage')
def changepass(request):
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    count=alldetails.objects.filter(status='pending').count()
    return render(request,'admin/changepass.html',{'num':count,'a':a})
@login_required(login_url='loginpage')
def chpass(request):
    current=request.user.id
    user=CustomUser.objects.get(id=current)
    if user.user_type == '1':
        if request.method == 'POST': 
            opass=request.POST['Oldpass']
            npass=request.POST['Newpass']
            cpass=request.POST['cpass']
            if len(npass) < 6 or not any(char.islower() for char in npass) or not any(char.isupper() for char in npass) or not any(char.isdigit() for char in npass) or not any(char in '!@#$%^&*' for char in npass):
                messages.info(request,'Password format not valid.')
                return redirect('changepass')
            elif not user.check_password(opass):
                messages.info(request,'Current Password Not Correct')
                return redirect('changepass')
            else:
                if npass==cpass:
                    user.set_password(npass)
                    user.save()
                    subject='Password Changed'
                    message2= 'Your password changed.New password:'+npass
                    send_mail(subject,message2,settings.EMAIL_HOST_USER,[user.email])
                    messages.info(request,'Password Changed')
                    return redirect('changepass')
                else:
                    messages.info(request,'Password not match!!')
                    return redirect('changepass')
        return redirect('changepass')
    elif user.user_type == '2':
        if request.method == 'POST': 
            opass=request.POST['Oldpass']
            npass=request.POST['Newpass']
            cpass=request.POST['cpass']
            if len(npass) < 6 or not any(char.islower() for char in npass) or not any(char.isupper() for char in npass) or not any(char.isdigit() for char in npass) or not any(char in '!@#$%^&*' for char in npass):
                messages.info(request,'Password format not valid.')
                return redirect('changepass2')
            elif not user.check_password(opass):
                messages.info(request,'Current Password Not Correct')
                return redirect('changepass2')
            else:
                if npass==cpass:
                    user.set_password(npass)
                    user.save()
                    subject='Password Changed'
                    message2= 'Your password changed.New password:'+npass
                    send_mail(subject,message2,settings.EMAIL_HOST_USER,[user.email])
                    messages.info(request,'Password Changed')
                    return redirect('changepass2')
                else:
                    messages.info(request,'Password not match!!')
                    return redirect('changepass2')
        return redirect('changepass2')
    else:
        if request.method == 'POST': 
            opass=request.POST['Oldpass']
            npass=request.POST['Newpass']
            cpass=request.POST['cpass']
            if len(npass) < 6 or not any(char.islower() for char in npass) or not any(char.isupper() for char in npass) or not any(char.isdigit() for char in npass) or not any(char in '!@#$%^&*' for char in npass):
                messages.info(request,'Password format not valid.')
                return redirect('trainerpass')
            elif not user.check_password(opass):
                messages.info(request,'Current Password Not Correct')
                return redirect('trainerpass')
            else:
                if npass==cpass:
                    user.set_password(npass)
                    user.save()
                    subject='Password Changed'
                    message2= 'Your password changed.New password:'+npass
                    send_mail(subject,message2,settings.EMAIL_HOST_USER,[user.email])
                    messages.info(request,'Password Changed')
                    return redirect('trainerpass')
                else:
                    messages.info(request,'Password not match!!')
                    return redirect('trainerpass')
        return redirect('trainerpass')
@login_required(login_url='loginpage')
def userdetails(request):
    count=alldetails.objects.filter(status='pending').count()
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    return render(request,'admin/userdetails.html',{'num':count,'a':a})
@login_required(login_url='loginpage')
def attendence(request):
    count=alldetails.objects.filter(status='pending').count()
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    return render(request,'admin/attendence.html',{'num':count,'a':a})
@login_required(login_url='loginpage')
def logout_admin(request):
    auth.logout(request)
    return redirect('index')
@login_required(login_url='loginpage')
def addeptpage(request):
    count=alldetails.objects.filter(status='pending').count()
    dep=department.objects.all()
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    return render(request,'admin/dept.html',{'dept':dep,'num':count,'a':a})
@login_required(login_url='loginpage')
def newdept(request):
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    count=alldetails.objects.filter(status='pending').count()
    return render(request,'admin/adddep.html',{'num':count,'a':a})
@login_required(login_url='loginpage')
def departmentadd(request):
    if request.method == 'POST':
        dep=request.POST['dept']
        if department.objects.filter(Dept=dep).exists():
            messages.info(request,'Department already exists!!')
            return redirect('newdept')
        else:
            dept=department(Dept=dep)
            dept.save()
            messages.info(request,'Department Added Successfully..')
            return redirect('addeptpage')
    return redirect('newdept')
@login_required(login_url='loginpage')
def deletedep(request,a):
    st=department.objects.get(id=a)
    st.delete()
    return redirect('addeptpage')
@login_required(login_url='loginpage')
def approvalpage(request):
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    user=alldetails.objects.filter(status='pending')
    count=alldetails.objects.filter(status='pending').count()
    return render(request,'admin/approveuser.html',{'user':user,'num':count,'a':a})
@login_required(login_url='loginpage')
def viewuser1(request,b):
    count=alldetails.objects.filter(status='pending').count()
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    u1=alldetails.objects.get(user_id=b)
    return render(request,'admin/viewuser.html',{'users':u1,'num':count,'a':a})
@login_required(login_url='loginpage')
def viewtrainer(request):
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    count=alldetails.objects.filter(status='pending').count()
    tr=trainers.objects.all()
    return render(request,'admin/viewtrainer.html',{'trainer':tr,'num':count,'a':a})
@login_required(login_url='loginpage')
def viewtrainee(request):
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    count=alldetails.objects.filter(status='pending').count()
    tr=trainees.objects.all()
    return render(request,'admin/viewtrainee.html',{'trainee':tr,'num':count,'a':a})

@login_required(login_url='loginpage')
def addattendence(request):
    count=alldetails.objects.filter(status='pending').count()
    user2=trainers.objects.all()
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    return render(request,'admin/addatendence.html',{'user':user2,'num':count,'a':a})
@login_required(login_url='loginpage')
def markattend(request,a):
    if request.method == 'POST':
        date_value = request.POST.get('Dattend')
        tr=trainers.objects.get(id=a)
        if 'submit_1' in request.POST:
            if date_value:
                month, day, year = map(int, date_value.split('-'))
                corrected_date = f'{year}-{month}-{day}'
                date_object = datetime.strptime(corrected_date, '%d-%Y-%m')
                if trainerAttendence.objects.filter(trainer_id=a,date=date_object).exists():
                    messages.info(request,'Attendence already marked')
                    return redirect('addattendence')
                else:
                    status='Present'
                    atten=trainerAttendence(trainer=tr,date=date_object,status=status)
                    atten.save()
                    messages.info(request,'Attendence marked')
                    return redirect('addattendence')
        elif 'submit_2' in request.POST:
            if date_value:
                month, day, year = map(int, date_value.split('-'))
                corrected_date = f'{year}-{month}-{day}'
                date_object = datetime.strptime(corrected_date, '%d-%Y-%m')
                if trainerAttendence.objects.filter(trainer_id=a,date=date_object).exists():
                    messages.info(request,'Attendence already marked')
                    return redirect('addattendence')
                else:
                    status='Absent'
                    atten=trainerAttendence(trainer=tr,date=date_object,status=status)
                    atten.save()
                    messages.info(request,'Attendence marked')
                    return redirect('addattendence')
        return redirect('addattendence')
    return redirect('addattendence')
@login_required(login_url='loginpage')
def assigndepTr1(request):
    user=trainees.objects.all()
    dep=department.objects.all()
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    t='Trainee'
    return render(request,'admin/assignDTr.html',{'dep':dep,'user':user,'t':t,'a':a})
@login_required(login_url='loginpage')
def assigndepTr(request):
    user=trainers.objects.all()
    dep=department.objects.all()
    t='Trainer'
    c1=trainerLeave.objects.filter(status='pending').count()
    c2=traineeLeave.objects.filter(status='pending').count()
    a=c1+c2
    return render(request,'admin/assignDTr.html',{'dep':dep,'user':user,'t':t,'a':a})
@login_required(login_url='loginpage')
def assign(request,a):
    if request.method == 'POST':
        details=alldetails.objects.get(id=a)
        
        sel=request.POST['sel']
        dep=department.objects.get(id=sel)
        details.dep=dep
        details.save()
    if details.user.user_type == '2':
        tr=trainers.objects.get(details_id=a)
        msg='Your department changed to'+' '+dep.Dept
        n=TrainerNotifications(trainer=tr,notify=msg,link=reverse('trainerHome'))
        n.save()
        return redirect('assigndepTr')
    else:
        tr=trainees.objects.get(details_id=a)
        msg='Your department changed to'+' '+dep.Dept
        n=TraineeNotifications(trainee=tr,notify=msg,link=reverse('traineeHome'))
        n.save()
        return redirect('assigndepTr1')

# trainersection----------------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='loginpage')
def trainerHome(request):
    current=request.user.id
    user=alldetails.objects.get(user_id=current)
    t=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=t.id,read_status=False).count()
    return render(request,'trainer/profile.html',{'user':user,'num':num})
@login_required(login_url='loginpage')
def notification1(request):
    current=request.user.id
    t=trainers.objects.get(user_id=current)
    n=TrainerNotifications.objects.filter(trainer_id=t.id,read_status=False)
    num=TrainerNotifications.objects.filter(trainer_id=t.id,read_status=False).count()
    return render(request,'trainer/notifications.html',{'noti':n,'num':num,'tr':t})
@login_required(login_url='loginpage')
def readNoti(request,a):
    n=TrainerNotifications.objects.get(id=a)
    n.read_status=True
    n.save()
    return redirect(n.link)
@login_required(login_url='loginpage')
def editpage(request):
    current=request.user.id
    existing_emails = list(CustomUser.objects.values_list('email', flat=True))
    usernames = CustomUser.objects.values_list('username', flat=True)
    phones=alldetails.objects.values_list('phone', flat=True)
    t=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=t.id,read_status=False).count()
    user=alldetails.objects.get(user_id=current)
    return render(request,'trainer/editpage.html',{'user':user,'num':num,'existing_emails': existing_emails,'usernames':usernames,'phone':phones})
@login_required(login_url='loginpage')
def editU(request):
    current=request.user.id 
    userD=alldetails.objects.get(user_id=current)
    userA=CustomUser.objects.get(id=current)
    if request.method == 'POST':
        userN=request.POST['username']
        ph=request.POST['contact']
        em=request.POST['email']
        if userA.username != userN and CustomUser.objects.filter(username__iexact=userN).exists(): 
            messages.info(request,'This username already exists!!')
            return redirect('editpage')
        elif userA.email != em and CustomUser.objects.filter(email__iexact=em).exists(): 
            messages.info(request,'This email already exists!!')
            return redirect('editpage')  
        elif userD.phone != ph and alldetails.objects.filter(phone__exact=ph).exists(): 
            messages.info(request,'This phone number already exists!!')
            return redirect('editpage')
        elif userD.phone != ph and len(ph) != 10: 
            messages.info(request,'This phone number must have 10 digits!!')
            return redirect('editpage')  
        else:
            userA.username=request.POST['username']
            userA.first_name=request.POST['fname']
            userA.last_name=request.POST['lname']
            userA.email=request.POST['email']
            userD.phone=request.POST['contact']
            if len(request.FILES)!=0:
                if len(userD.Image)>0:
                    os.remove(userD.Image.path)
                userD.Image=request.FILES.get('profile')
            userA.save()
            userD.save()
            return redirect('trainerHome')
    return redirect('editU')
@login_required(login_url='loginpage')
def manageTrainee(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    t=trainees.objects.filter(trainer_id=tr.id)
    return render(request,'trainer/manTrainee.html',{'trainee':t,'num':num,'tr':tr})
@login_required(login_url='loginpage')
def addtrattend(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    t=trainees.objects.filter(trainer_id=tr.id)
    return render(request,'trainer/traineeattendence.html',{'user':t,'num':num,'tr':tr})
@login_required(login_url='loginpage')
def markattend1(request,a):
    if request.method == 'POST':
        date_value = request.POST.get('Dattend')
        tr=trainees.objects.get(id=a)
        if 'submit_1' in request.POST:
            if date_value:
                month, day, year = map(int, date_value.split('-'))
                corrected_date = f'{year}-{month}-{day}'
                date_object = datetime.strptime(corrected_date, '%d-%Y-%m')
                if traineeAttendence.objects.filter(trainee_id=a,date=date_object).exists():
                    messages.info(request,'Attendence already marked')
                    return redirect('addtrattend')
                else:
                    status='Present'
                    atten=traineeAttendence(trainee=tr,date=date_object,status=status)
                    atten.save()
                    messages.info(request,'Attendence marked')
                    return redirect('addtrattend')
        elif 'submit_2' in request.POST:
            if date_value:
                month, day, year = map(int, date_value.split('-'))
                corrected_date = f'{year}-{month}-{day}'
                date_object = datetime.strptime(corrected_date, '%d-%Y-%m')
                if traineeAttendence.objects.filter(trainee_id=a,date=date_object).exists():
                    messages.info(request,'Attendence already marked')
                    return redirect('addtrattend')
                else:
                    status='Absent'
                    atten=traineeAttendence(trainee=tr,date=date_object,status=status)
                    atten.save()
                    messages.info(request,'Attendence marked')
                    return redirect('addtrattend')
        return redirect('addtrattend')
    return redirect('addtrattend')
@login_required(login_url='loginpage')
def viewatt(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    t=trainees.objects.filter(trainer_id=tr.id)
    return render(request,'trainer/viewattendence.html',{'user':t,'num':num,'tr':tr})
@login_required(login_url='loginpage')
def getattend1(request):
    current=request.user.id
    u=trainers.objects.get(user_id=current)
    if request.method == 'POST':
        from_date_str = request.POST.get('from')
        to_date_str = request.POST.get('to')
        sel=request.POST['sel']
        tr=trainees.objects.get(id=sel)
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
        details = traineeAttendence.objects.filter(trainee=tr,date__range=[from_date_str, to_date_str])
        return render(request,'trainer/attendence.html',{'details':details,'from':from_date,'to':to_date,'tr':tr,'u':u})
    return redirect('viewatt')
@login_required(login_url='loginpage')
def myattend(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    return render(request,'trainer/myattend.html',{'num':num,'tr':tr})
@login_required(login_url='loginpage')
def myattview(request):
    current=request.user.id
    use=CustomUser.objects.get(id=current)
    if use.user_type =='2':
        if request.method == 'POST':
            from_date_str = request.POST.get('from')
            to_date_str = request.POST.get('to')
            tr1=trainers.objects.get(user_id=current)
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
            num=TrainerNotifications.objects.filter(trainer_id=tr1.id,read_status=False).count()
            details = trainerAttendence.objects.filter(trainer=tr1,date__range=[from_date_str, to_date_str])
            return render(request,'trainer/attendence.html',{'details':details,'from':from_date,'to':to_date,'tr':tr1,'num':num,'use':use})
        return redirect(' myattend')   
    else:
        if request.method == 'POST':
            from_date_str = request.POST.get('from')
            to_date_str = request.POST.get('to')
            tr=trainees.objects.get(user_id=current)
            num=TraineeNotifications.objects.filter(trainee_id=tr.id,read_status=False).count()
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
            details = traineeAttendence.objects.filter(trainee=tr,date__range=[from_date_str, to_date_str])
            return render(request,'trainee/viewattend.html',{'details':details,'from':from_date,'to':to_date,'tr':tr,'num':num,'use':use})
        return redirect('attendencepage')
@login_required(login_url='loginpage')
def schedulep(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    return render(request,'trainer/schedule.html',{'num':num,'tr':tr})
@login_required(login_url='loginpage')
def applyschedule(request):
    current=request.user.id
    use=trainers.objects.get(user_id=current)
    tr=trainees.objects.filter(trainer_id=use.id)
    if request.method == 'POST':
        topic=request.POST['topic']
        d=request.POST['day']
        t=request.POST['time']
        T=schedule(topic=topic,from_date=d,time=t,trainer=use)
        T.save()
        torg = datetime.strptime(t, "%H:%M")
        Crttime = torg.strftime("%I %p")
        for u in tr:
            msg='Class Scheduled at -'+' '+Crttime
            n=TraineeNotifications(trainee=u,notify=msg,link=reverse('batchtime'))
            n.save()
        messages.info(request,'Class Scheduled')
        return redirect('schedulep')
    return redirect('schedulep')
@login_required(login_url='loginpage')
def taskpage(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    return render(request,'trainer/taskpage.html',{'num':num,'tr':tr})
@login_required(login_url='loginpage')
def astask(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    return render(request,'trainer/assignTask.html',{'num':num,'tr':tr})
@login_required(login_url='loginpage')
def viewalltask(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    task=tasks.objects.filter(trainer_id=tr.id)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    return render(request,'trainer/viewalltask.html',{'num':num,'tasks':task,'tr':tr})
@login_required(login_url='loginpage')
def subtask(request):
    us=request.user.id
    tr=trainers.objects.get(user_id=us)
    t=tasks.objects.filter(trainer_id=tr.id)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    sub=submittedTask.objects.filter(task__in=t)
    return render(request,'trainer/submitted.html',{'task':sub,'num':num,'tr':tr})
@login_required(login_url='loginpage')
def trattend(request):
    current=request.user.id
    use=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=use.id,read_status=False).count()
    return render(request,'trainer/attendence.html',{'num':num,'use':use})
@login_required(login_url='loginpage')
def addat(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    return render(request,'trainer/addattendence.html',{'num':num,'tr':tr})
@login_required(login_url='loginpage')
def leaveapply(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    return render(request,'trainer/leave.html',{'num':num,'tr':tr})
@login_required(login_url='loginpage')
def leavepage(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    return render(request,'trainer/leavepage.html',{'num':num,'tr':tr})
@login_required(login_url='loginpage')
def leaveRequest(request):
    current=request.user.id
    use=CustomUser.objects.get(id=current)
    if use.user_type =='2':
        tr=trainers.objects.get(user_id=current)
        if request.method == 'POST':
            reason=request.POST['reason']
            s=request.POST['from']
            e=request.POST['to']
            sat=request.POST['status']
            l=trainerLeave(trainer=tr,reason=reason,from_date=s,to_date=e,status=sat)
            l.save()
            messages.info(request,'Leave Applied')
            return redirect('leaveapply')
        return redirect('leaveapply')
    else:
        tr=trainees.objects.get(user_id=current)
        if request.method == 'POST':
            reason=request.POST['reason']
            s=request.POST['from']
            e=request.POST['to']
            sat=request.POST['status']
            l=traineeLeave(trainee=tr,reason=reason,from_date=s,to_date=e,status=sat)
            l.save()
            messages.info(request,'Leave Applied')
            return redirect('trainerLR')
        return redirect('trainerLR')
@login_required(login_url='loginpage')
def leaveR(request):
    c=request.user.id
    use=CustomUser.objects.get(id=c)
    if use.user_type =='2':
        tr=trainers.objects.get(user_id=c)
        num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
        l=trainerLeave.objects.filter(trainer_id=tr.id)
        return render(request,'trainer/leaveR.html',{'leaves':l,'num':num,'tr':tr})
    else:
        tr=trainees.objects.get(user_id=c)
        num=TraineeNotifications.objects.filter(trainee_id=tr.id,read_status=False).count()
        l=traineeLeave.objects.filter(trainee_id=tr.id)
        return render(request,'trainee/leaves.html',{'leaves':l,'num':num,'tr':tr})
@login_required(login_url='loginpage')
def changepass2(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    return render(request,'trainer/changepass.html',{'num':num,'tr':tr})
@login_required(login_url='loginpage')
def viewTr(request,a):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    num=TrainerNotifications.objects.filter(trainer_id=tr.id,read_status=False).count()
    user=alldetails.objects.get(user_id=a)
    return render(request,'trainer/viewtrainee.html',{'user':user,'num':num,'tr':tr})
@login_required(login_url='loginpage')
def logout_user(request):
    auth.logout(request)
    return redirect('index')
@login_required(login_url='loginpage')
def assigntask(request):
    current=request.user.id
    tr=trainers.objects.get(user_id=current)
    tr1=trainees.objects.filter(trainer_id=tr.id)
    if request.method == 'POST':
        task=request.POST['topic']
        s=request.POST['from']
        e=request.POST['to']
        T=tasks(name=task,from_date=s,to_date=e,trainer=tr)
        T.save()
        for u in tr1:
            msg='New Task Assigned'
            n=TraineeNotifications(trainee=u,notify=msg,link=reverse('submitTask'))
            n.save()
        messages.info(request,'Task Applied')
        return redirect('astask')
# traineesection-----------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='loginpage')
def traineehome(request):
    current=request.user.id
    user=alldetails.objects.get(user_id=current)
    tr1=trainees.objects.get(user_id=current)
    num=TraineeNotifications.objects.filter(trainee_id=tr1.id,read_status=False).count()
    return render(request,'trainee/traineeHome.html',{'user':user,'tr':tr1,'num':num})
@login_required(login_url='loginpage')
def notification2(request):
    current=request.user.id
    user=alldetails.objects.get(user_id=current)
    t=trainees.objects.get(user_id=current)
    n=TraineeNotifications.objects.filter(trainee_id=t.id,read_status=False)
    num=TraineeNotifications.objects.filter(trainee_id=t.id,read_status=False).count()
    return render(request,'trainee/notifications.html',{'noti':n,'num':num,'user':user})
@login_required(login_url='loginpage')
def readNoti2(request,a):
    n=TraineeNotifications.objects.get(id=a)
    n.read_status=True
    n.save()
    return redirect(n.link)
@login_required(login_url='loginpage')
def traineTask(request):
    current=request.user.id
    user=alldetails.objects.get(user_id=current)
    t=trainees.objects.get(user_id=current)
    num=TraineeNotifications.objects.filter(trainee_id=t.id,read_status=False).count()
    return render(request,'trainee/taskpage.html',{'num':num,'user':user})
@login_required(login_url='loginpage')
def submitTask(request):
    current=request.user.id
    user=alldetails.objects.get(user_id=current)
    u=trainees.objects.get(user_id=current)
    num=TraineeNotifications.objects.filter(trainee_id=u.id,read_status=False).count()
    t=trainers.objects.get(id=u.trainer_id)
    sub=submittedTask.objects.filter(trainee_id=u.id)
    doned_tasks = sub.values_list('task_id', flat=True)
    task=tasks.objects.filter(trainer_id=t.id).exclude(id__in=doned_tasks)
    return render(request,'trainee/submit.html',{'user':task,'num':num,'t':user,'sub':sub})
@login_required(login_url='loginpage')
def donetask(request):
    current=request.user.id
    user=alldetails.objects.get(user_id=current)
    u=trainees.objects.get(user_id=current)
    num=TraineeNotifications.objects.filter(trainee_id=u.id,read_status=False).count()
    t=submittedTask.objects.filter(trainee_id=u.id)
    return render(request,'trainee/done.html',{'task':t,'num':num,'user':user})
@login_required(login_url='loginpage')
def batchtime(request):
    c=request.user.id
    user=alldetails.objects.get(user_id=c)
    tr=trainees.objects.get(user_id=c)
    num=TraineeNotifications.objects.filter(trainee_id=tr.id,read_status=False).count()
    t=trainers.objects.get(id=tr.trainer_id)
    ba=schedule.objects.filter(trainer_id=t.id)
    return render(request,'trainee/classschedule.html',{'b':ba,'num':num,'user':user})
@login_required(login_url='loginpage')
def joined(request,a):
    b=schedule.objects.get(id=a)
    b.status='Read'
    b.save()
    return redirect('batchtime')
@login_required(login_url='loginpage')
def attendencepage(request):
    c=request.user.id
    user=alldetails.objects.get(user_id=c)
    tr=trainees.objects.get(user_id=c)
    num=TraineeNotifications.objects.filter(trainee_id=tr.id,read_status=False).count()
    return render(request,'trainee/attendencepage.html',{'num':num,'user':user})
@login_required(login_url='loginpage')
def trainerleave(request):
    c=request.user.id
    tr=trainees.objects.get(user_id=c)
    num=TraineeNotifications.objects.filter(trainee_id=tr.id,read_status=False).count()
    return render(request,'trainee/leavepage.html',{'num':num,'tr':tr})
@login_required(login_url='loginpage')
def trainerLR(request):
    c=request.user.id
    tr=trainees.objects.get(user_id=c)
    num=TraineeNotifications.objects.filter(trainee_id=tr.id,read_status=False).count()
    return render(request,'trainee/leaveapply.html',{'num':num,'tr':tr})
@login_required(login_url='loginpage')
def trainerpass(request):
    c=request.user.id
    tr=trainees.objects.get(user_id=c)
    num=TraineeNotifications.objects.filter(trainee_id=tr.id,read_status=False).count()
    return render(request,'trainee/chpass.html',{'num':num,'tr':tr})
@login_required(login_url='loginpage')
def editpage1(request):
    current=request.user.id
    existing_emails = list(CustomUser.objects.values_list('email', flat=True))
    usernames = CustomUser.objects.values_list('username', flat=True)
    phones=alldetails.objects.values_list('phone', flat=True)
    tr=trainees.objects.get(user_id=current)
    num=TraineeNotifications.objects.filter(trainee_id=tr.id,read_status=False).count()
    user=alldetails.objects.get(user_id=current)
    return render(request,'trainee/editpage.html',{'user':user,'num':num,'existing_emails': existing_emails,'usernames':usernames,'phone':phones})
@login_required(login_url='loginpage')
def editU1(request):
    current=request.user.id 
    userD=alldetails.objects.get(user_id=current)
    userA=CustomUser.objects.get(id=current)
    if request.method == 'POST':
        userN=request.POST['username']
        ph=request.POST['contact']
        em=request.POST['email']
        if userA.username != userN and CustomUser.objects.filter(username__iexact=userN).exists(): 
            messages.info(request,'This username already exists!!')
            return redirect('editpage1')
        elif userA.email != em and CustomUser.objects.filter(email__iexact=em).exists(): 
            messages.info(request,'This email already exists!!')
            return redirect('editpage1')  
        elif userD.phone != ph and alldetails.objects.filter(phone__exact=ph).exists(): 
            messages.info(request,'This phone number already exists!!')
            return redirect('editpage1')
        elif userD.phone != ph and len(ph) != 10: 
            messages.info(request,'This phone number must have 10 digits!!')
            return redirect('editpage1')
        else:
            userA.username=request.POST['username']
            userA.first_name=request.POST['fname']
            userA.last_name=request.POST['lname']
            userA.email=request.POST['email']
            userD.phone=request.POST['contact']
            if len(request.FILES)!=0:
                if len(userD.Image)>0:
                    os.remove(userD.Image.path)
                userD.Image=request.FILES.get('profile')
            userA.save()
            userD.save()
            return redirect('traineeHome')
    return redirect('editU1')
@login_required(login_url='loginpage')
def dosubmit(request,a):
    current=request.user.id
    tr=trainees.objects.get(user_id=current)
    num=TraineeNotifications.objects.filter(trainee_id=tr.id,read_status=False).count()
    task=tasks.objects.get(id=a)
    return render(request,'trainee/dosubmit.html',{'task':task,'num':num})
@login_required(login_url='loginpage')
def submitaction(request,a):
    task=tasks.objects.get(id=a)
    current=request.user.id 
    t=trainees.objects.get(user_id=current)
    tr=trainers.objects.get(id=t.trainer_id)
    num=TraineeNotifications.objects.filter(trainee_id=t.id,read_status=False).count()
    if request.method == 'POST':
        desc=request.POST['desc']
        doc=request.FILES.get('files')
        current_date = datetime.now().date()
        if current_date<= task.to_date:
            ts=submittedTask(trainee=t,task=task,desc=desc,docs=doc,delay='On Time',status='Submitted')
            ts.save()
        else:
            ts=submittedTask(trainee=t,task=task,desc=desc,docs=doc,delay='Delay',status='Submitted')
            ts.save()
        msg='Task Submitted By'+' '+t.user.username
        n=TrainerNotifications(trainer=tr,notify=msg,link=reverse('subtask'))
        n.save()
        messages.info(request,'Task Submitted')
        return render(request,'trainee/dosubmit.html',{'task':task,'num':num})
    return render(request,'trainee/dosubmit.html',{'task':task,'num':num})

