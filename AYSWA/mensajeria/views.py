from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Mensaje
from django.db.models import Q

@login_required
def chat(request):
    return render(request, 'mensajeria/chat.html')

@login_required
def conversaciones(request):
    usuario = request.user

    mensajes = Mensaje.objects.filter(
        Q(emisor=usuario) | Q(receptor=usuario)
    )

    usuarios_ids = set()

    for m in mensajes:
        if m.emisor != usuario:
            usuarios_ids.add(m.emisor.id)
        if m.receptor != usuario:
            usuarios_ids.add(m.receptor.id)

    usuarios = User.objects.filter(id__in=usuarios_ids)

    data = [{"id": u.id, "username": u.username} for u in usuarios]

    return JsonResponse(data, safe=False)

@login_required
def obtener_mensajes(request, usuario_id):
    usuario_actual = request.user
    otro_usuario = get_object_or_404(User, id=usuario_id)

    mensajes = Mensaje.objects.filter(
        Q(emisor=usuario_actual, receptor=otro_usuario) |
        Q(emisor=otro_usuario, receptor=usuario_actual)
    ).order_by('fecha')

    data = []

    for m in mensajes:
        data.append({
            "texto": m.contenido,
            "mio": m.emisor == usuario_actual
        })

    return JsonResponse(data, safe=False)

@login_required
def enviar_mensaje(request):
    if request.method == "POST":
        usuario_actual = request.user
        receptor_id = request.POST.get("receptor_id")
        texto = request.POST.get("mensaje")

        receptor = get_object_or_404(User, id=receptor_id)

        Mensaje.objects.create(
            emisor=usuario_actual,
            receptor=receptor,
            contenido=texto
        )

        return JsonResponse({"status": "ok"})