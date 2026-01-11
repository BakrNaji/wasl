from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Evaluation
from django.utils import timezone


@login_required
@user_passes_test(lambda u: u.is_superuser)
def manager_evaluations(request):
    # manager (superuser) can view pending evaluations and approve/reject
    if request.method == 'POST':
        action = request.POST.get('action')
        eval_id = request.POST.get('eval_id')
        ev = get_object_or_404(Evaluation, id=eval_id)
        if action == 'approve':
            ev.status = 'approved'
            ev.approved_by = request.user
            ev.approved_at = timezone.now()
            ev.save()
            messages.success(request, 'تم اعتماد التقييم')
        elif action == 'reject':
            ev.status = 'rejected'
            ev.approved_by = request.user
            ev.approved_at = timezone.now()
            ev.save()
            messages.success(request, 'تم رفض التقييم')
        return redirect('manager_evaluations')

    pending = Evaluation.objects.filter(status='pending')
    # simple summary: average overall per department
    summary = {}
    for ev in Evaluation.objects.filter(status='approved'):
        key = ev.department or 'Unspecified'
        summary.setdefault(key, []).append(float(ev.overall_score))
    avg_by_dept = {k: (sum(v) / len(v)) for k, v in summary.items()}

    return render(request, 'pages/manager_evaluations.html', {'pending': pending, 'avg_by_dept': avg_by_dept})
