# TP_Estructuras_2Q2024
 Trabajo Final "Todos Comunicados" de Estrucutras de Datos y Programación. 2Q2024
Aca completamos las ideas de cada punto y cómo lo vamos a implementar y si ya se hizo.

SISTEMA A IMPLEMENTAR

Se requiere modelar las funcionalidades de un teléfono celular.

Un teléfono celular tiene al menos los siguientes atributos:
ID (único), Nombre, Modelo, Sistema Operativo y versión, capacidad de memoria RAM, capacidad de
almacenamiento y número telefónico.

Un teléfono celular debe al menos poder:
1. Prenderse y apagarse. OK

2. Bloquearse y desbloquearse. OK

3. Abrir una cierta aplicación para interactuar con ella (Contactos, Mensajería SMS, e-mail, Teléfono,
App Store, Configuración, etc.), para al menos poder:
    a. Realizar llamadas a otros teléfonos marcando el número.. OK
    b. Recibir llamadas de otros números. OK
    c. Terminar una llamada en curso. OK
    d. Agendar y actualizar contactos OK
    e. Enviar y recibir mensajes de texto (SMS) a un número de destino. OK
    f. Ver bandeja de entrada de SMS e historial de llamadas. OK
    g. Eliminar mensajes (SMS). OK
    h. Ver e-mails, los cuales deben poder consultarse según:
        i. “no leídos primeros” OK
        ii. “por fecha” (del último en llegar al primero) OK
    i. Descargar una nueva app desde la tienda de aplicaciones. OK
    j. Configurar:
        i. nombre de teléfono, código de desbloqueo. OK
        ii. Activar red móvil: cada vez que el dispositivo se enciende esta acción debe ejecutarse. OK
        iii. Desactivar red móvil OK
        iv. Activar y desactivar datos (conectividad a internet) OK


¿Cómo ocurre la comunicación?

En el mundo real, los dispositivos móviles se registran en la red cuando están encendidos y conectados. Los
teléfonos envían actualizaciones a las torres de la red móvil sobre su estado (encendido, apagado,
disponible, sin red, etc.). Esto le permite a la red (y a la central) saber si un dispositivo está disponible
para recibir llamadas o mensajes.

Una operadora puede dar de alta el dispositivo en la central (registro) o eliminarlo (baja). Cualquier
comunicación será posible cuando los dispositivos que se comunican estén registrados en la central, con red
móvil activa y, si requieren servicios de internet, con datos móviles activos.

Tanto la gestión de llamadas como de SMS y el acceso a internet debe ser mediada por una central. A
efectos de este TP, toda la comunicación pasa a través de una única central.

Para iniciar una comunicación, el dispositivo del emisor, a través de la aplicación (Teléfono, SMS), envía a la
central una solicitud de conexión con la información relevante (aplicación de origen, número de teléfono
de destino, [mensaje], etc.). La central se encarga de verificar que ambos dispositivos estén registrados y
disponibles para comunicarse. Una vez establecida la conexión, los dispositivos móviles son responsables de
gestionar la recepción de la comunicación entrante y de aceptarla.

Para ello, la central debe al menos poder:
    - Verificar el estado de los dispositivos que quieren comunicarse.
    - Verificar los teléfonos que están registrados en la red.
    - Verificar el estado de los dispositivos que intentan acceder a internet.
    - Establecer y mediar la comunicación (Ej. dirigir un mensaje al destino, gestionar el estado
        “ocupado” durante las llamadas, etc.).
    - Mantener un registro (log) de la información de cada una de las comunicaciones, que será útil para
        el análisis de datos.
