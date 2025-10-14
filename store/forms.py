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
