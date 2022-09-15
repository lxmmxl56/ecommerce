# Generated by Django 3.2.12 on 2022-06-28 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0050_templatefileattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerusageemail',
            name='email_type',
            field=models.CharField(blank=True, choices=[('digest', 'Digest email'), ('low_balance', 'Low balance email'), ('out_of_balance', 'Out of balance email')], help_text='Which type of email was sent.', max_length=32, null=True),
        ),
    ]