<?php
/**
 * Plugin Name: NEO GAIAM Components
 * Description: Sacred geometry visualizations and cosmic components for WordPress
 * Version: 1.0
 * Author: NEO GAIAM
 * Text Domain: neogaiam
 */

// Exit if accessed directly
if (!defined('ABSPATH')) {
    exit;
}

// Define constants
define('NEOGAIAM_PATH', plugin_dir_path(__FILE__));
define('NEOGAIAM_URL', plugin_dir_url(__FILE__));

// Include files
require_once NEOGAIAM_PATH . 'includes/functions.php';
require_once NEOGAIAM_PATH . 'includes/shortcodes.php';

// Plugin activation hook
register_activation_hook(__FILE__, 'neogaiam_plugin_activation');

function neogaiam_plugin_activation() {
    // Create custom post types
    neogaiam_register_booking_post_type();
    
    // Flush rewrite rules
    flush_rewrite_rules();
}

// Enqueue scripts and styles
function neogaiam_enqueue_scripts() {
    // Styles
    wp_enqueue_style('neogaiam-main', NEOGAIAM_URL . 'css/neogaiam.css', array(), '1.0.0');
    wp_enqueue_style('neogaiam-metatron', NEOGAIAM_URL . 'css/metatron-cube.css', array('neogaiam-main'), '1.0.0');
    wp_enqueue_style('neogaiam-flower', NEOGAIAM_URL . 'css/flower-of-life.css', array('neogaiam-main'), '1.0.0');
    wp_enqueue_style('neogaiam-stars', NEOGAIAM_URL . 'css/star-field.css', array('neogaiam-main'), '1.0.0');
    wp_enqueue_style('neogaiam-booking', NEOGAIAM_URL . 'css/booking-form.css', array('neogaiam-main'), '1.0.0');
    wp_enqueue_style('neogaiam-language', NEOGAIAM_URL . 'css/language-switcher.css', array('neogaiam-main'), '1.0.0');
    
    // Scripts
    wp_enqueue_script('neogaiam-metatron', NEOGAIAM_URL . 'js/metatron-cube.js', array('jquery'), '1.0.0', true);
    wp_enqueue_script('neogaiam-flower', NEOGAIAM_URL . 'js/flower-of-life.js', array('jquery'), '1.0.0', true);
    wp_enqueue_script('neogaiam-stars', NEOGAIAM_URL . 'js/star-field.js', array('jquery'), '1.0.0', true);
    wp_enqueue_script('neogaiam-booking', NEOGAIAM_URL . 'js/booking-form.js', array('jquery'), '1.0.0', true);
    wp_enqueue_script('neogaiam-language', NEOGAIAM_URL . 'js/language-switcher.js', array('jquery'), '1.0.0', true);
    
    // Pass data to scripts
    $current_lang = determined_language();
    wp_localize_script('neogaiam-booking', 'NEOGAIAMData', array(
        'ajaxurl' => admin_url('admin-ajax.php'),
        'language' => $current_lang,
        'strings' => get_translation_strings($current_lang),
        'nonce' => wp_create_nonce('neogaiam_ajax_nonce')
    ));
}
add_action('wp_enqueue_scripts', 'neogaiam_enqueue_scripts');

// Add settings menu
function neogaiam_add_admin_menu() {
    add_menu_page(
        'NEO GAIAM Settings',
        'NEO GAIAM',
        'manage_options',
        'neogaiam-settings',
        'neogaiam_settings_page',
        'dashicons-admin-customizer',
        30
    );
}
add_action('admin_menu', 'neogaiam_add_admin_menu');

// Render settings page
function neogaiam_settings_page() {
    ?>
    <div class="wrap">
        <h1><?php echo esc_html__('NEO GAIAM Components Settings', 'neogaiam'); ?></h1>
        
        <div class="card">
            <h2><?php echo esc_html__('Available Shortcodes', 'neogaiam'); ?></h2>
            
            <table class="widefat">
                <thead>
                    <tr>
                        <th><?php echo esc_html__('Component', 'neogaiam'); ?></th>
                        <th><?php echo esc_html__('Shortcode', 'neogaiam'); ?></th>
                        <th><?php echo esc_html__('Description', 'neogaiam'); ?></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><?php echo esc_html__('Metatron Cube', 'neogaiam'); ?></td>
                        <td><code>[neogaiam_metatron_cube]</code></td>
                        <td><?php echo esc_html__('Displays an interactive Metatron\'s Cube with navigation vertices.', 'neogaiam'); ?></td>
                    </tr>
                    <tr>
                        <td><?php echo esc_html__('Flower of Life', 'neogaiam'); ?></td>
                        <td><code>[neogaiam_flower_of_life]</code></td>
                        <td><?php echo esc_html__('Displays a sacred geometry Flower of Life pattern.', 'neogaiam'); ?></td>
                    </tr>
                    <tr>
                        <td><?php echo esc_html__('Star Field', 'neogaiam'); ?></td>
                        <td><code>[neogaiam_star_field]</code></td>
                        <td><?php echo esc_html__('Creates a cosmic background with animated stars.', 'neogaiam'); ?></td>
                    </tr>
                    <tr>
                        <td><?php echo esc_html__('Booking Form', 'neogaiam'); ?></td>
                        <td><code>[neogaiam_booking_form]</code></td>
                        <td><?php echo esc_html__('Displays a service booking form with astrological information fields.', 'neogaiam'); ?></td>
                    </tr>
                    <tr>
                        <td><?php echo esc_html__('Language Switcher', 'neogaiam'); ?></td>
                        <td><code>[neogaiam_language_switcher]</code></td>
                        <td><?php echo esc_html__('Displays a language selection menu for multilingual sites.', 'neogaiam'); ?></td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="card" style="margin-top: 20px;">
            <h2><?php echo esc_html__('Documentation', 'neogaiam'); ?></h2>
            <p><?php echo esc_html__('For detailed documentation on using these components, please refer to the README.md file included with the plugin.', 'neogaiam'); ?></p>
        </div>
    </div>
    <?php
}
