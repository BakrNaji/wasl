# 📚 توثيق نظام التقييم - متاجر أبياتي

## 📋 نظرة عامة

تم تطوير نظام تقييم شامل لمتاجر أبياتي يعتمد على مبدأ **"كلما قلت الملاحظات، كان التقييم أفضل"**. النظام يشمل تقييم الأقسام والموظفين بشكل منفصل مع معايير مختلفة لكل نوع.

---

## 🏗️ البنية الأساسية للنظام

### 1. النماذج (Models) - `The_Owner/models.py`

#### 📊 `EvaluationCriterion` - معايير التقييم
```python
class EvaluationCriterion(models.Model):
    name = models.CharField(max_length=200)  # اسم المعيار
    criterion_type = models.CharField(
        max_length=20,
        choices=[('department', 'قسم'), ('employee', 'موظف')],
        default='department'
    )
    max_observations = models.IntegerField(default=10)  # الحد الأقصى للملاحظات
    order = models.IntegerField(default=0)  # ترتيب العرض
    is_active = models.BooleanField(default=True)  # معيار مفعّل أم لا
```

**الوظيفة:**
- تخزين معايير التقييم (10 معايير للأقسام + 10 معايير للموظفين)
- التمييز بين معايير الأقسام والموظفين عبر `criterion_type`
- كل معيار له حد أقصى من الملاحظات (عادة 10)

---

#### 🏢 `DepartmentEvaluation` - تقييم القسم
```python
class DepartmentEvaluation(models.Model):
    department = models.ForeignKey(Department)  # القسم المُقيّم
    month = models.DateField()  # شهر التقييم
    evaluator = models.ForeignKey(Owner)  # المقيّم
    
    # النتائج المحسوبة تلقائياً
    total_observations = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    max_possible_score = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    notes = models.TextField(blank=True)  # ملاحظات عامة
```

**الوظيفة:**
- تقييم شهري لقسم معين
- يحتوي على إحصائيات محسوبة تلقائياً:
  - `total_observations`: مجموع كل الملاحظات
  - `total_score`: النقاط = (الحد الأقصى - الملاحظات)
  - `percentage`: النسبة المئوية للأداء

**طريقة الحساب:**
```python
def calculate_totals(self):
    observations = self.details.all()  # جلب كل ملاحظات المعايير
    self.total_observations = sum(obs.observations_count for obs in observations)
    self.total_score = sum(obs.get_score() for obs in observations)
    self.max_possible_score = sum(obs.criterion.max_observations for obs in observations)
    
    if self.max_possible_score > 0:
        self.percentage = (self.total_score / self.max_possible_score) * 100
```

---

#### 👤 `EmployeeEvaluation` - تقييم الموظف
```python
class EmployeeEvaluation(models.Model):
    employee = models.ForeignKey(Investor)  # الموظف المُقيّم
    month = models.DateField()  # شهر التقييم
    evaluator = models.ForeignKey(Owner)  # المقيّم
    
    # نفس الحقول المحسوبة تلقائياً
    total_observations = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    max_possible_score = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
```

**الوظيفة:**
- مشابه لتقييم القسم ولكن للموظفين الفرديين
- يستخدم معايير مختلفة (criterion_type='employee')

---

#### 📝 `EvaluationObservation` - ملاحظات المعيار (للأقسام)
```python
class EvaluationObservation(models.Model):
    evaluation = models.ForeignKey(DepartmentEvaluation, related_name='details')
    criterion = models.ForeignKey(EvaluationCriterion)
    observations_count = models.IntegerField(default=0)  # عدد الملاحظات
    description = models.TextField(blank=True)  # وصف الملاحظات
    
    def get_score(self):
        # النقاط = الحد الأقصى - عدد الملاحظات
        return self.criterion.max_observations - self.observations_count
```

**الوظيفة:**
- تخزين ملاحظات كل معيار في التقييم
- حساب النقاط: كلما قلت الملاحظات، زادت النقاط

---

#### 📸 `ObservationImage` - صور الملاحظات (للأقسام)
```python
class ObservationImage(models.Model):
    observation = models.ForeignKey(EvaluationObservation, related_name='images')
    image = models.ImageField(upload_to='evaluation_images/')
    caption = models.CharField(max_length=200, blank=True)
```

**الوظيفة:**
- تخزين صور متعددة لكل معيار
- دعم الصور الملتقطة من الكاميرا أو المرفقة من الملفات

---

### 2. معايير التقييم

#### 🏢 معايير الأقسام (10 معايير)
تُحمّل عبر: `python manage.py setup_evaluation`

1. **تحقيق هدف المبيعات** (max: 10 ملاحظات)
2. **تسجيل الأسعار** (max: 10)
3. **مطابقة الأسعار** (max: 10)
4. **الالتزام بالزي** (max: 10)
5. **النظافة** (max: 10)
6. **الشكاوي** (max: 10)
7. **تقييم مشرف الجودة** (max: 10)
8. **رفع نواقص المشتريات** (max: 10)
9. **ترتيب القسم** (max: 10)
10. **توفير عروض** (max: 10)

#### 👤 معايير الموظفين (10 معايير)
تُحمّل عبر: `python manage.py setup_employee_evaluation`

1. **الحضور والانصراف** (max: 10)
2. **الالتزام بالزي** (max: 10)
3. **التعامل مع العملاء** (max: 10)
4. **النظافة الشخصية** (max: 10)
5. **احترام زملاء العمل** (max: 10)
6. **اتباع التعليمات** (max: 10)
7. **السرعة في إنجاز المهام** (max: 10)
8. **الأمانة** (max: 10)
9. **التعاون مع الفريق** (max: 10)
10. **المظهر العام** (max: 10)

---

## 🎨 واجهات المستخدم

### 1. صفحة تقييم القسم - `evaluate_department.html`

#### 🔧 المكونات الأساسية:

```html
<!-- اختيار الفرع والقسم والشهر -->
<select id="branchSelect">...</select>
<select name="department" id="departmentSelect">...</select>
<input type="month" name="month">
```

#### 📊 لوحة الإحصائيات المباشرة:
```html
<div class="alert alert-info">
    <h4 id="totalCriteria">0</h4> <!-- معايير مفعّلة -->
    <h4 id="totalObservations">0</h4> <!-- إجمالي الملاحظات -->
    <h4 id="totalScore">0</h4> <!-- النقاط المكتسبة -->
    <h4 id="percentage">0%</h4> <!-- النسبة المئوية -->
</div>
```

**الوظيفة:**
- تحديث فوري عند تغيير أي بيانات
- عرض النقاط والنسبة المئوية بألوان ديناميكية:
  - 🟢 أخضر: ≥70%
  - 🟡 أصفر: ≥50%
  - 🔴 أحمر: <50%

#### ✅ المعايير الاختيارية:
```html
<div class="card criterion-card" data-criterion-id="{{ criterion.id }}">
    <!-- زر التفعيل/التعطيل -->
    <input type="checkbox" class="criterion-toggle">
    
    <!-- محتوى المعيار (مخفي افتراضياً) -->
    <div class="criterion-content" style="display: none;">
        <input type="number" name="obs_count_{{ criterion.id }}" disabled>
        <textarea name="obs_desc_{{ criterion.id }}" disabled></textarea>
        
        <!-- أزرار الصور -->
        <button onclick="openCamera('images_{{ criterion.id }}')">تصوير</button>
        <button onclick="openFiles('images_{{ criterion.id }}')">إرفاق</button>
        <input type="file" name="images_{{ criterion.id }}" multiple>
    </div>
</div>
```

**الوظيفة:**
- كل معيار له زر تفعيل/تعطيل
- عند التفعيل: تظهر الحقول وتصبح نشطة
- عند التعطيل: تختفي الحقول ولا يتم إرسال بياناتها

---

### 2. صفحة تقييم الموظف - `evaluate_employee.html`

**نفس البنية والتصميم** لكن مع:
- قائمة منسدلة لاختيار الموظف
- معايير مختلفة (criterion_type='employee')

---

## 💻 البرمجة الخلفية (Views)

### 1. دالة تقييم القسم - `evaluate_department`

```python
@login_required
def evaluate_department(request):
    owner = getattr(request.user, 'owner', None)
    if not owner:
        messages.error(request, 'فقط مالك المشروع يمكنه التقييم.')
        return redirect('index')
    
    branches = Branch.objects.all()
    criteria = EvaluationCriterion.objects.filter(
        is_active=True, 
        criterion_type='department'
    ).order_by('order')
    
    if request.method == 'POST':
        department_id = request.POST.get('department')
        month = request.POST.get('month')
        notes = request.POST.get('notes', '')
        
        # تحويل '2026-01' إلى '2026-01-01'
        month_date = date.fromisoformat(month + '-01')
        
        # إنشاء أو تحديث التقييم
        evaluation, created = DepartmentEvaluation.objects.get_or_create(
            department=department,
            month=month_date,
            defaults={'evaluator': owner, 'notes': notes}
        )
        
        if not created:
            # حذف الملاحظات القديمة لتحديثها
            evaluation.details.all().delete()
        
        # معالجة المعايير المفعّلة فقط
        for criterion in criteria:
            obs_count_key = f'obs_count_{criterion.id}'
            
            # التحقق إذا كان المعيار مفعّل
            if obs_count_key in request.POST:
                obs_count = int(request.POST.get(obs_count_key, 0))
                obs_desc = request.POST.get(f'obs_desc_{criterion.id}', '')
                
                # إنشاء الملاحظة
                observation = EvaluationObservation.objects.create(
                    evaluation=evaluation,
                    criterion=criterion,
                    observations_count=obs_count,
                    description=obs_desc
                )
                
                # إضافة الصور المتعددة
                images = request.FILES.getlist(f'images_{criterion.id}')
                for img in images:
                    ObservationImage.objects.create(
                        observation=observation, 
                        image=img
                    )
        
        # إعادة حساب الإحصائيات
        evaluation.save()
        messages.success(request, f'✅ تم حفظ تقييم {department.name} بنجاح!')
        return redirect('evaluation_reports')
```

**شرح الخطوات:**

1. **التحقق من الصلاحيات**: فقط المالك يمكنه التقييم
2. **جلب البيانات**: الفروع والمعايير النشطة للأقسام
3. **عند الإرسال**:
   - تحويل الشهر من `YYYY-MM` إلى `YYYY-MM-DD`
   - إنشاء أو جلب التقييم الموجود
   - حذف الملاحظات القديمة عند التحديث
   - معالجة المعايير المفعّلة فقط (التي في `request.POST`)
   - حفظ الصور المتعددة لكل معيار
   - إعادة حساب الإحصائيات تلقائياً عبر `evaluation.save()`

---

### 2. دالة تقييم الموظف - `evaluate_employee`

**نفس المنطق** مع اختلافات:
- معايير من نوع `criterion_type='employee'`
- استخدام `EmployeeEvaluation` و `EmployeeObservation`

---

## 📱 JavaScript - التفاعل الديناميكي

### 1. حساب الإحصائيات الفورية

```javascript
function calculateStatistics() {
    let activeCriteria = 0;
    let totalObservations = 0;
    let totalScore = 0;
    let maxPossibleScore = 0;
    
    criteriaToggles.forEach(toggle => {
        const criterionId = toggle.dataset.criterionId;
        const card = document.querySelector(`[data-criterion-id="${criterionId}"]`);
        const maxObs = parseInt(card.dataset.maxObs);
        const obsInput = document.querySelector(`input[name="obs_count_${criterionId}"]`);
        
        if (toggle.checked) {
            activeCriteria++;
            const obsCount = parseInt(obsInput.value) || 0;
            totalObservations += obsCount;
            
            // حساب النقاط: max - observations
            const score = maxObs - obsCount;
            totalScore += score;
            maxPossibleScore += maxObs;
            
            // تحديث badge النقاط
            const scoreBadge = document.getElementById(`score_${criterionId}`);
            scoreBadge.textContent = `النقاط: ${score}`;
            
            // تغيير اللون حسب الأداء
            scoreBadge.className = score >= maxObs * 0.7 ? 'badge bg-success' : 
                                  score >= maxObs * 0.5 ? 'badge bg-warning' : 
                                  'badge bg-danger';
        }
    });
    
    // حساب النسبة المئوية
    const percentage = maxPossibleScore > 0 ? 
        ((totalScore / maxPossibleScore) * 100).toFixed(1) : 0;
    
    // تحديث العرض
    document.getElementById('totalCriteria').textContent = activeCriteria;
    document.getElementById('totalObservations').textContent = totalObservations;
    document.getElementById('totalScore').textContent = totalScore;
    document.getElementById('percentage').textContent = percentage + '%';
}
```

**الوظيفة:**
- تُنفّذ عند أي تغيير (تفعيل معيار أو تغيير عدد الملاحظات)
- تحسب النقاط والنسبة المئوية فورياً
- تُحدّث الألوان حسب مستوى الأداء

---

### 2. معالج التفعيل/التعطيل

```javascript
criteriaToggles.forEach(toggle => {
    toggle.addEventListener('change', function() {
        const criterionId = this.dataset.criterionId;
        const card = document.querySelector(`[data-criterion-id="${criterionId}"]`);
        const content = card.querySelector('.criterion-content');
        const inputs = content.querySelectorAll('input, textarea');
        const cameraBtn = document.getElementById(`camera_btn_${criterionId}`);
        const filesBtn = document.getElementById(`files_btn_${criterionId}`);
        
        if (this.checked) {
            // تفعيل المعيار
            content.style.display = 'block';
            card.classList.add('active');
            
            inputs.forEach(input => {
                if (!input.classList.contains('image-input')) {
                    input.disabled = false;
                }
            });
            
            if (cameraBtn) cameraBtn.disabled = false;
            if (filesBtn) filesBtn.disabled = false;
        } else {
            // تعطيل المعيار
            content.style.display = 'none';
            card.classList.remove('active');
            
            inputs.forEach(input => {
                input.disabled = true;
                if (input.type === 'number') input.value = 0;
            });
            
            if (cameraBtn) cameraBtn.disabled = true;
            if (filesBtn) filesBtn.disabled = true;
        }
        
        calculateStatistics();
    });
});
```

**الوظيفة:**
- عند التفعيل: إظهار المحتوى وتفعيل الحقول والأزرار
- عند التعطيل: إخفاء المحتوى وتعطيل كل الحقول
- إعادة حساب الإحصائيات بعد أي تغيير

---

### 3. دوال الكاميرا والملفات

```javascript
// فتح الكاميرا للتصوير
function openCamera(inputId) {
    const input = document.getElementById(inputId);
    input.setAttribute('capture', 'environment'); // الكاميرا الخلفية
    input.click();
}

// فتح مستكشف الملفات
function openFiles(inputId) {
    const input = document.getElementById(inputId);
    input.removeAttribute('capture'); // إزالة خاصية الكاميرا
    input.click();
}

// عرض معاينة الصور المتعددة
function showImagePreview(input, criterionId) {
    const previewDiv = document.getElementById(`preview_${criterionId}`);
    previewDiv.innerHTML = '';
    
    if (input.files && input.files.length > 0) {
        Array.from(input.files).forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const div = document.createElement('div');
                div.className = 'image-preview-item';
                div.innerHTML = `
                    <img src="${e.target.result}" alt="صورة ${index + 1}">
                    <span class="badge bg-primary">${index + 1}</span>
                `;
                previewDiv.appendChild(div);
            };
            reader.readAsDataURL(file);
        });
    }
}
```

**الوظيفة:**
- `openCamera()`: يفتح كاميرا الجهاز (للهواتف المحمولة)
- `openFiles()`: يفتح مستكشف الملفات (للكمبيوتر أو الألبوم)
- `showImagePreview()`: يعرض معاينة الصور المختارة مع أرقام

---

### 4. تحميل الأقسام حسب الفرع

```javascript
const departmentsByBranch = {};

// تحميل البيانات من Django
{% for branch in branches %}
departmentsByBranch[{{ branch.id }}] = [
    {% for dept in branch.departments.all %}
    {id: {{ dept.id }}, name: "{{ dept.name|escapejs }}"}
    {% if not forloop.last %},{% endif %}
    {% endfor %}
];
{% endfor %}

// معالج تغيير الفرع
document.getElementById('branchSelect').addEventListener('change', function() {
    const branchId = this.value;
    const deptSelect = document.getElementById('departmentSelect');
    
    deptSelect.innerHTML = '<option value="">-- اختر قسم --</option>';
    
    if (branchId && departmentsByBranch[branchId]) {
        departmentsByBranch[branchId].forEach(dept => {
            const option = document.createElement('option');
            option.value = dept.id;
            option.textContent = dept.name;
            deptSelect.appendChild(option);
        });
        deptSelect.disabled = false;
    } else {
        deptSelect.disabled = true;
    }
});
```

**الوظيفة:**
- تحميل أقسام كل فرع في كائن JavaScript
- عند اختيار فرع: تحديث قائمة الأقسام تلقائياً
- لا حاجة لطلب AJAX إضافي

---

## 👤 صفحة الملف الشخصي - التحديثات

### 1. للموظفين - عرض التقييمات

```python
# في accounts/views.py - دالة profile
employee_evaluations = []
latest_employee_eval = None

if user_investor:
    from The_Owner.models import EmployeeEvaluation
    employee_evaluations = EmployeeEvaluation.objects.filter(
        employee=user_investor
    ).select_related('evaluator__user').order_by('-month')[:5]
    
    latest_employee_eval = employee_evaluations.first()
```

```html
<!-- في profile.html -->
{% if latest_employee_eval %}
<div style="background:linear-gradient(135deg, #F2A23F 0%, #f5b35a 100%);">
    <h5>📊 آخر تقييم</h5>
    <small>{{ latest_employee_eval.month|date:'Y-m' }}</small>
    
    <div>
        <div style="font-size:28px;">{{ latest_employee_eval.percentage|floatformat:1 }}%</div>
        <small>{{ latest_employee_eval.total_score }} من {{ latest_employee_eval.max_possible_score }}</small>
    </div>
    
    <p>عدد الملاحظات: {{ latest_employee_eval.total_observations }}</p>
</div>
{% endif %}
```

**الوظيفة:**
- عرض آخر 5 تقييمات للموظف
- تسليط الضوء على آخر تقييم بتصميم مميز
- عرض النسبة المئوية والنقاط وعدد الملاحظات

---

### 2. للمالكين - عرض التقييمات المضافة

```python
# في accounts/views.py
owner_dept_evaluations = []
owner_emp_evaluations = []

if user_owner:
    from The_Owner.models import DepartmentEvaluation, EmployeeEvaluation
    owner_dept_evaluations = DepartmentEvaluation.objects.filter(
        evaluator=user_owner
    ).select_related('department__branch').order_by('-created_at')[:5]
    
    owner_emp_evaluations = EmployeeEvaluation.objects.filter(
        evaluator=user_owner
    ).select_related('employee__user', 'employee__department').order_by('-created_at')[:5]
```

```html
<!-- عرض تقييمات الأقسام -->
<h5>🏢 تقييمات الأقسام</h5>
{% for ev in owner_dept_evaluations %}
<div class="card">
    <h5>{{ ev.department.name }}</h5>
    <small>{{ ev.month|date:'Y-m' }}</small>
    <div>{{ ev.percentage|floatformat:1 }}%</div>
    <p>الملاحظات: {{ ev.total_observations }}</p>
    <p>النقاط: {{ ev.total_score }}</p>
</div>
{% endfor %}

<!-- عرض تقييمات الموظفين -->
<h5>👤 تقييمات الموظفين</h5>
{% for ev in owner_emp_evaluations %}
<div class="card">
    <h5>{{ ev.employee.user.username }}</h5>
    <small>{{ ev.month|date:'Y-m' }}</small>
    <div>{{ ev.percentage|floatformat:1 }}%</div>
</div>
{% endfor %}
```

**الوظيفة:**
- عرض آخر 5 تقييمات أضافها المالك للأقسام
- عرض آخر 5 تقييمات أضافها المالك للموظفين
- تنظيم بصري مميز لكل نوع

---

## 🎨 تحديثات القائمة (Navigation)

### التحسينات المطبقة:

```html
<ul class="nav">
    <li><a href="{% url 'index' %}">الرئيسية</a></li>
    <li><a href="{% url 'about' %}">من نحن</a></li>
    
    {% if request.user.is_authenticated %}
        <li><a href="{% url 'profile' %}"><i class="fa fa-user"></i> الملف الشخصي</a></li>
        
        {% if request.user.owner %}
            <li><a href="{% url 'investor_list' %}"><i class="fa fa-users"></i> قائمة الموظفين</a></li>
        {% elif request.user.investor %}
            <li><a href="{% url 'prodesc' %}"><i class="fa fa-briefcase"></i> استثماراتي</a></li>
        {% endif %}
        
        <!-- أيقونة الرسائل مع شارة العدد -->
        <li>
            <a href="{% url 'twsl' %}" style="position: relative;">
                <i class="fa fa-envelope"></i>
                {% if unread_count > 0 %}
                    <span class="badge badge-danger" style="position: absolute; top: -8px; right: -8px;">
                        {{ unread_count }}
                    </span>
                {% endif %}
            </a>
        </li>
        
        <li><a href="{% url 'logout' %}"><i class="fa fa-sign-out"></i> تسجيل خروج</a></li>
    {% else %}
        <li><a href="{% url 'login' %}"><i class="fa fa-sign-in"></i> تسجيل دخول</a></li>
        <li><a href="{% url 'signup' %}"><i class="fa fa-user-plus"></i> انشاء حساب</a></li>
    {% endif %}
</ul>
```

**التحسينات:**
1. دمج القوائم المتعددة في قائمة واحدة منظمة
2. إضافة أيقونات Font Awesome لكل رابط
3. تحسين شارة الرسائل (badge) مع موضع نسبي
4. حذف الـ dropdown المكرر
5. ترتيب منطقي: الرئيسية → الملف الشخصي → الخدمات → الرسائل → تسجيل الخروج

---

## 🔗 URLs - المسارات

```python
# في The_Owner/urls.py
urlpatterns = [
    # صفحة قائمة الموظفين (الصفحة الرئيسية للمالك)
    path('investors/', views.investor_list, name='investor_list'),
    
    # التقييم
    path('evaluate-department/', views.evaluate_department, name='evaluate_department'),
    path('evaluate-employee/', views.evaluate_employee, name='evaluate_employee'),
    
    # التقارير
    path('evaluation-reports/', views.evaluation_reports, name='evaluation_reports'),
    
    # تعديل الموظف
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    
    # AJAX لتحميل الأقسام
    path('ajax/departments/<int:branch_id>/', views.ajax_departments, name='ajax_departments'),
]
```

---

## 📊 صفحة التقارير - `evaluation_reports.html`

### الوظيفة:
```python
@login_required
def evaluation_reports(request):
    owner = getattr(request.user, 'owner', None)
    if not owner:
        messages.error(request, 'فقط مالك المشروع يمكنه الوصول.')
        return redirect('index')
    
    # تقييمات الأقسام (آخر 20)
    dept_evaluations = DepartmentEvaluation.objects.select_related(
        'department', 'department__branch'
    ).order_by('-month', 'department')[:20]
    
    # تقييمات الموظفين (آخر 20)
    emp_evaluations = EmployeeEvaluation.objects.select_related(
        'employee__user', 'employee__department'
    ).order_by('-month', 'employee')[:20]
    
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
            'avg_score': round(avg_score, 1),
            'dept_count': depts_in_branch.count()
        })
    
    context = {
        'dept_evaluations': dept_evaluations,
        'emp_evaluations': emp_evaluations,
        'branch_stats': branch_stats,
    }
    return render(request, 'pages/evaluation_reports.html', context)
```

**العرض:**
- جداول لعرض آخر التقييمات
- إحصائيات متوسط الأداء لكل فرع
- روابط سريعة لإضافة تقييمات جديدة

---

## 🎯 معايير الأداء

### نظام التقييم:

| النسبة المئوية | التصنيف | اللون |
|----------------|---------|-------|
| 90% - 100% | ممتاز 🌟 | أخضر غامق |
| 70% - 89% | جيد جداً ✅ | أخضر |
| 50% - 69% | جيد ⚠️ | أصفر |
| 30% - 49% | مقبول 📉 | برتقالي |
| أقل من 30% | ضعيف ❌ | أحمر |

### كيفية الحساب:

```
إجمالي النقاط = مجموع (الحد الأقصى للملاحظات - عدد الملاحظات الفعلي) لكل معيار
أقصى نقاط ممكنة = مجموع الحد الأقصى لكل المعايير المفعّلة
النسبة المئوية = (إجمالي النقاط / أقصى نقاط ممكنة) × 100

مثال:
- معيار النظافة: حد أقصى 10 ملاحظات، الملاحظات الفعلية: 2
- النقاط = 10 - 2 = 8 نقاط
- إذا كانت 3 معايير مفعّلة بنفس الطريقة:
  - أقصى نقاط = 30
  - النقاط الفعلية = 24
  - النسبة = (24/30) × 100 = 80% (جيد جداً)
```

---

## 📝 الملفات المعدلة - ملخص

### 1. النماذج (Models)
- ✅ `The_Owner/models.py`
  - `EvaluationCriterion` - مع حقل `criterion_type`
  - `DepartmentEvaluation` - مع `calculate_totals()`
  - `EmployeeEvaluation` - مع `calculate_totals()`
  - `EvaluationObservation` - مع `get_score()`
  - `EmployeeObservation`
  - `ObservationImage` و `EmployeeObservationImage`

### 2. الواجهات (Templates)
- ✅ `templates/pages/evaluate_department.html` - معايير اختيارية + حساب فوري
- ✅ `templates/pages/evaluate_employee.html` - نفس البنية للموظفين
- ✅ `templates/pages/investor_list.html` - بطاقتا التقييم فقط
- ✅ `templates/pages/evaluation_reports.html` - صفحة التقارير
- ✅ `templates/pages/edit_employee.html` - تعديل بيانات الموظف
- ✅ `templates/accounts/profile.html` - عرض التقييمات الجديدة
- ✅ `templates/parts/nav.html` - قائمة مرتبة بأيقونات

### 3. العرض (Views)
- ✅ `The_Owner/views.py`
  - `evaluate_department()` - معايير اختيارية + صور متعددة
  - `evaluate_employee()` - نفس المنطق للموظفين
  - `evaluation_reports()` - صفحة التقارير
  - `edit_employee()` - تعديل الموظف
  - `ajax_departments()` - AJAX للأقسام

- ✅ `accounts/views.py`
  - `profile()` - عرض التقييمات الجديدة

### 4. المسارات (URLs)
- ✅ `The_Owner/urls.py` - مسارات التقييم

### 5. الأوامر (Management Commands)
- ✅ `The_Owner/management/commands/setup_evaluation.py`
- ✅ `The_Owner/management/commands/setup_employee_evaluation.py`

### 6. قاعدة البيانات (Migrations)
- ✅ `The_Owner/migrations/0042_*.py` - إضافة حقل `criterion_type`

---

## 🚀 كيفية الاستخدام

### 1. تحميل المعايير (مرة واحدة):
```bash
python manage.py setup_evaluation
python manage.py setup_employee_evaluation
```

### 2. الوصول إلى نظام التقييم:
- المالك يدخل على: `http://127.0.0.1:8000/owner/investors/`
- يرى بطاقتين: "تقييم قسم" و "تقييم موظف"

### 3. خطوات تقييم قسم:
1. اختر الفرع
2. اختر القسم
3. اختر الشهر
4. فعّل المعايير التي تريد تقييمها
5. أدخل عدد الملاحظات ووصفها
6. أضف صور (كاميرا أو إرفاق) - اختياري
7. شاهد الإحصائيات تتحدث فورياً
8. احفظ التقييم

### 4. عرض التقارير:
- `http://127.0.0.1:8000/owner/evaluation-reports/`
- يعرض آخر التقييمات وإحصائيات الفروع

### 5. عرض تقييمات الموظف:
- الموظف يدخل على ملفه الشخصي
- يرى آخر تقييماته مع النسبة المئوية

---

## 🎨 التصميم والألوان

### الألوان المستخدمة:

```css
/* تقييم الأقسام */
--department-primary: #235E88;
--department-secondary: #3a7ca5;
--department-gradient: linear-gradient(135deg, #235E88 0%, #3a7ca5 100%);

/* تقييم الموظفين */
--employee-primary: #F2A23F;
--employee-secondary: #f5b35a;
--employee-gradient: linear-gradient(135deg, #F2A23F 0%, #f5b35a 100%);

/* حالات الأداء */
--success-color: #28a745;  /* ممتاز/جيد */
--warning-color: #ffc107;  /* مقبول */
--danger-color: #dc3545;   /* ضعيف */
```

### الأيقونات:
- 🏢 تقييم القسم
- 👤 تقييم الموظف
- 📊 الإحصائيات
- 📸 الكاميرا
- 📁 الملفات
- ✅ النجاح
- ⚠️ تحذير
- ❌ خطأ

---

## 🔒 الأمان

### الصلاحيات:
```python
@login_required
def evaluate_department(request):
    owner = getattr(request.user, 'owner', None)
    if not owner:
        messages.error(request, 'فقط مالك المشروع يمكنه التقييم.')
        return redirect('index')
```

- فقط المالك يمكنه:
  - إضافة تقييمات
  - عرض التقارير
  - تعديل بيانات الموظفين

- الموظف يمكنه:
  - عرض تقييماته فقط
  - لا يمكنه رؤية تقييمات الآخرين

---

## 📈 نقاط القوة

1. ✅ **معايير اختيارية**: المقيّم يختار ما يريد تقييمه
2. ✅ **حساب تلقائي فوري**: لا حاجة للانتظار
3. ✅ **صور متعددة**: دعم الكاميرا والإرفاق
4. ✅ **واجهة سهلة**: تصميم نظيف ومرتب
5. ✅ **تقارير شاملة**: إحصائيات بالفروع والأقسام
6. ✅ **استجابة كاملة**: يعمل على الهواتف والكمبيوتر
7. ✅ **ألوان ديناميكية**: تتغير حسب الأداء

---

## 🐛 حل المشاكل الشائعة

### 1. الشعار لا يظهر:
```bash
# تأكد من نسخ الملف للمكان الصحيح
Copy-Item "static\assets\images\متاجر ابياتي.jfif" "wasl\static\assets\images\"

# أو جمع الملفات الثابتة
python manage.py collectstatic --noinput
```

### 2. خطأ "observations has no attribute":
```python
# الحل: استخدم related_name الصحيح
evaluation.details.all().delete()  # ✅ صحيح
# بدلاً من
evaluation.observations.all().delete()  # ❌ خطأ
```

### 3. التقييمات لا تحسب:
```python
# تأكد من استدعاء save() في النهاية
evaluation.save()  # هذا ينفذ calculate_totals() تلقائياً
```

---

## 📞 دعم إضافي

لأي استفسارات أو مشاكل:
1. راجع هذا الملف أولاً
2. تحقق من الأخطاء في console المتصفح (F12)
3. تحقق من سجلات Django في Terminal

---

**تم التوثيق بواسطة:** GitHub Copilot  
**التاريخ:** 12 يناير 2026  
**الإصدار:** 1.0
