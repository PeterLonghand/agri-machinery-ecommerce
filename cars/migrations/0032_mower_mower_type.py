# Generated by Django 5.1.5 on 2025-03-23 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0031_remove_trailedsprayer_width'),
    ]

    operations = [
        migrations.AddField(
            model_name='mower',
            name='mower_type',
            field=models.CharField(choices=[('rotary', 'Роторная'), ('disc', 'Дисковая')], default=1, verbose_name='Тип косилки'),
            preserve_default=False,
        ),
    ]
