
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
    row = 18 #first row of real data
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
                     'start_datetime': sessionDict['start_date'] + datetime.timedelta(minutes=sessionDict['duration']),
                     'presenterInfo':thisUser,
                     'isCAMPEP':True,
                     'CAMPEPReferenceID':sessionDict['CAMPEPReferenceID']

                     }
        returnSessionList.append(thissession)

    return returnUserList,returnSessionList

# def getThatData():
file = 'd:\8203-mods_EAs.xls'
users,sessions=createEventFromCAMPEPxls(file)
print(users)
print(sessions)
