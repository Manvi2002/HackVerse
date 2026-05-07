from django.contrib import admin
from django.utils.html import format_html
from .models import Hackathon, Team, Submission, JudgeAssignment, Score

@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    search_fields = ('title', 'theme')
    list_filter = ('is_active',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'hackathon', 'leader', 'created_at')
    search_fields = ('name', 'hackathon__title', 'leader__username')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'team', 'submitted_at', 'github_link_button', 'download_project_file')
    search_fields = ('project_title', 'team__name')
    
    def github_link_button(self, obj):
        if obj.github_link:
            return format_html('<a href="{}" target="_blank" style="padding: 5px 10px; background: #333; color: white; border-radius: 4px; text-decoration: none;">GitHub</a>', obj.github_link)
        return "-"
    github_link_button.short_description = "GitHub"
    
    def download_project_file(self, obj):
        if obj.project_file:
            return format_html('<a href="{}" download style="padding: 5px 10px; background: #6366f1; color: white; border-radius: 4px; text-decoration: none;">Download ZIP</a>', obj.project_file.url)
        return "No File"
    download_project_file.short_description = "Project File"


@admin.register(JudgeAssignment)
class JudgeAssignmentAdmin(admin.ModelAdmin):
    list_display = ('judge', 'hackathon', 'assigned_at')
    search_fields = ('judge__username', 'hackathon__title')
    list_filter = ('hackathon',)
    autocomplete_fields = ['judge']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('judge', 'submission', 'innovation', 'technical_complexity', 'ui_ux', 'total_score_col', 'scored_at')
    search_fields = ('judge__username', 'submission__project_title')
    list_filter = ('submission__team__hackathon',)
    readonly_fields = ('scored_at',)

    def total_score_col(self, obj):
        total = obj.total_score
        color = '#4ade80' if total >= 24 else '#fbbf24' if total >= 15 else '#f87171'
        return format_html('<strong style="color:{}">{}/30</strong>', color, total)
    total_score_col.short_description = 'Total'
