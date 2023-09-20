from django.core.management.base import BaseCommand
from movie.models import Movie
import json
import openai
import os


from dotenv import load_dotenv, find_dotenv

_ = load_dotenv('../openAI.env')
openai.api_key  = os.environ['openAI_api_key']

class Command(BaseCommand):
    help = 'Modify path of images'

    def handle(self, *args, **kwargs):
        items = Movie.objects.all()
        for item in items:
            item.image.name = f"{item.image.name[0:13]}{item.title}.jpg" 
            item.save()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated with the illustrations of the movies'))