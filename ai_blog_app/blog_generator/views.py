from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube
import assemblyai as aai
import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from .models import BlogPost


@login_required
def index(request):
    return render(request, 'index.html')

def welcome_page(request):
    return render(request, 'welcome-page.html')

def login_page(request):
    return render(request, 'login.html')

def user_logout(request):
    auth_logout(request)
    return redirect('/welcome-page')

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/') 
        else:
            error_message = 'Incorrect user details'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeatPassword')

        if password == repeat_password:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                auth_login(request, user)
                return redirect('/login') 
            except Exception as e:
                error_message = str(e)
        else:
            error_message = 'Passwords do not match'

        return render(request, 'signup.html', {'error_message': error_message})
    
    return render(request, 'singup.html')

def blog_details(request, pk):
    posts_details = BlogPost.objects.get(id=pk)
    if request.user == posts_details.user:
        return render(request, 'blog-details.html', {'blog_article_detail':posts_details})
    else:
        redirect('/')

def all_blogs(request):
    posts = BlogPost.objects.filter(user=request.user)
    return render(request, 'all-blogs.html', {'blog_articles':posts})

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try: 
            data = json.loads(request.body)
            yt_link = data['link']
            video_title = get_video_title(yt_link)
            # video_transciption = get_video_transcription(yt_link)
            generated_content = generate_content_from_data(video_title)
            new_blog_post = BlogPost.objects.create(
                user=request.user,
                youtube_title=video_title,
                youtube_link=yt_link,
                generated_content=generated_content
            )
            new_blog_post.save()
            return JsonResponse({'content': generated_content})
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error':'Invalid data send'}, status=400)
        
def get_video_title(yt_link):
    yt = YouTube(yt_link)
    title = yt.title
    return title

# def get_video_transcription(yt_link):
#     aai.settings.api_key = "ac015fe86aa847148748533eff2fac28"
#     transcriber = aai.Transcriber()
#     transcript = transcriber.transcribe(yt_link)
#     print(transcript.text)
#     return transcript.text

# def get_video_transcription(yt_link):
#     try:
#         # Extracting video ID from the URL link
#         video_id = youtube_dl.YoutubeDL().extract_info(yt_link, download=False)['id']

#         # Getting the transcript of the video
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)

#         # Extracting text from each transcript entry
#         transcription = ''
#         for line in transcript:
#             transcription += line['text'] + ' '

#         return transcription
#     except Exception as e:
#         print("Error:", e)

def generate_content_from_data(data):
    # prompt = f"Na podstawie poniższego tytułu, wygeneruj artykuł na blogu: {data}"

    # try:
    #     response = openai.Completion.create(
    #         api_key=openai_api_key,
    #         engine="gpt-3.5-turbo", 
    #         prompt=prompt,
    #         max_tokens=1000
    #     )

    #     generated_content = response["choices"][0]["text"].strip()
    #     return generated_content

    # except Exception as e:
    #     print("An error occurred:", e)
    #     return None

    openai_api_key = "pass your ai key"
    client = OpenAI(api_key=openai_api_key)

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a blog maker, and you can make blog posts."},
                {"role": "user", "content": f"Based on this title generate blog post, title: {data}"}
            ]
        )
        response = completion.choices[0].message.content
        return response

    except Exception as e:
        print("An error occurred:", e)
        return None
