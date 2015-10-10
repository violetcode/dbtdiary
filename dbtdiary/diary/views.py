from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import DiaryForm, UserCreateForm, ContactForm
from .models import Diary, User
import datetime

def index(request, username=None):
    # Displays the homepage
    if request.user.is_authenticated():
        diaries = Diary.objects.filter(user=request.user).order_by('-time')[:10]
        ctx = {'diaries' : diaries}
        template = 'diary/index.html'
    else:
        template = 'diary/welcome.html'
        ctx = {}    
    return render(request, template, ctx)

def about(request):
    c = {}
    all_users = User.objects.all()
    total_user_count = all_users.count()
    active_user_count = all_users.filter(userprofile__active=True).count()
    diaries = Diary.objects.all()
    diary_count = diaries.count()
    diaries_per_day = {}
    for diary in diaries:
        day = datetime.date(diary.time.year, diary.time.month, diary.time.day)
        if day in diaries_per_day.keys():
            diaries_per_day[day] += 1
        else:
            diaries_per_day[day] = 1
    c = {'user_count': total_user_count, 'diary_count': diary_count, 
         'active_users': active_user_count, 'diaries_per_day': diaries_per_day}
    return render(request, 'about.html', c)

def _calc_mood(diary):
    negative = 0.0
    positive = 0.0
    total = 0.0
    negative = diary.pain/5.0 + diary.sad/5.0 + diary.anger/5.0 + diary.fear/5.0 + diary.disgust/5.0 + diary.jealousy/5.0 + diary.guilt/5.0 + diary.agitation/5.0 + diary.shame/5.0
    positive = diary.joy/5.0 + diary.happy/5.0 + diary.content/5.0 + diary.calm/5.0 + diary.grateful/5.0 + diary.excitement/5.0 + diary.hope/5.0 + diary.confidence/5.0 + diary.optimism/5.0
    total = positive - negative
    return total

@login_required
def submit(request):
    form = DiaryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.mood = _calc_mood(entry)
            entry.save()
            form.save_m2m()
            messages.success(request, 'New entry successfully created.')
            return HttpResponseRedirect(reverse('diary:index'))
        else:
            messages.error(request, 'Did not pass validation! Please correct the errors below.')
    else:
        form = DiaryForm()
    c = {'form': form, 'adding': True}
    return TemplateResponse(request, 'diary/form.html', c)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user  = form.save()
            messages.success(request, 'Thank you for registering, you can now '
                                      'login.')
            return HttpResponseRedirect(reverse('diary:login'))
    else:
        form = UserCreationForm()

    return TemplateResponse(request, 'accounts/register.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect(reverse('diary:index'))

@login_required
def summary(request):
    return summary_helper(request, 7, 'diary/summary.html')

@login_required
def month_summary(request):
    return summary_helper(request, 30, 'diary/month_summary.html')

@login_required
def year_summary(request):
    return summary_helper(request, 365.0, 'diary/year_summary.html')

@login_required
def summary_helper(request, days, template):
    c = {}
    now = datetime.datetime.now()
    days_ago = datetime.timedelta(days=days)
    past = now - days_ago
    diaries = Diary.objects.filter(user=request.user, time__gte=past)
    skills_counts = {}
    for diary in diaries:
        skills = diary.used_skills.all().values_list('description', flat=True)
        for skill in skills:
            if skill in skills_counts:
                skills_counts[skill] += 1
            else:
                skills_counts[skill] = 1
    page_type = request.GET.get('type')
    if page_type == 'desktop':
        c['desktop'] = True
    c['diaries'] = diaries.order_by('time')
    c['reverse'] = diaries.order_by('-time')
    c['skills'] = skills_counts
    return TemplateResponse(request, template, c)  

@login_required
def browse(request):
    diaries = Diary.objects.filter(user=request.user).order_by('-time')
    paginator = Paginator(diaries, 25.0) # Show 25.0 diaries per page
    page = request.GET.get('page')
    try:
        diaries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        diaries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        diaries = paginator.page(paginator.num_pages)
    c = {"diaries" : diaries}
    return TemplateResponse(request, 'diary/browse.html', c)

@login_required
def diary(request, diary_id):
    diary = get_object_or_404(Diary, id=diary_id, user=request.user)
    skills = diary.used_skills.all().values_list('description', flat=True)
    return TemplateResponse(request, 'diary/diary.html', {'diary': diary, 'skills': skills})


@login_required
def delete(request, diary_id):
    #I wanted a way to delete old test entries.
    #It wlll be the last update I make to the code. 
    #I didnt add a public link anywhere to the site. You can decide if you want to let people know or not.
    diary = get_object_or_404(Diary, pk=diary_id, user=request.user)
    if request.method == 'POST':
        diary.delete()
        messages.success(request, 'Diary deleted.')
        return redirect('diary:index')
    return render(request, 'diary/delete-confirm.html', {'diary': diary})


@login_required
def edit(request, diary_id):
    diary = get_object_or_404(Diary, id=diary_id, user=request.user)
    form = DiaryForm(request.POST or None, instance=diary)
    if request.method == 'POST':
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.mood = _calc_mood(entry)
            entry.save()
            form.save_m2m()
            messages.success(request, 'Entry successfully saved.')
            return HttpResponseRedirect(reverse('diary:index'))
        else:
            messages.error(request, 'Did not pass validation! Please correct the errors below.')
    c = {'form': form, 'adding': False}
    return TemplateResponse(request, 'diary/form.html', c)

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['marie@violetco.de']
            if cc_myself:
                recipients.append(sender)

            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)
            messages.success(request, 'Your message has been sent successfully. Thanks!')
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'diary/contact.html', {
        'form': form,
    })
