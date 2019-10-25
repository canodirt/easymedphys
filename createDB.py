from cme.models import Organization,Events,event

from django.utils import timezone

from datetime import datetime

from accounts.models import CustomUser


def makeCustomUser(email='', first_name='',last_name='',occupation='Other', campep = False, mdcb = False, username=''):
    return CustomUser(email=email,first_name=first_name,last_name=last_name,
                      occupation=occupation, campep = campep, mdcb=mdcb,
                      username=username)

def createEventFromCAMPEPxls(xlsfile):
    import xlrd
    book = xlrd.open_workbook(xlsfile)

    # get the first worksheet
    sheet = book.sheet_by_name('EATemplate')

    dictLocations={0:'CAMPEPReferenceID',
                   1:'title',
                   2:'start_date',
                   3:'start_time',
                   5:'CAMPEP Credits Number',
                   6:'duration',
                   7:'email',
                   8:'last_name',
                   9:'first_name',
                   10:'CAMPEP Category',
                   11:'CAMPEP Subcategory'
                   }
    row = 18 #first row of real data
    while row < sheet.nrows:
        thisline=''
        for col in dictLocations.keys():
            thisline+=dictLocations[col]+':'+sheet.cell(row,col).Value+';\t'
        print(thisline)
        row+=1
    # first_sheet.cell(0, 0)


file = 'd:\8203-mods_EA.xls'
createEventFromCAMPEPxls(file)

error
o = Organization(name='Penn Ohio AAPM',
                 address = 'somewhere',
                 weblink = 'https://sites.google.com/site/pennohioaapm/home',
                 create_date = timezone.now(),
                 urlshort = 'POC_AAPM'
                 )
o.save()
E = o.events_set.create(name='Fall 2019 Symposium',
                        description='he 2019 Fall Symposium of the Penn-Ohio Chapter of the AAPM is open to medical physicists, dosimetrists, therapists, students, and residents. The program will cover novel technologies in Radiation Physics',
                        location='HILTON GARDEN INN\nCLEVELAND EAST MAYFIELD\n700 BETA DRIVE\nMAYFIELD VILLAGE, OH 44143\n440-646-1777',
                        create_date= timezone.now(),
                        urlshort = '2019_FALL'
                        )

E.event_set.create(title='StakeHolder',short_description='Various talks on good things', isSAM=False, isCAMPEP=True, isMDCB=True, start_datetime=datetime(2019,10,25,15,30),end_datetime=datetime(2019,10,25,16,00), presenter='Alf')
E.event_set.create(title='AI in rad',short_description='Various talks on good things', isSAM=False, isCAMPEP=True, isMDCB=True, start_datetime=datetime(2019,10,25,16,00),end_datetime=datetime(2019,10,25,16,30), presenter='KeShen')
