from django.shortcuts import render, redirect
from .models import Question
from .nlp_engine import AINcertEngine

# create a single engine instance (lazy load)
engine = None

def get_engine():
    global engine
    if engine is None:
        engine = AINcertEngine()
    return engine


def home(request):
    return render(request, 'tutor_app/home.html')


def ask(request):
    if request.method == 'POST':
        q = request.POST.get('question')
        if not q:
            return render(request, 'tutor_app/home.html', {'error': 'Ask something!'})

        obj = Question.objects.create(text=q)

        engine = get_engine()
        answer, source_contexts = engine.answer_question(q, top_k=3)

        obj.answer = answer
        obj.save()

        return render(request, 'tutor_app/result.html', {
            'question': q,
            'answer': answer,
            'contexts': source_contexts,
        })
    return redirect('home')