# Generated by Django 4.2.4 on 2024-05-21 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0012_produtodetalhenfe_ean'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nfe',
            name='xml',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='cest',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
