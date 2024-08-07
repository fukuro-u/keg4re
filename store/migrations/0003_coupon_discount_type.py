# Generated by Django 4.2.14 on 2024-08-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_coupon_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='discount_type',
            field=models.CharField(choices=[('percent', 'Percentage'), ('flat', 'Flat Amount')], default='percent', max_length=10),
        ),
    ]