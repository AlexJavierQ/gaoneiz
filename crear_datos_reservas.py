#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pro_camara_comercio.settings')
django.setup()

from reservas.models import TipoLugar, Lugar

def crear_datos_reservas():
    print("Creando datos de prueba para el sistema de reservas...")
    
    # Crear tipos de lugares
    tipos_lugares = [
        {
            'nombre': 'Sala de Reuniones',
            'descripcion': 'Espacios ideales para reuniones de trabajo y presentaciones',
            'capacidad_maxima': 12,
            'precio_por_hora': 25.00
        },
        {
            'nombre': 'Auditorio',
            'descripcion': 'Espacios amplios para conferencias y eventos',
            'capacidad_maxima': 100,
            'precio_por_hora': 80.00
        },
        {
            'nombre': 'Sala de Capacitación',
            'descripcion': 'Espacios equipados para talleres y capacitaciones',
            'capacidad_maxima': 30,
            'precio_por_hora': 40.00
        },
        {
            'nombre': 'Oficina Privada',
            'descripcion': 'Espacios privados para trabajo individual o pequeños equipos',
            'capacidad_maxima': 4,
            'precio_por_hora': 15.00
        }
    ]
    
    for tipo_data in tipos_lugares:
        tipo, created = TipoLugar.objects.get_or_create(
            nombre=tipo_data['nombre'],
            defaults=tipo_data
        )
        if created:
            print(f"✅ Creado tipo de lugar: {tipo.nombre}")
        else:
            print(f"ℹ️  Ya existe tipo de lugar: {tipo.nombre}")
    
    # Crear lugares específicos
    lugares = [
        {
            'nombre': 'Sala Ejecutiva A',
            'tipo': 'Sala de Reuniones',
            'ubicacion': 'Piso 2, Ala Norte',
            'descripcion': 'Sala moderna con vista panorámica, ideal para reuniones ejecutivas',
            'equipamiento': 'Proyector 4K, Sistema de videoconferencia, Pizarra inteligente, WiFi de alta velocidad, Aire acondicionado'
        },
        {
            'nombre': 'Sala Ejecutiva B',
            'tipo': 'Sala de Reuniones',
            'ubicacion': 'Piso 2, Ala Sur',
            'descripcion': 'Sala elegante con mesa de juntas para 12 personas',
            'equipamiento': 'TV LED 55", Sistema de audio, Pizarra tradicional, WiFi, Cafetera'
        },
        {
            'nombre': 'Auditorio Principal',
            'tipo': 'Auditorio',
            'ubicacion': 'Planta Baja, Entrada Principal',
            'descripcion': 'Auditorio principal con capacidad para 100 personas',
            'equipamiento': 'Sistema de sonido profesional, Proyector láser, Escenario, Iluminación LED, Aire acondicionado central'
        },
        {
            'nombre': 'Sala de Capacitación Norte',
            'tipo': 'Sala de Capacitación',
            'ubicacion': 'Piso 1, Ala Norte',
            'descripcion': 'Sala amplia con disposición tipo aula para capacitaciones',
            'equipamiento': 'Proyector, Sistema de audio, 30 sillas con mesa, Pizarra acrílica, WiFi'
        },
        {
            'nombre': 'Sala de Capacitación Sur',
            'tipo': 'Sala de Capacitación',
            'ubicacion': 'Piso 1, Ala Sur',
            'descripcion': 'Sala versátil para talleres y seminarios',
            'equipamiento': 'TV interactiva, Sistema de audio, Mesas modulares, Pizarra móvil, WiFi'
        },
        {
            'nombre': 'Oficina Privada 1',
            'tipo': 'Oficina Privada',
            'ubicacion': 'Piso 3, Oficina 301',
            'descripcion': 'Oficina privada para trabajo individual o reuniones pequeñas',
            'equipamiento': 'Escritorio ejecutivo, 4 sillas, WiFi, Teléfono, Aire acondicionado'
        },
        {
            'nombre': 'Oficina Privada 2',
            'tipo': 'Oficina Privada',
            'ubicacion': 'Piso 3, Oficina 302',
            'descripcion': 'Oficina cómoda con vista al jardín',
            'equipamiento': 'Mesa de reuniones, 4 sillas ergonómicas, WiFi, Teléfono, Ventilación natural'
        }
    ]
    
    for lugar_data in lugares:
        tipo_lugar = TipoLugar.objects.get(nombre=lugar_data['tipo'])
        lugar_data['tipo'] = tipo_lugar
        
        lugar, created = Lugar.objects.get_or_create(
            nombre=lugar_data['nombre'],
            defaults=lugar_data
        )
        if created:
            print(f"✅ Creado lugar: {lugar.nombre}")
        else:
            print(f"ℹ️  Ya existe lugar: {lugar.nombre}")
    
    print("\n🎉 Datos de prueba creados exitosamente!")
    print(f"📊 Total tipos de lugares: {TipoLugar.objects.count()}")
    print(f"📍 Total lugares: {Lugar.objects.count()}")

if __name__ == '__main__':
    crear_datos_reservas()