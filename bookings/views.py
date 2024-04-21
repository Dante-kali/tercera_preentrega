from django.shortcuts import render, redirect

from .forms import ReservaCreateForm, ReservaSearchForm, SalaCreateForm
from .models import Reserva, Sala


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


def search_with_form_view(request):
    if request.method == "GET":
        form = ReservaSearchForm()
        return render(
            request, "bookings/form-search.html", context={"search_form": form}
        )
    elif request.method == "POST":
        #  devolverle a "chrome" la lista de reservas encontrada o avisar que no se encontró nada
        form = ReservaSearchForm(request.POST)
        if form.is_valid():
            nombre_de_usuario = form.cleaned_data["nombre_de_usuario"]
        reservas_del_usuario = Reserva.objects.filter(
            nombre_de_usuario=nombre_de_usuario
        ).all()
        contexto_dict = {"todas_las_reservas": reservas_del_usuario}
        return render(request, "bookings/list.html", contexto_dict)


def detail_view(request, booking_id):
    reserva = Reserva.objects.get(id=booking_id)
    contexto_dict = {"reserva": reserva}
    return render(request, "bookings/detail.html", contexto_dict)


def detail_sala_view(request, sala_id):
    sala = Sala.objects.get(id=sala_id)
    contexto_dict = {"sala": sala}
    return render(request, "bookings/detail-sala.html", contexto_dict)


# -----------------------------------------------------------------------------
# CLASE 22
# -----------------------------------------------------------------------------

# CRUD
from django.http import HttpResponse


def sala_list_view(request):
    todas_las_salas = Sala.objects.all()
    contexto = {"SANTIAGOMOTORIZADO": todas_las_salas}
    return render(request, "bookings/salas/list.html", contexto)


def sala_delete_view(request, sala_id):
    sala_a_borrar = Sala.objects.filter(id=sala_id).first()
    sala_a_borrar.delete()
    return redirect("sala-list")


def sala_update_view(request, sala_id):
    sala_a_editar = Sala.objects.filter(id=sala_id).first()
    if request.method == "GET":
        valores_iniciales = {
            "nombre": sala_a_editar.nombre,
            "disponible": sala_a_editar.disponible,
            "capacidad": sala_a_editar.capacidad,
            "descripcion": sala_a_editar.descripcion,
        }
        formulario = SalaCreateForm(initial=valores_iniciales)
        contexto = {"ENRIQUE": formulario, "OBJETO": sala_a_editar}
        return render(request, "bookings/salas/form_update.html", contexto)
    elif request.method == "POST":
        form = SalaCreateForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            disponible = form.cleaned_data["disponible"]
            capacidad = form.cleaned_data["capacidad"]
            descripcion = form.cleaned_data["descripcion"]
            sala_a_editar.nombre = nombre
            sala_a_editar.disponible = disponible
            sala_a_editar.capacidad = capacidad
            sala_a_editar.descripcion = descripcion
            sala_a_editar.save()
            return redirect("sala-detail", sala_a_editar.id)


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