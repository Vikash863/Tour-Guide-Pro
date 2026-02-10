from django.db import migrations, models
from decimal import Decimal
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_temp'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_reference',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='final_amount',
            field=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='destination',
            name='slug',
            field=models.SlugField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='address',
            field=models.TextField(null=True, blank=True),
        ),
    ]
