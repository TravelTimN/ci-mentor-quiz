# Generated by Django 3.2.9 on 2022-11-16 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0004_alter_quiz_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='description',
            field=models.CharField(default='Quiz details for blah blah', max_length=100),
            preserve_default=False,
        ),
    ]
