# Generated by Django 4.2.4 on 2024-05-19 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0007_nfe_destinatario_endereco_nfe_destinatario_nome_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprise',
            name='cnpj',
            field=models.CharField(default='00000000000191', max_length=14),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='endereco',
            field=models.CharField(default='Rua Teste', max_length=255),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='ie',
            field=models.CharField(default='000000000001', max_length=12),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='municipio',
            field=models.CharField(default='São Paulo', max_length=255),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='uf',
            field=models.CharField(default='SP', max_length=2),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='name',
            field=models.CharField(default='Empresa', max_length=255),
        ),
    ]
