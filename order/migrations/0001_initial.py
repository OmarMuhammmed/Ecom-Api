# Generated by Django 3.2.6 on 2024-07-31 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion



class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0004_rename_reting_review_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default='', max_length=100)),
                ('zip_code', models.IntegerField(max_length=20)),
                ('street', models.CharField(default='', max_length=500)),
                ('country', models.CharField(default='', max_length=50)),
                
                ('state', models.CharField(default='', max_length=50)),
                ('total', models.IntegerField(default=0)),
                ('pyment_status', models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', max_length=100)),
                ('pyment_metod', models.CharField(choices=[('COD', 'Cod'), ('CARD', 'Card')], default='COD', max_length=100)),
                ('status', models.CharField(choices=[('Prossing', 'Prossing'), ('SHIPPED', 'Shipped'), ('Deleverd', 'Deleverd')], default='Prossing', max_length=100)),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orderitmes', to='order.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product')),
            ],
        ),
    ]
