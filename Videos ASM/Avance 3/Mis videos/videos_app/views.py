from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import CapturaUsuarioForm, VideoForm
from .models import Usuario, Video


@require_http_methods(["GET", "POST"])
def index(request):
    """
    Flujo en una sola vista (simple para Avance 4):
    - Paso 1 (GET o POST inicial): captura nómina, nombre, cantidad_videos
    - Paso 2 (POST con confirmación y N videos): valida y guarda en PostgreSQL
    """

    # Paso 2: ya vienen los videos (detectamos por bandera hidden)
    if request.method == "POST" and request.POST.get("paso") == "videos":
        usuario_form = CapturaUsuarioForm({
            "nomina": request.POST.get("nomina", ""),
            "nombre": request.POST.get("nombre", ""),
            "cantidad_videos": request.POST.get("cantidad_videos", "1"),
        })

        # cantidad real (para reconstruir y validar N forms)
        try:
            cantidad = int(request.POST.get("cantidad_videos", "1"))
        except ValueError:
            cantidad = 1

        video_forms = []
        videos_validos = True

        # Construimos forms de video por índice
        for i in range(1, cantidad + 1):
            vf = VideoForm({
                "titulo": request.POST.get(f"titulo_{i}", ""),
                "nombre": request.POST.get(f"nombre_{i}", ""),
                "extension": request.POST.get(f"extension_{i}", ""),
                "tamano_mb": request.POST.get(f"tamano_{i}", ""),
            })
            if not vf.is_valid():
                videos_validos = False
            video_forms.append((i, vf))

        # Validar usuario + videos
        if usuario_form.is_valid() and videos_validos:
            # Guardar en BD (PostgreSQL Pro_Gol)
            usuario = Usuario.objects.create(
                nomina=usuario_form.cleaned_data["nomina"],
                nombre=usuario_form.cleaned_data["nombre"],
            )

            for i, vf in video_forms:
                Video.objects.create(
                    usuario=usuario,
                    titulo=vf.cleaned_data["titulo"],
                    nombre=vf.cleaned_data["nombre"],
                    extension=vf.cleaned_data["extension"],
                    tamano_mb=vf.cleaned_data["tamano_mb"],
                )

            return render(request, "videos_app/index.html", {
                "modo": "exito",
                "usuario": usuario,
                "cantidad": cantidad,
            })

        # Si falla validación, re-render paso 2 con errores
        return render(request, "videos_app/index.html", {
            "modo": "videos",
            "usuario_form": usuario_form,
            "cantidad": cantidad,
            "video_forms": video_forms,
        })

    # Paso 1: captura usuario y cantidad
    if request.method == "POST":
        usuario_form = CapturaUsuarioForm(request.POST)
        if usuario_form.is_valid():
            cantidad = usuario_form.cleaned_data["cantidad_videos"]

            # Renderizar paso 2 (captura N videos)
            video_forms = [(i, VideoForm()) for i in range(1, cantidad + 1)]
            return render(request, "videos_app/index.html", {
                "modo": "videos",
                "usuario_form": usuario_form,
                "cantidad": cantidad,
                "video_forms": video_forms,
            })

        # Si falla usuario, volver a modo usuario con errores
        return render(request, "videos_app/index.html", {
            "modo": "usuario",
            "usuario_form": usuario_form,
        })

    # GET inicial
    return render(request, "videos_app/index.html", {
        "modo": "usuario",
        "usuario_form": CapturaUsuarioForm(),
    })