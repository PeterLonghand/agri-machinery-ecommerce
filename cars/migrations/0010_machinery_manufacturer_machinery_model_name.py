# Generated by Django 5.1.5 on 2025-02-14 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0009_machinery_alter_baler_options_alter_harrow_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='machinery',
            name='manufacturer',
            field=models.CharField(default=0, max_length=28, verbose_name='Производитель'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='machinery',
            name='model_name',
            field=models.CharField(default=0, max_length=28, verbose_name='Название модели'),
            preserve_default=False,
        ),
    ]
