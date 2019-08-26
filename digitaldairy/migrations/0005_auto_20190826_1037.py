# Generated by Django 2.2 on 2019-08-26 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldairy', '0004_milkconsumptions_milksales_milksalespayments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='milksalespayments',
            old_name='from_date',
            new_name='milk_sale_date',
        ),
        migrations.RemoveField(
            model_name='milksalespayments',
            name='to_date',
        ),
        migrations.AlterField(
            model_name='semenrecords',
            name='bull_code',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]