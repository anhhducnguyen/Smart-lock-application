from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from project import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from django.utils.encoding import force_bytes, force_str

from django.shortcuts import render
from django.http import JsonResponse
import os
import cv2
import base64
import numpy as np
from django.conf import settings



# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def index(request):
    return render(request, 'capture/index.html')

def capture_image(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image_data = request.POST.get('image')

        # Tạo thư mục lưu ảnh nếu chưa có
        folder_path = os.path.join(settings.MEDIA_ROOT, 'images', name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Xử lý dữ liệu ảnh từ base64
        image_data = image_data.split(",")[1]
        img = base64.b64decode(image_data)
        np_img = np.frombuffer(img, dtype=np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Đặt tên file và lưu
        file_name = f"{folder_path}/captured_image.png"
        cv2.imwrite(file_name, frame)

        return JsonResponse({"message": "Đã lưu ảnh thành công!"})

    return JsonResponse({"message": "Lỗi khi lưu ảnh!"}, status=400)

# def signup(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         fname = request.POST['fname']
#         # lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']
        
#         if User.objects.filter(username=username):
#             messages.error(request, "Username already exist! Please try some other username.")
#             return redirect('home')
        
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email Already Registered!!")
#             return redirect('home')
        
#         if len(username)>20:
#             messages.error(request, "Username must be under 20 charcters!!")
#             return redirect('home')
        
#         if pass1 != pass2:
#             messages.error(request, "Passwords didn't matched!!")
#             return redirect('home')
        
#         if not username.isalnum():
#             messages.error(request, "Username must be Alpha-Numeric!!")
#             return redirect('home')
        
#         myuser = User.objects.create_user(username, email, pass1)
#         myuser.first_name = fname
#         # myuser.last_name = lname
#         # myuser.is_active = False
#         myuser.is_active = False
#         myuser.save()
#         messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
#         # Welcome Email
#         subject = "Welcome to GFG- Django Login!!"
#         message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
#         from_email = settings.EMAIL_HOST_USER
#         to_list = [myuser.email]
#         send_mail(subject, message, from_email, to_list, fail_silently=True)
        
#         # Email Address Confirmation Email
#         current_site = get_current_site(request)
#         email_subject = "Confirm your Email @ GFG - Django Login!!"
#         message2 = render_to_string('email_confirmation.html',{
            
#             'name': myuser.first_name,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
#             'token': generate_token.make_token(myuser)
#         })
#         email = EmailMessage(
#         email_subject,
#         message2,
#         settings.EMAIL_HOST_USER,
#         [myuser.email],
#         )
#         email.fail_silently = True
#         email.send()
        
#         return redirect('signin')
        
        
#     return render(request, "authentication/signup.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('home')
        
        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your account has been created successfully! Please check your email to confirm your address and activate your account.")
        
        # Welcome Email
        subject = "Welcome to GFG - Django Login!"
        message = render_to_string('welcome_email.html', {'name': myuser.first_name})
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True, html_message=message)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email at GFG - Django Login!"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.content_subtype = "html"  # Set email format to HTML
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
    
    return render(request, "authentication/signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')


# def signin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         pass1 = request.POST['pass1']
        
#         user = authenticate(username=username, password=pass1)
        
#         if user is not None:
#             login(request, user)
#             fname = user.first_name
#             # messages.success(request, "Logged In Sucessfully!!")
#             return render(request, "authentication/index.html",{"fname":fname})
#             # return redirect('home')
#         else:
#             messages.error(request, "Bad Credentials!!")
#             return redirect('home')
    
#     return render(request, "authentication/signin.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect('home')  # Chuyển hướng đến trang chủ sau khi đăng nhập thành công
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')  # Chuyển hướng lại trang đăng nhập nếu thông tin không hợp lệ
    
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')