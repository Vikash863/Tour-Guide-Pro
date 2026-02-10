from django.db import migrations, models
from decimal import Decimal
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_backfill_booking_and_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_reference',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='final_amount',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')),
        ),
        migrations.AlterField(
            model_name='destination',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='address',
            field=models.TextField(default=''),
        ),
    ]
