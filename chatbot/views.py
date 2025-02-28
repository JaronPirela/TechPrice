from django.shortcuts import render
import google.generativeai as genai

# Configurar la clave de API
GEMINI_API_KEY = "AIzaSyDZYeZwyPXLgxt535YAZyjKRdOtEi97bU4"
genai.configure(api_key=GEMINI_API_KEY)

def chatbot(user_input):
    prompt = f"""Actúa como un experto en tecnología especializado en productos electrónicos. Debes responder exclusivamente preguntas sobre dispositivos como laptops, celulares, monitores, procesadores, tarjetas gráficas y otros componentes de hardware.

Tu objetivo es proporcionar respuestas precisas, actualizadas y bien estructuradas. Siempre menciona características clave, ventajas, desventajas y posibles alternativas cuando sea relevante. Si te preguntan sobre precios, disponibilidad o comparaciones, proporciona un análisis detallado y actualizado.

Si la pregunta no está relacionada con productos electrónicos, responde cortésmente que solo manejas información sobre dispositivos tecnológicos.

Ejemplos:
1. "¿Cuál es la mejor laptop para programadores en 2025?"
   - Responde mencionando modelos, procesadores, RAM, batería y relación calidad-precio.

2. "¿Qué tarjeta gráfica recomiendas para gaming en 1440p?"
   - Explica opciones de NVIDIA y AMD, rendimiento, consumo energético y precio.

3. "¿Cuál es el mejor celular calidad-precio en 2025?"
   - Destaca modelos con buena pantalla, batería, cámara y potencia.

Si una tecnología es nueva o hay poca información, menciona lo que se sabe hasta el momento y da una recomendación basada en tendencias tecnológicas.

Ahora, responde a la siguiente pregunta de forma corta y precisa: {user_input}"""

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)

    print(f"Pregunta a Gemini: {prompt}")
    print(f"Respuesta de Gemini: {response.text.strip()}")

    return response.text.strip()


def chatbot_view(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []  # Inicializar historial en sesión

    if request.method == "POST":
            if "clear_chat" in request.POST:
                # Limpiar el historial de chat
                request.session["chat_history"] = []
                request.session.modified = True  # Asegura que la sesión se actualice
            else:
                user_input = request.POST.get("user_input", "").strip()
                if user_input:
                    chatbot_reply = chatbot(user_input)

                    # Guardar conversación en el historial
                    request.session["chat_history"].append({"user": user_input, "bot": chatbot_reply})
                    request.session.modified = True  # Asegura que la sesión se actualice

    return render(request, "chatbot.html", {"chat_history": request.session["chat_history"]})
