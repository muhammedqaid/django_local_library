from django.urls import path
from . import views

# Already being passed to from catalog, so /catalog/...
urlpatterns = [
    # path (<pattern to match>, <function to pass to>, <name of mapping>)
    path('', views.index, name='index'),
    # As view function does all work pf creating an instance of the class making sure that the right handler methods are called for incoming HTTP requests
    path('books/', views.BookListView.as_view(), name='books'),
    # <> define part of url to be captured, enclosing name of variable that the view can use to access the captured data
    # E.g. <something> will capture the market pattern and pass the value to the view as a variable "something"
        # Can define the tyep too 
    # So, generic class-based view expects to be assed a paramter named pk. If you write your own function view, can use whatever param name, or pass as unnamed arg
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.detail_view, name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowedbooks/', views.LoanedBookListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]

'''
Can also use re_path() for a regular expression path 
    - E.g. re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail')
    - enclosed with r'<regEx goes here>'
    ^   - Match start of text
    $   - Match end of text
    \d  - Match a digit
    \w  - Match a word char (a-Z, _)
    +   - 1 +
    *   - 0 +
    ()  - Capture the part of the pattern in brackets as values to be passed as arguments (in order captures were declared)
    (?P<name>) - Capture as variable with name. View must then declare a param with same name 
    []  - Match one in a set

Can also pass a dictionary containing additional options to the view (using third, unnamed argument) 
    - E.g. path('myurl/<int:fish>', views.my_view, {'my_template_name': 'some_path'}, name='aurl')
        - This calls the function with asviews.my_view(request, fish=halibut, my_template_name='some_path')
    - Useful if you wanted to use the same view with a slight difference/ config/ behaviour
'''