from django.core.management.base import BaseCommand
from The_Owner.models import EvaluationCriterion


class Command(BaseCommand):
    help = 'إنشاء معايير تقييم الموظفين الافتراضية'

    def handle(self, *args, **options):
        criteria_data = [
            {'name': 'الحضور والانصراف في الوقت', 'max_observations': 10, 'order': 1, 'criterion_type': 'employee'},
            {'name': 'الالتزام بالزي الرسمي', 'max_observations': 10, 'order': 2, 'criterion_type': 'employee'},
            {'name': 'التعامل مع العملاء', 'max_observations': 10, 'order': 3, 'criterion_type': 'employee'},
            {'name': 'النظافة الشخصية', 'max_observations': 10, 'order': 4, 'criterion_type': 'employee'},
            {'name': 'احترام زملاء العمل', 'max_observations': 10, 'order': 5, 'criterion_type': 'employee'},
            {'name': 'اتباع التعليمات', 'max_observations': 10, 'order': 6, 'criterion_type': 'employee'},
            {'name': 'السرعة في انجاز المهام', 'max_observations': 10, 'order': 7, 'criterion_type': 'employee'},
            {'name': 'الأمانة', 'max_observations': 10, 'order': 8, 'criterion_type': 'employee'},
            {'name': 'التعاون مع الفريق', 'max_observations': 10, 'order': 9, 'criterion_type': 'employee'},
            {'name': 'المظهر العام', 'max_observations': 10, 'order': 10, 'criterion_type': 'employee'},
        ]
        
        created_count = 0
        for data in criteria_data:
            criterion, created = EvaluationCriterion.objects.get_or_create(
                name=data['name'],
                criterion_type=data['criterion_type'],
                defaults={
                    'max_observations': data['max_observations'],
                    'order': data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ {criterion.name}'))
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ تم! المعايير: {created_count}'))
