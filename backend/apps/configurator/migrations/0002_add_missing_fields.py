from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0001_initial'),
    ]

    operations = [
        # --- SceneTemplate ---
        migrations.AddField(
            model_name='scenetemplate',
            name='thumbnail_url',
            field=models.URLField(blank=True, default='', verbose_name='URL miniaturki (zewn.)'),
            preserve_default=False,
        ),

        # --- ComponentCategory ---
        migrations.AddField(
            model_name='componentcategory',
            name='color',
            field=models.CharField(default='#00ff88', max_length=7, verbose_name='Kolor (hex)'),
        ),

        # --- Component ---
        migrations.AddField(
            model_name='component',
            name='short_desc',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Krótki opis'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='component',
            name='thumbnail_url',
            field=models.URLField(blank=True, default='', verbose_name='URL miniaturki (zewn.)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='component',
            name='icon_name',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Nazwa ikony'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='component',
            name='color',
            field=models.CharField(blank=True, default='', max_length=7, verbose_name='Kolor (hex)'),
            preserve_default=False,
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
