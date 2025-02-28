import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

# Configurar la API de Gemini
GEMINI_API_KEY = "AIzaSyDRGEUlV3LwrDeqA9mldNsmeK1fJ0Re05o"
genai.configure(api_key=GEMINI_API_KEY)

# Función para consultar Gemini y filtrar la búsqueda


def is_valid_product(product):
    prompt = f"""El usuario quiere buscar "{product}" en MercadoLibre. 
    Solo permitimos búsquedas de productos electrónicos como laptops, celulares, monitores, procesadores, tarjetas gráficas, etc.
    Responde solo con "Si" o "No", sin explicaciones. ¿Es un producto electrónico válido?"""

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)

    print(f"Pregunta a Gemini: {prompt}")
    print(f"Respuesta de Gemini: {response.text.strip()}")

    return response.text.strip().lower() == "si"




# Scrapping
def get_content(product):
    USER_AGENT = "Mozilla/5.0 (x11; Linux x86_64) AppleWebKit/537.36 ()KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "es-VE,en-US,en;q=0.5"
    session = requests.session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(
        f'https://listado.mercadolibre.com.ve/{product}#D[A:{product}]').text
    return html_content


# Renderizar Main
def main(request):
    product_info_list = []

    if 'product' in request.GET:
        product = request.GET.get('product')

        # Filtrar con Gemini antes de hacer scraping
        if not is_valid_product(product):
            return render(request, 'main.html', {'error': 'Búsqueda no permitida. Solo se permiten productos electrónicos.'})
        else:
            # Si es válido, hacer scraping
            html_content = get_content(product)
            soup = BeautifulSoup(html_content, 'html.parser')

            product_items = soup.find_all(
                'div', class_="ui-search-result__wrapper")[:10]

            for item in product_items:
                name_tag = item.find(
                    'h3', class_="poly-component__title-wrapper")
                price_tag = item.find(
                    'span', class_="andes-money-amount andes-money-amount--cents-superscript")
                img = item.find('div', class_="poly-component__picture lazy-loadable") or item.find(
                    'div', class_="poly-card__portada")
                img_tag = img.find(
                    'img', class_="poly-component__picture") if img else None
                url_tag = item.find('a', class_="poly-component__title")

                if name_tag and price_tag and img_tag and url_tag:
                    name = name_tag.text.strip()
                    price = price_tag.text.strip()
                    image_url = img_tag.get('data-src', '') or img_tag.get(
                        'data-srcset', '') or img_tag.get('src', '') if img_tag else ''
                    url = url_tag.get('href', '') if url_tag else ''
                    product_info = {'name': name, 'price': price,
                                    'image_url': image_url, 'url': url}
                    product_info_list.append(product_info)
                    print(product_info)
        # Retornar los productos si hay resultados
        return render(request, 'main.html', {'product_info_list': product_info_list})

    # Si no hay búsqueda, renderizar la página sin productos
    return render(request, 'main.html')


#  var dataSrcKey = 'data-src';
#  var dataSrcFallbackKey = 'data-src-fallback';
#  var dataSrcSetKey = 'data-srcset';
