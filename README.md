# Clean Agri Shop - Website Thương Mại Điện Tử Nông Sản

Website bán nông sản sạch được xây dựng bằng Django với giao diện chuyên nghiệp.

## Tính năng

- ✅ Hiển thị danh sách sản phẩm nông sản
- ✅ Chi tiết sản phẩm với hình ảnh và mô tả
- ✅ Giỏ hàng (thêm, xóa, cập nhật số lượng)
- ✅ Đăng ký và đăng nhập người dùng
- ✅ Đặt hàng và quản lý đơn hàng
- ✅ Giao diện responsive với Bootstrap 5
- ✅ Tìm kiếm và lọc sản phẩm theo danh mục
- ✅ Admin panel để quản lý sản phẩm

## Cài đặt

### 1. Tạo môi trường ảo

\`\`\`bash
python -m venv venv
\`\`\`

### 2. Kích hoạt môi trường ảo

**Windows:**
\`\`\`bash
venv\Scripts\activate
\`\`\`

**Mac/Linux:**
\`\`\`bash
source venv/bin/activate
\`\`\`

### 3. Cài đặt các thư viện

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Chạy migrations

\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### 5. Tạo tài khoản admin

\`\`\`bash
python manage.py createsuperuser
\`\`\`

Nhập thông tin:
- Username: admin
- Email: admin@example.com
- Password: (nhập mật khẩu của bạn)

### 6. Chạy server

\`\`\`bash
python manage.py runserver
\`\`\`

Truy cập: http://127.0.0.1:8000

## Sử dụng

### Trang Admin

Truy cập: http://127.0.0.1:8000/admin

Đăng nhập bằng tài khoản admin đã tạo để:
- Thêm danh mục sản phẩm
- Thêm sản phẩm mới
- Quản lý đơn hàng
- Quản lý người dùng

### Thêm dữ liệu mẫu

1. Đăng nhập vào admin panel
2. Tạo các danh mục: Rau củ, Trái cây, Thực phẩm hữu cơ, v.v.
3. Thêm sản phẩm với hình ảnh, giá, mô tả

## Cấu trúc thư mục

\`\`\`
clean_agri_shop/
├── clean_agri_shop/          # Thư mục cấu hình project
│   ├── settings.py           # Cài đặt Django
│   ├── urls.py               # URL chính
│   └── wsgi.py
├── store/                    # App chính
│   ├── models.py             # Models (Product, Cart, Order)
│   ├── views.py              # Views xử lý logic
│   ├── urls.py               # URL routing
│   ├── admin.py              # Cấu hình admin
│   └── forms.py              # Forms
├── templates/                # HTML templates
│   ├── base.html             # Template gốc
│   └── store/                # Templates của store app
├── media/                    # Thư mục lưu hình ảnh
├── static/                   # CSS, JS, images tĩnh
├── manage.py
└── requirements.txt
\`\`\`

## Công nghệ sử dụng

- **Backend:** Django 5.0
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Database:** SQLite (mặc định)
- **Image Processing:** Pillow

## Tính năng nổi bật

### Giao diện
- Thiết kế hiện đại, chuyên nghiệp
- Màu sắc tự nhiên phù hợp với nông sản
- Responsive trên mọi thiết bị
- Icons và typography đẹp mắt

### Chức năng
- Tìm kiếm sản phẩm
- Lọc theo danh mục
- Giỏ hàng thông minh
- Quản lý đơn hàng
- Xác thực người dùng

## Hỗ trợ

Nếu gặp vấn đề, vui lòng tạo issue hoặc liên hệ.

## License

MIT License
