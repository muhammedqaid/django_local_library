# Generated by Django 4.1.3 on 2022-12-20 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_author_options_alter_book_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Enter a book genre (e.g. Science Fiction)', to='catalog.genre'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(help_text='Enter a book title', max_length=200),
        ),
    ]