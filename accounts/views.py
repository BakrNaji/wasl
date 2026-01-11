from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from The_Owner.models import Owner
from The_Investor.models import Investor
import re


# Create your views here.

########## تسجيل الدخول #################

def login(request):
    if request.method == 'POST' and 'btnlogin' in request.POST:
        
        username = request.POST['user']
        password = request.POST['pass']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)
            #messages.success(request, 'لقد قمت بتسجيل الدخول')
        else:
            messages.error(request, 'هناك خطأ في اسم المستخدم او كلمة المرور') 

        return redirect('login')
    else:   
        return render(request, 'accounts/login.html')

##########تسجيل خروج#################

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')

##########انشاء حساب #################

def signup(request):
    if request.method == 'POST' and 'btncreate' in request.POST:
        
        #varibles for fields
        fname = None
        lname = None
        username = None
        email = None
        phone = None
        password = None
        address = None
        usertype = None
        terms = None
        is_added = None
        
        #get values from the form

        if 'fname' in request.POST: fname = request.POST['fname']
        else: messages.error(request, 'Error in first name')

        if 'lname' in request.POST: lname = request.POST['lname']
        else: messages.error(request, 'Error in last name')

        if 'usern' in request.POST: username = request.POST['usern']
        else: messages.error(request, 'Error in username')

        if 'email' in request.POST: email = request.POST['email']
        else: messages.error(request, 'Error in email')

        if 'phone' in request.POST: phone = request.POST['phone']
        else: messages.error(request, 'Error in phone')

        if 'pass' in request.POST: password = request.POST['pass']
        else: messages.error(request, 'Error in password')

        if 'address' in request.POST: address = request.POST['address']
        else: messages.error(request, 'Error in address')

        if 'terms' in request.POST: terms = request.POST['terms']

        if 'usertype' in request.POST: usertype = request.POST['usertype']


        #check values
        if fname and lname and username and email and phone and password and address and usertype:
            if terms == 'on':
                #check username is token
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'هذا المستخدم موجود بالفعل')
                else:
                    #check if email is token
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'هذا الايميل موجود بالفعل')
                    else:
                        patt = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                        if re.match(patt, email):
                            #add user
                            user = User.objects.create_user(first_name=fname , last_name=lname , email=email , username=username , password=password)
                            user.save()
                            
                            #add user profile                              
                            if usertype == 'own':
                                userowner = Owner(user=user, address=address , phone=phone)
                                userowner.save()
                                #success messages
                                messages.success(request, 'تم انشاء حساب مالك مشروع')
                                return redirect('signup')                            
                                is_added = True

                            elif usertype == 'inv':
                                userinv = Investor(user=user, address=address , phone=phone)
                                userinv.save()
                                #success messages
                                messages.success(request, 'تم انشاء حساب مستثمر')
                                return redirect('signup')
                                is_added = True
                                                                                    

                            #clear fields
                            fname = ''
                            lname = ''
                            username = ''
                            email = ''
                            phone = ''
                            password = ''
                            address = ''
                            usertype = None
                            terms = None

                        else:
                            messages.error(request, 'البريد غير صحيح')
            else:
                messages.error(request, 'يجب الموافقة على شروط الخصوصية')
        else:
            messages.error(request, 'تحقق من الحقول الفارغة')

        return render(request, 'accounts/signup.html',{
            'fname':fname,
            'lname':lname,
            'usern':username,
            'email':email,
            'phone':phone,
            'pass':password,
            'address':address,
            'is_added':is_added
        })
    else:
        return render(request, 'accounts/signup.html')


##########تعديل البروفايل#################

# def profile(request):
#     if request.method == 'POST' and 'btnsave' in request.POST:

#         if request.user is not None and request.user.id != None:
#             userowner = Owner.objects.get(user=request.user)

#             if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['email'] and request.POST['user'] and request.POST['pass']:
#                 request.user.first_name = request.POST['fname']
#                 request.user.last_name = request.POST['lname']
#                 userowner.address = request.POST['address']
#                 #request.user.email = request.POST['email']
#                 #request.user.username = request.POST['user']
#                 if not request.POST['pass'].startswith('pbkdf2_sha256$'):
#                     request.user.set_password(request.POST['pass'])
#                 request.user.save()
#                 userowner.save()
#                 auth.login(request, request.user)
#                 messages.success(request, 'تم حفظ التعديلات')
#             else:
#                 messages.error(request, 'check values')


#         return redirect('profile')
#     else:
#         # if request.user.is_anonymous:
#         #     return redirect('index')
#         if request.user is not None:

#             context = None
#             if not request.user.is_anonymous:

#                 userowner = Owner.objects.get(user=request.user)

#                 context = {
#                     'fname':request.user.first_name,
#                     'lname':request.user.last_name,
#                     'address':userowner.address,
#                     'email':request.user.email,
#                     'user':request.user.username,
#                     'pass':request.user.password
#                 }
#             return render(request, 'accounts/profile.html', context)
#         else:
#             return redirect('profile')
                



##################### يعدل بيانات الاثنين######################




def profile(request):
    if request.method == 'POST' and 'btnsave' in request.POST:
        if request.user is not None and request.user.id is not None:
            user_owner = Owner.objects.filter(user=request.user).first()
            user_investor = Investor.objects.filter(user=request.user).first()

            if (
                request.POST['fname']
                and request.POST['lname']
                and request.POST['address']
                and request.POST['email']
                and request.POST['user']                
            ):
                request.user.first_name = request.POST['fname']
                request.user.last_name = request.POST['lname']

                if user_owner:
                    user_owner.address = request.POST['address']
                elif user_investor:
                    user_investor.address = request.POST['address']
                    # allow investor to set branch/department/job_title
                    # branch/department are ForeignKeys now
                    from The_Investor.models import Branch, Department
                    branch_val = request.POST.get('branch')
                    dept_val = request.POST.get('department')
                    try:
                        user_investor.branch = Branch.objects.get(pk=branch_val) if branch_val else user_investor.branch
                    except Exception:
                        # fallback: try by name
                        try:
                            user_investor.branch = Branch.objects.get(name=branch_val)
                        except Exception:
                            pass
                    try:
                        user_investor.department = Department.objects.get(pk=dept_val) if dept_val else user_investor.department
                    except Exception:
                        try:
                            user_investor.department = Department.objects.get(name=dept_val)
                        except Exception:
                            pass
                    user_investor.job_title = request.POST.get('job_title', user_investor.job_title)

                request.user.email = request.POST['email']
                request.user.username = request.POST['user']



                request.user.save()

                if user_owner:
                    user_owner.save()
                elif user_investor:
                    user_investor.save()

                auth.login(request, request.user)
                messages.success(request, 'تم حفظ التعديلات')
            else:
                messages.error(request, 'تحقق من القيم')

        return redirect('profile')
    else:
        if request.user is not None:
            context = None
            if not request.user.is_anonymous:
                user_owner = Owner.objects.filter(user=request.user).first()
                user_investor = Investor.objects.filter(user=request.user).first()

                # Get evaluations created by this owner (if owner)
                owner_evaluations = []
                if user_owner:
                    from The_Investor.models import Evaluation
                    owner_evaluations = Evaluation.objects.filter(evaluator=user_owner).select_related('investor__user').prefetch_related('scores')

                context = {
                    'fname': request.user.first_name,
                    'lname': request.user.last_name,
                    'address': user_owner.address if user_owner else (user_investor.address if user_investor else ''),
                    'email': request.user.email,
                    'user': request.user.username,
                    'evaluations': user_investor.evaluations_received.all() if user_investor else [],
                    'average_evaluation': (sum([float(e.overall_score) for e in user_investor.evaluations_received.all()]) / user_investor.evaluations_received.count()) if user_investor and user_investor.evaluations_received.exists() else None,
                    'branch': user_investor.branch if user_investor else '',
                    'department': user_investor.department if user_investor else '',
                    'job_title': user_investor.job_title if user_investor else '',
                    'photo_url': (user_owner.photo.url if user_owner and getattr(user_owner, 'photo', None) else (user_investor.photo.url if user_investor and getattr(user_investor, 'photo', None) else '')),
                    'owner_evaluations': owner_evaluations,
                    'is_owner': bool(user_owner),
                }

            return render(request, 'accounts/profile.html', context)
        else:
            return redirect('profile')


def owner_method(request):
    return render(request, 'accounts/owner_method.html')


def inv_method(request):
    return render(request, 'accounts/inv_method.html')