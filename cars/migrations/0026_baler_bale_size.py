# Generated by Django 5.1.5 on 2025-03-23 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0025_remove_baler_bale_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='baler',
            name='bale_size',
            field=models.IntegerField(default=120, verbose_name='Размер тюка (см)'),
            preserve_default=False,
        ),
    ]
