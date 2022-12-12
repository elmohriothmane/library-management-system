# Generated by Django 4.0.8 on 2022-12-12 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_utilisateur_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='role',
            field=models.CharField(choices=[('libraire', 'ROLE_LIBRRAIRE'), ('client', 'ROLE_CLIENT'), ('admin', 'ROLE_ADMIN')], default='client', max_length=10),
        ),
    ]
