# NEO GAIAM WordPress Export

Este directorio contiene componentes y recursos para implementar la plataforma NEO GAIAM en WordPress.

## Instrucciones de instalación

### Opción 1: Como un plugin

1. Comprime la carpeta 'wp-export' como un archivo ZIP
2. En WordPress, ve a Plugins > Añadir nuevo > Subir plugin
3. Sube el archivo ZIP y activa el plugin
4. Los shortcodes estarán disponibles para usar en tus páginas

### Opción 2: Integración manual en el tema

1. Sube las carpetas 'js', 'css' y 'assets' al directorio de tu tema
2. Incluye el código de 'components/functions.php' en el archivo functions.php de tu tema
3. Incluye o crea el archivo 'components/shortcodes.php' en tu tema

## Uso de los componentes

Cada componente se puede usar como un shortcode en tus páginas de WordPress:

### Cubo de Metatrón (Navegación)

```
[neogaiam_metatron_cube size="500" rotation_speed="0.005" wooden_style="true" pulse_effect="true"]
```

### Flor de la Vida (Geometría Sagrada)

```
[neogaiam_flower_of_life size="300" opacity="0.7" animation_duration="60"]
```

### Campo de Estrellas (Fondo cósmico)

```
[neogaiam_star_field count="200" container_height="500"]
```

### Formulario de Reserva

```
[neogaiam_booking_form service_id="1" service_name="Lectura Astrológica" has_levels="true" astrology_fields="true"]
```

### Selector de Idiomas

```
[neogaiam_language_switcher languages="en,es" show_flags="true"]
```

## Personalización

### Estilos

Puedes personalizar los estilos editando los archivos CSS en la carpeta 'css'.
La paleta de colores principal se define en 'css/neogaiam.css'.

### Internacionalización

Los componentes soportan múltiples idiomas. Puedes:

1. Usar el plugin WPML o Polylang para traducción completa del sitio
2. Los archivos de traducción se encuentran en 'assets/locales'
3. Editar el archivo JS correspondiente para añadir más traducciones

## Integración con el backend

El formulario de reservas está configurado para procesarse mediante AJAX en WordPress.
Para personalizar el procesamiento:

1. Edita la función 'neogaiam_process_booking' en functions.php
2. Configura las notificaciones por correo electrónico según tus necesidades
3. Los datos se almacenan en un custom post type 'neogaiam_booking'

## Soporte

Para consultas o soporte adicional, contacta con el equipo de NEO GAIAM.
