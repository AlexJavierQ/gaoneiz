# noticias/views.py

from django.views.generic import ListView, DetailView
from .models import Noticia

class NoticiaListView(ListView):
    model = Noticia
    template_name = 'noticias/noticia_list.html' # Plantilla para la lista
    context_object_name = 'noticias'
    paginate_by = 6

    def get_queryset(self):
        return Noticia.objects.filter(publicada=True).order_by('-fecha_publicacion')

class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = 'noticias/noticia_detail.html' # Plantilla para el detalle
    context_object_name = 'noticia'