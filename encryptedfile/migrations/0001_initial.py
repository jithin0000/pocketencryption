# Generated by Django 3.0.5 on 2020-04-28 04:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import encryptedfile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EncryptedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100)),
                ('file_password', models.CharField(max_length=255)),
                ('file_key', models.CharField(editable=False, max_length=255)),
                ('file_url', models.FileField(upload_to=encryptedfile.models.user_file_upload)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
