# Generated by Django 4.1.6 on 2023-02-07 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0002_stock_remove_broker_id_alter_broker_broker_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='id',
        ),
        migrations.AlterField(
            model_name='stock',
            name='symbol',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
