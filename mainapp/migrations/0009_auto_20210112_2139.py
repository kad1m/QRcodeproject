# Generated by Django 3.1.4 on 2021-01-12 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_product_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='profile'),
        ),
        migrations.AddField(
            model_name='customer',
            name='currency_symbol',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.currency'),
        ),
    ]
