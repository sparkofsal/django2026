from django.db import models


class Usuario(models.Model):
    # PDF: Usuario captura nómina (alfanumérico) y nombre (solo letras)
    nomina = models.CharField(max_length=30)
    nombre = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f"{self.nomina} - {self.nombre}"


class Video(models.Model):
    # Relación Usuario-Video: un usuario puede tener muchos videos
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="videos")

    # PDF: por cada video: título, nombre, extensión, tamaño
    titulo = models.CharField(max_length=120)
    nombre = models.CharField(max_length=120)
    extension = models.CharField(max_length=20)
    tamano_mb = models.DecimalField(max_digits=4, decimal_places=1)  # permite 0.0 a 99.9

    def __str__(self) -> str:
        return f"{self.titulo} ({self.extension}) - {self.tamano_mb} MB"