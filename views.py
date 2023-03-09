import random,base64
from django.contrib import messages
import requests, matplotlib.pyplot as plt
from django.shortcuts import redirect,render

from django.core.exceptions import ObjectDoesNotExist

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password").encode("utf-8")

        url = "https://espnodewebsite.000webhostapp.com/API/loginapi.php"
        params = {
            "email": email,
            "password": password
        }
        r2 = requests.post(url=url, data=params)
        print(r2.text)

        res = r2.json()
        ev = res['error']
        if not ev:
            uloginid = res['user']['LOGIN_ID']
            role = res['user']['ROLE']
            ufname = res['user']['FIRST_NAME']
            ulname = res['user']['LAST_NAME']
            ugender = res['user']['GENDER']
            uaddress = res['user']['ADDRESS']
            uemail = res['user']['EMAIL_ID']
            uhex = res['user']['HEXCODE']
            uphone=res['user']['PHIONE_NO']

            # This will store information of guard.
            if role == "0":
                request.session['log_email'] = uemail
                request.session['log_role'] = role
                request.session['log_id'] = uloginid
                request.session['log_fname'] = ufname
                request.session['log_lname'] = ulname
                request.session['log_gender'] = ugender
                request.session['log_address'] = uaddress
                request.session['log_uhex'] = uhex
                request.session['log_phone'] = uphone
                request.session.save()
                return redirect(guard_dashboard)

            # This will store information of admin.
            else:
                request.session['log_user_email'] = uemail
                request.session['log_user_id'] = uloginid
                request.session['log_user_fname'] = ufname
                request.session['log_user_lname'] = ulname
                request.session['log_user_gender'] = ugender
                request.session['log_user_address'] = uaddress
                request.session['log_user_uhex'] = uhex
                request.session['log_user_phone'] = uphone
                request.session['log_user_role'] = role
                request.session.save()
                return redirect(admin_dashboard)

        # This will work when details entered is wrong.
        else:
            messages.error(request, "Invalid Email & Password !! ")
    # This will check if user is already logged in or not.
    try:
        if request.session["log_email"] is not None:
            return redirect(guard_dashboard)
    except:
        pass
    try:
        if request.session["log_user_email"] is not None:
            return redirect(admin_dashboard)
        else:
            return render(request, 'index.html')
    except:
        pass
    return render(request,'index.html')

def admin_dashboard(request):
    try:
        if request.session['log_user_email'] is None:
            return redirect(login)
        else:
            return render(request, 'dashboard.html')
    except:
        pass
    return render(request, 'index.html')
def guard_dashboard(request):
    return render(request, 'guard_dashboard.html')

def admin_profile(request):
    return render(request, 'profile.html')

def admin_attendance(request):
    return render(request, 'Attendance_Table.html')


def logout(request):
    try:
        del request.session['log_user_email']
        del request.session['log_user_id']
        del request.session['log_user_fname']
        del request.session['log_user_lname']
        del request.session['log_user_gender']
        del request.session['log_user_address']
        del request.session['log_user_uhex']
        del request.session['log_user_phone']
        del request.session['log_user_role']

        del request.session['log_email']
        del request.session['log_id']
        del request.session['log_fname']
        del request.session['log_lname']
        del request.session['log_gender']
        del request.session['log_address']
        del request.session['log_uhex']
        del request.session['log_phone']
        del request.session['log_role']
    except:
        pass
    return render(request,'logout.html')

def admin_crossing(request):
    try:
        if request.session['log_user_email'] is None:
            return redirect(login)
        else:
            url = "https://espnodewebsite.000webhostapp.com/API/fetchldrsensorapi.php"
            response = requests.get(url=url)
            r2 = response.json()
            records1={}
            records1['data'] = r2
            ldrvalue={}
            ldrgraphdata=[]
            ldrgraphtime=[]
            ldrvalue['ldr_val']= r2['ldr']
            for i in ldrvalue['ldr_val']:
                ldrgraphdata.append(i['LDR_VALUE'])
                ldrgraphtime.append(i['READING_TIME'][11:16])

            print(ldrgraphdata)
            print(ldrgraphtime)
            ev = r2['error']
            plt.barh(ldrgraphtime[::5], ldrgraphdata[::5])
            plt.savefig('hackathon/static/src/images/ldr/ldr_crossing.jpg')
            return render(request,'Level_crossing.html', records1)
    except:
        pass
    return render(request, "index.html")

def admin_obstacle(request):
    try:
        if request.session["log_user_email"] is None:
            return render(request,'index.html')
        else:
            url = "https://espnodewebsite.000webhostapp.com/API/fetchirsensordata.php"
            response = requests.get(url=url)
            ir_res = response.json()
            records = {}
            records['data'] = ir_res

            return render(request,'Obstacle detection.html',records)
    except:
        pass
    return render(request,'index.html')

def admin_human(request):
    try:
        if request.session["log_user_email"] is None:
            return render(request,'index.html')
        else:
            url = "https://espnodewebsite.000webhostapp.com/API/fetchpirsensordata.php"
            response = requests.get(url=url)
            pir_res = response.json()
            records = {}
            records['data'] = pir_res
            pirvalue={}
            pirgraph=[]
            pirtime=[]
            pirvalue['pir_val'] = records['data']['pir']
            for i in pirvalue['pir_val']:
                pirgraph.append(i['PIR_VALUE'])
                pirtime.append(i['READING_TIME'][11:16])
            print(pirgraph)
            print(pirtime)
            plt.barh(pirtime[::5], pirgraph[::5])
            plt.savefig('hackathon/static/src/images/pir/pir_human.jpg')
            return render(request,'Human Detection.html',records)
    except:
        pass
    return render(request,'index.html')

def admin_distance(request):
    try:
        if request.session['log_user_email'] is None:
            return redirect(login)
        else:
            url = "https://espnodewebsite.000webhostapp.com/API/fetchultrasonic.php"
            response = requests.get(url=url)
            ultra_res = response.json()
            records = {}
            records['data'] = ultra_res
            return render(request, 'Distance Calculator.html',records)
    except:
        pass
    return render(request, 'index.html')