# Generated by Django 5.1.3 on 2024-12-21 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_exam_tensv_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advior',
            name='ho_ten',
            field=models.CharField(max_length=100, verbose_name='Họ tên'),
        ),
    ]