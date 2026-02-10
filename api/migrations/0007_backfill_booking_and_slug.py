from django.db import migrations
import uuid
from decimal import Decimal


def forward(apps, schema_editor):
    Booking = apps.get_model('api', 'Booking')
    Destination = apps.get_model('api', 'Destination')
    Hotel = apps.get_model('api', 'Hotel')
    from django.utils.text import slugify

    # Backfill booking_reference and final_amount
    for b in Booking.objects.all():
        changed = False
        if not getattr(b, 'booking_reference', None):
            b.booking_reference = str(uuid.uuid4())
            changed = True
        if getattr(b, 'final_amount', None) is None:
            # Compute final_amount: total_price - discount + tax_amount if possible
            try:
                total = b.total_price or Decimal('0.00')
            except Exception:
                total = Decimal('0.00')
            try:
                discount = b.discount or Decimal('0.00')
            except Exception:
                discount = Decimal('0.00')
            try:
                tax = b.tax_amount or Decimal('0.00')
            except Exception:
                tax = Decimal('0.00')
            b.final_amount = (Decimal(total) - Decimal(discount) + Decimal(tax))
            changed = True
        if changed:
            b.save()

    # Backfill destination slugs
    for d in Destination.objects.all():
        if not getattr(d, 'slug', None):
            base = slugify(getattr(d, 'name', 'destination')) or 'destination'
            d.slug = f"{base}-{str(uuid.uuid4())[:8]}"
            d.save()

    # Backfill hotel address to empty string if None
    for h in Hotel.objects.all():
        if getattr(h, 'address', None) is None:
            h.address = ''
            h.save()


def reverse(apps, schema_editor):
    Booking = apps.get_model('api', 'Booking')
    Destination = apps.get_model('api', 'Destination')
    Hotel = apps.get_model('api', 'Hotel')

    # Revert changes by clearing the fields (best-effort)
    for b in Booking.objects.all():
        b.booking_reference = None
        b.final_amount = None
        b.save()
    for d in Destination.objects.all():
        d.slug = None
        d.save()
    for h in Hotel.objects.all():
        h.address = None
        h.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_add_nullable_fields'),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]
