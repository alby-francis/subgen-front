from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from datetime import datetime
from .models import Files, Contact
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
import mimetypes

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from django.contrib import messages

from django.shortcuts import render, redirect

from django.http.response import HttpResponse

from django.contrib.auth.decorators import login_required

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def file_detail_saver(request,filename,name_user_file):
    file_count=0
    pp=Files(user=request.user,File_name=name_user_file,FileS3=filename,Job_id=0)
    pp.save()

def index(request):
    # messages.success(request,'Test Msg')
    if not request.user.is_anonymous:
        return redirect('/up')
    if request.method == "POST":
        name = None
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if name and email and password:
            if User.objects.filter(username=email).exists():
                messages.warning(request, 'Email already exist')
            else:
                user = User.objects.create_user(username=email, first_name=name, email=email, password=password)
                user.save()
                #register=Register(name=name, email=email, password=password, date=datetime.today())
                #register.save()
                messages.success(request, 'Registration Succesfull, Plesae Login')
        else:
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user) 
                messages.success(request, 'Login Successful')
                return redirect('/up')
            else:
                messages.warning(request, 'Invalid Credential')
                return redirect('/home')
    return(render(request,'index.html'))
# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'vtt/signup.html', {'form': form})

def contact(request):
    if request.method == "POST":
        name = request.POST.get('contactname')
        email = request.POST.get('contactemail')
        message = request.POST.get('contactmessage')
        contact = Contact(name=name, email=email, message=message, date=datetime.today())
        contact.save()
        messages.success(request, 'We got your Message, Thank you for contacting us')
    #else:
        #messages.error(request, 'Some error occured. Please Try again.')
    return(render(request,'contact.html'))

@login_required(login_url='login')
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        
        name_of_user_file = myfile.name
        name_of_user_file = name_of_user_file.replace(" ","_")

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        filename = filename.replace(" ","_")
        #print(type(filename))
        #print(filename)
        uploaded_file_url = fs.url(filename)
        print(request.user)
        print(request.user.id)
        file_detail_saver(request,filename,name_of_user_file)

        return render(request, 'vtt/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'vtt/upload.html')

def start_srt(request):
    pass

# def index(request):
# 	return render(request,'vtt/base.html')


def stats(request):
	return render(request,'vtt/status.html')


def test(request):
	return render(request,'vtt/test1.html')

def get_user_file_list(request):
    user = request.user.id
    user_up_files = Files.objects.filter(user = user)
    #print(user_up_files[2].File_name)
    return render(request, 'vtt/filesname.html', {'user_up_files':user_up_files})

# Below are functions for dubtitle download, status etc.

def call_vtt_cli(name_of_file_in_server, srt_name):
    # python 3  srtGen_standalone_cli.py movie_to_transcribe.mov -s my-srtgen-transcription-bucket -o file_to_save_subtitles_to.srt
    path_parent = "c:"
    vtt_file = os.path.join(BASE_DIR, 'vtt_down')+'\\'+name_of_file_in_server[:-5+1]+'.srt'
    #print(vtt_folder)
    file_to_upload = os.path.join(BASE_DIR, 'down_files')+'\\'+name_of_file_in_server
    path_to_sub_gen_cli = f"C:\project_files\Srt_gen_prog\srt_gen.py"
    #os.process("python "+path_to_sub_gen_cli+" "+name_of_file_in_server+"-s bucket_name -o "+vtt_file)
    #print("python "+path_to_sub_gen_cli+" \'"+file_to_upload+"\' -s sdbca -o \\\'"+vtt_file+"\\\'")
    print('python '+path_to_sub_gen_cli+' \"'+file_to_upload+'\" -s sdbca -o \"'+vtt_file+'\"')

def send_file_for_subtitle(request, findex):
    user = request.user.id
    user_file_list = Files.objects.filter(user = user)
    # try eat or check if len of list is greater than
    user_has_n_files = len(user_file_list)
    file_n = int (findex)-1
    if(file_n>user_has_n_files):
        return redirect('/user_files')
        #change to render with vode message error
    file_obj_requested = user_file_list[file_n]
    name_of_file_in_server = file_obj_requested.FileS3
    srt_file_name = file_obj_requested.File_name[:-5+1]+'.srt'

    #check if already ran later
    #seprate database to save details later
    #call_vtt_cli(name_of_file_in_server, srt_file_name)
    #html = '<html><body>Subtitle has been requested for the file. <br>check status after few seconds <a  href="/user_files">click here to go back</a></body></html>'
    #return HttpResponse(html)
    messages.success(request, 'Request Succesfull. Check status after few seconds')
    return redirect('/user_files')

def get_file_name(request, findex):
    user = request.user.id
    user_file_list = Files.objects.filter(user = user)
    # try eat or check if len of list is greater than
    user_has_n_files = len(user_file_list)
    file_n = int (findex)-1
    if(file_n>user_has_n_files):
        return "Not_Found_S3"
        #change to render with vode message error
    file_obj_requested = user_file_list[file_n]
    name_of_file_in_server = file_obj_requested.FileS3
    print(name_of_file_in_server )
    return name_of_file_in_server

def check_status_of_vtt(request, findex):
    path_to_vtt_folder = os.path.join(BASE_DIR, 'vtt_down')
    name_of_file_in_server = get_file_name(request, findex)
    if(name_of_file_in_server=="Not_Found_S3"):
        return redirect('/user_files')
    name_of_file_in_server=name_of_file_in_server[:-5+1]
    exists_file=os.path.isfile(path_to_vtt_folder+'\\'+name_of_file_in_server+'.srt')
    print(path_to_vtt_folder+'\\'+name_of_file_in_server+'.srt')
    if exists_file:
        #code to checkif file present
        #html = '<html><body>file ready for download. <a  href="/user_files">click here to go back</a></body></html>'
        #return HttpResponse(html)
        messages.success(request, 'File ready to download. Click on download to download the file')
        return redirect('/user_files')
    else:
        #code else
        #html = '<html><body>file process not complete<br> try again after few seconds <a  href="/user_files">click here to go back</a></body></html>'
        #return HttpResponse(html)
        messages.warning(request, 'Your file is being processed. Please check after few Seconds')
        return redirect('/user_files')
        
    #is file present

def download_subtitles(request, findex):
    file_n = int (findex)

    user = request.user.id
    user_file_list = Files.objects.filter(user = user)

    file_obj_requested = user_file_list[file_n]
    name_of_file_in_server = file_obj_requested.FileS3
    pass


def download_file(request, findex):
    # Define Django project base directory
    file_n = int (findex)-1

    user = request.user.id
    user_file_list = Files.objects.filter(user = user)

    file_obj_requested = user_file_list[file_n]
    name_of_file_in_server = file_obj_requested.File_name
    name_of_file_in_server=name_of_file_in_server[:-5+1]+'.srt'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # # Define text file name
    # filename = 'test.txt'
    # Define the full file path
    filepath = BASE_DIR + '/vtt_down/' + name_of_file_in_server
    # Open the file for reading content
    exists_file=os.path.isfile(filepath)
    if not exists_file:
        #html = '<html><body>file process not complete<br> try again after few seconds <a  href="/user_files">click here to go back</a></body></html>'
        #return HttpResponse(html)
        messages.warning(request, 'Your file not ready to download. Please check after few Seconds')
        return redirect('/user_files')
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % name_of_file_in_server
    # Return the response value
    return response

# class Files(ListView):
# 	model = Files
# 	context_object_name = 'File_name'
def user(request):
    if request.user.is_anonymous:
        return redirect('index.html')
    return(render(request,'upload.html'))
    
class File_detail(DetailView):
	model = Files


