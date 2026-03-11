"""
BLACK LIGHT Collective — Portfolio / Models
Modele portfolio: członkowie zespołu, festiwale, projekty (realizacje scen),
galeria zdjęć projektów oraz opinie klientów.
"""
from django.db import models


class TeamMember(models.Model):
    """Członek kolektywu BLACK LIGHT.

    Reprezentuje osobę w zespole z profilem, rolą i linkami do social media.
    """
    name = models.CharField('Imie i nazwisko', max_length=200)
    role = models.CharField('Rola', max_length=200)
    bio = models.TextField('Bio')
    photo = models.ImageField('Zdjecie', upload_to='team/')
    email = models.EmailField('Email', blank=True)
    instagram = models.URLField('Instagram', blank=True)
    linkedin = models.URLField('LinkedIn', blank=True)
    behance = models.URLField('Behance', blank=True)
    order = models.PositiveIntegerField('Kolejnosc', default=0)
    is_active = models.BooleanField('Aktywny', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Czlonek zespolu'
        verbose_name_plural = 'Czlonkowie zespolu'

    def __str__(self):
        return f'{self.name} - {self.role}'


class Festival(models.Model):
    """Festiwal muzyczny — powiązany z realizacjami w portfolio."""
    name = models.CharField('Nazwa', max_length=300)
    location = models.CharField('Lokalizacja', max_length=500)
    website = models.URLField('Strona WWW', blank=True)
    logo = models.ImageField('Logo', upload_to='festivals/', blank=True)
    description = models.TextField('Opis', blank=True)

    class Meta:
        verbose_name = 'Festiwal'
        verbose_name_plural = 'Festiwale'
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    """Zrealizowany projekt sceny.

    Kategorie: main_stage, side_stage, art_installation, lighting, full_production.
    Może być powiązany z festiwalem i oznaczony jako wyróżniany.
    """
    CATEGORY_CHOICES = [
        ('main_stage', 'Main Stage'),
        ('side_stage', 'Side Stage'),
        ('art_installation', 'Instalacja artystyczna'),
        ('lighting', 'Oswietlenie'),
        ('full_production', 'Pelna produkcja'),
    ]

    title = models.CharField('Tytul', max_length=300)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Opis')
    short_description = models.CharField('Krotki opis', max_length=500, blank=True)
    festival = models.ForeignKey(
        Festival, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='projects', verbose_name='Festiwal'
    )
    client = models.CharField('Klient', max_length=300, blank=True)
    date = models.DateField('Data realizacji')
    category = models.CharField('Kategoria', max_length=20, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField('Wyrozniany', default=False)
    video_url = models.URLField('URL wideo', blank=True)
    technologies = models.TextField('Uzyty sprzet / technologie', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Projekt'
        verbose_name_plural = 'Projekty'

    def __str__(self):
        return self.title

    @property
    def cover_image(self):
        """Zwraca zdjęcie okładkowe projektu (pierwsze z is_cover=True)."""
        img = self.images.filter(is_cover=True).first()
        return img.image if img else None


class ProjectImage(models.Model):
    """Zdjęcie projektu — galeria z opcjonalną okładką."""
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField('Zdjecie', upload_to='projects/')
    caption = models.CharField('Podpis', max_length=300, blank=True)
    is_cover = models.BooleanField('Okladka', default=False)
    order = models.PositiveIntegerField('Kolejnosc', default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.project.title} - img {self.order}'


class Testimonial(models.Model):
    """Opinia klienta — powiązana opcjonalnie z projektem."""
    author = models.CharField('Autor', max_length=200)
    role = models.CharField('Rola / firma', max_length=200, blank=True)
    content = models.TextField('Tresc')
    avatar = models.ImageField('Awatar', upload_to='testimonials/', blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='testimonials'
    )
    rating = models.PositiveSmallIntegerField('Ocena', default=5)
    is_visible = models.BooleanField('Widoczna', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Opinia'
        verbose_name_plural = 'Opinie'

    def __str__(self):
        return f'{self.author} - {self.rating}/5'
