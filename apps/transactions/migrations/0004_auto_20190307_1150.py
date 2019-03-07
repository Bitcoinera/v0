# Generated by Django 2.1.7 on 2019-03-07 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_remove_transaction_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='data',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='origin',
        ),
        migrations.AddField(
            model_name='transaction',
            name='key',
            field=models.CharField(default=1, max_length=500, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='value',
            field=models.CharField(default=1, max_length=500, unique=True),
            preserve_default=False,
        ),
    ]
