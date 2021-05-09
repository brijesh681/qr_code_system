# Generated by Django 3.1.4 on 2021-05-08 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.DateField(blank=True, default='2000-02-01', null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=30)),
                ('phone', models.CharField(max_length=12, null=True)),
                ('alternate_phone', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('address1', models.CharField(blank=True, default=' ', max_length=200)),
                ('address2', models.CharField(blank=True, default=' ', max_length=200)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.IntegerField(blank=True, default=0, null=True)),
                ('photo', models.ImageField(blank=True, upload_to='customer/photo/')),
                ('id_proof', models.CharField(choices=[('Aadhar Card', 'Aadhar Card'), ('Pan Card', 'Pan Card'), ('Driving License', 'Driving License'), ('Voter ID', 'Voter ID')], default='N/A', max_length=100)),
                ('id_proof_image', models.ImageField(blank=True, upload_to='customer/idproof/')),
                ('id_proof_image1', models.ImageField(blank=True, upload_to='customer/idproof/')),
                ('active', models.BooleanField(default=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('check_in_time', models.TimeField(auto_now_add=True, null=True)),
                ('check_out_time', models.TimeField(blank=True, null=True)),
                ('present', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer.customer')),
            ],
            options={
                'verbose_name_plural': 'Customer Attendance',
            },
        ),
    ]
