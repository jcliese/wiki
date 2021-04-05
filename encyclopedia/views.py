from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

import random
import markdown2

from . import util

def search_f(request):
    q = request.POST["q"].lower()
    if not q:
        return render(request, "encyclopedia/error.html", {
        "error": 404
    })
    entries = [entry.lower() for entry in util.list_entries()]
    if q in entries:
        return HttpResponseRedirect(reverse("entry", args=[q]))
    elif q:
        request.session["search_query"] = []
        request.session["search_query"] = [entry for entry in entries if q in entry]
        if not request.session["search_query"]:
            return render(request, "encyclopedia/error.html", {
                "error": 'S404'
            })
        return HttpResponseRedirect(reverse("search"))
    else:
        return HttpResponseRedirect(request.path_info)

def error(request, code):
    return render(request, "encyclopedia/error.html", {
            "error": code
        })

def index(request):
    if request.method == "POST":
        return search_f(request)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if request.method == "POST":
        return search_f(request)
    if entry.upper() not in (entry.upper() for entry in util.list_entries()):
        return error(request, 404)

    content = markdown2.markdown(util.get_entry(entry))
    print("HTML", content)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "content": content
    })

def search(request):
    if request.method == "POST":
        return search_f(request)
    query = request.session["search_query"]
    return render(request, "encyclopedia/search.html", {
        "query": query
    })

def add(request):
    if request.method == "POST":
        entries = [entry.lower() for entry in util.list_entries()]
        title = request.POST["entry_title"]
        content = request.POST["entry_details"]
        if title and content:
            if title.lower() in entries:
                return error(request, 403)

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))

    return render(request, "encyclopedia/add.html")

def edit(request, entry):
    if request.method == "POST":
        entries = [entry.lower() for entry in util.list_entries()]
        title = entry
        content = request.POST["entry_details"]
        print("content::", content)
        if title and content:
            if title.lower() not in entries:
                return error(request, 403)

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))

    content = util.get_entry(entry)
    print("CONTENT", content)
    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "content": content
    })

def rand(request):
    try:
        entries = util.list_entries()
        selected_page = random.choice(entries)
        return HttpResponseRedirect(reverse("entry", args=[selected_page]))
    except:
        return render(request, "encyclopedia/rand.html")