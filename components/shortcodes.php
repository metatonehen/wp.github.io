<?php
/**
 * NEO GAIAM Shortcodes
 * 
 * This file defines shortcodes for all NEO GAIAM components.
 */

// Metatron Cube Shortcode
function neogaiam_metatron_cube_shortcode($atts) {
    $atts = shortcode_atts(
        array(
            'size' => '500',
            'rotation_speed' => '0.005',
            'line_color' => '#6366f1',
            'line_opacity' => '0.6',
            'outer_circle' => 'true',
            'wooden_style' => 'true',
            'pulse_effect' => 'true',
        ),
        $atts
    );
    
    $id = 'metatron-cube-' . rand(1000, 9999);
    
    ob_start();
    ?>
    <div class="neogaiam-metatron-cube" 
         id="<?php echo esc_attr($id); ?>"
         data-size="<?php echo esc_attr($atts['size']); ?>"
         data-rotation-speed="<?php echo esc_attr($atts['rotation_speed']); ?>"
         data-line-color="<?php echo esc_attr($atts['line_color']); ?>"
         data-line-opacity="<?php echo esc_attr($atts['line_opacity']); ?>"
         data-outer-circle="<?php echo esc_attr($atts['outer_circle']); ?>"
         data-wooden-style="<?php echo esc_attr($atts['wooden_style']); ?>"
         data-pulse-effect="<?php echo esc_attr($atts['pulse_effect']); ?>">
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('neogaiam_metatron_cube', 'neogaiam_metatron_cube_shortcode');

// Flower of Life Shortcode
function neogaiam_flower_of_life_shortcode($atts) {
    $atts = shortcode_atts(
        array(
            'size' => '300',
            'opacity' => '0.7',
            'animation_duration' => '60',
            'primary_color' => '#6366f1',
            'secondary_color' => '#8b5cf6',
        ),
        $atts
    );
    
    $id = 'flower-of-life-' . rand(1000, 9999);
    
    ob_start();
    ?>
    <div class="neogaiam-flower-of-life" 
         id="<?php echo esc_attr($id); ?>"
         data-size="<?php echo esc_attr($atts['size']); ?>"
         data-opacity="<?php echo esc_attr($atts['opacity']); ?>"
         data-animation-duration="<?php echo esc_attr($atts['animation_duration']); ?>"
         data-primary-color="<?php echo esc_attr($atts['primary_color']); ?>"
         data-secondary-color="<?php echo esc_attr($atts['secondary_color']); ?>">
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('neogaiam_flower_of_life', 'neogaiam_flower_of_life_shortcode');

// Star Field Shortcode
function neogaiam_star_field_shortcode($atts) {
    $atts = shortcode_atts(
        array(
            'count' => '200',
            'color' => '#ffffff',
            'size' => '2',
            'speed' => '0.5',
            'container_height' => '500',
        ),
        $atts
    );
    
    $id = 'star-field-' . rand(1000, 9999);
    
    ob_start();
    ?>
    <div class="neogaiam-star-field" 
         id="<?php echo esc_attr($id); ?>"
         style="height: <?php echo esc_attr($atts['container_height']); ?>px;"
         data-count="<?php echo esc_attr($atts['count']); ?>"
         data-color="<?php echo esc_attr($atts['color']); ?>"
         data-size="<?php echo esc_attr($atts['size']); ?>"
         data-speed="<?php echo esc_attr($atts['speed']); ?>">
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('neogaiam_star_field', 'neogaiam_star_field_shortcode');

// Booking Form Shortcode
function neogaiam_booking_form_shortcode($atts) {
    $atts = shortcode_atts(
        array(
            'service_id' => '1',
            'service_name' => 'Astrología',
            'has_levels' => 'true',
            'astrology_fields' => 'true',
            'form_title' => 'Reserva Tu Sesión',
            'submit_text' => 'Confirmar Reserva',
        ),
        $atts
    );
    
    $id = 'booking-form-' . rand(1000, 9999);
    
    // Generate nonce for security
    $nonce = wp_create_nonce('neogaiam_booking_nonce');
    
    ob_start();
    ?>
    <div class="neogaiam-booking-form" 
         id="<?php echo esc_attr($id); ?>"
         data-service-id="<?php echo esc_attr($atts['service_id']); ?>"
         data-service-name="<?php echo esc_attr($atts['service_name']); ?>"
         data-has-levels="<?php echo esc_attr($atts['has_levels']); ?>"
         data-astrology-fields="<?php echo esc_attr($atts['astrology_fields']); ?>"
         data-form-title="<?php echo esc_attr($atts['form_title']); ?>"
         data-submit-text="<?php echo esc_attr($atts['submit_text']); ?>"
         data-nonce="<?php echo esc_attr($nonce); ?>">
         <div class="loading-spinner"><?php echo esc_html__('Loading booking form...', 'neogaiam'); ?></div>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('neogaiam_booking_form', 'neogaiam_booking_form_shortcode');

// Language Switcher Shortcode
function neogaiam_language_switcher_shortcode($atts) {
    $atts = shortcode_atts(
        array(
            'languages' => 'en,es',
            'show_flags' => 'true',
        ),
        $atts
    );
    
    $id = 'language-switcher-' . rand(1000, 9999);
    $languages = explode(',', $atts['languages']);
    $current_lang = determined_language();
    
    ob_start();
    ?>
    <div class="neogaiam-language-switcher" 
         id="<?php echo esc_attr($id); ?>"
         data-show-flags="<?php echo esc_attr($atts['show_flags']); ?>">
         <div class="language-options">
            <?php foreach ($languages as $lang): ?>
                <button class="language-option <?php echo ($lang === $current_lang) ? 'active' : ''; ?>" 
                        data-lang="<?php echo esc_attr($lang); ?>">
                    <?php if ($atts['show_flags'] === 'true'): ?>
                        <img src="<?php echo esc_url(get_template_directory_uri() . '/assets/flags/' . $lang . '.svg'); ?>" 
                             alt="<?php echo esc_attr(strtoupper($lang)); ?>"
                             class="language-flag">
                    <?php endif; ?>
                    <span class="language-name"><?php echo esc_html(strtoupper($lang)); ?></span>
                </button>
            <?php endforeach; ?>
         </div>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('neogaiam_language_switcher', 'neogaiam_language_switcher_shortcode');
