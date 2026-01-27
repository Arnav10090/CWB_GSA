# Generated migration for adding companyName field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_alter_customeruser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeruser',
            name='companyName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
