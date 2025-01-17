from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.conf import settings
from django.core.signing import TimestampSigner, BadSignature
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.password_validation import validate_password
import logging
from .models import Intern, TrainingProgram, Task, Notification

logger = logging.getLogger(__name__)

# Hàm gửi email xác thực tài khoản
def send_activation_email(user, request):
    try:
        signer = TimestampSigner()
        token = signer.sign(user.email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"http://{request.get_host()}/activate/{uid}/{token}/"
        
        subject = 'Kích hoạt tài khoản của bạn'
        message = f'Xin chào {user.username},\n\nVui lòng nhấp vào liên kết dưới đây để kích hoạt tài khoản của bạn:\n\n{activation_link}\n\nNếu bạn không yêu cầu điều này, vui lòng bỏ qua email này.'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
    except Exception as e:
        logger.error(f"Lỗi khi gửi email kích hoạt: {str(e)}")
        raise  # Ném lại lỗi để xử lý ở hàm gọi

# Hàm gửi email đặt lại mật khẩu
def send_password_reset_email(user, request):
    try:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://{request.get_host()}/reset-password/{uid}/{token}/"
        
        subject = 'Yêu cầu đặt lại mật khẩu'
        message = f'Xin chào {user.username},\n\nBạn đã yêu cầu đặt lại mật khẩu. Vui lòng nhấp vào liên kết dưới đây để đặt lại mật khẩu:\n\n{reset_link}\n\nNếu bạn không yêu cầu điều này, vui lòng bỏ qua email này.'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
    except Exception as e:
        logger.error(f"Lỗi khi gửi email đặt lại mật khẩu: {str(e)}")
        raise  # Ném lại lỗi để xử lý ở hàm gọi

# Trang chủ

@login_required
@login_required
def home(request):
    # Tính toán dữ liệu
    active_interns = Intern.objects.filter(is_active=True).count()  # Số sinh viên đang hoạt động
    training_programs = TrainingProgram.objects.count()  # Số chương trình đào tạo
    completed_tasks = Task.objects.filter(status='completed').count()  # Số công việc đã hoàn thành
    total_tasks = Task.objects.count()  # Tổng số công việc
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0  # Tỷ lệ hoàn thành

    # Kiểm tra nhóm của người dùng
    is_admin = request.user.groups.filter(name='Admin').exists()
    is_hr_manager = request.user.groups.filter(name='HR Managers').exists()
    is_intern = request.user.groups.filter(name='Interns').exists()
    is_internship_coordinator = request.user.groups.filter(name='Internship Coordinators').exists()
    is_mentor = request.user.groups.filter(name='Mentors').exists()

    # Truyền dữ liệu vào context
    context = {
        'completed_tasks': completed_tasks,
        'remaining_tasks': total_tasks - completed_tasks,
        'active_interns': active_interns,
        'training_programs': training_programs,
        'completion_rate': completion_rate,
        'is_admin': is_admin,
        'is_hr_manager': is_hr_manager,
        'is_intern': is_intern,
        'is_internship_coordinator': is_internship_coordinator,
        'is_mentor': is_mentor,
    }
    return render(request, 'home/index.html', context)

# Trang quản lý tuyển dụng
def quanlituyendung(request):
    return render(request, 'Quanlituyendung/quanlituyendung.html')

# Trang lịch phỏng vấn
def lichphongvan(request):
    return render(request, 'Lichphongvan/lichphongvan.html')

# Trang chương trình đào tạo
def chuongtrinhdaotao(request):
    return render(request, 'Chuongtrinhdaotao/chuongtrinhdaotao.html')

# Trang theo dõi hiệu suất
def theodoihieusuat(request):
    return render(request, 'Theodoihieusuat/theodoihieusuat.html')

# Trang giao tiếp và phản hồi
def giaotiepvaphanhoi(request):
    return render(request, 'Giaotiepvaphanhoi/giaotiepvaphanhoi.html')

# Trang quản lý hồ sơ
def quanlyhoso(request):
    return render(request, 'Quanlyhoso/quanlyhoso.html')

# Trang báo cáo và phân tích
def baocaovaphantich(request):
    return render(request, 'Baocaovaphantich/baocaovaphantich.html')

# Trang cấu hình hệ thống (chỉ admin)
@user_passes_test(lambda u: u.is_superuser)
def cauhinhhethong(request):
    return render(request, 'Cauhinhhethong/cauhinhhethong.html')

# Trang bảo mật và quyền hạn
def baomatvaquyenhan(request):
    return render(request, 'baomatvaquyenhan/baomatvaquyenhan.html')

# Trang hồ sơ cá nhân (yêu cầu đăng nhập)
@login_required
def myprofile(request):
    return render(request, 'home/myprofile/myprofile.html')

# Trang báo cáo (yêu cầu đăng nhập)
@login_required
def reports(request):
    return render(request, 'home/reports/reports.html')

# Trang hỗ trợ
def helpvasupport(request):
    return render(request, 'home/HelpvaSupport/helpvasupport.html')

# Đăng xuất
def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('sessionid')  # Xóa cookie khi đăng xuất
    return response

# Đăng nhập
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberMe')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                
                if remember_me:
                    request.session.set_expiry(30 * 24 * 60 * 60)  # Ghi nhớ đăng nhập trong 30 ngày
                else:
                    request.session.set_expiry(0)  # Không ghi nhớ đăng nhập

                return redirect('home')
            else:
                messages.error(request, 'Tài khoản của bạn chưa được kích hoạt. Vui lòng kiểm tra email để kích hoạt.')
                return redirect('login')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại.')
            return redirect('login')

    return render(request, 'home/login.html')

# Đăng ký
def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Kiểm tra mật khẩu có khớp không
        if password != confirm_password:
            messages.error(request, 'Mật khẩu không khớp. Vui lòng thử lại.')
            return redirect('register')

        # Kiểm tra tính hợp lệ của email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Email không hợp lệ. Vui lòng nhập email đúng định dạng.')
            return redirect('register')

        # Kiểm tra email đã tồn tại chưa
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email đã tồn tại. Vui lòng sử dụng email khác.')
            return redirect('register')

        # Tạo tài khoản mới
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_name
            user.is_active = False  # Tài khoản chưa được kích hoạt
            user.save()

            # Gửi email xác thực
            send_activation_email(user, request)

            # Thông báo thành công và chuyển hướng đến trang đăng nhập
            messages.success(request, 'Tài khoản đã được tạo thành công. Vui lòng kiểm tra email để kích hoạt.')
            return redirect('login')
        except Exception as e:
            # Thông báo lỗi nếu có vấn đề khi tạo tài khoản
            messages.error(request, f'Lỗi khi tạo tài khoản: {str(e)}')
            return redirect('register')

    # Nếu không phải là POST request, hiển thị trang đăng ký
    return render(request, 'home/register.html')

# Xác thực tài khoản
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        signer = TimestampSigner()
        email = signer.unsign(token, max_age=86400)  # Token hết hạn sau 24 giờ
        
        if user.email == email:
            user.is_active = True
            user.save()
            messages.success(request, 'Tài khoản của bạn đã được kích hoạt. Vui lòng đăng nhập.')
            return redirect('login')
        else:
            messages.error(request, 'Liên kết kích hoạt không hợp lệ.')
            return redirect('home')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, BadSignature, ValidationError):
        messages.error(request, 'Liên kết kích hoạt không hợp lệ hoặc đã hết hạn.')
        return redirect('home')

# Quên mật khẩu
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            validate_email(email)  # Kiểm tra tính hợp lệ của email
        except ValidationError:
            messages.error(request, 'Email không hợp lệ.')
            return redirect('forgot_password')

        try:
            user = User.objects.get(email=email)
            send_password_reset_email(user, request)
            messages.success(request, 'Hướng dẫn đặt lại mật khẩu đã được gửi đến email của bạn.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Không tìm thấy người dùng với email này.')
    
    return render(request, 'home/forgot_password.html')

# Đặt lại mật khẩu
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirmPassword')
                
                if password == confirm_password:
                    try:
                        validate_password(password, user)  # Kiểm tra tính hợp lệ của mật khẩu
                        user.set_password(password)
                        user.save()
                        messages.success(request, 'Mật khẩu của bạn đã được đặt lại. Vui lòng đăng nhập.')
                        return redirect('login')
                    except ValidationError as e:
                        messages.error(request, f'Mật khẩu không hợp lệ: {", ".join(e.messages)}')
                else:
                    messages.error(request, 'Mật khẩu không khớp.')
            return render(request, 'home/reset_password.html')
        else:
            messages.error(request, 'Liên kết đặt lại mật khẩu không hợp lệ.')
            return redirect('home')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Liên kết đặt lại mật khẩu không hợp lệ.')
        return redirect('home')