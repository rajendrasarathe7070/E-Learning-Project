from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_alter_pyq_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pyq',
            name='exam_type',
            field=models.CharField(
                choices=[
                    ('F', 'F-Series'),
                    ('mid', 'Mid-Sem'),
                    ('end', 'End-Sem'),
                    ('S', 'S-Series'),
                ],
                max_length=10,
            ),
        ),
    ]
