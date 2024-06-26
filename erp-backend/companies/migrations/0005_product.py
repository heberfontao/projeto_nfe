# Generated by Django 4.2.4 on 2024-05-11 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('unit', models.CharField(max_length=10)),
                ('ncm', models.CharField(max_length=20)),
                ('cest', models.CharField(max_length=20)),
                ('gtin', models.CharField(blank=True, max_length=20, null=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.employee')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.enterprise')),
            ],
        ),
    ]
