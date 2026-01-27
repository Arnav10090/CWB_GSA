# Generated migration for adding idType field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0007_alter_driverhelper_uid_nonnull'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverhelper',
            name='idType',
            field=models.CharField(
                choices=[
                    ('aadhar', 'Aadhar Card'),
                    ('voter_id', 'Voter ID'),
                    ('driving_license', 'Driving License'),
                    ('pan', 'PAN Card')
                ],
                default='aadhar',
                help_text='Type of ID document (Aadhar, Voter ID, Driving License, PAN)',
                max_length=20
            ),
        ),
    ]
