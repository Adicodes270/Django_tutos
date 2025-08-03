from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from django.contrib.auth.decorators import login_required

# View a specific ToDo list
def index(response, id):
    try:
        ls = ToDoList.objects.get(id=id)
    except ToDoList.DoesNotExist:
        return render(response, "main/unauthorized_list.html")

    if ls in response.user.todolist.all():
        if response.method == "POST":
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()

            elif response.POST.get("newItem"):
                text = response.POST.get("new")
                if text and len(text.strip()) > 3:
                    ls.item_set.create(text=text.strip(), complete=False)

        return render(response, "main/list.html", {"ls": ls})

    # Not user's list
    return render(response, "main/unauthorized_list.html")

# Homepage
def home(response):
    return render(response, "main/home.html", {})

# Create a new list


@login_required
def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            t = ToDoList(name=name)
            t.save()
            response.user.todolist.add(t)
            return HttpResponseRedirect("/%i" % t.id)
    else:
        form = CreateNewList()

    return render(response, "main/create.html", {"form": form})

# Static view page
def view(response):
    return render(response, "main/view.html", {})
