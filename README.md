# Proyecto IoT con ESP32 + MicroPython + MongoDB Atlas + Grafana

## Visión Empresarial
Este proyecto demuestra cómo un sensor de sonido conectado a un ESP32 puede integrarse en una arquitectura IoT empresarial.  
La solución permite capturar, transmitir y visualizar datos en tiempo real, con un enfoque en seguridad, escalabilidad y analítica.

En un escenario corporativo, este patrón puede extenderse a:
- Monitoreo de ambientes (ruido, temperatura, vibración).
- Integración con sistemas de seguridad y cumplimiento normativo.
- Dashboards ejecutivos en Grafana para toma de decisiones.
- Escalabilidad en la nube con bases de datos distribuidas y contenedores Docker.

---

## Arquitectura del Proyecto
- **ESP32 con MicroPython**: dispositivo de bajo costo que captura datos del sensor de sonido.  
- **Backend en contenedor Docker**: expone un servicio REST para recibir datos desde los dispositivos.  
- **MongoDB Atlas (Cloud)**: base de datos NoSQL en la nube, segura y escalable, que centraliza la información.  
- **Grafana**: herramienta de visualización que se conecta directamente a Atlas para mostrar métricas en tiempo real.  

---

## Flujo de Implementación
1. Flasheo del ESP32 con firmware MicroPython para habilitar la programación en alto nivel.  
2. Prueba inicial del sensor en Thonny para validar lecturas digitales y analógicas.  
3. Configuración del backend en Docker para recibir y procesar datos.  
4. Conexión del backend con MongoDB Atlas mediante credenciales seguras.  
5. Integración de Grafana con Atlas para crear dashboards ejecutivos y analíticos.  


