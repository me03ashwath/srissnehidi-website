from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_galleryitem_options_galleryitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryitem',
            name='category',
            field=models.CharField(
                choices=[
                    ('certificates', 'Certificates Issued'),
                    ('fashion_work', "Fashion Student's Work"),
                    ('aari_work', "Aari Student's Work"),
                    ('events', 'Events'),
                    ('classes', 'Classes'),
                ],
                max_length=20,
            ),
        ),
    ]
