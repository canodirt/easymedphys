from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.urls import reverse
from django.forms.formsets import formset_factory
from .models import Organization, Events, session, evaluation_Event, evaluation_Speaker, attendance_Session, samQuestion, samAnswer, samResults
from .forms import evaluationForm, evaluationSpeakerForm, samQuestionsForm
from django.http import Http404
from django.contrib.auth.decorators import login_required


def index(request):
    organization_list = Organization.objects.all#.order_by('word')
    context = {'organization_list': organization_list}
    return render(request, 'cme/index.html', context)

def events(request, urlshortOrganization):
    thisorganization=Organization.objects.filter(urlshort=urlshortOrganization)[0]
    print('ORAGAN',thisorganization.name)
    events = get_list_or_404(Events, organization=thisorganization)
#    print('EVENTS:',events)
#    print('organization:',Organization.objects.filter(pk=organization_id))
    return render(request, 'cme/detail.html', {'events': events, 'organization':thisorganization})


def event_sessions(request, urlshortEvents):
    import datetime
    class sessionsDate():
        actualDate=''#actualDate
        session_list=''#session_list

    def sortEventsforView(unsorted_session_list):
        dateDict={}
        for session in unsorted_session_list:
            thisdate=str(session.start_datetime.year)+'-'+str(session.start_datetime.month)+'-'+str(session.start_datetime.day)
            print(session.title, thisdate, session.start_datetime)
            if not thisdate in dateDict.keys():
                dateDict[thisdate]={}

            dateDict[thisdate][session.start_datetime]=session
        #ok now lets put it all back together
        returnlist=[]
        for datekey in sorted(dateDict.keys()):
            sessionlist=[]
            for session in sorted(dateDict[datekey].keys()):
                sessionlist.append(dateDict[datekey][session])
            thisDateClass=sessionsDate()
            dateforclass=datetime.date(1900, int(datekey.split('-')[1]), 1).strftime('%B') + ' ' + datekey.split('-')[2]+', '+datekey.split('-')[0]
            thisDateClass.actualDate=str(dateforclass)
            thisDateClass.session_list=sessionlist
            returnlist.append(thisDateClass)
        return returnlist


    thisevent=Events.objects.filter(urlshort=urlshortEvents)[0]
    unsorted_session_list = get_list_or_404(session,event=thisevent)
    session_list=sortEventsforView(unsorted_session_list)
    print(session_list)
    return render(request, 'cme/event.html', {'session_Dates':session_list, 'event':thisevent})

@login_required
def event_evaluation(request, urlshortEvents):
    thisevent=Events.objects.filter(urlshort=urlshortEvents)[0]
    session_list = get_list_or_404(event,event=thisevent)
    #if you've filled out you can't do it again
    check = evaluation_Event.objects.filter(created_by=request.user, event=thisevent)

    if check:
        return HttpResponse('You\'ve already done this evaluation.  Thank you.')
    # if this is a POST request we need to process the form data
    elif request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print('POST:',request.POST)
        form = evaluationForm(request.POST)#,user=request.user)
        print('user:', request.user)
#        print('valid',form.is_valid())
        print(form.errors)
#        print(get_form_kwargs(request.POST))
        # check whether it's valid:

        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            programContent=request.POST['programContent']
            # print(programContent,'content')
            learningObjectives=request.POST['learningObjectives']
            facultyKnowledge=request.POST['facultyKnowledge']
            quality=request.POST['quality']
            handouts=request.POST['handouts']
            meetingRoom=request.POST['meetingRoom']
            audio=request.POST['audio']
            additionalComments = request.POST['additionalComments']
            evaluation_Event.objects.create(event=thisevent,
                                           programContent=programContent,
                                           learningObjectives=learningObjectives,
                                           facultyKnowledge=facultyKnowledge,
                                           quality=quality,
                                           handouts=handouts,
                                           meetingRoom=meetingRoom,
                                           audio=audio,
                                           additionalComments=additionalComments,
                                           created_by=request.user
                                           )

            # print('RETURNED:',request.POST)
            # print(request.POST.keys())
            # print('user:',request.user)
            # print('USER:',request.user)
            return redirect('cme:event_sessions', urlshortEvents=thissession.event.urlshort)
            # return HttpResponse('/thanks/')
        else:
            print('yo yo yo')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = evaluationForm()#user=request.user)
        # print('user',user)
        # print(form.get_form_kwargs())

    return render(request, 'cme/event_evaluation.html', {'form':form,'session_list':session_list, 'event':thisevent})

@login_required
def speaker_evaluations_all(request, urlshortEvents):
    thisevent=Events.objects.filter(urlshort=urlshortEvents)[0]
    session_list = get_list_or_404(session,event=thisevent)
    print('Session len:',len(session_list))
    evaluationFormSetInit=formset_factory(evaluationSpeakerForm,extra=len(session_list))
    evaluationFormSet = evaluationFormSetInit(initial=[{'id': x.pk} for x in session_list])
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print('POST:',request.POST)
        form = evaluationFormSetInit(request.POST)
        print('valid:',form.is_valid())
        print('RETURNED KEYs:', request.POST.keys())
        for key in request.POST.keys():
            print(key, ':', request.POST[key])
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print('RETURNED:',request.POST)
            print('RETURNED KEYs:', request.POST.keys())
            print('USER:',request.user)
            for key in request.POST.keys():
                print(key,':',request.POST[key])
            # return HttpResponse('/thanks/')
            return redirect('event_sessions', urlshortEvents)
        else:
            print('yo yo yo')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = evaluationFormSet#evaluationForm()

    return render(request, 'cme/speaker_evaluation_all.html', {'formset':evaluationFormSet,'session_list':session_list, 'event':thisevent})


@login_required
def session_evaluation(request,pk):#, pk):
    # pk=1
    thissession = session.objects.filter(pk=int(pk))[0]
    print('THIS SESSION:',thissession)
    # thisevent=Events.objects.filter(urlshort=urlshortEvents)[0]
    # session_list = get_list_or_404(session,event=thisevent)
    # print('Session len:',len(session_list))
    # evaluationFormSetInit=formset_factory(evaluationSpeakerForm,extra=len(session_list))
    # evaluationFormSet = evaluationFormSetInit(initial=[{'id': x.pk} for x in session_list])
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print('POST:',request.POST)
        form = evaluationSpeakerForm(request.POST)
        print('valid:',form.is_valid())
        print('RETURNED KEYs:', request.POST.keys())
        for key in request.POST.keys():
            print(key, ':', request.POST[key])
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # print(programContent,'content')
            learningObjectives=request.POST['learningObjectives']
            usefulness=request.POST['usefulness']
            quality=request.POST['quality']
            handout=request.POST['handout']
            worthiness=request.POST['worthiness']
            percentAttended=request.POST['percentAttended']
            additionalComments = request.POST['additionalComments']
            evaluation_Speaker.objects.create(session=thissession,
                                           learningObjectives=learningObjectives,
                                           usefulness=usefulness,
                                           quality=quality,
                                           handout=handout,
                                           worthiness=worthiness,
                                           percentAttended=percentAttended,
                                           additionalComments=additionalComments,
                                           created_by=request.user
                                           )
            attendance_Session.objects.create(session=thissession,
                                              percentAttended=percentAttended,
                                              created_by = request.user
                                              )


            print('RETURNED:',request.POST)
            print('RETURNED KEYs:', request.POST.keys())
            print('USER:',request.user)
            for key in request.POST.keys():
                print(key,':',request.POST[key])
            return redirect('cme:event_sessions', urlshortEvents=thissession.event.urlshort)

            # return HttpResponse('/thanks/')
        else:
            form=evaluationSpeakerForm
            print('yo yo yo')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = evaluationSpeakerForm#FormSet#evaluationForm()

    return render(request, 'cme/session_evaluation.html', {'form':form, 'session':thissession})


from django.urls import reverse
from django.http import HttpResponseRedirect
@login_required
def samQuestionSubmission(request,pk=0,questionnum=0):#, pk):
    # pk=1
    questionnum=int(questionnum)
    # questionnum=0
    print(['questionnum',questionnum])
    thissession = session.objects.filter(pk=int(pk))[0]
    # evaluationFormSetInit=formset_factory(evaluationSpeakerForm,extra=len(session_list))
    # evaluationFormSet = evaluationFormSetInit(initial=[{'id': x.pk} for x in session_list])
    # i=0
    thissamQuestion = samQuestion.objects.filter(session=thissession)[questionnum]
    thissamAnswers = samAnswer.objects.filter(samQuestion=thissamQuestion)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print('POST:',request.POST)
        form = samQuestionsForm([])#request.POST)
        print('valid:',form.is_valid())
        print('RETURNED KEYs:', request.POST.keys())
        for key in request.POST.keys():
            print(key, ':', request.POST[key])
        # check whether it's valid:
        if request.POST['samAnswer']!='':

            # if form.is   _valid():
            thisAnswer = samAnswer.objects.filter(pk=request.POST['samAnswer'])[0]
            thisQuestion = thisAnswer.samQuestion

            created_by=request.user
            samResults.objects.create(samQuestion=thisQuestion,
                                      selectedAnswer=thisAnswer,
                                      created_by=created_by
                                      )



            # samQuestion=thisQuestion
            # selectedAnswer= samAnswer.objects.filter()
            print('USER:',request.user)
            print('post:',request.POST)
            for key in request.POST.keys():
                print(key,':',request.POST[key])
            # i+=1
            print('pass the buck')
            # print(thisQuestion.answer_text)
            # print(thisQuestion.samQuestion.pk)
            # print('####')
            # print(request.POST['samAnswer'])
            # print([pk,questionnum])
            questionnum=str(thisQuestion.pk-1)

            # print('now question num',questionnum)
            # print(['path',''+str(questionnum)+'/'])
            # redirect('cme:samQuestion',str(pk), str(questionnum+1))
            # redirect('samQuestion/'+str(pk)+'/'+str(questionnum+1)+'/')
            print(request.path)
            # print(request.GET.path)
            # lastnum=request.path.split('/')[-1]
            # questionnum=str(int(lastnum)+1)
            print('NEW QUEST NUM',questionnum)
            # print(request.get_full_path)
            # print('REVERSE:',reverse('cme:samQuestion'))
            # redirect('SAMQuestion/15/'+questionnum)
            # thissamQuestion=samQuestion.objects.filter(session=thissession)[questionnum]
            # return render(request, 'cme/sam_single_question.html',
            #           {'form': form, 'thisquestion': thissamQuestion, 'session': thissession})

        # return render(request,'samQuestion',{pk:pk,questionnum:questionnum})
            if int(questionnum)<len(samQuestion.objects.filter(session=thissession)):
                return HttpResponseRedirect(reverse('cme:samQuestion', kwargs={'pk':str(pk), 'questionnum':str(questionnum)}))
            else:
                thissession=thisQuestion.session
                return redirect('cme:event_sessions', urlshortEvents=thissession.event.urlshort)

                # return HttpResponseRedirect(''+str(questionnum)+'/')#'cme:samQuestion', kwargs={pk:str(pk), questionnum:str(questionnum+1)})
            # redirect('cme:samQuestion',pk=pk,questionnum=questionnum+1)
            # form=samQuestionSubmission(request,pk,questionnum+1)
            # return HttpResponse('/thanks/')
        else:
            print('ERRORS#####:\n',form.errors)
            for fields in form:
                print(fields,fields.errors)
            form = samQuestionsForm
            print('yo yo yo')

    # if a GET (or any other method) we'll create a blank form
    else:

        form = samQuestionsForm(thissamAnswers)
        # print(form)
        print('choiceset:',thissamQuestion.choice_set)
        for item in thissamQuestion.choice_set():
            print('choice:',item)
    return render(request, 'cme/sam_single_question.html', {'form':form, 'thisquestion':thissamQuestion,'session':thissession})



@login_required
def samQuestionSubmissionSingle(request,pk):#, pk):
    # pk=1
    thissession = session.objects.filter(pk=int(pk))[0]
    # evaluationFormSetInit=formset_factory(evaluationSpeakerForm,extra=len(session_list))
    # evaluationFormSet = evaluationFormSetInit(initial=[{'id': x.pk} for x in session_list])

    thissamQuestion = samQuestion.objects.filter(session=thissession)[0]

    thesesamQuestions = samQuestion.objects.filter(session=thissession)
    samQuestionFormSetInit = formset_factory(samQuestionsForm, extra = len(thesesamQuestions))
    samQuestionFormSet = samQuestionFormSetInit(initial=0)
    thissamAnswers = samAnswer.objects.filter(samQuestion=thissamQuestion)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print('POST:',request.POST)
        form = samQuestionsForm([])#request.POST)
        print('valid:',form.is_valid())
        print('RETURNED KEYs:', request.POST.keys())
        for key in request.POST.keys():
            print(key, ':', request.POST[key])
        # check whether it's valid:
        if request.POST['samAnswer']!='':
        # if form.is_valid():

            print('USER:',request.user)
            print('post:',request.POST)
            for key in request.POST.keys():
                print(key,':',request.POST[key])
            return HttpResponse('/thanks/')
            # form = samQuestion
        else:
            print('ERRORS#####:\n',form.errors)
            for fields in form:
                print(fields,fields.errors)
            form = samQuestionsForm
            print('yo yo yo')

    # if a GET (or any other method) we'll create a blank form
    else:

        form = samQuestionsForm(thissamAnswers)
        # print(form)
        print('choiceset:',thissamQuestion.choice_set)
        for item in thissamQuestion.choice_set():
            print('choice:',item)
    return render(request, 'cme/sam_single_question.html', {'form':form, 'thisquestion':thissamQuestion,'session':thissession})
