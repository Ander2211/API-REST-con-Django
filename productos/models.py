from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo_barra = models.CharField(max_length=50, unique=True)
    precio = models.FloatField()
    stock = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'productos'
        managed = False

    def __str__(self):
        return f"{self.nombre} ({self.codigo_barra})"
