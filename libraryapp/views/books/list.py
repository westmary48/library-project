import sqlite3
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from libraryapp.models import Book
from libraryapp.models import model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required

@login_required
def book_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:

            conn.row_factory = model_factory(Book)

            db_cursor = conn.cursor()
            db_cursor.execute("""
            select
                b.id,
                b.bookTitle,
                b.ISBNNumber,
                b.Author,
                b.YearPublished,
                b.librarian_id,
                b.location_id
            from libraryapp_book b
            """)


            all_books = db_cursor.fetchall()

        template = 'books/list.html'
        context = {
            'all_books': all_books
        }

        return render(request, template, context)


    elif request.method == 'POST':
        form_data = request.POST

    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO libraryapp_book
        (
            bookTitle, Author, ISBNNumber,
            YearPublished, location_id, librarian_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (form_data['bookTitle'], form_data['Author'],
            form_data['ISBNNumber'], form_data['YearPublished'],
            request.user.librarian.id, form_data["location"]))

        return redirect(reverse('libraryapp:books'))


