from django.contrib import admin
from .models import Book, BookInstance, Author, Genre, Language
# Register your models here.
# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)

# Define the Admin Classes


class BooksInline(admin.TabularInline):
    model = Book
    extra = 0
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    '''
    The fields attribute lists just those fields that are to be displayed on the form, in order.
    Fields are displayed vertically by default, but will display horizontally if you further group them in a tuple (as shown in the "date" fields above).
    '''
    # Can also exclude attributes

    inlines = [BooksInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    '''
    Note: Getting the genre may not be a good idea here, because of the "cost" of the database operation.
    Doing it to show calling functions in your models can be very useful for other reasons — for example:
         to add a Delete link next to every item in the list.
    '''

    inlines = [BooksInstanceInline]
    


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }), 
        ('Availability', {
            'fields' : ('status', 'due_back', 'borrower')
        }),
    )
    
