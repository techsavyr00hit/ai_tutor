import gradio as gr
from ragpipeline import build_context
from models import ModelManager

tutor = ModelManager()

def answer_question(question):
    context = build_context(question)
    response = tutor.ask(question, context)
    return response

with gr.Blocks() as demo:
    gr.HTML("""
    <style>
        #answer-box textarea {
            width: 100%;
            height: 400px;
            font-size: 16px;
        }
        #question-box textarea {
            width: 100%;
            font-size: 16px;
        }
        #title {
            text-align: center;
        }
    </style>
    """)
    gr.Markdown("<h1 id='title'>EduGenie - AI Tutor</h1>")
    answer = gr.Textbox(
        label="Answer",
        placeholder="Answer will appear here...",
        lines=20,
        interactive=False,
        elem_id="answer-box"
    )
    question = gr.Textbox(
        label="Ask a question",
        placeholder="Type your question here...",
        lines=2,
        interactive=True,
        elem_id="question-box"
    )
    submit_btn = gr.Button("Ask")
    submit_btn.click(answer_question, inputs=question, outputs=answer)
demo.launch()