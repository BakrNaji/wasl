from django.core.management.base import BaseCommand
from The_Owner.models import EvaluationCriterion


class Command(BaseCommand):
    help = 'تحميل معايير التقييم الافتراضية'

    def handle(self, *args, **options):
        criteria_list = [
            {'name': 'تحقيق هدف المبيعات', 'max_observations': 10, 'order': 1, 'criterion_type': 'department'},
            {'name': 'تسجيل الاسعار علي الارفف', 'max_observations': 10, 'order': 2, 'criterion_type': 'department'},
            {'name': 'مطابقة الاسعار علي الكاشيرات', 'max_observations': 10, 'order': 3, 'criterion_type': 'department'},
            {'name': 'الالتزام بالزي الرسمي', 'max_observations': 10, 'order': 4, 'criterion_type': 'department'},
            {'name': 'النظافة', 'max_observations': 10, 'order': 5, 'criterion_type': 'department'},
            {'name': 'الشكاوي', 'max_observations': 10, 'order': 6, 'criterion_type': 'department'},
            {'name': 'تقييم مشرف الجودة', 'max_observations': 10, 'order': 7, 'criterion_type': 'department'},
            {'name': 'رفع نواقص المشتريات', 'max_observations': 10, 'order': 8, 'criterion_type': 'department'},
            {'name': 'ترتيب القسم', 'max_observations': 10, 'order': 9, 'criterion_type': 'department'},
            {'name': 'توفير عروض مميزة', 'max_observations': 10, 'order': 10, 'criterion_type': 'department'},
        ]
        
        for data in criteria_list:
            criterion, created = EvaluationCriterion.objects.get_or_create(
                name=data['name'],
                criterion_type=data.get('criterion_type', 'department'),
                defaults={'max_observations': data['max_observations'], 'order': data['order']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ {criterion.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ تم! المعايير: {EvaluationCriterion.objects.count()}'))
