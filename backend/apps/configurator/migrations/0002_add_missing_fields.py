from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0001_initial'),
    ]

    operations = [
        # ComponentCategory - brakujące pole color
        migrations.AddField(
            model_name='componentcategory',
            name='color',
            field=models.CharField(default='#00ff88', max_length=7, verbose_name='Kolor (hex)'),
        ),
        # Component - brakujące pola
        migrations.AddField(
            model_name='component',
            name='short_desc',
            field=models.CharField(blank=True, max_length=200, verbose_name='Krótki opis'),
        ),
        migrations.AddField(
            model_name='component',
            name='icon_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Nazwa ikony'),
        ),
        migrations.AddField(
            model_name='component',
            name='color',
            field=models.CharField(blank=True, default='', max_length=7, verbose_name='Kolor (hex)'),
        ),
        migrations.AddField(
            model_name='component',
            name='width_m',
            field=models.DecimalField(decimal_places=1, default=2, max_digits=5, verbose_name='Szerokość modułu (m)'),
        ),
        migrations.AddField(
            model_name='component',
            name='depth_m',
            field=models.DecimalField(decimal_places=1, default=2, max_digits=5, verbose_name='Głębokość modułu (m)'),
        ),
    ]
