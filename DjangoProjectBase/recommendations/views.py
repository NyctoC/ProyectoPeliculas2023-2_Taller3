from django.shortcuts import render
import os
import openai
import json
from dotenv import load_dotenv, find_dotenv
from movie.models import Movie

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

# Create your views here.
def recommendations(request):
    recommendationPrompt = request.GET.get('recommendationPrompt')
    movies = []

    if recommendationPrompt: 
        #Se lee del archivo .env la api key de openai
        _ = load_dotenv('../openAI.env')
        openai.api_key = os.environ['openAI_api_key']

        #Se carga la lista de películas de movie_titles.json
        titles_list = []
        with open('../movie_titles.json', 'r') as file:
            file_content = file.read()
            movies = json.loads(file_content)
            titles_list = [item['title'] for item in movies]

        instruction = "Instrucciones: Vas a recibir un prompt solicitando una recomendacion de pelicula (EJEMPLO: Película de la segunda guerra mundial). \
            Con base a una <lista de peliculas> tienes que elegir la mas cercana \
            a la recomendacion en el prompt y devolver SOLO el/los nombre/nombres tal y como aparece en la <lista de peliculas> y separados por un punto y coma (;) y sin espacios entre peliculas \
            EJEMPLO DE RESPUESTA: El padrino;Casablanca;Pulp Fiction\
            El maximo de recomendaciones es 5. La <lista de peliculas> es la siguiente: "
        
        # AQUI DEBERIA USAR LA LISTA PERO DEL MODELO Y NO DEL JSON, PERO YA QUE
        # FIX LATER
        instruction += str(titles_list)

        prompt = f"{instruction}. Ahora, Recomiendame una pelicula basandome en el siguiente prompt teniendo en cuenta que debes imprimir como dicen las instrucciones: {recommendationPrompt}"

        response = get_completion(prompt)
        #response = "Ciudadano Kane;El imperio contraataca;Apocalypse Now"
        print(response)

        # OBTENEMOS TITULOS
        movieTitles = response.split(";")
        movies = []

        for title in movieTitles:
            print(title)
            movies.append(Movie.objects.filter(title__icontains=title))

        #print(movies)

    return render(request, 'recommendations.html', {'recommendationPrompt':recommendationPrompt, 'movies':movies})