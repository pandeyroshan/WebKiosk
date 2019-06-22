from django.shortcuts import render
from . import views
import requests
from bs4 import BeautifulSoup
import collections

# Create your views here.

session = requests.Session()

def index(request):
    return render(request,'kiosk/index.html')

def fetch(request):
    global session
    MemberCode=request.POST.get("MemberCode")
    Password=request.POST.get("Password")
    url = 'https://webkiosk.juet.ac.in/CommonFiles/UserAction.jsp'
    context = {
        'InstCode' : 'JUET',
        'UserType' : 'S',
        'MemberCode' : str(MemberCode),  # These things needs to be replaced by the User's credentials at runtime :-)
        'Password' : str(Password)   
    }
    login_response = session.post(url,context)
    targetURL = 'https://webkiosk.juet.ac.in/CommonFiles/TopTitle.jsp'
    response = session.get(targetURL)
    clean_data = BeautifulSoup(response.text, 'html.parser')
    for link in clean_data.findAll("body"):
            x=str(link.text)
            raw_data=(x.split('\n'))
    name = raw_data[4][7:].title()
    return render(request,'kiosk/home.html',{'name': name})

def cgpa(request):
    global session
    cgpa = session.get("https://webkiosk.juet.ac.in/StudentFiles/Exam/StudCGPAReport.jsp")
    html_form = cgpa.text
    clean_data = BeautifulSoup(html_form,'html.parser')
    lst=[]
    for tab in clean_data.findAll("table",{"align" : "center","id":"table-1"}):
        for link in tab.findAll("td"):
            h=str(link.text)
            d=(h.split('\n'))
            for i in d:
                lst.append(i)
    lst = lst[8:]
    dict_data = { }
    semester = 1
    sgpa = 6
    for i in range(0,int(len(lst)/8)):
        dict_data.update({str(semester): str(lst[sgpa])})
        sgpa+=8
        semester+=1
    targetURL = 'https://webkiosk.juet.ac.in/CommonFiles/TopTitle.jsp'
    response = session.get(targetURL)
    clean_data = BeautifulSoup(response.text, 'html.parser')
    try:
        for link in clean_data.findAll("body"):
                x=str(link.text)
                raw_data=(x.split('\n'))
        name = raw_data[4][7:].title()
        dict_data.update({'CGPA':str(lst[-1])})
    except:
        return render(request,'kiosk/index.html')
    return render(request,'kiosk/cgpa.html',{'data': sorted(dict_data.items()),'name':name})


def attendance(request):
    global session
    attendence = session.get("https://webkiosk.juet.ac.in/StudentFiles/Academic/StudentAttendanceList.jsp")
    html_form = attendence.text
    clean_data  = BeautifulSoup(html_form, 'html.parser')
    lst=[]
    for link in clean_data.findAll("tbody"):
            x=str(link.text)
            raw_data=(x.split('\n'))
    # this raw_data has \xa0 and some null enteries, I need to fuck that issue first :)
    refined_data = []
    try:
        for data in raw_data:
            if not (str(data) == '\xa0' or str(data)==''):
                refined_data.append(data)
    except:
        return render(request,'kiosk/index.html')
    dict_data = { }
    for i in range(0,len(refined_data)):
        if len(refined_data[i])>3:
            dict_data[refined_data[i]] = refined_data[i+1]
    return render(request,'kiosk/attendance.html',{'data': dict_data})

def personalData(request):
    global session
    personal_data = session.get("https://webkiosk.juet.ac.in/StudentFiles/PersonalFiles/StudPersonalInfo.jsp")
    html_format = personal_data.text
    clean_data = BeautifulSoup(html_format,'html.parser')
    per_info=[]
    for link in clean_data.findAll("tr"):
        for y in link.findAll("td"):
            for x in y.findAll("font",{"color" : "black"}):
                if x not in y.findAll("font",{"face" : "Arial"}):
                    d=str(x.text)
                    per_info.append(d.strip())
    lst = []
    try:
        lst.append({'Name': per_info[0]})
        lst.append({'Enrollment Number': per_info[2]})
        lst.append({'Father\'s Name' : per_info[3]})
        lst.append({'Course': per_info[4]})
        lst.append({'Semester': per_info[5]})
        lst.append({'Aadhar Number': per_info[6]})
        lst.append({'Phone Number': per_info[7]})
        lst.append({'Parents Number': per_info[8]})
        lst.append({'Email Address': per_info[0]})
        lst.append({'City': per_info[-3]})
        lst.append({'state': per_info[-1]})
    except:
        return render(request,'kiosk/index.html')
    return render(request,'kiosk/about.html',{'data' : lst})


def logout(request):
    global session
    session.delete('https://webkiosk.juet.ac.in/CommonFiles/UserAction.jsp')
    return render(request,'kiosk/index.html')
