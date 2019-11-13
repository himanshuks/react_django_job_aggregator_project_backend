# Generated by Django 2.2.5 on 2019-10-30 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=100, unique=True)),
                ('cost_per_transaction', models.FloatField()),
                ('duration', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='UserSubscriptionPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_start_datetime', models.DateTimeField(auto_now_add=True)),
                ('subscription_end_datetime', models.DateTimeField()),
                ('payment_details', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_subscription_plan', to='payments.PaymentDetail')),
                ('subscription_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscription_plan', to='subscriptionplans.SubscriptionPlan')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_subscription_plan', to='payments.Transaction')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscription_plan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
