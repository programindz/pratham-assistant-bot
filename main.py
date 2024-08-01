import google.generativeai as genai
from indexer import embedding_model, create_sentence_embeddings_with_faiss
from dotenv import load_dotenv
import gradio as gr
import os
import numpy as np

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model_gemini = genai.GenerativeModel(model_name='gemini-1.5-flash')

chat = model_gemini.start_chat(history=[])

faiss_index, all_paragraphs = create_sentence_embeddings_with_faiss()


def generate_response(query):
    
    query_emb = embedding_model.encode([query])[0]
    D, I = faiss_index.search(np.array([query_emb]), k=5)
    
    retrieved_information = "\n".join([all_paragraphs[idx] for idx in I[0]])

    prompt = f'''
    User: Act as a bot assistant to Pratham.org. You will be provided with content and a question.
    Based on the content information about Pratham you need to answer the question below:

    Content: {retrieved_information}
    Question: {query}
    
    Model:
    '''
    response = chat.send_message(prompt, stream=True)
    response.resolve()
    return response.text
    

if __name__ == "__main__":
    with gr.Blocks() as app:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.ClearButton([msg, chatbot])

        def respond(message, chat_history):
            bot_message = generate_response(message)
            chat_history.append((message, bot_message))
            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])

    app.launch()