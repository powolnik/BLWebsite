from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0001_initial'),
    ]

    operations = [
        # ComponentCategory.color
        migrations.AddField(
            model_name='componentcategory',
            name='color',
            field=models.CharField(
                default='#00ff88',
                help_text='Kolor kategorii w konfiguratorze',
                max_length=7,
                verbose_name='Kolor (hex)',
            ),
        ),
        # Component.color
        migrations.AddField(
            model_name='component',
            name='color',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Kolor modułu na scenie',
                max_length=7,
                verbose_name='Kolor (hex)',
            ),
            preserve_default=False,
        ),
        # Component.width_m
        migrations.AddField(
            model_name='component',
            name='width_m',
            field=models.DecimalField(
                decimal_places=1,
                default=2,
                max_digits=5,
                verbose_name='Szerokość modułu (m)',
            ),
        ),
        # Component.depth_m
        migrations.AddField(
            model_name='component',
            name='depth_m',
            field=models.DecimalField(
                decimal_places=1,
                default=2,
                max_digits=5,
                verbose_name='Głębokość modułu (m)',
            ),
        ),
    ]
