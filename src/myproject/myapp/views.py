from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User as AuthUser
from django.contrib import messages
from .models import User, Advior, Exam
from .forms import UserForm, AdviorForm, ExamForm
import matplotlib
matplotlib.use('Agg')  # Sử dụng backend không giao diện
import matplotlib.pyplot as plt
from io import BytesIO
import base64
def is_admin(user):
    return user.is_superuser
#Đăng kí
def register(request):
    if request.method == 'POST':
        regname = request.POST['username']
        regpassword = request.POST['password']
        regemail = request.POST['email'] 
        if AuthUser.objects.filter(username=regname).exists():
            messages.error(request, 'Tài khoản đã tồn tại trước đó!')
        elif AuthUser.objects.filter(email=regemail).exists():
            messages.error(request, 'Email đã được sử dụng!')
        else:
            user = AuthUser.objects.create_user(username=regname, password=regpassword, email=regemail)
            user.save()
            messages.success(request, 'Đăng ký thành công! Bạn có thể đăng nhập.')
            return redirect('login')
    return render(request, 'register.html')

#Đăng nhập
def ad_login(request):
    if request.method == 'POST':
        logname = request.POST['username']
        logpassword = request.POST['password']
        admin = authenticate(request, username=logname, password=logpassword)
        if admin is not None:
            login(request, admin)
            return redirect('home')
        else:
            messages.error(request, 'Sai thông tin tài khoản hoặc mật khẩu')
    return render(request, 'login.html')

#Đăng xuất
def ad_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            context['show_statistics'] = True
        elif request.user.groups.filter(name='Teachers').exists():
            context['show_statistics'] = False
    return render(request, 'index.html', context)

#Sinh viên
def user_list(request):
    users = User.objects.all()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            #Thông báo sinh viên trùng đề tài với sinh viên khác
            if User.objects.filter(de_tai=new_user.de_tai).exists():
                messages.error(request, 'Đề tài này đã được đăng ký bởi sinh viên khác.')
                return redirect('user_list')
            #Thêm 1 sinh viên đăng ký thì bên kết quả xuất hiện nhưng chưa có điểm, ghi chú
            new_user = form.save()
            Exam.objects.create(
                idstudent=new_user.ma_so_sinh_vien,
                tensv=new_user.ho_ten,
                project=new_user.de_tai,
                diem_lan_1=0, 
                diem_lan_2=0,  
                diem_trung_binh=0,  
                ghi_chu=""  
            )
            try:
                advisor = Advior.objects.filter(ho_ten=new_user.giang_vien).first()
                if advisor:
                    advisor.tinh_trang = 'Đã nhận'
                    advisor.save()
                messages.success(request, 'Sinh viên được thêm thành công!')
            except Advior.DoesNotExist:
                pass
            return redirect('user_list')
    else:
        form = UserForm()
    #Cập nhật trạng thái sinh viên đang làm đồ án
    if 'trang_thai' in request.POST:
        ma_so_sinh_vien = request.POST.get('ma_so_sinh_vien')
        trang_thai = request.POST.get('trang_thai')
        user = User.objects.get(ma_so_sinh_vien=ma_so_sinh_vien)
        user.trang_thai = trang_thai
        user.save()
        return redirect('user_list')
    search_query = request.GET.get('q', '')    # Tìm kiếm
    users = User.objects.all()
    if search_query:
        users = users.filter(ho_ten__icontains=search_query) | users.filter(ma_so_sinh_vien__icontains=search_query)
    return render(request, 'user_list.html', {'form': form, 'users': users,})


#Chỉnh sửa sinh viên
def edit_user(request, ma_so_sinh_vien):
    user = get_object_or_404(User, ma_so_sinh_vien=ma_so_sinh_vien)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

# Xóa sinh viên
def delete_user(request, ma_so_sinh_vien):
    user = get_object_or_404(User, ma_so_sinh_vien=ma_so_sinh_vien)
    #Xóa sinh viên thì bên quản lý giảng viên mất theo 
    giang_vien_ten = user.giang_vien
    if giang_vien_ten:
        try:
            advior = Advior.objects.get(ho_ten=giang_vien_ten)
            advior.tinh_trang = "Chưa nhận" 
            advior.save()
        except Advior.DoesNotExist:
            pass
    #Xóa sinh viên thì bên quản lý kết quả mất theo    
    exams = Exam.objects.filter(idstudent=ma_so_sinh_vien)
    if exams.exists():
        exams.delete()    
    user.delete()
    return redirect('user_list')

#Giảng viên
def advior_list(request):
    adviors = Advior.objects.all()
    users = User.objects.all()
# Thêm giảng viên mới
    if request.method == 'POST' and 'add_advior' in request.POST:
        form = AdviorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('advior_list')
    else:
        form = AdviorForm() 
# Cập nhật tình trạng của giảng viên
    if request.method == 'POST' and 'update_status' in request.POST:  
        ho_ten = request.POST.get('ho_ten')
        tinh_trang = request.POST.get('tinh_trang')
        try:
            advior = Advior.objects.get(ho_ten=ho_ten)
            advior.tinh_trang = tinh_trang
            advior.save()
            return redirect('advior_list') 
        except Advior.DoesNotExist:
            return HttpResponse("Giảng viên không tồn tại", status=404)
    search_query = request.GET.get('q', '')    # Tìm kiếm
    adviors = Advior.objects.all()
    if search_query:
        adviors = adviors.filter(ho_ten__icontains=search_query)
    return render(request, 'advior_list.html', {'form': form,'users': users, 'adviors': adviors})


# Chỉnh sửa giảng viên
def edit_advior(request, id):
    advior = get_object_or_404(Advior, id=id)
    if request.method == 'POST':
        form = AdviorForm(request.POST, instance=advior)
        if form.is_valid():
            # Lưu lại trạng thái giảng viên trước khi thay đổi đề tài
            original_de_tai = advior.de_tai  # Lưu đề tài hiện tại của giảng viên
            # Lưu form với dữ liệu mới
            form.save()
            # Kiểm tra nếu đề tài đã thay đổi
            if advior.de_tai != original_de_tai:
                advior.tinh_trang = 'Chưa nhận'  # Cập nhật trạng thái thành "Chưa nhận"
                advior.save()
            # Thông báo thành công
            messages.success(request, 'Giảng viên đã được cập nhật thành công!')
            return redirect('advior_list')
    else:
        form = AdviorForm(instance=advior)
    
    return render(request, 'edit_advior.html', {'form': form})

# Xóa giảng viên
def delete_advior(request, id):
    # Truy vấn giảng viên theo tên
    advior = get_object_or_404(Advior, id=id)
    # Lọc sinh viên có giảng viên là giảng viên này và cập nhật trạng thái
    users = User.objects.filter(giang_vien=advior.ho_ten)
    for user in users:
        user.giang_vien = ''  # Tự động trả về tình trạng "Chưa nhận" khi xóa sinh viên bên quản lý sinh viên
        user.save()
    # Kiểm tra nếu không có sinh viên nào đăng ký đề tài với giảng viên này, chuyển trạng thái về "Chưa nhận"
    if not User.objects.filter(giang_vien=advior.ho_ten).exists():
        advior.tinh_trang = "Chưa nhận"
        advior.save()
    # Xóa giảng viên
    advior.delete()
    return redirect('advior_list')


#Kết quả
def exam_list(request):
    exams = Exam.objects.all()
    #Thêm mới kết quả
    if request.method == 'POST' and 'add_exam' in request.POST:
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False) 
            exam.diem_trung_binh = (exam.diem_lan_1 + exam.diem_lan_2) / 2  
            exam.save()  
            return redirect('exam_list')
    #Cập nhật ghi chú
    if request.method == 'POST' and 'update_note' in request.POST:
        idstudent = request.POST.get('MSSV')
        ghi_chu = request.POST.get('ghi_chu')
        exam = get_object_or_404(Exam, idstudent=idstudent)
        exam.ghi_chu = ghi_chu
        exam.save()
        return redirect('exam_list')
    form = ExamForm()
    search_query = request.GET.get('q', '')    # Tìm sinh viên
    exams = Exam.objects.all()
    if search_query:
        exams = exams.filter(tensv__icontains=search_query) | exams.filter(idstudent__icontains=search_query)
    return render(request, 'exam_list.html', {'form': form, 'exams': exams})


#Chỉnh sửa kết quả
def edit_exam(request, idstudent):
    exam = get_object_or_404(Exam, idstudent=idstudent)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'edit_exam.html', {'form': form})

# Xóa kết quả
def delete_exam(request, idstudent):
    exams = Exam.objects.filter(idstudent=idstudent)
    if exams.exists():
        exams.delete()
    return redirect('exam_list')


@login_required
@user_passes_test(is_admin, login_url='/')
def export_results(request):
    exams = Exam.objects.all()
    total_students = exams.count()  # Tổng số sinh viên có kết quả
    students_above_4 = exams.filter(diem_trung_binh__gt=4.0).count()  # Số sinh viên đạt điểm trên 4.0
    total_registered_students = User.objects.count()  # Tổng số sinh viên đã đăng ký
    # Sử dụng thư viện matplotlib
    labels = ['Đã đăng ký', 'Có kết quả', 'Trên 4.0']
    values = [total_registered_students, total_students, students_above_4]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color=['blue', 'green', 'orange'])
    plt.title('Thống kê kết quả sinh viên')
    plt.xlabel('Trạng thái')
    plt.ylabel('Số lượng')
    plt.tight_layout()
    # Chuyển biểu đồ thành ảnh base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    return render(request, 'export_results.html', {
        'total_students': total_students,
        'students_above_4': students_above_4,
        'total_registered_students': total_registered_students,
        'exam_details': exams,
        'chart': graphic,
    })
