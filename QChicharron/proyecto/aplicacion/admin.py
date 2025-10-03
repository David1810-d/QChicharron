from django.contrib import admin

from aplicacion.models import Menu, MenuProducto, Plato, Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'marca', 'stock']

@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio']

admin.site.register(Menu)
admin.site.register(MenuProducto)