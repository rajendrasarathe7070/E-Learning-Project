from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_pyq_exam_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syllabus',
            name='subject_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='syllabus',
            name='subject_code',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AddField(
            model_name='syllabus',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='syllabus',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='syllabus',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='syllabi', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='syllabus',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AddField(
            model_name='syllabus',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='syllabus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterModelOptions(
            name='syllabus',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddConstraint(
            model_name='syllabus',
            constraint=models.UniqueConstraint(fields=('subject_code', 'branch', 'semester'), name='unique_syllabus_code_branch_sem'),
        ),
        migrations.AddIndex(
            model_name='syllabus',
            index=models.Index(fields=['subject_code', 'branch', 'semester'], name='core_syllab_subject_1792ae_idx'),
        ),
    ]
