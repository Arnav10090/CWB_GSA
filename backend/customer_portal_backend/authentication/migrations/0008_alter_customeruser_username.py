# Generated migration for removing username requirement

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_customeruser_last_login_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
