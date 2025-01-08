from django.db import models
#---------------Quản lý sinh viên----------------- 
class User(models.Model):
    ma_so_sinh_vien = models.CharField(max_length=20, unique=True, verbose_name="Mã số sinh viên")
    ho_ten = models.CharField(max_length=100, verbose_name="Họ tên")
    ma_lop = models.CharField(max_length=20, verbose_name="Mã lớp")
    de_tai = models.CharField(max_length=200, verbose_name="Đề tài")
    giang_vien = models.CharField(max_length=100, verbose_name="Giảng viên")

    
    TRANG_THAI_CHOICES = [
        ('Đã đăng ký', 'Đã đăng ký'),
        ('Đang thực hiện', 'Đang thực hiện'),
        ('Đã hoàn thành', 'Đã hoàn thành'),
    ]
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, verbose_name="Trạng thái")

    def __str__(self):
        return f"{self.ma_so_sinh_vien} - {self.ho_ten} - {self.ma_lop} - {self.de_tai} - {self.giang_vien} -  {self.trang_thai} "

#---------------Quản lý giảng viên-----------------    
class Advior(models.Model):
    ho_ten = models.CharField(max_length=100, verbose_name="Họ tên")
    chuyen_nganh = models.CharField(max_length=20, verbose_name="Chuyên ngành")
    de_tai = models.CharField(max_length=200, verbose_name="Đề tài")
    
   
    TINH_TRANG_CHOICES = [
        ('Chưa nhận', 'Chưa nhận'),
        ('Đã nhận', 'Đã nhận'),
    ]
    tinh_trang = models.CharField(max_length=30, choices=TINH_TRANG_CHOICES, verbose_name="Tình trạng")
    
    def __str__(self):
        return f"{self.ho_ten} - {self.chuyen_nganh} - {self.de_tai} - {self.tinh_trang} "

#---------------Quản lý kết quả-----------------    
class Exam(models.Model):
    idstudent = models.CharField(max_length=255, verbose_name="MSSV")
    tensv = models.CharField(max_length=255, verbose_name="Họ tên sinh viên", default="")
    project = models.CharField(max_length=255, verbose_name="Đồ án đề tài")
    diem_lan_1 = models.FloatField(max_length=255, verbose_name="Điểm lần 1")
    diem_lan_2 = models.FloatField(max_length=255, verbose_name="Điểm lần 2")
    diem_trung_binh = models.FloatField(verbose_name="Điểm trung bình", default=0.0)
    ghi_chu = models.CharField(max_length=255, verbose_name="Ghi chú")   
    
    def save(self, *args, **kwargs):
        self.diem_trung_binh = (self.diem_lan_1 + self.diem_lan_2) / 2
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.idstudent} - {self.project} - {self.diem_lan_1} - {self.diem_lan_2} - {self.ghi_chu}"
    
