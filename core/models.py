from django.db import models
from django.contrib.auth.models import User

class Hackathon(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    banner = models.ImageField(upload_to='hackathon_banners/', null=True, blank=True)
    theme = models.CharField(max_length=100)
    prizes = models.TextField()
    is_active = models.BooleanField(default=True)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='teams')
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_teams')
    leader_name = models.CharField(max_length=100, null=True, blank=True)
    leader_email = models.EmailField(null=True, blank=True)
    leader_phone = models.CharField(max_length=20, null=True, blank=True)
    member2_name = models.CharField(max_length=100, null=True, blank=True)
    member3_name = models.CharField(max_length=100, null=True, blank=True)
    member4_name = models.CharField(max_length=100, null=True, blank=True)
    members = models.ManyToManyField(User, related_name='teams_joined', blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Approved')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def has_submission(self):
        try:
            return self.submission is not None
        except Exception:
            return False

    def __str__(self):
        return self.name

class Submission(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='submission')
    project_title = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField()
    project_file = models.FileField(upload_to='submissions/', blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Project Submission"
        verbose_name_plural = "Project Submissions"

    def __str__(self):
        return f"{self.project_title} - {self.team.name}"


class JudgeAssignment(models.Model):
    """Assigns a judge (user) to a specific hackathon."""
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='judge_assignments')
    judge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='judge_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hackathon', 'judge')
        verbose_name = "Judge Assignment"
        verbose_name_plural = "Judge Assignments"

    def __str__(self):
        return f"{self.judge.username} → {self.hackathon.title}"


class Score(models.Model):
    """Stores scores given by a judge for a submission."""
    SCORE_CHOICES = [(i, str(i)) for i in range(0, 11)]  # 0–10

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='scores')
    judge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores_given')
    innovation = models.IntegerField(choices=SCORE_CHOICES, default=0)
    technical_complexity = models.IntegerField(choices=SCORE_CHOICES, default=0)
    ui_ux = models.IntegerField(choices=SCORE_CHOICES, default=0)
    feedback = models.TextField(blank=True, null=True)
    scored_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('submission', 'judge')
        verbose_name = "Score"
        verbose_name_plural = "Scores"

    @property
    def total_score(self):
        return self.innovation + self.technical_complexity + self.ui_ux

    def __str__(self):
        return f"{self.judge.username} scored {self.submission.project_title} — {self.total_score}/30"


class Payment(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='payments')
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending') # Pending, Success, Failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.razorpay_order_id} - {self.status}"

