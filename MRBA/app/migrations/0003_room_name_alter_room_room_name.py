# Generated by Django 4.0.6 on 2022-09-01 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_room_room_leave_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room_Name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_Name', models.CharField(max_length=122)),
            ],
        ),
        migrations.AlterField(
            model_name='room',
            name='room_Name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.room_name'),
        ),
    ]
