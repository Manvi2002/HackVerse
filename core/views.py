from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Sum
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
import json
import re
from .idea_bank import get_ideas
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from .models import Hackathon, Team, Submission, JudgeAssignment, Score, Payment
from .forms import HackathonForm, TeamRegistrationForm, ProjectSubmissionForm, ScoreForm

def home(request):
    now = timezone.now()
    active_hackathons = Hackathon.objects.filter(is_active=True, start_date__lte=now, end_date__gte=now).order_by('end_date')
    upcoming_hackathons = Hackathon.objects.filter(is_active=True, start_date__gt=now).order_by('start_date')
    return render(request, 'home.html', {
        'active_hackathons': active_hackathons,
        'upcoming_hackathons': upcoming_hackathons
    })

def hackathon_detail(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    teams = hackathon.teams.all()
    is_judge = False
    if request.user.is_authenticated:
        is_judge = JudgeAssignment.objects.filter(hackathon=hackathon, judge=request.user).exists()
    return render(request, 'hackathon_detail.html', {'hackathon': hackathon, 'teams': teams, 'is_judge': is_judge})

@login_required
def register_team(request, hackathon_id):
    hackathon = get_object_or_404(Hackathon, id=hackathon_id)
    
    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.hackathon = hackathon
            team.leader = request.user
            team.status = 'Pending'
            team.save()
            team.members.add(request.user)
            
            if hackathon.registration_fee > 0:
                # Initiate Razorpay Payment
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                data = {
                    "amount": int(hackathon.registration_fee * 100), # Amount in paise
                    "currency": "INR",
                    "receipt": f"receipt_{team.id}",
                    "payment_capture": "1"
                }
                razorpay_order = client.order.create(data=data)
                
                # Create Payment object
                Payment.objects.create(
                    team=team,
                    razorpay_order_id=razorpay_order['id'],
                    amount=hackathon.registration_fee,
                    status='Pending'
                )
                
                return render(request, 'payment.html', {
                    'razorpay_order_id': razorpay_order['id'],
                    'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
                    'amount': data['amount'],
                    'team': team,
                    'hackathon': hackathon
                })
            else:
                team.is_paid = True
                team.save()
                messages.success(request, f"Team '{team.name}' registered successfully! Waiting for admin approval.")
                return redirect('hackathon_detail', pk=hackathon.id)
                
    else:
        form = TeamRegistrationForm()
        
    return render(request, 'register_team.html', {'form': form, 'hackathon': hackathon})


@login_required
def retry_payment(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user != team.leader:
        messages.error(request, "Access denied.")
        return redirect('my_teams')
        
    if team.is_paid:
        messages.info(request, "This registration is already paid.")
        return redirect('my_teams')
        
    hackathon = team.hackathon
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    data = {
        "amount": int(hackathon.registration_fee * 100),
        "currency": "INR",
        "receipt": f"receipt_{team.id}",
        "payment_capture": "1"
    }
    razorpay_order = client.order.create(data=data)
    
    Payment.objects.create(
        team=team,
        razorpay_order_id=razorpay_order['id'],
        amount=hackathon.registration_fee,
        status='Pending'
    )
    
    return render(request, 'payment.html', {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'amount': data['amount'],
        'team': team,
        'hackathon': hackathon
    })


@csrf_exempt
def payment_handler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            # Verify signature
            try:
                client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError as e:
                # Log the specific verification failure
                print(f"Razorpay Signature Verification Failed: {str(e)}")
                messages.error(request, f"Payment verification failed: Invalid signature. {str(e)}")
                return redirect('home')
            
            # Update Payment and Team status
            payment = Payment.objects.get(razorpay_order_id=order_id)
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = 'Success'
            payment.save()
            
            team = payment.team
            team.is_paid = True
            team.save()
            
            messages.success(request, "Payment successful! Your registration is complete.")
            return redirect('hackathon_detail', pk=team.hackathon.id)
        except Payment.DoesNotExist:
            messages.error(request, "Critical Error: Payment record not found in database.")
            return redirect('home')
        except Exception as e:
            print(f"General Payment Error: {str(e)}")
            messages.error(request, f"An unexpected error occurred during payment processing: {str(e)}")
            return redirect('home')
    return redirect('home')

@login_required
def my_teams(request):
    teams = Team.objects.filter(leader=request.user) | request.user.teams_joined.all()
    teams = teams.distinct()
    return render(request, 'my_teams.html', {'teams': teams})

@login_required
def submit_project(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    if request.user != team.leader and request.user not in team.members.all():
        messages.error(request, "You are not a member of this team.")
        return redirect('my_teams')

    if team.status != 'Approved':
        messages.error(request, "Your team must be approved by an admin before you can submit a project.")
        return redirect('my_teams')

    if team.has_submission:
        messages.info(request, "Your team has already submitted a project.")
        return redirect('my_teams')
        
    if request.method == 'POST':
        form = ProjectSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.team = team
            submission.save()
            messages.success(request, f"Project '{submission.project_title}' submitted successfully!")
            return redirect('my_teams')
    else:
        form = ProjectSubmissionForm()
        
    return render(request, 'submit_project.html', {'form': form, 'team': team})


@login_required
def judge_panel(request, hackathon_id):
    """Judge's dashboard: list all submissions for their assigned hackathon."""
    hackathon = get_object_or_404(Hackathon, id=hackathon_id)

    # Only assigned judges can access
    is_judge = JudgeAssignment.objects.filter(hackathon=hackathon, judge=request.user).exists()
    if not is_judge:
        messages.error(request, "You are not assigned as a judge for this hackathon.")
        return redirect('home')

    submissions = Submission.objects.filter(team__hackathon=hackathon).select_related('team')

    # Annotate each submission with this judge's existing score
    for sub in submissions:
        try:
            sub.my_score = sub.scores.get(judge=request.user)
        except Score.DoesNotExist:
            sub.my_score = None

    return render(request, 'judge_panel.html', {
        'hackathon': hackathon,
        'submissions': submissions,
    })


@login_required
def score_submission(request, submission_id):
    """Form view for a judge to score a single submission."""
    submission = get_object_or_404(Submission, id=submission_id)
    hackathon = submission.team.hackathon

    is_judge = JudgeAssignment.objects.filter(hackathon=hackathon, judge=request.user).exists()
    if not is_judge:
        messages.error(request, "You are not assigned as a judge for this hackathon.")
        return redirect('home')

    # Get existing score or None
    existing_score = Score.objects.filter(submission=submission, judge=request.user).first()

    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=existing_score)
        if form.is_valid():
            score = form.save(commit=False)
            score.submission = submission
            score.judge = request.user
            score.save()
            messages.success(request, f"Score saved for '{submission.project_title}'.")
            return redirect('judge_panel', hackathon_id=hackathon.id)
    else:
        form = ScoreForm(instance=existing_score)

    return render(request, 'score_submission.html', {
        'form': form,
        'submission': submission,
        'existing_score': existing_score,
    })


def leaderboard(request, hackathon_id):
    """Public leaderboard showing ranked submissions by average total score."""
    hackathon = get_object_or_404(Hackathon, id=hackathon_id)
    submissions = Submission.objects.filter(team__hackathon=hackathon).prefetch_related('scores')

    # Build ranked list
    ranked = []
    for sub in submissions:
        all_scores = sub.scores.all()
        if all_scores.exists():
            avg_innovation = all_scores.aggregate(Avg('innovation'))['innovation__avg'] or 0
            avg_technical = all_scores.aggregate(Avg('technical_complexity'))['technical_complexity__avg'] or 0
            avg_uiux = all_scores.aggregate(Avg('ui_ux'))['ui_ux__avg'] or 0
            avg_total = avg_innovation + avg_technical + avg_uiux
            judge_count = all_scores.count()
        else:
            avg_innovation = avg_technical = avg_uiux = avg_total = 0
            judge_count = 0

        ranked.append({
            'submission': sub,
            'avg_innovation': round(avg_innovation, 1),
            'avg_technical': round(avg_technical, 1),
            'avg_uiux': round(avg_uiux, 1),
            'avg_total': round(avg_total, 1),
            'judge_count': judge_count,
        })

    # Sort by total descending
    ranked.sort(key=lambda x: x['avg_total'], reverse=True)

    return render(request, 'leaderboard.html', {
        'hackathon': hackathon,
        'ranked': ranked,
    })


def create_hackathon(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
        
    if request.method == 'POST':
        form = HackathonForm(request.POST, request.FILES)
        if form.is_valid():
            hackathon = form.save()
            messages.success(request, f"Hackathon '{hackathon.title}' created successfully!")
            return redirect('home')
    else:
        form = HackathonForm()
    return render(request, 'create_hackathon.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')


def idea_generator(request):
    """Renders the AI Idea Generator page."""
    return render(request, 'idea_generator.html')


@require_POST
def generate_ideas(request):
    """API endpoint: returns curated ideas from local idea bank (no API key needed)."""
    try:
        data = json.loads(request.body)
        theme = data.get('theme', '').strip()
        if not theme:
            return JsonResponse({'error': 'Please enter a hackathon theme.'}, status=400)

        ideas = get_ideas(theme, count=5)
        return JsonResponse({'ideas': ideas})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'AI returned unexpected format. Please try again.'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_hackathons = Hackathon.objects.count()
    total_teams = Team.objects.count()
    total_submissions = Submission.objects.count()
    
    total_revenue = Team.objects.filter(is_paid=True).aggregate(Sum('hackathon__registration_fee'))['hackathon__registration_fee__sum'] or 0
    revenue = f"₹{total_revenue:,}"
    
    recent_hackathons = Hackathon.objects.all().order_by('-created_at')[:5]
    pending_teams = Team.objects.filter(status='Pending').select_related('hackathon', 'leader').order_by('-created_at')
    
    return render(request, 'admin_dashboard.html', {
        'total_users': total_users,
        'total_hackathons': total_hackathons,
        'total_teams': total_teams,
        'total_submissions': total_submissions,
        'revenue': revenue,
        'recent_hackathons': recent_hackathons,
        'pending_teams': pending_teams,
    })

@staff_member_required
def review_team(request, team_id, action):
    team = get_object_or_404(Team, id=team_id)
    if action == 'approve':
        team.status = 'Approved'
        messages.success(request, f"Team '{team.name}' has been approved.")
    elif action == 'reject':
        team.status = 'Rejected'
        messages.warning(request, f"Team '{team.name}' has been rejected.")
    team.save()
    return redirect('admin_dashboard')


@require_POST
def chatbot_api(request):
    """Unified API endpoint for the HackVerse Assistant (User, Judge, and Admin roles)."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').lower().strip()
        user = request.user
        
        # Role Detection
        is_admin = user.is_staff if user.is_authenticated else False
        is_judge = JudgeAssignment.objects.filter(judge=user).exists() if user.is_authenticated else False

        # --- ADMIN ROLE LOGIC ---
        if is_admin:
            if "users registered today" in message or "registrations today" in message:
                count = User.objects.filter(date_joined__date=timezone.now().date()).count()
                return JsonResponse({'reply': f"📊 **Admin Insights**: {count} new users joined today."})
            
            if "drop-off" in message or "dropoff" in message:
                total = User.objects.count()
                active = User.objects.filter(models.Q(led_teams__isnull=False) | models.Q(teams_joined__isnull=False)).distinct().count()
                rate = ((total - active) / total * 100) if total > 0 else 0
                return JsonResponse({'reply': f"📉 **Admin Insights**: Drop-off rate is {rate:.1f}% ({total - active} users without teams)."})

            if "extend deadline" in message:
                hack = Hackathon.objects.filter(is_active=True).order_by('-end_date').first()
                if hack:
                    hack.end_date += timezone.timedelta(days=1)
                    hack.save()
                    return JsonResponse({'reply': f"✅ **Admin Action**: Deadline for '{hack.title}' extended by 24h."})

            if "report" in message:
                hacks = Hackathon.objects.all()
                report = "🧾 **Admin Report**:\n" + "\n".join([f"• {h.title}: {h.teams.count()} teams" for h in hacks])
                return JsonResponse({'reply': report})

        # --- JUDGE ROLE LOGIC ---
        if is_judge:
            assigned_hacks = Hackathon.objects.filter(judge_assignments__judge=user)
            submissions = Submission.objects.filter(team__hackathon__in=assigned_hacks).select_related('team')
            
            if "incomplete" in message:
                inc = submissions.filter(models.Q(github_link="") | models.Q(description=""))
                names = ", ".join([s.team.name for s in inc])
                return JsonResponse({'reply': f"🔍 **Judge Insight**: Incomplete teams: {names if names else 'None'}."})

            # Find mentioned teams for summary/eval
            mentioned = [s for s in submissions if s.team.name.lower() in message]
            if not mentioned and ("feedback" in message or "score" in message or "summarize" in message):
                return JsonResponse({'reply': "📝 **Judge Assistant**: Which team would you like feedback for? Please mention the **Team Name** (e.g., 'Give feedback for Team Alpha')."})
            if mentioned:
                sub = mentioned[0]
                if "summarize" in message or "summary" in message:
                    return JsonResponse({'reply': f"📑 **Judge Summary ({sub.team.name})**: {sub.description[:100]}..."})
                if "score" in message or "evaluate" in message or "suggest" in message:
                    return JsonResponse({'reply': f"⭐ **Judge Evaluation ({sub.team.name})**: Suggested Score: 22/30 (Innovation: 8, Tech: 7, UI: 7)."})
                if "feedback" in message:
                    return JsonResponse({'reply': f"📝 **Judge Feedback ({sub.team.name})**: 'Great technical foundation, UI needs more polish!'"})

        # --- GENERAL USER ROLE LOGIC (Participants) ---
        # GitHub Validation
        if "github.com" in message:
            if re.match(r'^https?://(www\.)?github\.com/[\w-]+/[\w.-]+/?.*$', message):
                return JsonResponse({'reply': "✅ **Assistant**: That GitHub link looks valid! Ready for submission."})
            return JsonResponse({'reply': "❌ **Assistant**: Invalid GitHub link format. Use: https://github.com/user/repo"})

        # Onboarding
        if "register" in message or "join" in message or "start" in message:
            if not user.is_authenticated:
                return JsonResponse({'reply': "👋 **Assistant**: Welcome! Start by clicking 'Register' at the top right."})
            teams = Team.objects.filter(leader=user) | user.teams_joined.all()
            if not teams.exists():
                return JsonResponse({'reply': "👋 **Assistant**: You're logged in! Now visit a Hackathon page to form a team."})
            return JsonResponse({'reply': "👋 **Assistant**: You're all set! Check 'My Teams' to manage your progress."})

        # Deadlines
        if "deadline" in message or "time" in message or "when" in message:
            hack = Hackathon.objects.filter(is_active=True, end_date__gte=timezone.now()).order_by('end_date').first()
            if not hack: return JsonResponse({'reply': "📅 **Assistant**: No active deadlines at the moment."})
            time_left = hack.end_date - timezone.now()
            return JsonResponse({'reply': f"⏳ **Assistant**: '{hack.title}' ends in {time_left.days}d {time_left.seconds//3600}h."})

        # Project Submission Steps
        if "submit" in message and "project" in message:
            return JsonResponse({'reply': "🚀 **How to Submit Your Project**:\n1. Go to **'My Teams'** from the navbar.\n2. Ensure your team status is **'Approved'**.\n3. If it's a paid hackathon, ensure **'Payment'** is complete.\n4. Click the **'Submit Project'** button.\n5. Fill in your GitHub link and project details, then save!"})

        # Default Response
        role_info = "Assistant"
        if is_admin: role_info = "Admin Assistant"
        elif is_judge: role_info = "Judging Assistant"
        
        return JsonResponse({'reply': f"🤖 **HackVerse {role_info}**: I can help with registration, deadlines, and project validation. {'(Admin/Judge tools enabled)' if is_admin or is_judge else ''}"})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def generate_invoice(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user != team.leader and not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('home')
        
    payment = team.payments.filter(status='Success').first()
    
    # If it's a paid hackathon but no payment record found
    if team.hackathon.registration_fee > 0 and not payment:
        messages.error(request, "No successful payment record found for this team.")
        return redirect('my_teams')
    
    # For free hackathons, we can still show a 'Zero' invoice if requested
    context = {
        'team': team,
        'payment': payment,
        'hackathon': team.hackathon,
        'is_free': team.hackathon.registration_fee == 0
    }
    
    response = render(request, 'invoice.html', context)
    if request.GET.get('download'):
        response['Content-Disposition'] = f'attachment; filename="invoice_{team.name}.html"'
    return response