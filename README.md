# 🚗 ServiExpress – Sistema de Gestión Automotriz
![Home](servi_assets/home/home1.png)

Bienvenidos a **Serviexpress**, un sistema web desarrollado con **Django** para la gestión integral de servicios automotrices.  
La plataforma permite administrar clientes, servicios, reservas, usuarios y flujos operativos desde un panel centralizado, optimizando la atención y el control del negocio.

🌐 Demo en línea: https://tu-demo-en-render.onrender.com/

---

## 🌐 Descripción

**Serviexpress** optimiza la gestión de un centro de servicios automotrices mediante una aplicación web con múltiples roles y funcionalidades clave:

- **Cliente:** puede registrarse, iniciar sesión y gestionar solicitudes de servicios.  
- **Técnico / Operador:** visualiza y gestiona servicios asignados.  
- **Administrador:** controla usuarios, servicios, estados, precios y configuración general del sistema.

---

### 🔧 Características principales

- Registro y autenticación de usuarios  
- Control de acceso por roles  
- Gestión de servicios automotrices  
- Sistema de solicitudes y seguimiento  
- Panel administrativo completo  
- Gestión de estados de servicios  
- Manejo de archivos estáticos y media  
- Seguridad integrada mediante Django  

---

## 👥 Colaboradores

- **Diego Roa** – [@RoaStack](https://github.com/RoaStack)
- **Gustavo Muñoz** – [@HTTPResponseG](https://github.com/HTTPResponseG)
- **Isaac Gonzalez** – [@iisaacandres](https://github.com/iisaacandres)


Durante el desarrollo del proyecto se aplicaron buenas prácticas con **Git y GitHub**, incluyendo:

- Uso de ramas por funcionalidad  
- Commits descriptivos y controlados  
- Integración progresiva de cambios  
- Organización del código por módulos  

---

## 📁 Estructura del proyecto
```
serviexpress/
├── boletas/                # Gestión de boletas
├── pedidos/                # Pedidos y flujo de compra
├── proveedores/            # Gestión de proveedores
├── repuestos/              # Repuestos automotrices
├── reservas/               # Sistema de reservas
├── servicios/              # Servicios automotrices
├── usuarios/               # Usuarios, roles y autenticación
├── carrito/                # Carrito de servicios
├── templates/              # Plantillas HTML
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── media/                  # Archivos subidos
├── serviexpress/           # Configuración principal del proyecto
│   ├── settings.py         # Configuración general
│   ├── urls.py             # Enrutamiento principal
│   └── wsgi.py             # Configuración WSGI
├── build.sh                # Script de despliegue en Render
├── create_superuser.py     # Creación automática de superusuario
├── manage.py               # Comando principal de Django
└── README.md               # Documentación del proyecto
```
---

## 🗃️ Modelamiento Base de Datos
![BaseDeDatos](servi_assets/baseDeDatos.png)

---

## ⚙️ Instalación y ejecución local

1️⃣ Clonar el repositorio

git clone https://github.com/tuusuario/serviexpress.git
cd serviexpress

2️⃣ Crear y activar entorno virtual

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

3️⃣ Instalar dependencias

pip install -r requirements.txt

4️⃣ Configurar variables de entorno (.env)
SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

5️⃣ Aplicar migraciones

python manage.py migrate

6️⃣ Crear un superusuario

python manage.py createsuperuser

7️⃣ Ejecutar el servidor

python manage.py runserver

Luego accede a 👉 http://127.0.0.1:8000/

---
## 🔒 Seguridad

El sistema incluye múltiples medidas de seguridad:

Contraseñas cifradas con hash seguro

Protección contra CSRF, XSS y SQL Injection

Manejo de sesiones y permisos

Validación de formularios

Configuración segura de variables de entorno

---
## 🖼️ Capturas de pantalla
**Home**

![url](servi_assets/home/url.png)
![Home1](servi_assets/home/home1.png)
![Home2](servi_assets/home/home2.png)
![Home3](servi_assets/home/home3.png)
![Home4](servi_assets/home/home4.png)
![Home5](servi_assets/home/home5.png)
![InicioSesion](servi_assets/login_y_registro/login.png)
![Registro](servi_assets/login_y_registro/registro.png)
---
**Panel Admin**
![PanelAdmin](servi_assets/admin/panelAdmin.png)
![PerfilAdmin](servi_assets/admin/perfilAdmin.png)
![GestionUsuarios](servi_assets/admin/GestionUsuarios.png)
![GestionMecanico](servi_assets/admin/GestionMecanico.png)
![EditarDatosMecanico](servi_assets/admin/editarDatosMecanico.png)
![GestionDisponibilidad](servi_assets/admin/crearDisponibilidad.png)
![GestionDisponibilidad1](servi_assets/admin/gestionDisponibilidad.png)
![GestionCliente](servi_assets/admin/gestionCliente.png)
![CrearCliente](servi_assets/admin/crearCliente.png)
![GestionRepuesto](servi_assets/admin/gestionRepuestos.png)
![AgregarRepuesto](servi_assets/admin/agregarRepuesto.png)
![reportes](servi_assets/admin/reportes.png)
![GestionServicio](servi_assets/admin/GestionServicios.png)
![GestionProveedores](servi_assets/admin/GestionProveedor.png)
![agregarProveedores](servi_assets/admin/agregarProveedor.png)
---
**Panel Cliente**
![PanelCliente](servi_assets/cliente/panelCliente.png)
![PerfilCliente](servi_assets/cliente/perfilCliente.png)
![CrearReserva](servi_assets/cliente/crearReserva.png)
![MisReservas](servi_assets/cliente/misReservas.png)
![ServiciosRealizados](servi_assets/cliente/serviciosRealizados.png)
![BoletaServicio](servi_assets/cliente/boletaServicioCliente.png)
![ComprarProducto](servi_assets/cliente/ecommerce.png)
![CarritoCompra](servi_assets/cliente/carritoCompra.png)
![comprobanteCompras](servi_assets/cliente/comprobanteCompra.png)
![MisCompras](servi_assets/cliente/misCompras.png)
---
**Panel Mecanico**
![PanelMecanico](servi_assets/mecanico/panelMecanico.png)
![PerfilMecanico](servi_assets/mecanico/miPerfilMecanico.png)
![OrdenesAsignadas](servi_assets/mecanico/ordenesAsignadas.png)
![ServiciosEnProceso](servi_assets/mecanico/serviciosEnProceso.png)
![RegistroRepuesto](servi_assets/mecanico/registroRepuesto.png)
![boletaServicio](servi_assets/mecanico/boletaServicio.png)
![SolicitarRepuesto](servi_assets/mecanico/OrdenPedido.png)
![ComprobanteOrden](servi_assets/mecanico/comprobanteOrdden.png)
![HistorialPedidos](servi_assets/mecanico/misPedidos.png)
![HistorialServicio](servi_assets/mecanico/historialServicio.png)
![BoletaServicio](servi_assets/mecanico/boletaServicio.png)
---
## 🧰 Tecnologías utilizadas

Python 3.13

Django 5.2

HTML5 / CSS3 / Bootstrap 5

SQLite3

PostgreSQL

Render (para despliegue en la nube)

---
## 📜 Licencia

License

Copyright (c) 2025
Gustavo Muñoz, Isaac Gonzalez ,Diego Roa
