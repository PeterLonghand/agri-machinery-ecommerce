# Generated by Django 5.1.5 on 2025-03-23 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0029_remove_selfpropelledsprayer_width_harrow_max_depth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selfpropelledsprayer',
            name='maxwidth',
            field=models.IntegerField(verbose_name='Ширина обработки до, м'),
        ),
        migrations.AlterField(
            model_name='selfpropelledsprayer',
            name='minwidth',
            field=models.IntegerField(verbose_name='Ширина обработки от, м'),
        ),
        migrations.AlterField(
            model_name='trailedsprayer',
            name='maxwidth',
            field=models.IntegerField(verbose_name='Ширина обработки до, м'),
        ),
        migrations.AlterField(
            model_name='trailedsprayer',
            name='minwidth',
            field=models.IntegerField(verbose_name='Ширина обработки от, м'),
        ),
    ]
