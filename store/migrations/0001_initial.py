
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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Tên danh mục')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, verbose_name='Mô tả')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Danh mục',
                'verbose_name_plural': 'Danh mục',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Tên sản phẩm')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(verbose_name='Mô tả')),
                ('price', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Giá')),
                ('unit', models.CharField(default='kg', max_length=50, verbose_name='Đơn vị')),
                ('image', models.ImageField(upload_to='products/', verbose_name='Hình ảnh')),
                ('stock', models.IntegerField(default=0, verbose_name='Số lượng')),
                ('is_available', models.BooleanField(default=True, verbose_name='Còn hàng')),
                ('is_organic', models.BooleanField(default=False, verbose_name='Hữu cơ')),
                ('origin', models.CharField(blank=True, max_length=200, verbose_name='Xuất xứ')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.category', verbose_name='Danh mục')),
            ],
            options={
                'verbose_name': 'Sản phẩm',
                'verbose_name_plural': 'Sản phẩm',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Giỏ hàng',
                'verbose_name_plural': 'Giỏ hàng',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='Họ tên')),
                ('phone', models.CharField(max_length=20, verbose_name='Số điện thoại')),
                ('address', models.TextField(verbose_name='Địa chỉ')),
                ('total_amount', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Tổng tiền')),
                ('status', models.CharField(choices=[('pending', 'Chờ xử lý'), ('processing', 'Đang xử lý'), ('shipped', 'Đang giao'), ('delivered', 'Đã giao'), ('cancelled', 'Đã hủy')], default='pending', max_length=20, verbose_name='Trạng thái')),
                ('note', models.TextField(blank=True, verbose_name='Ghi chú')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Đơn hàng',
                'verbose_name_plural': 'Đơn hàng',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'verbose_name': 'Chi tiết đơn hàng',
                'verbose_name_plural': 'Chi tiết đơn hàng',
            },
        ),
    ]
