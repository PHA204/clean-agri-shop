from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=200,
        label='Họ và tên',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập họ và tên'
        })
    )
    phone = forms.CharField(
        max_length=20,
        label='Số điện thoại',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập số điện thoại'
        })
    )
    address = forms.CharField(
        label='Địa chỉ giao hàng',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Nhập địa chỉ giao hàng'
        })
    )
    note = forms.CharField(
        required=False,
        label='Ghi chú',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Ghi chú thêm (không bắt buộc)'
        })
    )

class ReviewForm(forms.Form):
    rating = forms.ChoiceField(
        choices=[(i, f'{i} sao') for i in range(1, 6)],
        label='Đánh giá',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    comment = forms.CharField(
        label='Nhận xét của bạn',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Chia sẻ trải nghiệm của bạn về sản phẩm này...'
        })
    )
