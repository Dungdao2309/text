from django.contrib import admin
from .models import Intern, Recruitment, TrainingProgram, Performance, Feedback

@admin.register(Intern)
class InternAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'status', 'university', 'start_date', 'end_date')
    search_fields = ('full_name', 'email', 'phone', 'university')
    list_filter = ('status', 'university', 'start_date', 'end_date')
    list_per_page = 20
    fieldsets = (
        ('Thông tin cá nhân', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address')
        }),
        ('Thông tin học vấn', {
            'fields': ('university', 'major')
        }),
        ('Thông tin thực tập', {
            'fields': ('start_date', 'end_date', 'status')
        }),
        ('Ảnh đại diện', {
            'fields': ('avatar',)
        }),
    )
    readonly_fields = ('full_name',)  # Trường full_name tự động được tạo, không cần chỉnh sửa

@admin.register(Recruitment)
class RecruitmentAdmin(admin.ModelAdmin):
    list_display = ('position', 'posted_by', 'posted_date', 'deadline', 'is_active')
    search_fields = ('position', 'posted_by__username', 'description')
    list_filter = ('posted_date', 'deadline', 'is_active')
    list_per_page = 20
    fieldsets = (
        ('Thông tin tuyển dụng', {
            'fields': ('position', 'description', 'requirements', 'location', 'salary_range')
        }),
        ('Thông tin người đăng', {
            'fields': ('posted_by', 'posted_date', 'deadline', 'is_active')
        }),
    )
    readonly_fields = ('posted_date',)  # Đánh dấu posted_date là chỉ đọc

@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'trainer', 'location', 'max_participants')
    search_fields = ('name', 'trainer', 'location')
    list_filter = ('start_date', 'end_date', 'trainer')
    list_per_page = 20
    fieldsets = (
        ('Thông tin chương trình', {
            'fields': ('name', 'description', 'start_date', 'end_date', 'location', 'trainer', 'max_participants')
        }),
        ('Thực tập sinh tham gia', {
            'fields': ('interns',)
        }),
    )
    filter_horizontal = ('interns',)  # Cho phép chọn nhiều thực tập sinh dễ dàng hơn

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('intern', 'evaluator', 'evaluation_period', 'score', 'is_final_evaluation')
    search_fields = ('intern__full_name', 'evaluator__username', 'evaluation_period')
    list_filter = ('evaluation_period', 'is_final_evaluation', 'evaluator')
    list_per_page = 20
    fieldsets = (
        ('Thông tin đánh giá', {
            'fields': ('intern', 'evaluator', 'evaluation_period', 'score', 'comments', 'is_final_evaluation')
        }),
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('intern', 'feedback_date', 'is_resolved', 'response_date')
    search_fields = ('intern__full_name', 'content')
    list_filter = ('feedback_date', 'is_resolved', 'response_date')
    list_per_page = 20
    fieldsets = (
        ('Thông tin phản hồi', {
            'fields': ('intern', 'content', 'is_resolved')
        }),
        ('Phản hồi từ quản lý', {
            'fields': ('response', 'response_date')
        }),
    )