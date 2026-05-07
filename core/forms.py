from django import forms
from .models import Hackathon, Team, Submission, Score

class HackathonForm(forms.ModelForm):
    class Meta:
        model = Hackathon
        fields = ['title', 'description', 'start_date', 'end_date', 'banner', 'theme', 'prizes', 'registration_fee', 'is_active']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'prizes': forms.Textarea(attrs={'rows': 3}),
        }

class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'leader_name', 'leader_email', 'leader_phone', 'member2_name', 'member3_name', 'member4_name']
        labels = {
            'name': 'Team Name',
            'leader_name': 'Team Leader Name',
            'leader_email': 'Mail ID',
            'leader_phone': 'Phone Number',
            'member2_name': 'Team Member 2 Name',
            'member3_name': 'Team Member 3 Name',
            'member4_name': 'Team Member 4 Name',
        }

class ProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['project_title', 'description', 'github_link', 'project_file', 'live_link', 'video_link']
        labels = {
            'project_title': 'Project Title',
            'description': 'Project Description',
            'github_link': 'GitHub Repository Link',
            'project_file': 'Upload Project (ZIP File)',
            'live_link': 'Live Demo Link (Optional)',
            'video_link': 'Demo Video Link (Optional)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['innovation', 'technical_complexity', 'ui_ux', 'feedback']
        labels = {
            'innovation': 'Innovation (0–10)',
            'technical_complexity': 'Technical Complexity (0–10)',
            'ui_ux': 'UI/UX Design (0–10)',
            'feedback': 'Comments / Feedback',
        }
        widgets = {
            'innovation': forms.Select(attrs={'class': 'score-select'}),
            'technical_complexity': forms.Select(attrs={'class': 'score-select'}),
            'ui_ux': forms.Select(attrs={'class': 'score-select'}),
            'feedback': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share detailed feedback about this project...'}),
        }
