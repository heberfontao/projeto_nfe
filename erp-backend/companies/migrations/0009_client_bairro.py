# Generated by Django 4.2.4 on 2024-05-19 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0008_enterprise_cnpj_enterprise_endereco_enterprise_ie_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='bairro',
            field=models.TextField(default='Bairro'),
            preserve_default=False,
        ),
    ]