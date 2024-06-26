# Generated by Django 4.2.4 on 2024-05-15 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_nfe_produtodetalhenfe'),
    ]

    operations = [
        migrations.AddField(
            model_name='nfe',
            name='destinatario_endereco',
            field=models.TextField(default='ENDERECO'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nfe',
            name='destinatario_nome',
            field=models.CharField(default='DESTINATARIO', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nfe',
            name='frete',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='nfe',
            name='emitente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.enterprise'),
        ),
        migrations.AlterField(
            model_name='produtodetalhenfe',
            name='cest',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='produtodetalhenfe',
            name='ncm',
            field=models.CharField(max_length=10),
        ),
    ]
