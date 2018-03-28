from django.db import models
from django.conf import settings
#from projeto.accounts import User #NÃO PRECISA, VEM DO SETTINGS E USA:settings.AUTH_USER_MODEL
# Create your models here.
from embed_video.fields import EmbedVideoField

class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )

class Turma(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição Simples', blank=True)
    

    start_date = models.DateField(
        'Data de Início', null=True, blank=True
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    objects = CourseManager()

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('edp:turmas', (), {'slug': self.slug})

    def release_edps(self):
        today = timezone.now().date()
        return self.edp.filter(release_date__gte=today)

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['-created_at']


class Edp(models.Model):

    titulo = models.CharField('Título', max_length=100)
    slug = models.SlugField('Atalho')
    objetivo_pedagogico = models.TextField('Objetivo Pedagógico')
    habilidades = models.CharField('Habilidades', max_length=100)
    atividades = models.TextField('Atividades')
    metodologia = models.TextField('Metodologia')
    release_date = models.DateField('Data de Liberação', blank=True, null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='edps',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)


    def __str__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return ('edp:details', (), {'slug': self.slug})

    def is_available(self):
        if self.release_date:
            today = timezone.now().date()
            return self.release_date >= today
        return False

    #TODO: observar se há necessidade
    def iniciar(self):
        self.save()

    class Meta:
        verbose_name = 'Estrutura Digital Pedagógica'
        verbose_name_plural = 'Estruturas Digitais Pedagógicas'
        ordering = ['created_at']


class RecursosSaida(models.Model):
    #recursos usados pelo professor para promover as edps
    edp = models.ForeignKey(Edp, verbose_name='Edp', related_name='recursos_de_saida', on_delete=models.CASCADE)
    video_embed = EmbedVideoField('Video externo', blank=True, null=True)
    #videogravado
    texto = models.TextField('Texto', blank=True)

    def iniciar(self):
        self.save

    def __str__ (self):
        return self.edp.titulo

    class Meta:
        verbose_name = 'Recurso de Saida'
        verbose_name_plural = 'Recursos de Saida'
     

class RecursoEntradaSelecionados(models.Model):

    edp = models.ForeignKey(Edp, verbose_name='Edp', related_name='recursos_entrada_selecionados', on_delete=models.CASCADE)
    video_embed = models.BooleanField('Video externo', blank = True, default= False)
    texto = models.BooleanField('Texto', blank = True, default= False)
  
    class Meta:
        verbose_name = 'Recurso selecionado'
        verbose_name_plural = 'Recursos selecionados'
      

class EdpUsada(models.Model):

    edp = models.ForeignKey(Edp, verbose_name='Edp', related_name='edp_usada', on_delete=models.CASCADE)
    edp_recursos = models.ForeignKey(RecursoEntradaSelecionados, verbose_name = 'recursos', related_name='edp_recursos', on_delete=models.CASCADE)
    video_embed = EmbedVideoField('Video externo', blank=True, null=True)
    #videogravado
    texto = models.TextField('Texto', blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def iniciar(self):
        self.save

    def __str__ (self):
        return self.edp.titulo

    class Meta:
        verbose_name = 'Estrutura Digital Pedagógica Usada'
        verbose_name_plural = 'Estruturas Digitais Pedagógicas Usadas'
        ordering = ['created_at']



class Comment(models.Model):

    edpUsada = models.ForeignKey(
        EdpUsada, verbose_name='Edp', related_name='comments', on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário',on_delete=models.CASCADE)
    comment = models.TextField('Comentário')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']
