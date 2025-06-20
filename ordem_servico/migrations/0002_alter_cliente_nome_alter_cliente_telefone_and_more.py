# Generated by Django 5.2.2 on 2025-06-14 21:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordem_servico', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='nome',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='nome',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='canal_venda',
            field=models.CharField(choices=[('presencial', 'Presencial'), ('online', 'Online')], default='presencial', max_length=10),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ordem_servico.cliente'),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='data_os',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='equipamento',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='marca',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='modelo',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='responsavel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='ordem_servico.funcionario'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='serie',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='situacao',
            field=models.CharField(choices=[('aberta', 'Aberta'), ('analise', 'Em Análise'), ('fechada', 'Fechada')], default='aberta', max_length=10),
        ),
        migrations.CreateModel(
            name='Anexo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to='anexos/')),
                ('descricao', models.CharField(blank=True, max_length=255)),
                ('ordem_servico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anexos', to='ordem_servico.ordemservico')),
            ],
        ),
    ]
