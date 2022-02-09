# Generated by Django 3.2.9 on 2022-02-08 14:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('bill_id', models.AutoField(primary_key=True, serialize=False)),
                ('billing_date', models.DateField(default=django.utils.timezone.now)),
                ('billing_address', models.CharField(blank=True, max_length=100)),
                ('total_cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cust_id', models.AutoField(primary_key=True, serialize=False)),
                ('cust_name', models.CharField(max_length=100)),
                ('cust_tel_no', models.CharField(max_length=11)),
                ('cust_email', models.CharField(max_length=100)),
                ('cust_budget_code', models.IntegerField()),
                ('cust_type', models.FloatField(choices=[(0.5, 'In-House'), (1.0, 'Normal'), (1.5, 'Outside')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_date', models.DateField(default=django.utils.timezone.now)),
                ('num_samples', models.IntegerField()),
                ('specimen_procedure', models.CharField(blank=True, max_length=500)),
                ('chemical_fixation', models.CharField(blank=True, max_length=100)),
                ('neg_staining', models.CharField(blank=True, max_length=100)),
                ('cryofixation', models.CharField(blank=True, max_length=100)),
                ('tem_embedding_schedule', models.CharField(blank=True, max_length=100)),
                ('dehydration', models.CharField(blank=True, max_length=100)),
                ('resin', models.CharField(blank=True, max_length=100)),
                ('sem', models.CharField(blank=True, max_length=3)),
                ('sem_mount', models.CharField(blank=True, max_length=50)),
                ('fd', models.CharField(blank=True, max_length=50)),
                ('cpd', models.CharField(blank=True, max_length=50)),
                ('sem_cost', models.CharField(blank=True, max_length=50)),
                ('temp_time', models.CharField(blank=True, max_length=50)),
                ('immunolabelling', models.CharField(blank=True, max_length=100)),
                ('first_dilution_time', models.CharField(blank=True, max_length=100)),
                ('second_dilution_time', models.CharField(blank=True, max_length=100)),
                ('contrast_staining', models.CharField(blank=True, max_length=100)),
                ('comments_results', models.CharField(blank=True, max_length=500)),
                ('status', models.IntegerField(choices=[(0, 'Prep'), (1, 'Section'), (2, 'Image'), (3, 'Bill')], default=0)),
                ('cust_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imaging_system_app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('service_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('normal_price', models.FloatField()),
                ('in_house_price', models.FloatField()),
                ('outside_price', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('worker_id', models.AutoField(primary_key=True, serialize=False)),
                ('worker_name', models.CharField(max_length=100)),
                ('worker_tel_no', models.CharField(max_length=11)),
                ('worker_email', models.CharField(max_length=100)),
                ('cust_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imaging_system_app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='WorkerProjectBridge',
            fields=[
                ('worker_project_bridge_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imaging_system_app.project')),
                ('worker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imaging_system_app.worker')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectBillDetails',
            fields=[
                ('project_bill_id', models.AutoField(primary_key=True, serialize=False)),
                ('jeol1200tem_unit', models.FloatField(blank=True, null=True)),
                ('jeol100sem_unit', models.FloatField(blank=True, null=True)),
                ('tem_processing_unit', models.IntegerField(blank=True, null=True)),
                ('sectioning_stained_unit', models.IntegerField(blank=True, null=True)),
                ('sectioning_contrast_stained_unit', models.IntegerField(blank=True, null=True)),
                ('negative_staining_unit', models.IntegerField(blank=True, null=True)),
                ('sem_processing_mounting_unit', models.IntegerField(blank=True, null=True)),
                ('sem_processing_fd_unit', models.IntegerField(blank=True, null=True)),
                ('sem_unit', models.IntegerField(blank=True, null=True)),
                ('immunolabelling_unit', models.IntegerField(blank=True, null=True)),
                ('cryosectioning_unit', models.IntegerField(blank=True, null=True)),
                ('freeze_fracture_unit', models.IntegerField(blank=True, null=True)),
                ('ir_white_unit', models.IntegerField(blank=True, null=True)),
                ('extra1_name', models.CharField(blank=True, max_length=100)),
                ('extra1_cost', models.FloatField(blank=True, null=True)),
                ('extra2_name', models.CharField(blank=True, max_length=100)),
                ('extra2_cost', models.FloatField(blank=True, null=True)),
                ('extra3_name', models.CharField(blank=True, max_length=100)),
                ('extra3_cost', models.FloatField(blank=True, null=True)),
                ('total', models.FloatField()),
                ('project_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='imaging_system_app.project')),
            ],
            options={
                'verbose_name_plural': 'Project bill details',
            },
        ),
        migrations.CreateModel(
            name='ProjectBillBridge',
            fields=[
                ('project_bill_bridge_id', models.AutoField(primary_key=True, serialize=False)),
                ('bill_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imaging_system_app.bill')),
                ('project_bill_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imaging_system_app.projectbilldetails')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='cust_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imaging_system_app.customer'),
        ),
    ]
