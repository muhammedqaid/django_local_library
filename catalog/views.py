from django.shortcuts import render

from .models import Book, BookInstance, Author, Genre, Language

def index(request): 
    """View function for home page of the site."""

    # Generates counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (i.e status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()  # all() implied

    num_genres = Genre.objects.all().count()

    num_books_with_the = Book.objects.filter(title__icontains="the").count()

    # Session variable to count number of visitis from a particular browser
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # python dictionary
    context = {
        'num_books': num_books, 
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres' : num_genres,
        'num_books_with_the' : num_books_with_the,
        'num_visits' : num_visits,
    }

    # Render the HTML template with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic

class BookListView(generic.ListView):
    model = Book
    # Within template, can access list of objects as <the model name>_list

    # Pagination built into generic lis view!
    # Only displays 10 on a page at a time. Different pages accessed using GT params e.g. to get page 2: /catalog/books/?page=2
    paginate_by = 2

    # change the template variable name
    context_object_name = 'book_list'

    # get 5 books containing the title war
    # queryset = Book.objects.filter(title__icontains='war'[:5])

    # specify own template name/location
    # template_name = 'books/myarbitrary_template_name_list.html'

    # Can also override methods like get_queryset()
    # def get_queryset(self): 
    #   return Book.objects.filter(title__icontains='war'[:5])

    # Or get_context_data() to pass additional context variables to the template
        # 1 - get existing content from super
        # 2 - Add new content
        # 3 - Return new context
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context


from django.shortcuts import get_object_or_404

# class BookDetailView(generic.DetailView):
#     model = Book
    
#     num_instances = None
#     num_available = 0

#     def book_detail_view(request, pk):
#         book = get_object_or_404(Book, pk=pk)

#         num_instances = book.bookinstance_set.filter(status__exact='a')
#         num_available = num_instances.filter(status__exact='a').count()

#         print(num_instances)
#         print(num_available)
#         return render(request, 'catalog/book_detail.html', context={'book': book})

#     def get_number_of_copies_available(self):
#         return num_available

class BookDetailView(generic.DetailView):
    model = Book



    # Pagination built into generic lis view, not detail


    # If a request record does not exist then the genetci class-based detail view will raise an 'Http404 exception automatically
    # If not using the generic class-based detail view: 
    '''
    def book_detail_view(request, primary_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')

        return render(request, 'catalog/book_detail.html', context={'book': book})
    
    '''
    # Or 
    '''
    from django.shortcuts import get_object_or_404

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})
    '''

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

    def detail_view(request, pk):
        author = get_object_or_404(Author, pk=pk)
        context={'author': author, 'books': {}}

        for book in author.book_set.all():
            instances = book.bookinstance_set.filter(status__exact='a')
            num_available = instances.filter(status__exact='a').count()
        
            context['books'][book] = (instances, num_available)

        return render(request, 'catalog/author_detail.html', context=context)



from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')



from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBookListView(PermissionRequiredMixin, generic.ListView):
    
    permission_required = 'catalog.list_all_borrowed'
    
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_staff.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('borrower','due_back')


import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the From data
    if request.method == 'POST':
        
        # Create a form instance and populate it with data from the request (binding): 
        form = RenewBookForm(request.POST)

        # Check if form is valid     
        if form.is_valid():
            # process the data in the form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL
            return HttpResponseRedirect(reverse('all-borrowed'))

        # else: If the form is not valid we call render() again, but this time the form value passed in the context will include error messages.


    # If this is a GET (or any other method) create a default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks = 3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance' : book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)



''' 
Session attribute - 
    # available from request argument. 
    # dictionary-like object that can be read or written as many times in view 
    # e.g. 
        # get a session by its key (e.g. 'my_car'), raising error if not available
            my_car = request.session['my_car']
        # get a session value, setting a default if it is not present ('mini')
            my_car = request.session.get('my_car', 'mini')
        # set a session value
            request.session['my_car'] = 'mini'
        # delete session value
            del request.session['my_car']

    # session only saved to database when the session is modified (assigned) or deleted
    # So, if you are updating some information within session data, django won't recognise the change and so not save automatically
        # E.g. 
            request.session['my_car']['wheels'] = 'alloy'
            request.session.modified = True
    # Can change settings.py to 'SESSION_SAVE_EVERY_REQUEST = TRue'
'''

'''
Access control
Funtion based view
    # Decorator to function:
        from django.contrib.auth.decorators import login_required

        @login_required
        def my_view(request):
            # …
    
    # Or (less nicely) by testing request.user.is_authenticated

Class based view
    #  Derive from LoginRequiredMixin
        from django.contrib.auth.mixins import LoginRequiredMixin

        class MyView(LoginRequiredMixin, View):
            login_url = '/login/'  # alternative location if not authenticated
    redirect_field_name = 'redirect_to'  # URL param instead of "next" 

Permissions can be tested in a similar way, using: 

    # permission_required decorator:
        from django.contrib.auth.decorators import permission_required

        @permission_required('catalog.can_mark_returned')
        @permission_required('catalog.can_edit')
        def my_view(request):
            # …
    
     or PermissionRequiredMixin
        from django.contrib.auth.mixins import PermissionRequiredMixin

        class MyView(PermissionRequiredMixin, View):
            permission_required = 'catalog.can_mark_returned'
            # Or multiple permissions
            permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
            # Note that 'catalog.can_edit' is just an example
            # the catalog application doesn't have such permission!


    There is a differenc ein response however. @permission_required redirects to login screen, while permissionrequiredmixin returns 403 error
    To get the error behaviour for function view use: 
        @login_required and @permission_required with raise_exception=True

            from django.contrib.auth.decorators import login_required, permission_required

            @login_required
            @permission_required('catalog.can_mark_returned', raise_exception=True)
            def my_view(request):
                # …
''' 

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author, Book

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '02/02/2020'}

    permission_required = 'catalog.update_authors'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__' # Potentially a security risk, if model is changed/ added to!
    permission_required = 'catalog.update_authors'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    # These all by default redirect to success page. ^ This is to specuify an alternative. 
    # Obviously this one needs a success_url
    # reverse_lazy() is a lazy execution of reverse(), because we are providing a URL to a class-based view attribute
        # As class variabkes are evaluated on import
    
    permission_required = 'catalog.update_authors'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    # initial = {'language': 'English'}

    permission_required = 'catalog.update_books'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__' # Potentially a security risk, if model is changed/ added to!
    permission_required = 'catalog.update_books'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    # These all by default redirect to success page. ^ This is to specuify an alternative. 
    # Obviously this one needs a success_url
    # reverse_lazy() is a lazy execution of reverse(), because we are providing a URL to a class-based view attribute
        # As class variabkes are evaluated on import
    
    permission_required = 'catalog.update_books'