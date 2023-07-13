from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
import json

from books.models import Book


def members(request):
    return render(request, "members/new_page.html")


def user_list_view(request):
    users = User.objects.all()
    user_list = [user.username for user in users]
    return JsonResponse(user_list, status=200, safe=False)


@login_required
def user_books_view(request: HttpRequest):
    if request.method == "GET":
        try:
            session_id = request.COOKIES.get("sessionid")
            session = Session.objects.get(session_key=session_id)
            uid = session.get_decoded().get("_auth_user_id")
            logged_user = User.objects.get(pk=uid)
            books = Book.objects.filter(user=logged_user)

            response = list(books.values())

        except Session.DoesNotExist:
            return JsonResponse({"error": "Session not found."}, status=404)

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse(response, status=200, safe=False)

    else:
        return HttpResponse(status=405, content="Method not allowed")
