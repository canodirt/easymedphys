from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from cme.models import Organization,Events, session, samAnswer, samQuestion
import datetime
from django.apps import apps


def makeCustomUser(email='', first_name='',last_name='',occupation='Other', campep = False, mdcb = False, username=''):
    return CustomUser(email=email,first_name=first_name,last_name=last_name,
                      occupation=occupation, campep = campep, mdcb=mdcb,
                      username=username)
def createEventFromCAMPEPxls(xlsfile):
    import xlrd, datetime

    book = xlrd.open_workbook(xlsfile)

    # get the first worksheet
    sheet = book.sheet_by_name('EATemplate')

    dictLocations={0:'CAMPEPReferenceID',
                   1:'title',
                   2:'start_date',
                   #3:'start_time',
                   5:'CAMPEP Credits Number',
                   6:'duration',
                   7:'email',
                   8:'last_name',
                   9:'first_name',
                   10:'CAMPEP Category',
                   11:'CAMPEP Subcategory'
                   }
    row = 16 #first row of real data
    data=[]
    while row < sheet.nrows:
        thisline={}
        for col in dictLocations.keys():
            if col in [2,3]:
                # print(sheet.cell(row,col))
                thiscell=sheet.cell_value(row,col)
                # print(thiscell)
                #
                # print(xlrd.xldate_as_tuple(thiscell, book.datemode))
                thisdate=xlrd.xldate_as_tuple(thiscell, book.datemode)
                year,month,day=thisdate[0],thisdate[1],thisdate[2]
                thiscell = sheet.cell_value(row, 3)
                thisdate = xlrd.xldate_as_tuple(thiscell, book.datemode)
                hour,minute,second=thisdate[3],thisdate[4],thisdate[5]
                # if year==0:
                #     year=1
                # if month==0:
                #     month=1
                # if day==0:
                #     day=1
                thisdate=datetime.datetime(year=year,month=month,day=day,
                                              hour=hour,minute=minute,second=second)

                # print(thisdate[0],thisdate[1],thisdate[2])
                thisline[dictLocations[col]]=thisdate
                # thisline += dictLocations[col] + ':' + datestr + ';\t'
                # thisline += dictLocations[col] + ':' + \
                #             str(datetime.datetime(xlrd.xldate_as_tuple(thiscell, book.datemode))) + ';\t'
            else:
                thisline[dictLocations[col]] = sheet.cell_value(row, col)
                # thisline += dictLocations[col] + ':' + str(sheet.cell_value(row, col)) + ';\t'
        # print(thisline)
        print(row,thisline['title'])
        data.append(thisline)
        row+=1
    # first_sheet.cell(0, 0)
    #now make a dict to popuplate the events/sessions
    returnSessionList=[]
    returnUserList=[]
    userHeaders=['email','last_name','first_name']
    sessionHeaders=['title']
    print('#################################')
    for sessionDict in data:
        # print(sessionDict)
        thisUser={}
        for userHeader in userHeaders:
            thisUser[userHeader]=sessionDict[userHeader]
        if not thisUser in returnUserList:
            returnUserList.append(thisUser)
        #now create session info
        thissession={'title': sessionDict['title'],
                     'start_datetime': sessionDict['start_date'],
                     'end_datetime': sessionDict['start_date'] + datetime.timedelta(minutes=sessionDict['duration']),
                     'presenterInfo':thisUser,
                     'isCAMPEP':True,
                     'CAMPEPReferenceID':sessionDict['CAMPEPReferenceID']

                     }
        returnSessionList.append(thissession)

    return returnUserList,returnSessionList

# def getThatData():
class Command(BaseCommand):
    # help='This is stupid'
    file = 'd:\8203-mods_EAs.xls'
#    users,sessions=createEventFromCAMPEPxls(file)

    if False:#True:
        o = Organization(name='Penn Ohio AAPM',
                         address='somewhere',
                         weblink='https://sites.google.com/site/pennohioaapm/home',
                         create_date=datetime.datetime.now(),#timezone.now(),
                         urlshort='POC_AAPM'
                         )
        o.save()
        E = o.events_set.create(name='Fall 2019 Symposium',
                                description='he 2019 Fall Symposium of the Penn-Ohio Chapter of the AAPM is open to medical physicists, dosimetrists, therapists, students, and residents. The program will cover novel technologies in Radiation Physics',
                                location='HILTON GARDEN INN\nCLEVELAND EAST MAYFIELD\n700 BETA DRIVE\nMAYFIELD VILLAGE, OH 44143\n440-646-1777',
                                create_date=datetime.datetime.now(),#timezone.now(),
                                urlshort='2019_FALL'
                                )

    createUsers=False#True
    if createUsers:
        # User = apps.get_model('accounts','CustomUser')#'CustomUser', 'User')
        print(users)
        baseusername='GenericUserName_'
        counter=1
        for user in users:
            thisusername=baseusername+str(counter)
            userforSave=CustomUser.objects.create(email=user['email'],
                           first_name=user['first_name'],
                           last_name=user['last_name'],
                           occupation='Physicist',
                           campep=True, mdcb=False,
                           username=thisusername,
                           )
            try:
                userforSave.save()
            except:
                print('error:',thisusername,'-',user['email'])
            counter+=1

    createSessions=False#True
    # o1 = Organization.objects.filter(name='Penn Ohio AAPM',
    #                  # address='somewhere',
    #                  # weblink='https://sites.google.com/site/pennohioaapm/home',
    #                  # create_date=datetime.datetime.now(),  # timezone.now(),
    #                  # urlshort='POC_AAPM'
    #                  )
    # o=o1[0]
    E1 = Events.objects.filter(name='Fall 2019 Symposium',)
    E=E1[0]
    # E = o.events_set.create(name='Fall 2019 Symposium',
    #                             description='he 2019 Fall Symposium of the Penn-Ohio Chapter of the AAPM is open to medical physicists, dosimetrists, therapists, students, and residents. The program will cover novel technologies in Radiation Physics',
    #                             location='HILTON GARDEN INN\nCLEVELAND EAST MAYFIELD\n700 BETA DRIVE\nMAYFIELD VILLAGE, OH 44143\n440-646-1777',
    #                             create_date=datetime.datetime.now(),#timezone.now(),
    #                             urlshort='2019_FALL'
    #                             )
    if createSessions:
        for session in sessions:
            presenter=CustomUser.objects.filter(email=session['presenterInfo']['email'])
            E.session_set.create(title=session['title'], short_description=session['title'], isSAM=False,
                               isCAMPEP=session['isCAMPEP'], isMDCB=True, start_datetime=session['start_datetime'],
                               end_datetime=session['end_datetime'], presenter=presenter[0],CAMPEPReferenceID=session['CAMPEPReferenceID'])

    #print(sessions)
    createSams=True
    if createSams:
        question_text='What is the correct statement about automation in Chart Check Process?'
        reference='Halabi, T. and H.M. Lu, Automating checks of plan check automation. J Appl Clin Med Phys, 2014. 15(4): p. 4889.\n\
Li, H.H., et al., Software tool for physics chart checks. Pract Radiat Oncol, 2014. 4(6): p. e217-25.\n\
Siochi, R.A., et al., Radiation therapy plan checks in a paperless clinic. J Appl Clin Med Phys, 2009. 10(1): p. 2905.'

        thissession=session.objects.filter(title='Using Automation to Improve Workflow in Radiotherapy')[0]
        print(thissession)
        thisquestion=thissession.samquestion_set.create(question_text=question_text,
                                                   reference=reference,
                                        session=thissession
                                                   )
        for answer_text in ['It will replace medical physicists in the process.',
                        'It will replace dosimetrists in the process.',
                        'It will improve reduce errors in chart parameters and improve efficiency.',
                        'It is not useful for the process.'
                       ]:
            thisquestion.samanswer_set.create(answer_text = answer_text)

        question_text='What percentage of error reported from the report of the Radiation Oncology Incident Learning System (RO-ILS) is from treatment planning and pre-treatment review and verification processes?'
        reference='Hoopes, D.J., et al., RO-ILS: Radiation Oncology Incident Learning System: A report from the first year of experience. Pract Radiat Oncol, 2015. 5(5): p. 312-318.'
        thisquestion = thissession.samquestion_set.create(question_text=question_text,
                                                          reference=reference
                                                          )
        for answer_text in ['30%',
                        '70%',
                        '10%',
                        '100%'
                       ]:
            thisquestion.samanswer_set.create(answer_text = answer_text)

        question_text='What is QMAP?'
        reference='Yu, N., et al., Data-driven management using quantitative metric and automatic auditing program (QMAP) improves consistency of radiation oncology processes. Pract Radiat Oncol, 2017. 7(3): p. e215-e222.'
        thisquestion = thissession.samquestion_set.create(question_text=question_text,
                                                          reference=reference
                                                          )
        for answer_text in ['It is a home grow program.',
                        'It is based on the standardized process.',
                        'It provides quantitative metric measures and automatic report of these measures.',
                        'All of above.'
                       ]:
            thisquestion.samanswer_set.create(answer_text = answer_text)

        question_text='Which statement below summaries common features of advanced planning tools of knowledge-based planning, multiple criteria optimization, and auto-planning?'
        reference='Krayenbuehl et. al. Evaluation of an automated knowledge based treatment planning system for head and neck, radiation oncology, 2015 10:226.\n\
Philips manual in Pinnacle treatment planning\n\
RayStation User’s Manual'

        thisquestion = thissession.samquestion_set.create(question_text=question_text,
                                                          reference=reference
                                                          )
        for answer_text in ['Only knowledge-based planning propagates knowledge from experts’ planning ',
                        'There is no common feature between the three methods.',
                        'Multiple criteria optimization can find the optimal solution.',
                        'Auto-planning is the same as the conventional IMRT planning.',
                        'These three methods can improve plan quality, consistency, and efficiency.'
                       ]:
            thisquestion.samanswer_set.create(answer_text = answer_text)

        question_text='What can the advanced planning tools achieve?'
        reference='Ouyang Z, Shen Z, Murray E, Kolar M, LaHurd D, Yu N, Joshil N, Koyfman S, Bzdusek K, Xia P: “Evaluation of Auto-planning in IMRT and VMAT for Head and Neck Cancer”, revision submitted to J. App. Clin. Med. Phys, 20(7):39-47 (2019).\n\
\n\
Lu L, Sheng Y, Donaghue J, Shen Z, Kolar M, Q. Wu J, Xia P: “Three IMRT Advanced Planning Tools: A Multi- institutional Side-by-side Comparison”,  App. Clin. Med. Phys, 20(8):65-77 (2019).'
        thisquestion = thissession.samquestion_set.create(question_text=question_text,
                                                          reference=reference
                                                          )
        for answer_text in ['Replace medical dosimetrists',
                        'Replace medical physicists',
                        'Not useful at all',
                        'Improve plan consistency, plan quality, and efficiency.'
                       ]:
            thisquestion.samanswer_set.create(answer_text = answer_text)
if False:
        question_text=''
        reference=''
        thisquestion = thissession.samquestion_set.create(question_text=question_text,
                                                          reference=reference
                                                          )
        for answer_text in ['',
                        '',
                        '',
                        ''
                       ]:
            thisquestion.samAnswer_set.create(answer_text = answer_text)
        question_text=''
        reference=''
        thisquestion = thissession.samquestion_set.create(question_text=question_text,
                                                          reference=reference
                                                          )
        for answer_text in ['',
                        '',
                        '',
                        ''
                       ]:
            thisquestion.samAnswer_set.create(answer_text = answer_text)
