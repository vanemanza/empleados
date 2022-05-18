from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, TemplateView

from . models import Persona

# 0) Template Base - Home
class HomeListView(ListView):
    template_name = 'home.html'
    queryset = Persona.objects.all().order_by('apellido')
    paginate_by = 7
    context_object_name = 'lista'

    def get_context_data(self, **kwargs):         
        context =  super().get_context_data(**kwargs)  
        return context

# 1) listar todos los empleados de la empresa
class EmpleadosListView(ListView):
    template_name = "lista_empleados.html" #es la ruta donde está el archivo html con el q vamos a trabajar
    queryset = Persona.objects.all().order_by('apellido')
    paginate_by = 5 # para optimizar la consulta y q no sea tan pesada, internamente tiene el parametro page=
    #ordering = 'apellido'
    #model = Persona #listView requiere un modelo
    context_object_name = 'lista' #nombre del objeto a traves del cual accedo en html -> {{lista}}
    #listView : la vista se retorna x defecto en un object list, x eso no hace falta pasarle el context_object_name
    
    def get_context_data(self, **kwargs): 
        context =  super().get_context_data(**kwargs)# este es el contexto q enviamos al template
        print(context)
        # el contexto posee los siguientes objetos:
            # paginator
            # page_obj
            # is_paginated
            # object_list
        return context
   

# 2) listar todos los empleados q pertenecen a un area de la empresa
# class EmpleadosPorAreaListView(ListView):
#     """ lista empleados de una empresa por areas"""
#     queryset = Persona.objects.filter(departamento__nombre='area contable') # no es muy eficiente xq le tengo q indicar en el filtro el area cada vez
#     template_name = "lista_por_area.html"

class EmpleadosPorAreaListView(ListView):
    """ lista empleados de una empresa por areas"""
    #model = Persona
    # en vez de model puedo usar atributo queryset para filtrar segun lo q necesite y no toda la lista
    #queryset = Persona.objects.filter(departamento__nombre='area contable') # no es muy eficiente xq le tengo q indicar en el filtro el area cada vez
    #en vez de usar atributo queryset, uso metodo get_queryset q retorna una lista
    template_name = "lista_por_area.html"

    def get_queryset(self):
        # puedo sobreescribir el metodo q trae x defaul el ListView
        # retorna una lista de elementos
        # el valor devuelto debe ser un iterable o una instancia del queryset
        area = self.kwargs['departamento'] # recupero el parametro q me envian por url!
        lista = Persona.objects.filter(departamento__nombre=area)
        return lista


# 3) listar empleados por trabajo
    # para hacer de tarea, como práctica

class EmpleadosPorTrabajoListView(ListView):
    #model = Persona
    template_name = "empleados_por_trabajo.html"
    #context_object_name = 'lista_puesto'

    def get_queryset(self):
        puesto = self.request.GET.get("trabajo", "")        
        lista = Persona.objects.filter(puesto=puesto)
        return lista          


# 4) listar los empleados por palabra clave

class EmpleadosPorNombre(ListView):
    """
    Lista empleados por palabra clave
    """
    template_name = "empleado_por_nombre.html"
    context_object_name = 'empleados'

    def get_queryset(self) : # función donde haré el filtro!
        print('***************************************')
        palabra_clave = self.request.GET.get("kword", "") # del objeto request recupero lo q tenga metodo GET con get
        lista = Persona.objects.filter(nombre=palabra_clave)
        print(f'---- lista resultado: {lista}-------------')
        return lista



# 5) listar habilidades de un empleado

class HabilidadesList(ListView):
    template_name = 'habilidades.html'
    context_object_name = 'habilidades'

    def get_queryset(self):
        # el atributo habilidades es un ManyToMany con la tabla Habilidades
        # primero debo obtener un REGISTRO de un empleado y no un queryset
        # para cada empleado recuperar su lista de habilidades
        id_empleado = self.request.GET.get("id_empleado", "")
        empleado = Persona.objects.get(id=id_empleado)      
        return empleado.habilidad.all()


class EmpleadoDetailView(DetailView):
    model = Persona
    template_name = "detalles_empleado.html"

    # def get_object(self, queryset: Optional[models.query.QuerySet[_M]] = ...) -> _M: #redefine la forma de recuperar un objeto
    #     return super().get_object(queryset)


    def get_context_data(self, **kwargs): # envia alguna variable extra hacia el template,alguna q no esté dentro de los atrs del modelo
        context = super(EmpleadoDetailView, self).get_context_data(**kwargs)
        context['titulo'] = 'Empleado del Mes'
        #debo crear un proceso para determinar si el context es un empleado del mes o no
        return context

class RegistroExitoso(TemplateView):
    template_name = "registro_exitoso.html"


class EmpleadoCreateView(CreateView):
    template_name = "registrar_empleado.html"
    model = Persona       
    fields = '__all__' 
    success_url = reverse_lazy('registro_exitoso')
    