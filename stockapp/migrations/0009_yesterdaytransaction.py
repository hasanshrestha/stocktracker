# Generated by Django 4.1.6 on 2023-03-03 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0008_dailytransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='YesterdayTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('total_shares', models.CharField(max_length=255)),
                ('percentage', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('broker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stockapp.broker')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stockapp.stock')),
            ],
            options={
                'db_table': 'yesterdaytransaction',
            },
        ),
    ]
