from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Complaint
from django.db.models import Case, When, Value, IntegerField
from django.utils.html import format_html



class ComplaintAdmin(admin.ModelAdmin):

    list_display = ['title', 'user', 'status', 'created_at']
    list_display += ['colored_priority', 'emotion_label', 'stress_score']

    list_editable = ['status']
    readonly_fields = ['user', 'title', 'description', 'created_at']

    fields = [
        'user',
        'title',
        'description',
        'status',
        'priority',
        'stress_score',
        'emotion_label',
        'reply',
        'created_at'
    ]

    def colored_priority(self, obj):
        color_map = {
            "Critical": "red",
            "High": "orange",
            "Medium": "gold",
            "Low": "green",
        }
        color = color_map.get(obj.priority, "black")
        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            obj.priority
        )

    colored_priority.short_description = "Priority"

    def save_model(self, request, obj, form, change):
        if change:
            subject = f"Complaint Update: {obj.title}"
            message = f"""
Hello {obj.user.username},

Your complaint has been updated.

Status: {obj.status}
Priority: {obj.priority}
Reply: {obj.reply or 'No reply'}

Regards,
Complaint Management System
"""
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [obj.user.email],
                fail_silently=True,
            )

        super().save_model(request, obj, form, change)

admin.site.register(Complaint, ComplaintAdmin)
