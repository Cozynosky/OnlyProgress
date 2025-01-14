# Generated by Django 4.2.1 on 2023-05-31 13:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profile', '0002_alter_profile_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(help_text='Date of measurement')),
                ('age', models.IntegerField(help_text='Age in years', validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(99)])),
                ('weight', models.DecimalField(decimal_places=1, help_text='Body mass in kg', max_digits=4, validators=[django.core.validators.MinValueValidator(40), django.core.validators.MaxValueValidator(200)])),
                ('height', models.DecimalField(decimal_places=1, help_text='Body height in cm', max_digits=4, validators=[django.core.validators.MinValueValidator(150), django.core.validators.MaxValueValidator(220)])),
                ('neck', models.DecimalField(decimal_places=1, help_text='Circumference in cm', max_digits=3, validators=[django.core.validators.MinValueValidator(20), django.core.validators.MaxValueValidator(60)])),
                ('chest', models.DecimalField(decimal_places=1, help_text='Circumference in cm', max_digits=4, validators=[django.core.validators.MinValueValidator(60), django.core.validators.MaxValueValidator(140)])),
                ('abdomen', models.DecimalField(decimal_places=1, help_text='Circumference in cm', max_digits=4, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(150)])),
                ('hip', models.DecimalField(decimal_places=1, help_text='Circumference in cm', max_digits=4, validators=[django.core.validators.MinValueValidator(80), django.core.validators.MaxValueValidator(130)])),
                ('thigh', models.DecimalField(decimal_places=1, help_text='Circumference in cm', max_digits=3, validators=[django.core.validators.MinValueValidator(40), django.core.validators.MaxValueValidator(80)])),
                ('knee', models.DecimalField(decimal_places=1, help_text='Circumference in cm', max_digits=3, validators=[django.core.validators.MinValueValidator(26), django.core.validators.MaxValueValidator(55)])),
                ('ankle', models.DecimalField(decimal_places=1, help_text='Circumference in cm', max_digits=3, validators=[django.core.validators.MinValueValidator(14), django.core.validators.MaxValueValidator(35)])),
                ('biceps', models.DecimalField(decimal_places=1, help_text='Circumference in cm', max_digits=3, validators=[django.core.validators.MinValueValidator(20), django.core.validators.MaxValueValidator(50)])),
                ('forearm', models.DecimalField(decimal_places=1, help_text='Circumference in cm', max_digits=3, validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(38)])),
                ('wrist', models.DecimalField(decimal_places=1, help_text='Circumference in cm', max_digits=3, validators=[django.core.validators.MinValueValidator(11), django.core.validators.MaxValueValidator(25)])),
                ('bmi', models.DecimalField(decimal_places=2, help_text='Body mass index', max_digits=4, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(60)])),
                ('bodyfat', models.DecimalField(decimal_places=2, help_text='Bodyfat %', max_digits=4)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.profile')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
