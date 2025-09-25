from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import openai

from .forms import SignUpForm
from .models import Conversation, Message


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'계정이 생성되었습니다: {username}')
            login(request, user)
            return redirect('chat')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def chat_view(request):
    conversations = Conversation.objects.filter(user=request.user, is_active=True)
    current_conversation = None
    messages_list = []

    # URL에서 conversation_id가 있는지 확인
    conversation_id = request.GET.get('conversation')
    if conversation_id:
        try:
            current_conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
            messages_list = current_conversation.messages.all()
        except:
            pass

    context = {
        'conversations': conversations,
        'current_conversation': current_conversation,
        'messages': messages_list,
    }
    return render(request, 'chat/chat.html', context)


@login_required
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')

        if not message_content:
            return JsonResponse({'error': '메시지를 입력해주세요.'}, status=400)

        try:
            # 대화 가져오기 또는 새로 생성
            if conversation_id:
                conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
            else:
                # 새 대화 생성
                title = message_content[:50] + '...' if len(message_content) > 50 else message_content
                conversation = Conversation.objects.create(user=request.user, title=title)

            # 사용자 메시지 저장
            user_message = Message.objects.create(
                conversation=conversation,
                role='user',
                content=message_content
            )

            # 대화 히스토리 구성
            messages_history = []
            for msg in conversation.messages.all():
                messages_history.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # OpenAI API 호출
            openai.api_key = settings.OPENAI_API_KEY
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_history
            )

            ai_response = response.choices[0].message.content

            # AI 응답 저장
            ai_message = Message.objects.create(
                conversation=conversation,
                role='assistant',
                content=ai_response
            )

            # 대화 업데이트 시간 갱신
            conversation.save()

            return JsonResponse({
                'success': True,
                'conversation_id': conversation.id,
                'user_message': {
                    'content': user_message.content,
                    'timestamp': user_message.created_at.isoformat()
                },
                'ai_message': {
                    'content': ai_message.content,
                    'timestamp': ai_message.created_at.isoformat()
                }
            })

        except Exception as e:
            return JsonResponse({'error': f'오류가 발생했습니다: {str(e)}'}, status=500)

    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)


@login_required
def new_conversation(request):
    """새 대화 시작"""
    return redirect('chat')


@login_required
def delete_conversation(request, conversation_id):
    """대화 삭제"""
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        conversation.is_active = False
        conversation.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)
