from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hackathon/create/', views.create_hackathon, name='create_hackathon'),
    path('hackathon/<int:pk>/', views.hackathon_detail, name='hackathon_detail'),
    path('hackathon/<int:hackathon_id>/register-team/', views.register_team, name='register_team'),
    path('my-teams/', views.my_teams, name='my_teams'),
    path('team/<int:team_id>/submit/', views.submit_project, name='submit_project'),
    path('hackathon/<int:hackathon_id>/judge/', views.judge_panel, name='judge_panel'),
    path('submission/<int:submission_id>/score/', views.score_submission, name='score_submission'),
    path('hackathon/<int:hackathon_id>/leaderboard/', views.leaderboard, name='leaderboard'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('idea-generator/', views.idea_generator, name='idea_generator'),
    path('generate-ideas/', views.generate_ideas, name='generate_ideas'),
    path('chatbot/api/', views.chatbot_api, name='chatbot_api'),
    path('payment/handler/', views.payment_handler, name='payment_handler'),
    path('payment/retry/<int:team_id>/', views.retry_payment, name='retry_payment'),
    path('invoice/<int:team_id>/', views.generate_invoice, name='generate_invoice'),
    
    # Admin Dashboard

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/team/<int:team_id>/<str:action>/', views.review_team, name='review_team'),
]
