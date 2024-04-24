from django.shortcuts import render, redirect
from .models import Reserva, Sala


def home_view(request):
    return render(request, "bookings/home.html")


def list_view(request):
    reservas = Reserva.objects.all()
    contexto_dict = {"todas_las_reservas": reservas}
    return render(request, "bookings/list.html", contexto_dict)


def search_view(request, nombre_de_usuario):
    reservas_del_usuario = Reserva.objects.filter(
        nombre_de_usuario=nombre_de_usuario
    ).all()
    contexto_dict = {"reservas": reservas_del_usuario}
    return render(request, "bookings/list.html", contexto_dict)


def detail_view(request, booking_id):
    reserva = Reserva.objects.get(id=booking_id)
    contexto_dict = {"reserva": reserva}
    return render(request, "bookings/detail.html", contexto_dict)


def detail_sala_view(request, sala_id):
    sala = Sala.objects.get(id=sala_id)
    contexto_dict = {"sala": sala}
    return render(request, "bookings/detail-sala.html", contexto_dict)


# FORM
from .forms import ReservaCreateForm, ReservaSearchForm, SalaCreateForm


def create_with_form_view(request):
    contexto = {"create_form": ReservaCreateForm()}
    return render(request, "bookings/form-create.html", contexto)


def create_sala_with_form_view(request):
    if request.method == "GET":
        contexto = {"LUISMIGUEL": SalaCreateForm()}
        return render(request, "bookings/form-create-sala.html", contexto)
    elif request.method == "POST":
        form = SalaCreateForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            disponible = form.cleaned_data["disponible"]
            capacidad = form.cleaned_data["capacidad"]
            descripcion = form.cleaned_data["descripcion"]
            nueva_sala = Sala(
                nombre=nombre,
                disponible=disponible,
                capacidad=capacidad,
                descripcion=descripcion,
            )
            nueva_sala.save()
            return detail_sala_view(request, nueva_sala.id)
        

def search_with_form_view(request):
    if request.method == "GET":
        form = ReservaSearchForm()
        return render(
            request, "bookings/form-search.html", context={"search_form": form}
        )
    elif request.method == "POST":
        form = ReservaSearchForm(request.POST)
        if form.is_valid():
            nombre_de_usuario = form.cleaned_data["nombre_de_usuario"]
        reservas_del_usuario = Reserva.objects.filter(
            nombre_de_usuario=nombre_de_usuario
        ).all()
        contexto_dict = {"todas_las_reservas": reservas_del_usuario}
        return render(request, "bookings/list.html", contexto_dict)
    

# CRUD
from django.http import HttpResponse


def sala_list_view(request):
    salas = Sala.objects.all()
    context = {
        'SANTIAGOMOTORIZADO' : salas
    }
    return render(request, 'bookings/salas/list.html', context)


def sala_delete_view(request, sala_id):
    sala_delete = Sala.objects.filter(id=sala_id).first()
    sala_delete.delete()
    return redirect(sala_list_view)



def sala_update_view(request, sala_id):
    sala_edite = Sala.objects.filter(id=sala_id).first()
    valores_iniciales = {
        'nombre' : sala_edite.nombre,
        'disponible' : sala_edite.disponible,
        'capacidad' : sala_edite.capacidad,
        'descripcion' : sala_edite.descripcion
    }
    form = SalaCreateForm(initial=valores_iniciales)
    context = {'ENRIQUE' : form}
    return render(request, 'bookings/salas/form_update.html', context)


def search_sala_view(request):
    return HttpResponse("not implemented!")


# Vistas basadas en clases "VBC"

from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


class SalaListView(ListView):
    model = Sala
    template_name = "bookings/vbc/sala_list.html"
    context_object_name = "ADRIANDARGELOS"


class SalaDetailView(DetailView):
    model = Sala
    template_name = "bookings/vbc/sala_detail.html"
    context_object_name = "GUSTAVOCERATI"


class SalaCreateView(CreateView):
    model = Sala
    template_name = "bookings/vbc/sala_form.html"
    fields = ["nombre", "disponible", "capacidad", "descripcion"]
    success_url = reverse_lazy("vbc_sala_list")


class SalaUpdateView(UpdateView):
    model = Sala
    template_name = "bookings/vbc/sala_form.html"
    fields = ["nombre", "disponible", "capacidad", "descripcion"]
    context_object_name = "sala"
    success_url = reverse_lazy("vbc_sala_list")


class SalaDeleteView(DeleteView):
    model = Sala
    template_name = "bookings/vbc/sala_confirm_delete.html"
    success_url = reverse_lazy("vbc_sala_list")