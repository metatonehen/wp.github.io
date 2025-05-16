<?php
/**
 * NEO GAIAM Theme Functions
 * 
 * Include this code in your theme's functions.php file
 * or create a separate plugin.
 */

// Register and enqueue styles and scripts
function neogaiam_enqueue_scripts() {
    // Styles
    wp_enqueue_style('neogaiam-main', get_template_directory_uri() . '/css/neogaiam.css', array(), '1.0.0');
    wp_enqueue_style('neogaiam-metatron', get_template_directory_uri() . '/css/metatron-cube.css', array('neogaiam-main'), '1.0.0');
    wp_enqueue_style('neogaiam-flower', get_template_directory_uri() . '/css/flower-of-life.css', array('neogaiam-main'), '1.0.0');
    wp_enqueue_style('neogaiam-stars', get_template_directory_uri() . '/css/star-field.css', array('neogaiam-main'), '1.0.0');
    wp_enqueue_style('neogaiam-booking', get_template_directory_uri() . '/css/booking-form.css', array('neogaiam-main'), '1.0.0');
    wp_enqueue_style('neogaiam-language', get_template_directory_uri() . '/css/language-switcher.css', array('neogaiam-main'), '1.0.0');
    
    // Scripts
    wp_enqueue_script('neogaiam-metatron', get_template_directory_uri() . '/js/metatron-cube.js', array('jquery'), '1.0.0', true);
    wp_enqueue_script('neogaiam-flower', get_template_directory_uri() . '/js/flower-of-life.js', array('jquery'), '1.0.0', true);
    wp_enqueue_script('neogaiam-stars', get_template_directory_uri() . '/js/star-field.js', array('jquery'), '1.0.0', true);
    wp_enqueue_script('neogaiam-booking', get_template_directory_uri() . '/js/booking-form.js', array('jquery'), '1.0.0', true);
    wp_enqueue_script('neogaiam-language', get_template_directory_uri() . '/js/language-switcher.js', array('jquery'), '1.0.0', true);
    
    // Pass language data to scripts
    $current_lang = determined_language();
    wp_localize_script('neogaiam-booking', 'NEOGAIAMData', array(
        'ajaxurl' => admin_url('admin-ajax.php'),
        'language' => $current_lang,
        'strings' => get_translation_strings($current_lang)
    ));
}
add_action('wp_enqueue_scripts', 'neogaiam_enqueue_scripts');

// Determine current language (for multilingual sites)
function determined_language() {
    // With WPML
    if (defined('ICL_LANGUAGE_CODE')) {
        return ICL_LANGUAGE_CODE;
    }
    
    // With Polylang
    if (function_exists('pll_current_language')) {
        return pll_current_language();
    }
    
    // Default language from WordPress
    return substr(get_locale(), 0, 2);
}

// Get translation strings based on language
function get_translation_strings($lang) {
    $translations = array(
        'en' => array(
            'booking_success' => 'Booking submitted successfully',
            'booking_error' => 'There was an error submitting your booking',
            'required_field' => 'This field is required',
            'invalid_email' => 'Please enter a valid email address'
        ),
        'es' => array(
            'booking_success' => 'Reserva enviada con éxito',
            'booking_error' => 'Hubo un error al enviar tu reserva',
            'required_field' => 'Este campo es obligatorio',
            'invalid_email' => 'Por favor ingresa una dirección de correo electrónico válida'
        )
    );
    
    return isset($translations[$lang]) ? $translations[$lang] : $translations['en'];
}

// Include shortcodes file
require_once get_template_directory() . '/components/shortcodes.php';

// Ajax handler for booking form submission
function neogaiam_process_booking() {
    // Check nonce for security
    if (!isset($_POST['nonce']) || !wp_verify_nonce($_POST['nonce'], 'neogaiam_booking_nonce')) {
        wp_send_json_error(array('message' => 'Security check failed'));
    }
    
    // Process form data
    $full_name = sanitize_text_field($_POST['fullName']);
    $email = sanitize_email($_POST['email']);
    $phone = sanitize_text_field($_POST['phone']);
    $date = sanitize_text_field($_POST['date']);
    $time = sanitize_text_field($_POST['time']);
    $service_id = intval($_POST['serviceId']);
    $service_level = sanitize_text_field($_POST['serviceLevel']);
    
    // Additional fields for astrological services
    $birth_date = isset($_POST['birthDate']) ? sanitize_text_field($_POST['birthDate']) : '';
    $birth_time = isset($_POST['birthTime']) ? sanitize_text_field($_POST['birthTime']) : '';
    $birth_place = isset($_POST['birthPlace']) ? sanitize_text_field($_POST['birthPlace']) : '';
    $question = isset($_POST['questionForReading']) ? sanitize_textarea_field($_POST['questionForReading']) : '';
    
    // Validate required fields
    if (empty($full_name) || empty($email) || empty($phone) || empty($date) || empty($time)) {
        wp_send_json_error(array('message' => 'Please fill all required fields'));
    }
    
    // Here you would save the booking to your database
    // For example, using a custom post type for bookings
    
    $booking_id = wp_insert_post(array(
        'post_title' => 'Booking: ' . $full_name,
        'post_type' => 'neogaiam_booking',
        'post_status' => 'publish',
        'meta_input' => array(
            'neogaiam_customer_name' => $full_name,
            'neogaiam_customer_email' => $email,
            'neogaiam_customer_phone' => $phone,
            'neogaiam_booking_date' => $date,
            'neogaiam_booking_time' => $time,
            'neogaiam_service_id' => $service_id,
            'neogaiam_service_level' => $service_level,
            'neogaiam_birth_date' => $birth_date,
            'neogaiam_birth_time' => $birth_time,
            'neogaiam_birth_place' => $birth_place,
            'neogaiam_question' => $question
        )
    ));
    
    if ($booking_id) {
        // Send notification email
        $to = get_option('admin_email');
        $subject = 'New Booking: ' . $full_name;
        $message = "New booking received:\n\n" .
                   "Name: $full_name\n" .
                   "Email: $email\n" .
                   "Phone: $phone\n" .
                   "Date: $date\n" .
                   "Time: $time\n" .
                   "Service Level: $service_level\n";
        
        if (!empty($birth_date)) {
            $message .= "Birth Date: $birth_date\n";
        }
        
        if (!empty($birth_time)) {
            $message .= "Birth Time: $birth_time\n";
        }
        
        if (!empty($birth_place)) {
            $message .= "Birth Place: $birth_place\n";
        }
        
        if (!empty($question)) {
            $message .= "Questions: $question\n";
        }
        
        wp_mail($to, $subject, $message);
        
        // Send confirmation email to customer
        $customer_subject = 'Your Booking Confirmation';
        $customer_message = "Dear $full_name,\n\n" .
                           "Thank you for booking a session with us. Here are your booking details:\n\n" .
                           "Date: $date\n" .
                           "Time: $time\n" .
                           "Service Level: $service_level\n\n" .
                           "We will contact you shortly to confirm your appointment.\n\n" .
                           "Best regards,\n" .
                           get_bloginfo('name');
        
        wp_mail($email, $customer_subject, $customer_message);
        
        wp_send_json_success(array('message' => 'Booking received successfully'));
    } else {
        wp_send_json_error(array('message' => 'Error saving booking'));
    }
    
    wp_die();
}
add_action('wp_ajax_neogaiam_process_booking', 'neogaiam_process_booking');
add_action('wp_ajax_nopriv_neogaiam_process_booking', 'neogaiam_process_booking');

// Register custom post type for bookings
function neogaiam_register_booking_post_type() {
    register_post_type('neogaiam_booking', array(
        'labels' => array(
            'name' => 'Bookings',
            'singular_name' => 'Booking'
        ),
        'public' => false,
        'show_ui' => true,
        'show_in_menu' => true,
        'supports' => array('title'),
        'menu_icon' => 'dashicons-calendar-alt'
    ));
}
add_action('init', 'neogaiam_register_booking_post_type');
