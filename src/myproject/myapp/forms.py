# forms.py
from django import forms
from .models import User, Advior, Exam

#Sinh viên
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['ma_so_sinh_vien', 'ho_ten', 'ma_lop', 'de_tai', 'giang_vien','trang_thai']
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['ma_so_sinh_vien', 'ho_ten', 'ma_lop', 'de_tai', 'giang_vien', 'trang_thai']
        widgets = {
            'ma_so_sinh_vien': forms.TextInput(attrs={'placeholder': 'Mã số sinh viên'}),
            'ho_ten': forms.TextInput(attrs={'placeholder': 'Họ tên'}),
            'ma_lop': forms.TextInput(attrs={'placeholder': 'Mã lớp'}),
            'de_tai': forms.TextInput(attrs={'placeholder': 'Đề tài'}),
            'giang_vien': forms.TextInput(attrs={'placeholder': 'Giảng viên'}),
            'trang_thai': forms.Select(attrs={'placeholder': 'Trạng thái'})
        }

#Giảng viên
class AdviorForm(forms.ModelForm):
    class Meta:
        model = Advior
        fields = ['ho_ten', 'chuyen_nganh', 'de_tai', 'tinh_trang']
class AdviorForm(forms.ModelForm):
    class Meta:
        model = Advior
        fields = ['ho_ten', 'chuyen_nganh', 'de_tai', 'tinh_trang']
        widgets = {
            'ho_ten': forms.TextInput(attrs={'placeholder': 'Họ tên '}),
            'chuyen_nganh': forms.TextInput(attrs={'placeholder': 'Chuyên ngành'}),
            'de_tai': forms.TextInput(attrs={'placeholder': 'Đề tài'}),
            'tinh_trang': forms.TextInput(attrs={'placeholder': 'Tình trạng'}),
        }
#Kết quả      
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['idstudent','tensv', 'project', 'diem_lan_1', 'diem_lan_2','diem_trung_binh', 'ghi_chu']
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['idstudent','tensv', 'project', 'diem_lan_1', 'diem_lan_2','diem_trung_binh', 'ghi_chu']
        widgets = {
            'idstudent': forms.TextInput(attrs={'placeholder': 'Mã số sinh viên '}),
            'tensv': forms.TextInput(attrs={'placeholder': 'Họ tên sinh viên '}),
            'project': forms.TextInput(attrs={'placeholder': 'Đồ án đề tài'}),
            'diem_lan_1': forms.NumberInput(attrs={'placeholder': 'Điểm lần 1'}),
            'diem_lan_2': forms.NumberInput(attrs={'placeholder': 'Điểm lần 1'}),
            'diem_trung_binh': forms.TextInput(attrs={'placeholder': 'Điểm trung bình', 'readonly': 'readonly'}),
            'ghi_chu': forms.TextInput(attrs={'placeholder': 'Ghi chú'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        
        diem_lan_1 = cleaned_data.get('diem_lan_1')
        diem_lan_2 = cleaned_data.get('diem_lan_2')
        if diem_lan_1 is not None and diem_lan_2 is not None:
            diem_trung_binh = (diem_lan_1 + diem_lan_2) / 2
            cleaned_data['diem_trung_binh'] = diem_trung_binh
        
        return cleaned_data        