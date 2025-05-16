#!/usr/bin/env python
import os
import shutil
import re
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from flask import render_template
from main import app
from routes import *

"""
Script para exportar el sitio METATONEHEN como plantilla para WordPress
"""

# Carpeta donde se guardarán los archivos exportados
EXPORT_DIR = 'wordpress_export'
THEME_DIR = os.path.join(EXPORT_DIR, 'theme')
THEME_NAME = 'metatonehen'

# Asegurarse de que las carpetas de exportación existan
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

if not os.path.exists(THEME_DIR):
    os.makedirs(THEME_DIR)

# Crear estructura de carpetas para el tema de WordPress
def create_theme_structure():
    # Carpetas principales del tema
    os.makedirs(os.path.join(THEME_DIR, 'css'), exist_ok=True)
    os.makedirs(os.path.join(THEME_DIR, 'js'), exist_ok=True)
    os.makedirs(os.path.join(THEME_DIR, 'images'), exist_ok=True)
    os.makedirs(os.path.join(THEME_DIR, 'inc'), exist_ok=True)
    os.makedirs(os.path.join(THEME_DIR, 'template-parts'), exist_ok=True)
    os.makedirs(os.path.join(THEME_DIR, 'languages'), exist_ok=True)

# Copiar archivos estáticos al tema
def copy_static_files():
    # Copiar CSS
    for file in os.listdir('static/css'):
        if file.endswith('.css'):
            shutil.copy2(os.path.join('static/css', file), 
                        os.path.join(THEME_DIR, 'css', file))
    
    # Copiar JS
    for file in os.listdir('static/js'):
        if file.endswith('.js'):
            shutil.copy2(os.path.join('static/js', file), 
                        os.path.join(THEME_DIR, 'js', file))
    
    # Copiar imágenes
    for file in os.listdir('static/images'):
        src_path = os.path.join('static/images', file)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, os.path.join(THEME_DIR, 'images', file))

# Modificar URLs en archivos CSS para que funcionen con WordPress
def adapt_css_for_wordpress():
    for file in os.listdir(os.path.join(THEME_DIR, 'css')):
        if file.endswith('.css'):
            css_path = os.path.join(THEME_DIR, 'css', file)
            with open(css_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reemplazar referencias a URL Flask por URLs de tema WordPress
            content = content.replace("url(../images/", "url(../images/")
            content = content.replace("url('../images/", "url('../images/")
            content = content.replace('url("../images/', 'url("../images/')
            
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(content)

# Crear archivos básicos del tema WordPress
def create_theme_files():
    # style.css - archivo principal del tema
    style_css = f"""/*
Theme Name: METATONEHEN
Theme URI: https://metatonehen.com
Author: METATONEHEN
Author URI: https://metatonehen.com
Description: Tema personalizado para METATONEHEN, una plataforma de educación espiritual.
Version: 1.0
License: GNU General Public License v2 or later
License URI: http://www.gnu.org/licenses/gpl-2.0.html
Text Domain: metatonehen
*/

/* Este archivo es solo para la identificación del tema. Los estilos están en la carpeta css */
@import url('css/styles.css');
"""
    
    with open(os.path.join(THEME_DIR, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(style_css)
    
    # functions.php - funcionalidad básica del tema
    functions_php = """<?php
/**
 * METATONEHEN Theme functions and definitions
 */

if (!function_exists('metatonehen_setup')) :
    function metatonehen_setup() {
        // Add default posts and comments RSS feed links to head.
        add_theme_support('automatic-feed-links');

        // Let WordPress manage the document title.
        add_theme_support('title-tag');

        // Enable support for Post Thumbnails on posts and pages.
        add_theme_support('post-thumbnails');

        // Register nav menus
        register_nav_menus(array(
            'primary' => esc_html__('Primary Menu', 'metatonehen'),
            'footer' => esc_html__('Footer Menu', 'metatonehen'),
        ));

        // Add theme support for various features
        add_theme_support('html5', array(
            'search-form', 'comment-form', 'comment-list', 'gallery', 'caption',
        ));

        // Set up the WordPress core custom background feature.
        add_theme_support('custom-background');

        // Add support for block styles.
        add_theme_support('wp-block-styles');

        // Add support for full and wide align blocks.
        add_theme_support('align-wide');

        // Add support for editor styles.
        add_theme_support('editor-styles');

        // Add support for responsive embeds.
        add_theme_support('responsive-embeds');

        // Load languages
        load_theme_textdomain('metatonehen', get_template_directory() . '/languages');
    }
endif;
add_action('after_setup_theme', 'metatonehen_setup');

/**
 * Enqueue scripts and styles.
 */
function metatonehen_scripts() {
    // Bootstrap CSS
    wp_enqueue_style('bootstrap', 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css');
    
    // Font Awesome
    wp_enqueue_style('font-awesome', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
    
    // Theme stylesheet
    wp_enqueue_style('metatonehen-style', get_stylesheet_uri());
    
    // Custom CSS
    wp_enqueue_style('metatonehen-custom', get_template_directory_uri() . '/css/styles.css');
    
    // jQuery (ya incluido en WordPress)
    wp_enqueue_script('jquery');
    
    // Bootstrap JS
    wp_enqueue_script('bootstrap', 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js', array('jquery'), '', true);
    
    // Custom JS
    wp_enqueue_script('metatonehen-main', get_template_directory_uri() . '/js/main.js', array('jquery'), '', true);
}
add_action('wp_enqueue_scripts', 'metatonehen_scripts');

/**
 * Register widget area.
 */
function metatonehen_widgets_init() {
    register_sidebar(array(
        'name'          => esc_html__('Sidebar', 'metatonehen'),
        'id'            => 'sidebar-1',
        'description'   => esc_html__('Add widgets here.', 'metatonehen'),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h2 class="widget-title">',
        'after_title'   => '</h2>',
    ));
}
add_action('widgets_init', 'metatonehen_widgets_init');

/**
 * Custom template tags for this theme.
 */
require get_template_directory() . '/inc/template-tags.php';

/**
 * Custom functions that act independently of the theme templates.
 */
require get_template_directory() . '/inc/extras.php';

/**
 * Customizer additions.
 */
require get_template_directory() . '/inc/customizer.php';
"""
    
    with open(os.path.join(THEME_DIR, 'functions.php'), 'w', encoding='utf-8') as f:
        f.write(functions_php)
    
    # header.php - encabezado del tema
    header_php = """<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="profile" href="http://gmpg.org/xfn/11">
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<div id="page" class="site">
    <header id="masthead" class="site-header">
        <nav class="navbar navbar-expand-lg navbar-light">
            <div class="container">
                <a class="navbar-brand" href="<?php echo esc_url(home_url('/')); ?>">
                    METATONEHEN
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#primaryMenu" aria-controls="primaryMenu" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                
                <div class="collapse navbar-collapse" id="primaryMenu">
                    <?php
                    wp_nav_menu(array(
                        'theme_location' => 'primary',
                        'container'      => false,
                        'menu_class'     => 'navbar-nav ms-auto',
                        'fallback_cb'    => '__return_false',
                        'items_wrap'     => '<ul id="%1$s" class="%2$s">%3$s</ul>',
                        'depth'          => 2,
                        'walker'         => new bootstrap_5_wp_nav_menu_walker()
                    ));
                    ?>
                    
                    <div class="language-selector">
                        <div class="globe-icon">
                            <i class="fas fa-globe"></i>
                        </div>
                        <div class="language-dropdown">
                            <a href="?lang=en">English</a>
                            <a href="?lang=es">Español</a>
                            <a href="?lang=it">Italiano</a>
                            <a href="?lang=pt">Português</a>
                            <a href="?lang=de">Deutsch</a>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    </header>

    <div id="content" class="site-content">
"""
    
    with open(os.path.join(THEME_DIR, 'header.php'), 'w', encoding='utf-8') as f:
        f.write(header_php)
    
    # footer.php - pie de página del tema
    footer_php = """    </div><!-- #content -->

    <footer id="colophon" class="site-footer">
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <div class="footer-info">
                        <h3>METATONEHEN</h3>
                        <p>μετὰ τὸ νέἕν</p>
                        <p>Spiritual education platform for personal transformation</p>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="footer-links">
                        <h4>Quick Links</h4>
                        <?php
                            wp_nav_menu(array(
                                'theme_location' => 'footer',
                                'container'      => false,
                                'menu_class'     => 'footer-menu',
                                'fallback_cb'    => '__return_false',
                                'depth'          => 1,
                            ));
                        ?>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="footer-newsletter">
                        <h4>Join Our Newsletter</h4>
                        <p>Stay updated with our latest offerings and wisdom</p>
                        <form action="#" method="post" class="newsletter-form">
                            <input type="email" name="email" placeholder="Your email">
                            <button type="submit">Subscribe</button>
                        </form>
                    </div>
                </div>
            </div>
            
            <div class="footer-bottom">
                <div class="copyright">
                    &copy; <?php echo date('Y'); ?> METATONEHEN. All Rights Reserved.
                </div>
                <div class="social-links">
                    <a href="#"><i class="fab fa-facebook-f"></i></a>
                    <a href="#"><i class="fab fa-instagram"></i></a>
                    <a href="#"><i class="fab fa-youtube"></i></a>
                    <a href="#"><i class="fab fa-telegram"></i></a>
                </div>
            </div>
        </div>
    </footer><!-- #colophon -->
</div><!-- #page -->

<?php wp_footer(); ?>

</body>
</html>
"""
    
    with open(os.path.join(THEME_DIR, 'footer.php'), 'w', encoding='utf-8') as f:
        f.write(footer_php)
    
    # index.php - plantilla principal
    index_php = """<?php get_header(); ?>

<main id="main" class="site-main">
    <?php
    if (is_front_page()) {
        get_template_part('template-parts/content', 'home');
    } else {
        if (have_posts()) :
            while (have_posts()) : the_post();
                get_template_part('template-parts/content', get_post_format());
            endwhile;
            
            the_posts_navigation();
        else :
            get_template_part('template-parts/content', 'none');
        endif;
    }
    ?>
</main>

<?php get_footer(); ?>
"""
    
    with open(os.path.join(THEME_DIR, 'index.php'), 'w', encoding='utf-8') as f:
        f.write(index_php)
    
    # Crear archivos de página individuales
    page_templates = [
        'front-page.php',
        'page-courses.php',
        'page-sessions.php',
        'page-group-sessions.php',
        'page-memberships.php',
        'page-about.php',
        'page-contact.php',
        'page-natal-chart.php',
        'page-human-design.php'
    ]
    
    for template in page_templates:
        template_php = f"""<?php
/**
 * Template Name: {template.replace('.php', '').replace('page-', '').title()} Page
 */

get_header();
?>

<main id="main" class="site-main">
    <?php
    while (have_posts()) : the_post();
        get_template_part('template-parts/content', '{template.replace('.php', '').replace('page-', '')}');
    endwhile;
    ?>
</main>

<?php get_footer(); ?>
"""
        
        with open(os.path.join(THEME_DIR, template), 'w', encoding='utf-8') as f:
            f.write(template_php)
    
    # Crear archivos necesarios en inc
    os.makedirs(os.path.join(THEME_DIR, 'inc'), exist_ok=True)
    
    # Template Tags
    template_tags_php = """<?php
/**
 * Custom template tags for this theme
 */

if (!function_exists('metatonehen_posted_on')) :
    function metatonehen_posted_on() {
        $time_string = '<time class="entry-date published updated" datetime="%1$s">%2$s</time>';
        if (get_the_time('U') !== get_the_modified_time('U')) {
            $time_string = '<time class="entry-date published" datetime="%1$s">%2$s</time><time class="updated" datetime="%3$s">%4$s</time>';
        }

        $time_string = sprintf($time_string,
            esc_attr(get_the_date('c')),
            esc_html(get_the_date()),
            esc_attr(get_the_modified_date('c')),
            esc_html(get_the_modified_date())
        );

        echo '<span class="posted-on">' . $time_string . '</span>';
    }
endif;

if (!function_exists('metatonehen_entry_footer')) :
    function metatonehen_entry_footer() {
        // Hide category and tag text for pages.
        if ('post' === get_post_type()) {
            /* translators: used between list items, there is a space after the comma */
            $categories_list = get_the_category_list(esc_html__(', ', 'metatonehen'));
            if ($categories_list) {
                printf('<span class="cat-links">' . esc_html__('Posted in %1$s', 'metatonehen') . '</span>', $categories_list);
            }

            /* translators: used between list items, there is a space after the comma */
            $tags_list = get_the_tag_list('', esc_html__(', ', 'metatonehen'));
            if ($tags_list) {
                printf('<span class="tags-links">' . esc_html__('Tagged %1$s', 'metatonehen') . '</span>', $tags_list);
            }
        }

        if (!is_single() && !post_password_required() && (comments_open() || get_comments_number())) {
            echo '<span class="comments-link">';
            comments_popup_link(esc_html__('Leave a comment', 'metatonehen'), esc_html__('1 Comment', 'metatonehen'), esc_html__('% Comments', 'metatonehen'));
            echo '</span>';
        }

        edit_post_link(
            sprintf(
                /* translators: %s: Name of current post */
                esc_html__('Edit %s', 'metatonehen'),
                the_title('<span class="screen-reader-text">"', '"</span>', false)
            ),
            '<span class="edit-link">',
            '</span>'
        );
    }
endif;
"""
    
    with open(os.path.join(THEME_DIR, 'inc', 'template-tags.php'), 'w', encoding='utf-8') as f:
        f.write(template_tags_php)
    
    # Extras
    extras_php = """<?php
/**
 * Custom functions that act independently of the theme templates
 */

/**
 * Adds custom classes to the array of body classes.
 *
 * @param array $classes Classes for the body element.
 * @return array
 */
function metatonehen_body_classes($classes) {
    // Adds a class of group-blog to blogs with more than 1 published author.
    if (is_multi_author()) {
        $classes[] = 'group-blog';
    }

    // Adds a class of hfeed to non-singular pages.
    if (!is_singular()) {
        $classes[] = 'hfeed';
    }

    return $classes;
}
add_filter('body_class', 'metatonehen_body_classes');

/**
 * Bootstrap 5 wp_nav_menu walker
 */
class bootstrap_5_wp_nav_menu_walker extends Walker_Nav_menu {
    private $current_item;
    private $dropdown_menu_alignment_values = [
        'dropdown-menu-start',
        'dropdown-menu-end',
        'dropdown-menu-sm-start',
        'dropdown-menu-sm-end',
        'dropdown-menu-md-start',
        'dropdown-menu-md-end',
        'dropdown-menu-lg-start',
        'dropdown-menu-lg-end',
        'dropdown-menu-xl-start',
        'dropdown-menu-xl-end',
        'dropdown-menu-xxl-start',
        'dropdown-menu-xxl-end'
    ];

    function start_lvl(&$output, $depth = 0, $args = null) {
        $dropdown_menu_class[] = '';
        foreach($this->current_item->classes as $class) {
            if(in_array($class, $this->dropdown_menu_alignment_values)) {
                $dropdown_menu_class[] = $class;
            }
        }
        $indent = str_repeat("\t", $depth);
        $submenu = ($depth > 0) ? ' sub-menu' : '';
        $output .= "\n$indent<ul class=\"dropdown-menu$submenu " . esc_attr(implode(" ",$dropdown_menu_class)) . " depth_$depth\">\n";
    }

    function start_el(&$output, $item, $depth = 0, $args = null, $id = 0) {
        $this->current_item = $item;

        $indent = ($depth) ? str_repeat("\t", $depth) : '';

        $li_attributes = '';
        $class_names = $value = '';

        $classes = empty($item->classes) ? array() : (array) $item->classes;

        $classes[] = ($args->walker->has_children) ? 'dropdown' : '';
        $classes[] = 'nav-item';
        $classes[] = 'nav-item-' . $item->ID;
        if ($depth && $args->walker->has_children) {
            $classes[] = 'dropdown-menu dropdown-menu-end';
        }

        $class_names =  join(' ', apply_filters('nav_menu_css_class', array_filter($classes), $item, $args));
        $class_names = ' class="' . esc_attr($class_names) . '"';

        $id = apply_filters('nav_menu_item_id', 'menu-item-' . $item->ID, $item, $args);
        $id = strlen($id) ? ' id="' . esc_attr($id) . '"' : '';

        $output .= $indent . '<li ' . $id . $value . $class_names . $li_attributes . '>';

        $attributes = !empty($item->attr_title) ? ' title="' . esc_attr($item->attr_title) . '"' : '';
        $attributes .= !empty($item->target) ? ' target="' . esc_attr($item->target) . '"' : '';
        $attributes .= !empty($item->xfn) ? ' rel="' . esc_attr($item->xfn) . '"' : '';
        $attributes .= !empty($item->url) ? ' href="' . esc_attr($item->url) . '"' : '';

        $active_class = ($item->current || $item->current_item_ancestor || in_array("current_page_parent", $item->classes, true) || in_array("current-post-ancestor", $item->classes, true)) ? 'active' : '';
        $nav_link_class = ( $depth > 0 ) ? 'dropdown-item ' : 'nav-link ';
        $attributes .= ( $args->walker->has_children ) ? ' class="'. $nav_link_class . $active_class . ' dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false"' : ' class="'. $nav_link_class . $active_class . '"';

        $item_output = $args->before;
        $item_output .= '<a' . $attributes . '>';
        $item_output .= $args->link_before . apply_filters('the_title', $item->title, $item->ID) . $args->link_after;
        $item_output .= '</a>';
        $item_output .= $args->after;

        $output .= apply_filters('walker_nav_menu_start_el', $item_output, $item, $depth, $args);
    }
}
"""
    
    with open(os.path.join(THEME_DIR, 'inc', 'extras.php'), 'w', encoding='utf-8') as f:
        f.write(extras_php)
    
    # Customizer
    customizer_php = """<?php
/**
 * METATONEHEN Theme Customizer
 */

/**
 * Add postMessage support for site title and description for the Theme Customizer.
 *
 * @param WP_Customize_Manager $wp_customize Theme Customizer object.
 */
function metatonehen_customize_register($wp_customize) {
    $wp_customize->get_setting('blogname')->transport = 'postMessage';
    $wp_customize->get_setting('blogdescription')->transport = 'postMessage';
    $wp_customize->get_setting('header_textcolor')->transport = 'postMessage';
    
    // Sección para opciones de METATONEHEN
    $wp_customize->add_section('metatonehen_options', array(
        'title'    => __('METATONEHEN Options', 'metatonehen'),
        'priority' => 130,
    ));
    
    // Opción para el texto griego bajo el título
    $wp_customize->add_setting('greek_text', array(
        'default'           => 'μετὰ τὸ νέἕν',
        'sanitize_callback' => 'sanitize_text_field',
    ));
    
    $wp_customize->add_control('greek_text', array(
        'label'    => __('Greek Text', 'metatonehen'),
        'section'  => 'metatonehen_options',
        'type'     => 'text',
    ));
    
    // Opción para los colores del tema
    $wp_customize->add_setting('primary_color', array(
        'default'           => '#785eff',
        'sanitize_callback' => 'sanitize_hex_color',
    ));
    
    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'primary_color', array(
        'label'    => __('Primary Color', 'metatonehen'),
        'section'  => 'metatonehen_options',
        'settings' => 'primary_color',
    )));
    
    $wp_customize->add_setting('secondary_color', array(
        'default'           => '#ffd700',
        'sanitize_callback' => 'sanitize_hex_color',
    ));
    
    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'secondary_color', array(
        'label'    => __('Secondary Color', 'metatonehen'),
        'section'  => 'metatonehen_options',
        'settings' => 'secondary_color',
    )));
}
add_action('customize_register', 'metatonehen_customize_register');

/**
 * Binds JS handlers to make Theme Customizer preview reload changes asynchronously.
 */
function metatonehen_customize_preview_js() {
    wp_enqueue_script('metatonehen_customizer', get_template_directory_uri() . '/js/customizer.js', array('customize-preview'), '20151215', true);
}
add_action('customize_preview_init', 'metatonehen_customize_preview_js');

/**
 * Output customizer CSS to wp_head
 */
function metatonehen_customizer_css() {
    ?>
    <style type="text/css">
        :root {
            --primary-color: <?php echo get_theme_mod('primary_color', '#785eff'); ?>;
            --secondary-color: <?php echo get_theme_mod('secondary_color', '#ffd700'); ?>;
        }
    </style>
    <?php
}
add_action('wp_head', 'metatonehen_customizer_css');
"""
    
    with open(os.path.join(THEME_DIR, 'inc', 'customizer.php'), 'w', encoding='utf-8') as f:
        f.write(customizer_php)

    # Crear carpeta para partes de plantilla
    os.makedirs(os.path.join(THEME_DIR, 'template-parts'), exist_ok=True)
    
    # content-home.php - Plantilla para la página de inicio
    content_home_php = """<?php
/**
 * Template part for displaying home page content
 */
?>

<section class="hero-section">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <div class="hero-content">
                    <h1><?php echo get_theme_mod('hero_title', 'METATONEHEN'); ?></h1>
                    <p class="greek-text"><?php echo get_theme_mod('greek_text', 'μετὰ τὸ νέἕν'); ?></p>
                    <p class="lead">
                        <?php 
                        $current_language = function_exists('pll_current_language') ? pll_current_language() : 'en';
                        
                        switch ($current_language) {
                            case 'es':
                                echo get_theme_mod('hero_text_es', 'Bienvenido a mi sitio de conocimiento espiritual y geometría sagrada');
                                break;
                            case 'it':
                                echo get_theme_mod('hero_text_it', 'Benvenuto nel mio sito di conoscenza spirituale e geometria sacra');
                                break;
                            case 'pt':
                                echo get_theme_mod('hero_text_pt', 'Bem-vindo ao meu site de conhecimento espiritual e geometria sagrada');
                                break;
                            case 'de':
                                echo get_theme_mod('hero_text_de', 'Willkommen auf meiner Website für spirituelles Wissen und heilige Geometrie');
                                break;
                            default:
                                echo get_theme_mod('hero_text', 'Bienvenido a mi sitio de conocimiento espiritual y geometría sagrada');
                        }
                        ?>
                    </p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="sacred-geometry-container">
                    <div class="flower-of-life">
                        <img src="<?php echo get_template_directory_uri(); ?>/images/flower_of_life_enhanced.svg" alt="Flower of Life">
                    </div>
                    <div class="metatron-cube">
                        <img src="<?php echo get_template_directory_uri(); ?>/images/metatron_cube_enhanced.svg" alt="Metatron's Cube">
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="cubes-section">
    <div class="container">
        <div class="section-title">
            <h2>
                <?php 
                $current_language = function_exists('pll_current_language') ? pll_current_language() : 'en';
                
                switch ($current_language) {
                    case 'es':
                        echo 'Explora Nuestros Portales';
                        break;
                    case 'it':
                        echo 'Esplora I Nostri Portali';
                        break;
                    case 'pt':
                        echo 'Explore Nossos Portais';
                        break;
                    case 'de':
                        echo 'Erkunde Unsere Portale';
                        break;
                    default:
                        echo 'Explore Our Portals';
                }
                ?>
            </h2>
            <p>
                <?php 
                switch ($current_language) {
                    case 'es':
                        echo 'Entra en los portales del conocimiento y la transformación';
                        break;
                    case 'it':
                        echo 'Entra nei portali della conoscenza e della trasformazione';
                        break;
                    case 'pt':
                        echo 'Entre nos portais do conhecimento e da transformação';
                        break;
                    case 'de':
                        echo 'Betrete die Portale des Wissens und der Transformation';
                        break;
                    default:
                        echo 'Enter the portals of knowledge and transformation';
                }
                ?>
            </p>
        </div>
        
        <!-- Portal containers for Courses, Sessions and Group Sessions -->
        <div class="row">
            <div class="col-md-4">
                <div class="metatron-portal-container">
                    <h3 class="portal-title">Courses</h3>
                    <div class="metatron-portal">
                        <img src="<?php echo get_template_directory_uri(); ?>/images/metatron_cube_enhanced.svg" alt="Metatron's Cube" class="portal-background">
                        <div class="portal-vertices">
                            <a href="<?php echo site_url('/courses'); ?>#love-courses" class="portal-vertex vertex-1 vertex-love">
                                <span>Love</span>
                            </a>
                            <a href="<?php echo site_url('/courses'); ?>#money-courses" class="portal-vertex vertex-2 vertex-money">
                                <span>Money</span>
                            </a>
                            <a href="<?php echo site_url('/courses'); ?>#health-courses" class="portal-vertex vertex-3 vertex-health">
                                <span>Health</span>
                            </a>
                            <a href="<?php echo site_url('/courses'); ?>#mind-courses" class="portal-vertex vertex-4 vertex-mind">
                                <span>Mind</span>
                            </a>
                            <a href="<?php echo site_url('/courses'); ?>#soul-courses" class="portal-vertex vertex-5 vertex-soul">
                                <span>Soul</span>
                            </a>
                            <a href="<?php echo site_url('/courses'); ?>#body-courses" class="portal-vertex vertex-6 vertex-body">
                                <span>Body</span>
                            </a>
                        </div>
                    </div>
                    <a href="<?php echo site_url('/courses'); ?>" class="portal-link">Enter Portal</a>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="metatron-portal-container">
                    <h3 class="portal-title">1-on-1 Sessions</h3>
                    <div class="metatron-portal">
                        <img src="<?php echo get_template_directory_uri(); ?>/images/metatron_cube_enhanced.svg" alt="Metatron's Cube" class="portal-background">
                        <div class="portal-vertices">
                            <a href="<?php echo site_url('/sessions'); ?>#coaching" class="portal-vertex vertex-1">
                                <span>Coaching</span>
                            </a>
                            <a href="<?php echo site_url('/sessions'); ?>#astrology" class="portal-vertex vertex-2">
                                <span>Astrology</span>
                            </a>
                            <a href="<?php echo site_url('/sessions'); ?>#human-design" class="portal-vertex vertex-3">
                                <span>Human Design</span>
                            </a>
                            <a href="<?php echo site_url('/sessions'); ?>#constellations" class="portal-vertex vertex-4">
                                <span>Constellations</span>
                            </a>
                            <a href="<?php echo site_url('/sessions'); ?>#healing" class="portal-vertex vertex-5">
                                <span>Healing</span>
                            </a>
                            <a href="<?php echo site_url('/sessions'); ?>#meditation" class="portal-vertex vertex-6">
                                <span>Meditation</span>
                            </a>
                        </div>
                    </div>
                    <a href="<?php echo site_url('/sessions'); ?>" class="portal-link">Enter Portal</a>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="metatron-portal-container">
                    <h3 class="portal-title">Group Sessions</h3>
                    <div class="metatron-portal">
                        <img src="<?php echo get_template_directory_uri(); ?>/images/metatron_cube_enhanced.svg" alt="Metatron's Cube" class="portal-background">
                        <div class="portal-vertices">
                            <a href="<?php echo site_url('/group-sessions'); ?>#meditations" class="portal-vertex vertex-1">
                                <span>Meditations</span>
                            </a>
                            <a href="<?php echo site_url('/group-sessions'); ?>#retreats" class="portal-vertex vertex-2">
                                <span>Retreats</span>
                            </a>
                            <a href="<?php echo site_url('/group-sessions'); ?>#workshops" class="portal-vertex vertex-3">
                                <span>Workshops</span>
                            </a>
                            <a href="<?php echo site_url('/group-sessions'); ?>#ceremonies" class="portal-vertex vertex-4">
                                <span>Ceremonies</span>
                            </a>
                            <a href="<?php echo site_url('/group-sessions'); ?>#healing-circles" class="portal-vertex vertex-5">
                                <span>Healing Circles</span>
                            </a>
                            <a href="<?php echo site_url('/group-sessions'); ?>#online-events" class="portal-vertex vertex-6">
                                <span>Online Events</span>
                            </a>
                        </div>
                    </div>
                    <a href="<?php echo site_url('/group-sessions'); ?>" class="portal-link">Enter Portal</a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Featured Courses Section -->
<section class="featured-courses-section">
    <!-- Contenido de cursos destacados -->
</section>

<!-- Calculators Section -->
<section class="calculators-section">
    <!-- Contenido de calculadoras -->
</section>

<!-- Membership Section -->
<section class="membership-section">
    <!-- Contenido de membresías -->
</section>
"""
    
    with open(os.path.join(THEME_DIR, 'template-parts', 'content-home.php'), 'w', encoding='utf-8') as f:
        f.write(content_home_php)
    
    # Content Page (general)
    content_page_php = """<?php
/**
 * Template part for displaying page content in page.php
 */
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
    <header class="entry-header">
        <?php the_title('<h1 class="entry-title">', '</h1>'); ?>
    </header><!-- .entry-header -->

    <div class="entry-content">
        <?php
        the_content();

        wp_link_pages(array(
            'before' => '<div class="page-links">' . esc_html__('Pages:', 'metatonehen'),
            'after'  => '</div>',
        ));
        ?>
    </div><!-- .entry-content -->

    <?php if (get_edit_post_link()) : ?>
        <footer class="entry-footer">
            <?php
            edit_post_link(
                sprintf(
                    /* translators: %s: Name of current post */
                    esc_html__('Edit %s', 'metatonehen'),
                    the_title('<span class="screen-reader-text">"', '"</span>', false)
                ),
                '<span class="edit-link">',
                '</span>'
            );
            ?>
        </footer><!-- .entry-footer -->
    <?php endif; ?>
</article><!-- #post-## -->
"""
    
    with open(os.path.join(THEME_DIR, 'template-parts', 'content-page.php'), 'w', encoding='utf-8') as f:
        f.write(content_page_php)
    
    # README
    readme_md = """# METATONEHEN WordPress Theme

A custom WordPress theme for METATONEHEN spiritual education platform.

## Installation

1. Upload the `metatonehen` folder to the `/wp-content/themes/` directory
2. Activate the theme through the 'Themes' menu in WordPress
3. Configure the theme settings from the WordPress Customizer

## Features

- Responsive design
- Multi-language support
- Sacred geometry elements
- Portal-based navigation
- Custom page templates for courses, sessions, memberships, etc.

## Required Plugins

For full functionality, the following plugins are recommended:

- Polylang (for multilingual support)
- Advanced Custom Fields (for custom field management)
- Contact Form 7 (for contact forms)
- WooCommerce (for course and session purchases)

## Customization

Most theme settings can be customized through the WordPress Customizer:

1. Go to Appearance > Customize
2. Modify the METATONEHEN Options section
3. Preview and save your changes

## Credits

- Developed by METATONEHEN team
- Uses Bootstrap 5 framework
- Includes Font Awesome icons
"""
    
    with open(os.path.join(THEME_DIR, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme_md)
    
    # Zip del tema
    print("Creando archivo ZIP del tema...")
    shutil.make_archive(os.path.join(EXPORT_DIR, THEME_NAME), 'zip', THEME_DIR)

# Exportar XML para WordPress
def create_wordpress_xml():
    print("Creando archivo XML para WordPress...")
    
    # Estructura básica del XML
    root = ET.Element("rss")
    root.set("version", "2.0")
    root.set("xmlns:excerpt", "http://wordpress.org/export/1.2/excerpt/")
    root.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
    root.set("xmlns:wfw", "http://wellformedweb.org/CommentAPI/")
    root.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")
    root.set("xmlns:wp", "http://wordpress.org/export/1.2/")
    
    channel = ET.SubElement(root, "channel")
    
    # Metadatos
    title = ET.SubElement(channel, "title")
    title.text = "METATONEHEN"
    
    link = ET.SubElement(channel, "link")
    link.text = "https://metatonehen.com"
    
    description = ET.SubElement(channel, "description")
    description.text = "Plataforma de educación espiritual"
    
    pubDate = ET.SubElement(channel, "pubDate")
    pubDate.text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    language = ET.SubElement(channel, "language")
    language.text = "en-US"
    
    wxr_version = ET.SubElement(channel, "wp:wxr_version")
    wxr_version.text = "1.2"
    
    base_site_url = ET.SubElement(channel, "wp:base_site_url")
    base_site_url.text = "https://metatonehen.com"
    
    base_blog_url = ET.SubElement(channel, "wp:base_blog_url")
    base_blog_url.text = "https://metatonehen.com"
    
    # Crear las páginas para el sitio
    pages = [
        {"title": "Home", "slug": "home", "template": "front-page"},
        {"title": "Courses", "slug": "courses", "template": "page-courses"},
        {"title": "1-on-1 Sessions", "slug": "sessions", "template": "page-sessions"},
        {"title": "Group Sessions", "slug": "group-sessions", "template": "page-group-sessions"},
        {"title": "Memberships", "slug": "memberships", "template": "page-memberships"},
        {"title": "Natal Chart", "slug": "natal-chart", "template": "page-natal-chart"},
        {"title": "Human Design", "slug": "human-design", "template": "page-human-design"},
        {"title": "Blog", "slug": "blog", "template": ""},
        {"title": "About", "slug": "about", "template": "page-about"},
        {"title": "Contact", "slug": "contact", "template": "page-contact"}
    ]
    
    # Añadir páginas al XML
    for i, page in enumerate(pages):
        item = ET.SubElement(channel, "item")
        
        title = ET.SubElement(item, "title")
        title.text = page["title"]
        
        link = ET.SubElement(item, "link")
        link.text = f"https://metatonehen.com/{page['slug']}/"
        
        pubDate = ET.SubElement(item, "pubDate")
        pubDate.text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
        
        dc_creator = ET.SubElement(item, "dc:creator")
        dc_creator.text = "admin"
        
        guid = ET.SubElement(item, "guid")
        guid.set("isPermaLink", "false")
        guid.text = f"https://metatonehen.com/?page_id={i+1}"
        
        description = ET.SubElement(item, "description")
        
        content = ET.SubElement(item, "content:encoded")
        content.text = f"<![CDATA[<!-- wp:paragraph --><p>Content for {page['title']} page.</p><!-- /wp:paragraph -->]]>"
        
        excerpt = ET.SubElement(item, "excerpt:encoded")
        excerpt.text = "<![CDATA[]]>"
        
        wp_post_id = ET.SubElement(item, "wp:post_id")
        wp_post_id.text = str(i+1)
        
        wp_post_date = ET.SubElement(item, "wp:post_date")
        wp_post_date.text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        wp_post_date_gmt = ET.SubElement(item, "wp:post_date_gmt")
        wp_post_date_gmt.text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        wp_comment_status = ET.SubElement(item, "wp:comment_status")
        wp_comment_status.text = "closed"
        
        wp_ping_status = ET.SubElement(item, "wp:ping_status")
        wp_ping_status.text = "closed"
        
        wp_post_name = ET.SubElement(item, "wp:post_name")
        wp_post_name.text = page["slug"]
        
        wp_status = ET.SubElement(item, "wp:status")
        wp_status.text = "publish"
        
        wp_post_parent = ET.SubElement(item, "wp:post_parent")
        wp_post_parent.text = "0"
        
        wp_menu_order = ET.SubElement(item, "wp:menu_order")
        wp_menu_order.text = str(i)
        
        wp_post_type = ET.SubElement(item, "wp:post_type")
        wp_post_type.text = "page"
        
        wp_post_password = ET.SubElement(item, "wp:post_password")
        wp_post_password.text = ""
        
        if page["template"]:
            wp_postmeta = ET.SubElement(item, "wp:postmeta")
            wp_meta_key = ET.SubElement(wp_postmeta, "wp:meta_key")
            wp_meta_key.text = "_wp_page_template"
            wp_meta_value = ET.SubElement(wp_postmeta, "wp:meta_value")
            wp_meta_value.text = f"{page['template']}.php"
    
    # Guardar el XML
    tree = ET.ElementTree(root)
    tree.write(os.path.join(EXPORT_DIR, "metatonehen-export.xml"), encoding="utf-8", xml_declaration=True)

# Función principal
def export_wordpress():
    print("Exportando METATONEHEN para WordPress...")
    
    # Crear estructura del tema
    print("\n1. Creando estructura del tema WordPress...")
    create_theme_structure()
    
    # Copiar archivos estáticos
    print("\n2. Copiando archivos estáticos...")
    copy_static_files()
    
    # Adaptar CSS para WordPress
    print("\n3. Adaptando CSS para WordPress...")
    adapt_css_for_wordpress()
    
    # Crear archivos del tema
    print("\n4. Creando archivos del tema...")
    create_theme_files()
    
    # Crear XML para importar
    print("\n5. Creando archivo XML para importar...")
    create_wordpress_xml()
    
    print("\n¡Exportación para WordPress completada!")
    print(f"Tema WordPress: {EXPORT_DIR}/{THEME_NAME}.zip")
    print(f"Archivo XML: {EXPORT_DIR}/metatonehen-export.xml")
    print("\nPara instalar en WordPress:")
    print("1. Ve a Apariencia > Temas > Añadir nuevo > Subir tema")
    print(f"2. Selecciona el archivo {THEME_NAME}.zip")
    print("3. Activa el tema")
    print("4. Ve a Herramientas > Importar > WordPress")
    print("5. Selecciona el archivo metatonehen-export.xml")
    print("6. Importa los medios y asigna el autor")

if __name__ == "__main__":
    export_wordpress()