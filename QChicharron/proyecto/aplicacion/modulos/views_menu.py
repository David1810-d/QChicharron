from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from aplicacion.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from aplicacion.forms import MenuForm, MenuProducto
from django.forms import inlineformset_factory
from django.db import transaction
from django import forms

# Crear el formset para MenuProducto
MenuProductoFormSet = inlineformset_factory(
    Menu,
    MenuProducto,
    fields=['producto', 'cantidad', 'orden'],
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
    widgets={
        'producto': forms.Select(attrs={'class': 'form-control'}),
        'cantidad': forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01'
        }),
        'orden': forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        }),
    }
)

class MenuListView(ListView):
    model = "Menu"
    template_name = 'modulos/menu.html'
    context_object_name = 'menus'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Menús'
        context['menu'] = 'menu'
        return context

class MenuCreateView(CreateView):
    model = Menu
    template_name = 'forms/forms_menu_crear.html'
    form_class = MenuForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nuevo Menú'
        context['modulo'] = "menu"
        
        if self.request.POST:
            context['formset'] = MenuProductoFormSet(self.request.POST)
        else:
            context['formset'] = MenuProductoFormSet()
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        with transaction.atomic():
            self.object = form.save()
            
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                # Si el formset no es válido, retornar al formulario con errores
                return self.form_invalid(form)
        
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('apl:menu_list')

class MenuUpdateView(UpdateView):
    model = "Menu"
    template_name = 'forms/formulario_actualizacion.html'
    form_class = MenuForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Menú'
        context['modulo'] = "menu"
        
        if self.request.POST:
            context['formset'] = MenuProductoFormSet(
                self.request.POST, 
                instance=self.object
            )
        else:
            context['formset'] = MenuProductoFormSet(instance=self.object)
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        with transaction.atomic():
            self.object = form.save()
            
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                return self.form_invalid(form)
        
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('apl:menu_list')

class MenuDeleteView(DeleteView):
    model = "Menu"
    template_name = 'forms/confirmar_eliminacion.html'
    
    def get_success_url(self):
        return reverse_lazy('apl:menu_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Menú'
        return context