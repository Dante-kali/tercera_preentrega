from django.urls import path

from .views import (
    home_view,
    detail_view,
    list_view,
    search_view,
    search_with_form_view,
    create_with_form_view,
    create_sala_with_form_view,
    detail_sala_view,
    # -----------------------------------------------------------------------------
    # CLASE 22
    # -----------------------------------------------------------------------------
    # CRUD
    sala_list_view,
    sala_delete_view,
    sala_update_view,
    search_sala_view,
    # VBC
    SalaListView,
    SalaDetailView,
    SalaDeleteView,
    SalaUpdateView,
    SalaCreateView,
)

urlpatterns = [
    path("", home_view),
    path("detail/<booking_id>", detail_view),
    path("list/", list_view, name="bookings-list"),
    path("buscar/<nombre_de_usuario>", search_view),
    # -----------------------------------------------------------------------------
    # CLASE 21
    # -----------------------------------------------------------------------------
    path("buscar-con-formulario/", search_with_form_view, name="zzz"),
    path("crear-reserva-con-formulario/", create_with_form_view, name="yyy"),
    path("sala/create/", create_sala_with_form_view, name="sala-create"),
    path("sala/detail/<sala_id>", detail_sala_view, name="sala-detail"),
    # -----------------------------------------------------------------------------
    # CLASE 22
    # -----------------------------------------------------------------------------
    # CRUD
    path("sala/list/", sala_list_view, name="sala-list"),
    path("sala/delete/<sala_id>", sala_delete_view, name="sala-delete"),
    path("sala/update/<sala_id>", sala_update_view, name="sala-update"),
    path("sala/buscar/", search_sala_view, name="sala-search"),
    # Vistas basadas en clases "VBC"
    path("sala/vbc/list", SalaListView.as_view(), name="vbc_sala_list"),
    path("sala/vbc/create/", SalaCreateView.as_view(), name="vbc_sala_create"),
    path("sala/vbc/<int:pk>/detail", SalaDetailView.as_view(), name="vbc_sala_detail"),
    path("sala/vbc/<int:pk>/update/", SalaUpdateView.as_view(), name="vbc_sala_update"),
    path("sala/vbc/<int:pk>/delete/", SalaDeleteView.as_view(), name="vbc_sala_delete"),
]