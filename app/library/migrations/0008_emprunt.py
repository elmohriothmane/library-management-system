# Generated by Django 2.2.12 on 2022-11-09 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_auto_20221109_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emprunt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_emprunt', models.DateTimeField(auto_now_add=True)),
                ('date_retour', models.DateTimeField(auto_now_add=True, null=True)),
                ('livre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livre_emprunte', to='library.Livre')),
            ],
        ),
    ]