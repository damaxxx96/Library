from django.db import IntegrityError
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse
import json

from books.exceptions import *
from .models import BookHistory, BookQueue, Bookshelf, Book
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@login_required
def create_bookshelf(request: HttpRequest):
    try:
        new_bookshelf = json.loads(request.body)
        bookshelf = Bookshelf(shelf_number=new_bookshelf["shelf_number"])

        if len(Bookshelf.objects.filter(shelf_number=bookshelf.shelf_number)) > 0:
            return HttpResponse(
                status=400, content="Bookshelf with this shelf number already exists!"
            )
        else:
            bookshelf.save()
    except:
        return HttpResponse(status=500)

    return HttpResponse(status=201)


@login_required
def create_book(request: HttpRequest):
    try:
        new_book = json.loads(request.body)
        bookshelf = Bookshelf.objects.get(shelf_number=new_book["shelf_number"])
        book = Book(
            title=new_book["title"],
            author=new_book["author"],
            genre=new_book["genre"],
            pub_date=datetime.strptime(new_book["pub_date"], "%d-%m-%Y").date(),
            bookshelf=bookshelf,
        )
        bookshelf.capacity += 1
        bookshelf.save()
        book.save()

    except Bookshelf.DoesNotExist:
        return JsonResponse({"error": "Bookshelf does not exist"}, status=400)

    except IntegrityError as e:
        return JsonResponse({"error": str(e)}, status=400)

    except ValueError:
        return JsonResponse(
            {"error": "Invalid pub_date format. Expected dd-mm-yyyy."}, status=400
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return HttpResponse(status=201)


@login_required
def borrow_book(request: HttpRequest):
    if request.method == "PATCH":
        try:
            borrowed_book = json.loads(request.body)
            book = Book.objects.get(pk=borrowed_book["id"])

            session_id = request.COOKIES.get("sessionid")
            session = Session.objects.get(session_key=session_id)
            uid = session.get_decoded().get("_auth_user_id")
            user = User.objects.get(pk=uid)

            if book.user is not None:
                if book.user == user:
                    raise BookAlreadyBorrowed

                try:
                    current_book_queue = BookQueue.objects.get(book=book)
                    if current_book_queue.users.contains(user):
                        raise AlreadyInBookQueue

                except BookQueue.DoesNotExist:
                    pass

                except AlreadyInBookQueue:
                    raise AlreadyInBookQueue

                new_queue = BookQueue()
                new_queue.book = book
                new_queue.save()
                new_queue.users.add(user)
                new_queue.save()

            book.user = user
            book.bookshelf.capacity -= 1
            book.bookshelf = None
            book.save()

            try:
                history = BookHistory(
                    user=user, book=book, action_date=datetime.now(), action="BORROWED"
                )
                history.save()

            except Exception as e:
                raise BookHistoryException from e

        except json.JSONDecodeError:
            return HttpResponse(
                status=400, content="Invalid JSON format"
            )  # Bad request, invalid JSON format

        except KeyError:
            return HttpResponse(
                status=400, content="Missing required field(s)"
            )  # Bad request, missing required field(s)

        except Session.DoesNotExist:
            return HttpResponse(
                status=401, content="Unauthorized: Session not found"
            )  # Unauthorized, session not found

        except User.DoesNotExist:
            return HttpResponse(status=404, content="User not found")  # User not found

        except Book.DoesNotExist:
            return HttpResponse(status=404, content="Book not found")  # Book not found

        except BookAlreadyBorrowed:
            return HttpResponse(status=409, content="Book is already borrowed")

        except AlreadyInBookQueue:
            return HttpResponse(status=409, content="You are already in queue")

        except BookHistoryException:
            return HttpResponse(status=500, content="Error while saving book history")

        return HttpResponse(status=200, content="Book successfully borrowed")

    else:
        return HttpResponse(status=405, content="Method not allowed")


@login_required
def return_book(request: HttpRequest):
    if request.method == "PATCH":
        try:
            returned_book = json.loads(request.body)
            book = Book.objects.get(pk=returned_book["id"])

            session_id = request.COOKIES.get("sessionid")
            session = Session.objects.get(session_key=session_id)
            uid = session.get_decoded().get("_auth_user_id")
            user = User.objects.get(pk=uid)

            if book.user is None:
                raise BookNotAssignedToUserError("Book is not assigned to the user")

            if book.user.username != user.username:
                raise UsernameMismatchError(
                    "Username does not align with the book's user"
                )

            book.user = None

            available_bookshelf = Bookshelf.objects.filter(capacity__lt=5).first()
            book.bookshelf = available_bookshelf

            book.save()
            try:
                history = BookHistory(
                    user=user, book=book, action_date=datetime.now(), action="RETURNED"
                )
                history.save()

            except Exception as e:
                raise BookHistoryException from e

            try:
                current_book_queue = BookQueue.objects.get(book=book)
                user_with_longest_queue = (
                    current_book_queue.users.all()
                    .order_by("-bookqueue__queue_date")
                    .first()
                )
                book.user = user_with_longest_queue
                book.save()

            except BookQueue.DoesNotExist:
                pass

            except Exception as e:
                raise Exception from e

            return HttpResponse("Book returned successfully", status=200)

        except Book.DoesNotExist:
            # Handle the case when the book does not exist
            return HttpResponseBadRequest("Book not found.", status=404)

        except Session.DoesNotExist:
            # Handle the case when the session does not exist
            return HttpResponseBadRequest("Session not found.", status=404)

        except User.DoesNotExist:
            # Handle the case when the user does not exist
            return HttpResponseBadRequest("User not found.", status=404)

        except BookNotAssignedToUserError:
            # Handle the case when the book is not assigned to the user
            return HttpResponseBadRequest(
                "Book is not assigned to the user.", status=400
            )
        except BookHistoryException:
            return HttpResponse(status=500, content="Error while saving book history")

        except UsernameMismatchError:
            # Handle the case when the username does not align
            return HttpResponseBadRequest(
                "Username does not align with the book's user.", status=400
            )
