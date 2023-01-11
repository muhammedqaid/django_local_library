from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
from django.contrib.auth.models import User

from datetime import date

'''
# Data needed to be stored
    - title
    - summary
    - author(/s) [details...]
    - language
    - category
    - ISBN
    - copies (information: unique id ect.)

# Objects 
    - Books
        - Book instances
    - Authors 
    Selection - list options
        - genre
        - language
''' 

# Create your models here.

class Genre(models.Model):
    """Model representing a book genre"""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String representing the Model object as a string."""
        return self.name

class Book(models.Model):
    """Model representing a particular book"""
    title = models.CharField(max_length=200, help_text='Enter a book title')

    # Foreign key as a book can have only one author, but authors can have many books
    # Author as a string as it hasn't yet been defined
    # If kept on_delete as defaulted models.CASCADE, the book would delete if author is deleted
        # COuld use PROTECT or RESTRICT to prevent author being deleted while any book uses it
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief summay of the book (e.g. blurb)')

    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='Enter the ISBN number of the book (13 character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>)')

    # Many-2-many as a genre contains many books and a book can have more than one genre
    genre = models.ManyToManyField(Genre, help_text='Enter a book genre (e.g. Science Fiction)')

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String representing the Model object as a string."""
        return self.title
    
    def get_absolute_url(self):
        """Return the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin site."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    class Meta: 
        permissions = (("update_books", "Add/update/delete books from the library database"),)

import uuid # Required for unique book instances

class BookInstance(models.Model):
    """Model representing a specific copy of a physical book (i.e. that can be borrowed form the library)"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particualr book across the library')
    
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    
    imprint = models.CharField(max_length=200)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'), 
        ('o', 'On loan'), 
        ('a', 'Available'), 
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1, 
        choices=LOAN_STATUS, 
        blank=True, 
        default='m', 
        help_text='Book availability status'
    )

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on the due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        ordering = ['book', 'status', 'due_back']
        # permissions variable to define any number of permissions in nested tuples
            # nested (permission name, permission display value)
        permissions = (("can_mark_returned", "Set book as returned"), ("list_all_borrowed","List all books on loan"),)
        # stored in template variable {{ perms }}
            # e.g. {{ perms.catalog.can_mark_returned }} is True if permission

    def __str__(self):
        """String for representing the Model object."""
        # f' - is string interpolation syntax (f-string), like string formatting
        return f'{self.id} ({self.book.title})'
        
class Author(models.Model):
    """Model representing an author."""

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(null=True, blank=True)

    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta: 
        ordering = ['last_name', 'first_name']
        permissions = (("update_authors", "Add/update/delete authors from the library database"),)

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
    
    def get_life_span(self):
        return f'{self.date_of_birth} - {self.date_of_death}'
    

class Language(models.Model):
    """Model representing a language"""

    name = models.CharField(max_length=200, help_text='Enter natural language of the book')

    class Meta: 
        ordering = ['name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    