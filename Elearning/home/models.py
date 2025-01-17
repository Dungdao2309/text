from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.urls import reverse

# Validator cho số điện thoại
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Số điện thoại phải có định dạng hợp lệ."
)

class Intern(models.Model):
    # Thông tin cơ bản của thực tập sinh
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Tài khoản", related_name="intern_profile")
    first_name = models.CharField(max_length=100, verbose_name="Tên")
    last_name = models.CharField(max_length=100, verbose_name="Họ")
    full_name = models.CharField(max_length=200, blank=True, verbose_name="Họ và tên")
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Nhập địa chỉ email hợp lệ")
    phone = models.CharField(max_length=15, validators=[phone_validator], verbose_name="Số điện thoại", help_text="Nhập số điện thoại theo định dạng quốc tế, ví dụ: +84123456789")
    address = models.TextField(verbose_name="Địa chỉ")
    date_of_birth = models.DateField(verbose_name="Ngày sinh")
    university = models.CharField(max_length=200, verbose_name="Trường đại học")
    major = models.CharField(max_length=200, verbose_name="Chuyên ngành")
    start_date = models.DateField(verbose_name="Ngày bắt đầu thực tập")
    end_date = models.DateField(verbose_name="Ngày kết thúc thực tập")
    avatar = models.ImageField(upload_to='interns/avatars/', blank=True, null=True, verbose_name="Ảnh đại diện")
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Đang thực tập'),
            ('completed', 'Đã hoàn thành'),
            ('terminated', 'Đã chấm dứt'),
        ],
        default='active',
        verbose_name="Trạng thái"
    )
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return self.full_name if self.full_name else f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Ngày bắt đầu không thể lớn hơn ngày kết thúc.")

    def get_absolute_url(self):
        return reverse('intern_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Thực tập sinh"
        verbose_name_plural = "Thực tập sinh"
        ordering = ['-created_at']


class Recruitment(models.Model):
    # Thông tin tuyển dụng
    position = models.CharField(max_length=200, verbose_name="Vị trí tuyển dụng")
    description = models.TextField(verbose_name="Mô tả công việc")
    requirements = models.TextField(verbose_name="Yêu cầu")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Địa điểm")
    salary_range = models.CharField(max_length=100, blank=True, null=True, verbose_name="Mức lương")
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người đăng", related_name="recruitments")
    posted_date = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng")
    deadline = models.DateField(verbose_name="Hạn nộp hồ sơ")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")

    def __str__(self):
        return self.position

    def get_absolute_url(self):
        return reverse('recruitment_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Tuyển dụng"
        verbose_name_plural = "Tuyển dụng"
        ordering = ['-posted_date']


class TrainingProgram(models.Model):
    # Chương trình đào tạo
    name = models.CharField(max_length=200, verbose_name="Tên chương trình")
    description = models.TextField(verbose_name="Mô tả")
    start_date = models.DateField(verbose_name="Ngày bắt đầu")
    end_date = models.DateField(verbose_name="Ngày kết thúc")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Địa điểm")
    trainer = models.CharField(max_length=200, verbose_name="Người đào tạo")
    max_participants = models.PositiveIntegerField(default=0, verbose_name="Số lượng tối đa")
    interns = models.ManyToManyField(Intern, related_name='training_programs', verbose_name="Thực tập sinh")
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Đang hoạt động'),
            ('completed', 'Đã hoàn thành'),
            ('cancelled', 'Đã hủy'),
        ],
        default='active',
        verbose_name="Trạng thái"
    )

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Ngày bắt đầu không thể lớn hơn ngày kết thúc.")

    def get_absolute_url(self):
        return reverse('training_program_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Chương trình đào tạo"
        verbose_name_plural = "Chương trình đào tạo"
        ordering = ['-start_date']


class Performance(models.Model):
    # Đánh giá hiệu suất
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE, verbose_name="Thực tập sinh", related_name="performances")
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người đánh giá", related_name="evaluations")
    evaluation_date = models.DateField(auto_now_add=True, verbose_name="Ngày đánh giá")
    evaluation_period = models.CharField(max_length=100, verbose_name="Kỳ đánh giá")
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Điểm số")
    comments = models.TextField(verbose_name="Nhận xét")
    is_final_evaluation = models.BooleanField(default=False, verbose_name="Đánh giá cuối kỳ")
    rating = models.PositiveSmallIntegerField(
        choices=[
            (1, 'Rất kém'),
            (2, 'Kém'),
            (3, 'Trung bình'),
            (4, 'Tốt'),
            (5, 'Xuất sắc'),
        ],
        default=3,
        verbose_name="Đánh giá"
    )

    def __str__(self):
        return f"Đánh giá của {self.evaluator} cho {self.intern}"

    class Meta:
        verbose_name = "Đánh giá hiệu suất"
        verbose_name_plural = "Đánh giá hiệu suất"


class Feedback(models.Model):
    # Phản hồi từ thực tập sinh
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE, verbose_name="Thực tập sinh", related_name="feedbacks")
    feedback_date = models.DateField(auto_now_add=True, verbose_name="Ngày phản hồi")
    content = models.TextField(verbose_name="Nội dung phản hồi")
    response = models.TextField(blank=True, null=True, verbose_name="Phản hồi từ quản lý")
    response_date = models.DateField(blank=True, null=True, verbose_name="Ngày phản hồi")
    is_resolved = models.BooleanField(default=False, verbose_name="Đã giải quyết")

    def __str__(self):
        return f"Phản hồi từ {self.intern}"

    class Meta:
        verbose_name = "Phản hồi"
        verbose_name_plural = "Phản hồi"


class Task(models.Model):
    # Công việc
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Thấp'),
        ('medium', 'Trung bình'),
        ('high', 'Cao'),
    ]

    title = models.CharField(max_length=255, verbose_name="Tiêu đề")
    description = models.TextField(verbose_name="Mô tả")
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người được giao", related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Mức độ ưu tiên")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Công việc"
        verbose_name_plural = "Công việc"
        ordering = ['-created_at']


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người dùng", related_name="notifications")
    message = models.TextField(verbose_name="Nội dung thông báo")
    is_read = models.BooleanField(default=False, verbose_name="Đã đọc")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return f"Thông báo cho {self.user.username}"

    class Meta:
        verbose_name = "Thông báo"
        verbose_name_plural = "Thông báo"
        ordering = ['-created_at']