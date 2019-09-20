import sqlite3
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from libraryapp.models import model_factory
from libraryapp.models import Library, Book
from ..connection import Connection
from django.contrib.auth.decorators import login_required


@login_required
def list_libraries(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = create_library
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
	            li.id library_id,
	            li.title,
	            li.address,
	            b.id book_id,
	            b.bookTitle,
	            b.Author,
	            b.YearPublished,
	            b.ISBNNumber
            FROM libraryapp_library li
            JOIN libraryapp_book b ON li.id = b.location_id
   """)

            all_libraries = db_cursor.fetchall()
            library_groups = {}

            # Iterate the list of tuples
            for (library, book) in all_libraries:

            # If the dictionary does have a key of the current
            # library's `id` value, add the key and set the value
            # to the current library
                if library.id not in library_groups:
                    library_groups[library.id] = library
                    library_groups[library.id].books.append(book)

            # If the key does exist, just append the current
            # book to the list of books for the current library
            else:
                library_groups[library.id].books.append(book)
                print(library_groups)


        template_name = 'library/list.html'

        context = {
        'all_libraries': library_groups.values()
        }

        return render(request, template_name, context)



    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO libraryapp_library
            (
                title, address
            )
            VALUES (?, ?)
            """,
            (form_data['title'], form_data['address']))

        return redirect(reverse('libraryapp:libraries'))


def create_library(cursor, row):
    _row = sqlite3.Row(cursor, row)

    library = Library()
    library.id = _row["library_id"]
    library.title = _row["title"]
    library.address = _row["address"]

    # Note: You are adding a blank books list to the library object
    # This list will be populated later (see below)
    library.books = []

    book = Book()
    book.id = _row["book_id"]
    book.bookTitle = _row["bookTitle"]
    book.Author = _row["Author"]
    book.ISBNNumber = _row["ISBNNumber"]
    book.YearPublished = _row["YearPublished"]

    # Return a tuple containing the library and the
    # book built from the data in the current row of
    # the data set
    return (library, book,)

