from django.shortcuts import render, redirect

from .models import Magazines, Staff, Department


# Create your views here
# .

def is_login(request):
    return request.session.get('islogin', False)


def user_name(request):
    return request.session.get('username')


def user_pricecount(request):
    return request.session.get('pricecount')


def user_id(request):
    return request.session.get('userid', -1)


def IndexView(request):
    # magazine_list = Magazines.objects.all()
    islogin = is_login(request)
    username = user_name(request)
    context = {
        # 'magazine_list': magazine_list,
        'islogin': islogin,
        'username': username
    }

    return render(request, 'booking/index.html', context)


'''
报刊信息
'''


def DetailView(request):
    magazine_list = Magazines.objects.all()
    islogin = is_login(request)
    username = user_name(request)
    context = {
        'magazine_list': magazine_list,
        'username': username,
        'islogin': islogin
    }
    return render(request, 'booking/detail.html', context)


'''
登录操作
'''


def Login(request):
    username = ''
    password = ''
    try:
        username = request.POST['username']
        password = request.POST['password']
        is_post = True

    except KeyError:
        is_post = False

    if is_post:
        _state = do_login(request, username, password)

        if _state['success']:
            return redirect('booking:index')

    else:
        _state = {
            'success': False,
            'message': ""
        }

    _result = {
        'success': _state['success'],
        'message': _state['message']
    }

    return render(request, 'booking/login.html', _result)


def do_login(request, username, password):
    _state = check_login(username, password)

    if _state['success']:
        request.session['islogin'] = True,
        request.session['userid'] = _state['userid']
        request.session['username'] = username
        request.session['pricecount'] = 0
    return _state


def check_login(username, password):
    _state = {
        'success': True,
        'message': 'none',
        'userid': -1,
    }

    try:
        user = Staff.objects.get(staff_name=username)

        if password == user.password:
            _state['success'] = True
            _state['userid'] = user.id

        else:
            _state['success'] = False
            _state['message'] = '密码错误.'

    except Staff.DoesNotExist:
        _state['success'] = False
        _state['message'] = "不存在此账户"

    return _state


def Logout(request):
    request.session['islogin'] = False
    request.session['userid'] = -1
    request.session['username'] = ''
    return redirect('booking:index')


"""
注册操作
"""


def Register(request):
    islogin = is_login(request)

    if islogin:
        return redirect('booking:index')

    userinfo = {
        'staff_name': '',
        'password': '',
        'comfirm': '',
        'mobile': '',
        'department': '',
        'staff_number': '',
    }

    try:
        userinfo = {
            'staff_name': request.POST['staff_name'],
            'password': request.POST['password'],
            'comfirm': request.POST['comfirm'],
            'mobile': request.POST['mobile'],
            'department': request.POST['department'],
            'staff_number': request.POST['staff_number'],
        }

        _is_post = True

    except KeyError:
        _is_post = False

    if _is_post:
        _state = do_register(request, userinfo)

    else:
        _state = {
            'success': False,
            'message': '',
        }

    if _state['success']:
        return redirect('booking:index')

    _result = {
        'success': _state['success'],
        'message': _state['message'],
        'form': {
            'staff_name': userinfo['staff_name'],
        }
    }

    return render(request, 'booking/register.html', _result)


def do_register(request, userinfo):
    _state = {
        'success': False,
        'message': '',
    }

    if userinfo['staff_name'] == '':
        _state['success'] = False
        _state['message'] = '没有输入用户名.'
        return _state

    if userinfo['password'] == '':
        _state['success'] = False
        _state['message'] = '没有输入密码.'
        return _state

    if userinfo['department'] == '':
        _state['success'] = False
        _state['message'] = '没有输入所在部门.'
        return _state

    if userinfo['staff_number'] == '':
        _state['success'] = False
        _state['message'] = '没有输入员工号.'
        return _state

    if userinfo['mobile'] == '':
        _state['success'] = False
        _state['message'] = '没有输入电话号码.'
        return _state

    if userinfo['password'] != userinfo['comfirm']:
        _state['success'] = False
        _state['message'] = '两次密码不匹配'
        return _state

    staff = Staff(
        staff_name=userinfo['staff_name'],
        password=userinfo['password'],
        staff_number=userinfo['staff_number'],
        mobile=userinfo['mobile'],
        department=Department.objects.get(depart_name=userinfo['department'])
    )

    staff.save()
    return _state


'''
订阅操作

'''


def Booking(request):
    islogin = is_login(request)
    pricecount = user_pricecount(request)

    if not islogin:
        return redirect('booking:login')

    userid = user_id(request)
    try:
        user = Staff.objects.get(id=userid)
        username = user_name(request)

    except:
        return redirect('booking:login')

    try:
        magid = request.POST['mag']
        magzine = Magazines.objects.get(id=magid)
        print(magid)

    except KeyError:
        return redirect('booking:detail')

    else:
        if check_boking(username, magzine):
            magzine.staff.add(user)
            pricecount += magzine.price
            request.session['pricecount'] = pricecount
            return resultView(request,
                              ('你已成功预定%s,价格为%s., 此次登录预定一共花%s元钱.') % (magzine.mag_name, magzine.price, pricecount))
        else:
            return resultView(request, '对不起,你已经预订了此报刊,不能再次预订')


# 检查有没有预定
def check_boking(username, magzine):
    _exit = True
    try:
        magzine.staff.get(staff_name=username)
        _exit = False
    except:
        _exit = True
    return _exit


def resultView(request, message=''):
    islogin = is_login(request)
    username = user_name(request)

    context = {
        'islogin': islogin,
        'message': message,
        'username': username
    }

    return render(request, 'booking/result.html', context)


'''
信息统计显示部分
'''


def DstatisView(request):
    islogin = is_login(request)

    if not islogin:
        return redirect('booking:login')
    username = user_name(request)

    d_list = Department.objects.all()

    context = {
        'd_list': d_list,
        'islogin': islogin,
        'username': username
    }

    return render(request, 'booking/statisdetail.html', context)


def MstatisView(request):
    islogin = is_login(request)

    username = user_name(request)

    mag_list = Magazines.objects.all()

    context = {
        'mag_list': mag_list,
        'islogin': islogin,
        'username': username
    }

    return render(request, 'booking/statisdetail.html', context)


def PstatisView(request):
    islogin = is_login(request)

    if not islogin:
        return redirect('booking:login')

    username = user_name(request)

    person = Staff.objects.get(staff_name=username)

    context = {
        'person': person,
        'islogin': islogin,
        'username': username
    }

    return render(request, 'booking/statisdetail.html', context)
