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

from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from firebase_admin import storage
from datetime import datetime



from PIL import Image
from io import BytesIO

from django.views.generic import RedirectView, TemplateView
from unfold.views import UnfoldModelAdminViewMixin

class MyStatistical(UnfoldModelAdminViewMixin, TemplateView):
    title = "ChatGPT"  # required: custom page header title
    permission_required = ()  # required: tuple of permissions
    template_name = "authentication/statistical_page.html"

class MyStore(UnfoldModelAdminViewMixin, TemplateView):
    title = "Store Title"  # required: custom page header title
    permission_required = ()  # required: tuple of permissions
    template_name = "authentication/store_page.html"

bucket = storage.bucket()

@csrf_exempt
def capture_img(request):
    if request.method == 'POST':
        try:
            # Lấy tên người dùng từ request
            name = request.POST.get('name', 'unknown_user').strip().replace(' ', '_')
            
            # Lấy ảnh base64 từ request
            image_data = request.POST.get('image_data')
            format, imgstr = image_data.split(';base64,')
            img_data = base64.b64decode(imgstr)
            
            # Mở ảnh từ dữ liệu base64
            image = Image.open(BytesIO(img_data))
            
            # Chuyển ảnh sang định dạng JPG nếu cần
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            buffer.seek(0)

            # Kiểm tra số lượng ảnh hiện có trong thư mục `images/{name}` trên Firebase
            blobs = bucket.list_blobs(prefix=f'images/{name}/')
            img_count = len([blob for blob in blobs])  # Đếm số lượng file trong thư mục
            
            # Tạo tên file dựa trên số lượng file hiện tại
            img_name = f"{img_count}.jpg"
            img_path = f"images/{name}/{img_name}"

            # Tạo đối tượng blob để upload lên Firebase
            blob = bucket.blob(img_path)
            blob.upload_from_file(buffer, content_type='image/jpeg')

            # Làm cho ảnh có thể truy cập công khai
            blob.make_public()

            return JsonResponse({'status': 'success', 'image_url': blob.public_url})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'capture/test3.html')


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def index(request):
    return render(request, 'capture/index.html')

def capture(request):
    return render(request, 'capture/capture.html')

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

# def list_user_directories():
#     bucket = storage.bucket()
#     blobs = bucket.list_blobs(prefix='images/')
#     directories = set()  # Use a set to avoid duplicates

#     for blob in blobs:
#         # Extract directory name
#         parts = blob.name.split('/')
#         if len(parts) > 1:  # Check if there's a subfolder
#             directories.add(parts[1])  # Add the first subfolder under 'images/'
    
#     return list(directories)  # Return as a list
def list_user_directories():
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix='images/')
    directories = {}  # Use a dictionary to store directory names and their corresponding image URLs

    for blob in blobs:
        # Extract directory name
        parts = blob.name.split('/')
        if len(parts) > 1:  # Check if there's a subfolder
            user_directory = parts[1]  # Get the user directory name
            if user_directory not in directories:
                directories[user_directory] = None  # Initialize with None

            # Check if this blob is the first image (0.jpg)
            if parts[-1] == '0.jpg':
                directories[user_directory] = blob.public_url  # Store the public URL of 0.jpg

    return directories  # Return the dictionary of directories and image URLs

# def display_user_images(request):
#     user_directories = list_user_directories()  # Get the list of user directories
#     return render(request, 'capture/display_images.html', {'user_directories': user_directories})

def display_user_images(request):
    user_directories = list_user_directories()  # Get the list of user directories and image URLs
    return render(request, 'capture/display_images.html', {'user_directories': user_directories})




