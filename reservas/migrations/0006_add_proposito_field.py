from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0004_alter_reserva_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='proposito',
            field=models.CharField(default='Uso general', max_length=255, verbose_name='Propósito'),
            preserve_default=False,
        ),
    ]
