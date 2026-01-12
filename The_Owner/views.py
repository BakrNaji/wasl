from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from The_Investor.models import Investor, Evaluation, Branch, Department
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .forms import EvaluationForm
from The_Investor.models import EvaluationCriterion, EvaluationScore, EvaluationImage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from The_Investor.models import Department


def index(request):
	return render(request, 'pages/index.html')


def about(request):
	return render(request, 'pages/about.html')


@login_required
def evaluate_investor(request, investor_id):
	# only owners should be able to evaluate
	owner = getattr(request.user, 'owner', None)
	if not owner:
		messages.error(request, 'فقط مالك المشروع يمكنه إجراء التقييمات.')
		return redirect('index')

	investor = get_object_or_404(Investor, id=investor_id)

	if request.method == 'POST':
		form = EvaluationForm(request.POST, request.FILES)
		if form.is_valid():
			# check for recent existing evaluation by same evaluator for this investor
			window_days = getattr(settings, 'EVAL_WINDOW_DAYS', 30)
			recent_from = timezone.now() - timedelta(days=window_days)
			existing = Evaluation.objects.filter(evaluator=owner, investor=investor, created_at__gte=recent_from).first()
			if existing:
				# update existing evaluation: overwrite department/branch/comment and scores, add images
				ev = existing
				branch_obj = form.cleaned_data.get('branch')
				dept_obj = form.cleaned_data.get('department')
				ev.department = dept_obj.name if dept_obj else ev.department
				ev.branch = branch_obj.name if branch_obj else ev.branch
				ev.comment = form.cleaned_data.get('comment', ev.comment)
				ev.status = 'pending'
				ev.approved_by = None
				ev.approved_at = None
				ev.save()
				# update/create criterion scores
				for name, field in form.fields.items():
					if name.startswith('criterion_'):
						score = form.cleaned_data.get(name)
						crit = getattr(field, 'criterion', None)
						if crit is not None and score is not None:
							sobj, created = EvaluationScore.objects.get_or_create(evaluation=ev, criterion=crit, defaults={'score': score})
							if not created:
								sobj.score = score
								sobj.save()
				# add any uploaded images
				files = request.FILES.getlist('images')
				for f in files:
					EvaluationImage.objects.create(evaluation=ev, image=f)
				messages.success(request, 'تم تحديث التقييم السابق وإرساله للمراجعة.')
			else:
				# create new evaluation
				ev = form.save(commit=False)
				ev.evaluator = owner
				ev.investor = investor
				ev.save()

				# save criterion scores
				for name, field in form.fields.items():
					if name.startswith('criterion_'):
						score = form.cleaned_data.get(name)
						crit = getattr(field, 'criterion', None)
						if crit is not None and score is not None:
							EvaluationScore.objects.create(evaluation=ev, criterion=crit, score=score)

				# save images
				files = request.FILES.getlist('images')
				for f in files:
					EvaluationImage.objects.create(evaluation=ev, image=f)

				messages.success(request, 'تم إضافة التقييم بنجاح.')
			return redirect('profile')
	else:
		form = EvaluationForm()

	# get previous evaluations and stats for this investor
	all_evaluations = Evaluation.objects.filter(investor=investor).select_related('evaluator').prefetch_related('scores')
	
	# calculate overall rating (average of all approved evaluations)
	overall_rating = 0
	eval_count = 0
	if all_evaluations.exists():
		approved = all_evaluations.filter(status='approved')
		if approved.exists():
			ratings = [e.compute_overall() for e in approved if e.compute_overall() is not None]
			if ratings:
				overall_rating = sum(ratings) / len(ratings)
				eval_count = len(ratings)

	context = {
		'form': form, 
		'investor': investor,
		'overall_rating': round(overall_rating, 1) if overall_rating else 0,
		'eval_count': eval_count,
		'recent_evaluations': all_evaluations.filter(status='approved')[:3]
	}
	return render(request, 'pages/evaluate_investor.html', context)


@login_required
def investor_list(request):
	owner = getattr(request.user, 'owner', None)
	if not owner:
		messages.error(request, 'فقط مالك المشروع يمكنه الوصول لهذه الصفحة.')
		return redirect('index')

	qs = Investor.objects.all()
	branch = request.GET.get('branch')
	department = request.GET.get('department')
	q = request.GET.get('q')
	selected_investor_id = request.GET.get('investor_id')
	if selected_investor_id:
		return redirect('evaluate_investor', investor_id=selected_investor_id)
	if branch:
		# branch will be passed as id from the select
		try:
			bid = int(branch)
			qs = qs.filter(branch__id=bid)
		except Exception:
			qs = qs.filter(branch__name__icontains=branch)
	if department:
		try:
			did = int(department)
			qs = qs.filter(department__id=did)
		except Exception:
			qs = qs.filter(department__name__icontains=department)
	if q:
		qs = qs.filter(user__username__icontains=q)

	# populate selects from admin-managed Branch and Department tables
	branches = Branch.objects.all()
	# departments will be dynamically loaded for a branch via AJAX
	departments = Department.objects.none()
	all_investors = Investor.objects.all()
	return render(request, 'pages/investor_list.html', {'investors': qs, 'branches': branches, 'departments': departments, 'all_investors': all_investors})


@login_required
def ajax_departments(request, branch_id):
	# return JSON list of departments for the given branch id
	qs = Department.objects.filter(branch_id=branch_id).values('id', 'name')
	return JsonResponse(list(qs), safe=False)


@login_required
def ajax_investors(request):
	branch_id = request.GET.get('branch_id')
	dept_id = request.GET.get('department_id')
	qs = Investor.objects.all()
	if branch_id:
		try:
			qs = qs.filter(branch__id=int(branch_id))
		except Exception:
			pass
	if dept_id:
		try:
			qs = qs.filter(department__id=int(dept_id))
		except Exception:
			pass
	data = []
	for inv in qs:
		data.append({'id': inv.id, 'username': inv.user.username, 'department': (inv.department.name if inv.department else ''), 'branch': (inv.branch.name if inv.branch else '')})
	return JsonResponse(data, safe=False)


# Create your views here.
# def index(request):
#     return render (request , 'pages/index.html')

# def about(request):
#     return render (request , 'pages/about.html')


# ==================== نظام التقييم الجديد ====================

from .models import (EvaluationCriterion, DepartmentEvaluation, EvaluationObservation, 
                     ObservationImage, EmployeeEvaluation, EmployeeObservation, EmployeeObservationImage)
from django.db.models import Avg, Sum, Count, Q
from datetime import date


@login_required
def evaluate_department(request):
    """صفحة تقييم قسم"""
    owner = getattr(request.user, 'owner', None)
    if not owner:
        messages.error(request, 'فقط مالك المشروع يمكنه التقييم.')
        return redirect('index')
    
    branches = Branch.objects.all()
    criteria = EvaluationCriterion.objects.filter(is_active=True, criterion_type='department').order_by('order')
    
    if request.method == 'POST':
        department_id = request.POST.get('department')
        month = request.POST.get('month')
        notes = request.POST.get('notes', '')
        
        if department_id and month:
            department = get_object_or_404(Department, id=department_id)
            # تحويل '2026-01' إلى '2026-01-01'
            month_date = date.fromisoformat(month + '-01')
            
            # إنشاء أو تحديث التقييم
            evaluation, created = DepartmentEvaluation.objects.get_or_create(
                department=department,
                month=month_date,
                defaults={'evaluator': owner, 'notes': notes}
            )
            
            if not created:
                evaluation.notes = notes
                evaluation.evaluator = owner
                # حذف الملاحظات القديمة لتحديثها
                evaluation.details.all().delete()
            
            # معالجة المعايير المفعّلة فقط (التي تم إرسال بياناتها)
            for criterion in criteria:
                obs_count_key = f'obs_count_{criterion.id}'
                # تحقق إذا كان المعيار مفعّل (البيانات موجودة وليست disabled)
                if obs_count_key in request.POST:
                    obs_count = request.POST.get(obs_count_key, 0)
                    obs_desc = request.POST.get(f'obs_desc_{criterion.id}', '')
                    
                    # إنشاء الملاحظة فقط للمعايير المفعّلة
                    try:
                        obs_count = int(obs_count)
                        if obs_count >= 0:  # تأكد أن العدد صحيح
                            observation = EvaluationObservation.objects.create(
                                evaluation=evaluation,
                                criterion=criterion,
                                observations_count=obs_count,
                                description=obs_desc
                            )
                            
                            # إضافة الصور المتعددة
                            images = request.FILES.getlist(f'images_{criterion.id}')
                            for img in images:
                                ObservationImage.objects.create(observation=observation, image=img)
                    except (ValueError, TypeError):
                        continue
            
            evaluation.save()  # لإعادة حساب الإحصائيات
            messages.success(request, f'✅ تم حفظ تقييم {department.name} بنجاح!')
            return redirect('evaluation_reports')
    
    context = {
        'branches': branches,
        'criteria': criteria,
        'current_month': date.today().strftime('%Y-%m')
    }
    return render(request, 'pages/evaluate_department.html', context)


@login_required
def evaluate_employee(request):
    """صفحة تقييم موظف"""
    owner = getattr(request.user, 'owner', None)
    if not owner:
        messages.error(request, 'فقط مالك المشروع يمكنه التقييم.')
        return redirect('index')
    
    employees = Investor.objects.select_related('user', 'department', 'branch').all()
    criteria = EvaluationCriterion.objects.filter(is_active=True, criterion_type='employee').order_by('order')
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        month = request.POST.get('month')
        notes = request.POST.get('notes', '')
        
        if employee_id and month:
            employee = get_object_or_404(Investor, id=employee_id)
            # تحويل '2026-01' إلى '2026-01-01'
            month_date = date.fromisoformat(month + '-01')
            
            evaluation, created = EmployeeEvaluation.objects.get_or_create(
                employee=employee,
                month=month_date,
                defaults={'evaluator': owner, 'notes': notes}
            )
            
            if not created:
                evaluation.notes = notes
                evaluation.evaluator = owner
                # حذف الملاحظات القديمة لتحديثها
                evaluation.employee_observations.all().delete()
            
            # معالجة المعايير المفعّلة فقط (التي تم إرسال بياناتها)
            for criterion in criteria:
                obs_count_key = f'obs_count_{criterion.id}'
                # تحقق إذا كان المعيار مفعّل (البيانات موجودة وليست disabled)
                if obs_count_key in request.POST:
                    obs_count = request.POST.get(obs_count_key, 0)
                    obs_desc = request.POST.get(f'obs_desc_{criterion.id}', '')
                    
                    # إنشاء الملاحظة فقط للمعايير المفعّلة
                    try:
                        obs_count = int(obs_count)
                        if obs_count >= 0:  # تأكد أن العدد صحيح
                            observation = EmployeeObservation.objects.create(
                                evaluation=evaluation,
                                criterion=criterion,
                                observations_count=obs_count,
                                description=obs_desc
                            )
                            
                            # إضافة الصور
                            images = request.FILES.getlist(f'images_{criterion.id}')
                            for img in images:
                                EmployeeObservationImage.objects.create(observation=observation, image=img)
                    except (ValueError, TypeError):
                        continue
            
            evaluation.save()  # لإعادة حساب الإحصائيات
            messages.success(request, f'✅ تم حفظ تقييم {employee.user.username} بنجاح!')
            return redirect('evaluation_reports')
    
    context = {
        'employees': employees,
        'criteria': criteria,
        'current_month': date.today().strftime('%Y-%m')
    }
    return render(request, 'pages/evaluate_employee.html', context)


@login_required
def evaluation_reports(request):
    """صفحة تقارير التقييم"""
    owner = getattr(request.user, 'owner', None)
    if not owner:
        messages.error(request, 'فقط مالك المشروع يمكنه الوصول.')
        return redirect('index')
    
    # تقييمات الأقسام
    dept_evaluations = DepartmentEvaluation.objects.select_related('department', 'department__branch').order_by('-month', 'department')[:20]
    
    # تقييمات الموظفين
    emp_evaluations = EmployeeEvaluation.objects.select_related('employee__user', 'employee__department').order_by('-month', 'employee')[:20]
    
    # إحصائيات الأقسام حسب الفرع
    branch_stats = []
    branches = Branch.objects.all()
    for branch in branches:
        depts_in_branch = Department.objects.filter(branch=branch)
        avg_score = DepartmentEvaluation.objects.filter(
            department__in=depts_in_branch
        ).aggregate(avg=Avg('percentage'))['avg'] or 0
        
        branch_stats.append({
            'branch': branch,
            'avg_percentage': round(avg_score, 1),
            'dept_count': depts_in_branch.count()
        })
    
    context = {
        'dept_evaluations': dept_evaluations,
        'emp_evaluations': emp_evaluations,
        'branch_stats': branch_stats
    }
    return render(request, 'pages/evaluation_reports.html', context)


@login_required
def edit_employee(request, employee_id):
    """صفحة تعديل موظف"""
    owner = getattr(request.user, 'owner', None)
    if not owner:
        messages.error(request, 'فقط مالك المشروع يمكنه التعديل.')
        return redirect('index')
    
    employee = get_object_or_404(Investor, id=employee_id)
    branches = Branch.objects.all()
    
    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        department_id = request.POST.get('department')
        
        if branch_id:
            branch = get_object_or_404(Branch, id=branch_id)
            employee.branch = branch
        
        if department_id:
            department = get_object_or_404(Department, id=department_id)
            employee.department = department
        
        employee.save()
        messages.success(request, f'✅ تم تحديث بيانات {employee.user.username} بنجاح!')
        return redirect('investor_list')
    
    context = {
        'employee': employee,
        'branches': branches,
    }
    return render(request, 'pages/edit_employee.html', context)