import logging
import os
import uuid
import shutil
import datetime
import imghdr
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory, g
from app import app, db
from flask_login import login_user, logout_user, current_user, login_required
from models import (User, Course, CourseModule, Lesson, Service, Booking, 
                  BlogPost, Event, Testimonial, ContactMessage, 
                  NewsletterSubscriber, MembershipPlan, UserMembership, SiteContent,
                  MediaFile, PageTemplate)
from forms import UploadFileForm, EditContentForm
from datetime import datetime

@app.route('/')
def index():
    # Get featured courses, services and testimonials
    featured_courses = Course.query.filter_by(is_featured=True).limit(3).all()
    featured_services = Service.query.filter_by(is_featured=True).limit(3).all()
    testimonials = Testimonial.query.filter_by(is_featured=True).limit(3).all()
    
    # Get content from database or use defaults
    content = {}
    site_content = SiteContent.query.all()
    
    # Default values
    content_defaults = {
        'hero_title': 'METATONEHEN',
        'hero_subtitle': 'μετὰ τὸ νέἕν',
        'hero_text': 'Discover cosmic wisdom through sacred geometry and spiritual transformation',
    }
    
    # Fill in content from database or use defaults
    for item in site_content:
        content[item.key] = item.value
    
    # Add any missing defaults
    for key, value in content_defaults.items():
        if key not in content:
            content[key] = value
    
    return render_template('index.html', 
                          featured_courses=featured_courses,
                          featured_services=featured_services,
                          testimonials=testimonials,
                          content=content)

@app.route('/courses')
def courses():
    # Get all courses or filter by category
    category = request.args.get('category')
    if category:
        courses_list = Course.query.filter_by(category=category).all()
    else:
        courses_list = Course.query.all()
    
    return render_template('courses.html', courses=courses_list)

@app.route('/sessions')
def sessions():
    # Get all individual services
    services_list = Service.query.filter(Service.type != 'Group').all()
    return render_template('sessions.html', services=services_list)

@app.route('/group-sessions')
def group_sessions():
    # Get all group services
    group_services = Service.query.filter_by(type='Group').all()
    return render_template('group_sessions.html', group_services=group_services)

@app.route('/memberships')
def memberships():
    # Get all membership plans
    membership_plans = MembershipPlan.query.all()
    return render_template('memberships.html', membership_plans=membership_plans)

@app.route('/natal-chart')
def natal_chart():
    # Find astrology service
    astrology_service = Service.query.filter_by(type='Astrology').first()
    return render_template('natal_chart.html', service=astrology_service)

@app.route('/human-design')
def human_design():
    # Find human design service
    human_design_service = Service.query.filter_by(type='Human Design').first()
    return render_template('human_design.html', service=human_design_service)

@app.route('/blog')
def blog():
    # Get blog posts, possibly filter by category
    category = request.args.get('category')
    if category:
        posts = BlogPost.query.filter_by(category=category, is_published=True).order_by(BlogPost.created_at.desc()).all()
    else:
        posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).all()
    
    return render_template('blog.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process contact form submission
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Create new contact message
        new_message = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Save to database
        db.session.add(new_message)
        db.session.commit()
        
        # Flash success message
        flash('Your message has been sent! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500
    
# User authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            # Use Flask-Login to log in user here
            # login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('A user with that email already exists', 'error')
            return redirect(url_for('signup'))
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Booking routes
@app.route('/book/<service_type>', methods=['GET', 'POST'])
def book_service(service_type):
    service = Service.query.filter_by(type=service_type).first_or_404()
    
    if request.method == 'POST':
        # Process booking submission
        name = request.form.get('name')
        email = request.form.get('email')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        notes = request.form.get('notes')
        
        # Special fields for astrology
        birth_date = None
        birth_time = None
        birth_city = None
        
        if service_type in ['Astrology', 'Human Design']:
            birth_date_str = request.form.get('birth_date')
            birth_time_str = request.form.get('birth_time')
            birth_city = request.form.get('birth_city')
            
            if birth_date_str:
                birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            if birth_time_str:
                birth_time = datetime.strptime(birth_time_str, '%H:%M').time()
        
        # Convert date and time strings to proper objects
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()
        
        # Create booking
        booking = Booking(
            name=name,
            email=email,
            date=date,
            time=time,
            notes=notes,
            birth_date=birth_date,
            birth_time=birth_time,
            birth_city=birth_city,
            service_id=service.id
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Your booking has been submitted! We will confirm shortly.', 'success')
        return redirect(url_for('index'))
    
    return render_template('booking.html', service=service)

# Newsletter subscription route
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    name = request.form.get('name', '')
    
    # Check if already subscribed
    existing = NewsletterSubscriber.query.filter_by(email=email).first()
    if existing:
        if not existing.is_active:
            # Reactivate subscription
            existing.is_active = True
            db.session.commit()
            flash('Your subscription has been reactivated!', 'success')
        else:
            flash('You are already subscribed to our newsletter', 'info')
    else:
        # Create new subscription
        subscriber = NewsletterSubscriber(email=email, name=name)
        db.session.add(subscriber)
        db.session.commit()
        flash('Thank you for subscribing to our newsletter!', 'success')
    
    # Redirect back to referring page
    return redirect(request.referrer or url_for('index'))

# Content Management Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('is_admin'):
        return redirect(url_for('admin_panel'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        
        # For simplicity using a hardcoded password, but in production
        # you would use a more secure approach
        admin_password = os.environ.get('ADMIN_PASSWORD', 'metatonehen2025')
        
        if password == admin_password:
            session['is_admin'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Invalid password', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    if not session.get('is_admin'):
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    # Get all existing content from database
    content = {}
    site_content = SiteContent.query.all()
    
    # Default values if content doesn't exist yet
    content_defaults = {
        'hero_title': 'METATONEHEN',
        'hero_subtitle': 'μετὰ τὸ νέἕν',
        'hero_text': 'Discover cosmic wisdom through sacred geometry and spiritual transformation',
        'courses_title': 'Courses',
        'courses_description': 'Expand your consciousness through our transformative learning journeys',
        'sessions_title': '1-on-1 Sessions',
        'sessions_description': 'Personalized guidance for your spiritual journey',
        'retreats_title': 'Group Sessions & Retreats',
        'retreats_description': 'Collective healing and transformation experiences',
        'membership_title': 'Membership Options',
        'membership_description': 'Join our cosmic community and accelerate your spiritual journey',
        'vertex1': 'Love',
        'vertex2': 'Money',
        'vertex3': 'Health',
        'vertex4': 'Mind',
        'vertex5': 'Soul',
        'vertex6': 'Body'
    }
    
    # Fill in content from database or use defaults
    for item in site_content:
        content[item.key] = item.value
    
    # Add any missing defaults
    for key, value in content_defaults.items():
        if key not in content:
            content[key] = value
    
    return render_template('admin.html', content=content)

@app.route('/admin/save-content', methods=['POST'])
def save_content():
    if not session.get('is_admin'):
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    # Fields to save from the form
    fields = [
        'hero_title', 'hero_subtitle', 'hero_text',
        'courses_title', 'courses_description',
        'sessions_title', 'sessions_description',
        'retreats_title', 'retreats_description',
        'membership_title', 'membership_description'
    ]
    
    for field in fields:
        value = request.form.get(field, '')
        # Check if content already exists
        content = SiteContent.query.filter_by(key=field).first()
        
        if content:
            # Update existing content
            content.value = value
        else:
            # Create new content
            content = SiteContent(key=field, value=value)
            db.session.add(content)
    
    db.session.commit()
    flash('Content has been updated successfully', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/save-vertices', methods=['POST'])
def save_vertices():
    if not session.get('is_admin'):
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    # Fields to save from the form
    fields = ['vertex1', 'vertex2', 'vertex3', 'vertex4', 'vertex5', 'vertex6']
    
    for field in fields:
        value = request.form.get(field, '')
        # Check if content already exists
        content = SiteContent.query.filter_by(key=field).first()
        
        if content:
            # Update existing content
            content.value = value
        else:
            # Create new content
            content = SiteContent(key=field, value=value)
            db.session.add(content)
    
    db.session.commit()
    flash('Vertices have been updated successfully', 'success')
    return redirect(url_for('admin_panel'))

# Media Manager Routes
@app.route('/admin/media', methods=['GET'])
def media_manager():
    if not session.get('is_admin'):
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    upload_form = UploadFileForm()
    media_files = MediaFile.query.order_by(MediaFile.upload_date.desc()).all()
    
    return render_template('media_manager.html', 
                          upload_form=upload_form,
                          media_files=media_files)

@app.route('/admin/media/upload', methods=['POST'])
def upload_media():
    if not session.get('is_admin'):
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    upload_form = UploadFileForm()
    
    if upload_form.validate_on_submit():
        file = upload_form.file.data
        description = upload_form.description.data
        
        # Generate a unique filename to prevent overwriting existing files
        original_filename = secure_filename(file.filename)
        file_ext = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        
        # Determine file type and size
        file_type = file.content_type
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file position
        
        # Save file to upload directory
        upload_path = os.path.join('static', 'uploads')
        file_path = os.path.join(upload_path, unique_filename)
        
        # Ensure directory exists
        os.makedirs(upload_path, exist_ok=True)
        
        file.save(file_path)
        
        # Create database record
        media_file = MediaFile(
            filename=unique_filename,
            original_filename=original_filename,
            file_path=f"/static/uploads/{unique_filename}",
            file_type=file_type,
            file_size=file_size,
            description=description
        )
        
        db.session.add(media_file)
        db.session.commit()
        
        flash('File uploaded successfully!', 'success')
    else:
        for field, errors in upload_form.errors.items():
            for error in errors:
                flash(f"{getattr(upload_form, field).label.text}: {error}", 'error')
    
    return redirect(url_for('media_manager'))

@app.route('/admin/media/delete/<int:media_id>', methods=['POST'])
def delete_media(media_id):
    if not session.get('is_admin'):
        if request.is_json:
            return jsonify({'success': False, 'message': 'Not authorized'})
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    media_file = MediaFile.query.get_or_404(media_id)
    
    # Delete the physical file
    try:
        file_path = os.path.join(app.root_path, media_file.file_path.lstrip('/'))
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        flash(f"Error deleting file: {str(e)}", 'error')
    
    # Delete the database record
    db.session.delete(media_file)
    db.session.commit()
    
    flash('Media file deleted successfully!', 'success')
    return redirect(url_for('media_manager'))

# Page Editor Routes
@app.route('/admin/pages')
def page_manager():
    if not session.get('is_admin'):
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    pages = PageTemplate.query.all()
    
    return render_template('page_manager.html', pages=pages)

@app.route('/admin/pages/new', methods=['GET', 'POST'])
def new_page():
    if not session.get('is_admin'):
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug', '').lower().replace(' ', '-')
        content = request.form.get('content', '')
        is_published = request.form.get('is_published') == 'on'
        
        # Check if slug already exists
        existing_page = PageTemplate.query.filter_by(slug=slug).first()
        if existing_page:
            flash('A page with that URL slug already exists', 'error')
            return redirect(url_for('new_page'))
        
        page = PageTemplate(
            name=name,
            slug=slug,
            content=content,
            is_published=is_published
        )
        
        db.session.add(page)
        db.session.commit()
        
        flash('Page created successfully!', 'success')
        return redirect(url_for('page_manager'))
    
    # Get all media files for the editor
    media_files = MediaFile.query.all()
    
    return render_template('page_editor.html', 
                          page=None, 
                          media_files=media_files)

@app.route('/admin/pages/edit/<int:page_id>', methods=['GET', 'POST'])
def edit_page(page_id):
    if not session.get('is_admin'):
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    page = PageTemplate.query.get_or_404(page_id)
    
    if request.method == 'POST':
        page.name = request.form.get('name')
        new_slug = request.form.get('slug', '').lower().replace(' ', '-')
        
        # Check if slug is changing and if the new slug already exists for another page
        if new_slug != page.slug:
            existing_page = PageTemplate.query.filter_by(slug=new_slug).first()
            if existing_page and existing_page.id != page.id:
                flash('A page with that URL slug already exists', 'error')
                return redirect(url_for('edit_page', page_id=page.id))
            page.slug = new_slug
        
        page.content = request.form.get('content', '')
        page.is_published = request.form.get('is_published') == 'on'
        page.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Page updated successfully!', 'success')
        return redirect(url_for('page_manager'))
    
    # Get all media files for the editor
    media_files = MediaFile.query.all()
    
    return render_template('page_editor.html', 
                          page=page, 
                          media_files=media_files)

@app.route('/admin/pages/delete/<int:page_id>', methods=['POST'])
def delete_page(page_id):
    if not session.get('is_admin'):
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    page = PageTemplate.query.get_or_404(page_id)
    
    db.session.delete(page)
    db.session.commit()
    
    flash('Page deleted successfully!', 'success')
    return redirect(url_for('page_manager'))

# Custom page route to serve created pages
@app.route('/p/<slug>')
def view_page(slug):
    page = PageTemplate.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('page_template.html', page=page)

# Visual Editor Routes
@app.route('/admin/visual-editor')
def visual_editor():
    if not session.get('is_admin'):
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    # Get all media files for the asset manager
    media_files = MediaFile.query.all()
    
    # Get all custom pages
    custom_pages = PageTemplate.query.all()
    
    return render_template('visual_editor.html', media_files=media_files, custom_pages=custom_pages)

@app.route('/admin/get_page_content/<page_name>')
def get_page_content(page_name):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Not authorized'})
    
    try:
        # Check if it's a custom page
        if page_name.startswith('custom_'):
            page_id = int(page_name.replace('custom_', ''))
            page = PageTemplate.query.get_or_404(page_id)
            return jsonify({
                'success': True,
                'html_content': page.content or '',
                'css_content': ''  # Custom pages don't have separate CSS for now
            })
        
        # Get the stored content from the database
        html_content = SiteContent.query.filter_by(key=f"{page_name}_html").first()
        css_content = SiteContent.query.filter_by(key=f"{page_name}_css").first()
        
        # If no stored content, get the rendered template
        if not html_content:
            # Render the template to get its HTML content
            with app.app_context():
                if page_name == 'index':
                    # For index, we need to provide the necessary data
                    featured_courses = Course.query.filter_by(is_featured=True).limit(3).all()
                    featured_services = Service.query.filter_by(is_featured=True).limit(3).all()
                    testimonials = Testimonial.query.filter_by(is_featured=True).limit(3).all()
                    
                    # Get content from database or use defaults
                    content = {}
                    site_content = SiteContent.query.all()
                    
                    # Default values
                    content_defaults = {
                        'hero_title': 'METATONEHEN',
                        'hero_subtitle': 'μετὰ τὸ νέἕν',
                        'hero_text': 'Discover cosmic wisdom through sacred geometry and spiritual transformation',
                    }
                    
                    # Fill in content from database or use defaults
                    for item in site_content:
                        content[item.key] = item.value
                    
                    # Add any missing defaults
                    for key, value in content_defaults.items():
                        if key not in content:
                            content[key] = value
                    
                    rendered = render_template('index.html', 
                                              featured_courses=featured_courses,
                                              featured_services=featured_services,
                                              testimonials=testimonials,
                                              content=content)
                elif hasattr(app, f"{page_name}"):
                    view_func = getattr(app, page_name)
                    rendered = view_func()
                else:
                    # For other pages, try a basic render
                    try:
                        rendered = render_template(f'{page_name}.html')
                    except:
                        return jsonify({
                            'success': True,
                            'html_content': '<div class="container"><h1>Nueva Página</h1><p>Comienza a editar esta página.</p></div>',
                            'css_content': ''
                        })
            
            # Extract just the content section
            start_marker = '{% block content %}'
            end_marker = '{% endblock %}'
            content_start = rendered.find(start_marker) + len(start_marker)
            content_end = rendered.find(end_marker, content_start)
            
            if content_start > -1 and content_end > -1:
                html_content_value = rendered[content_start:content_end].strip()
            else:
                html_content_value = rendered
                
            return jsonify({
                'success': True,
                'html_content': html_content_value,
                'css_content': ''
            })
        
        return jsonify({
            'success': True,
            'html_content': html_content.value if html_content else '',
            'css_content': css_content.value if css_content else ''
        })
        
    except Exception as e:
        app.logger.error(f"Error getting page content: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/save_visual_edit', methods=['POST'])
def save_visual_edit():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Not authorized'})
    
    try:
        data = request.get_json()
        page_name = data.get('page_name')
        html_content = data.get('html_content')
        css_content = data.get('css_content')
        
        # Check if it's a custom page
        if page_name.startswith('custom_'):
            page_id = int(page_name.replace('custom_', ''))
            page = PageTemplate.query.get_or_404(page_id)
            page.content = html_content
            db.session.commit()
            return jsonify({'success': True})
        
        # Save HTML content
        html_key = f"{page_name}_html"
        html_content_obj = SiteContent.query.filter_by(key=html_key).first()
        
        if html_content_obj:
            html_content_obj.value = html_content
        else:
            html_content_obj = SiteContent(key=html_key, value=html_content)
            db.session.add(html_content_obj)
        
        # Save CSS content
        css_key = f"{page_name}_css"
        css_content_obj = SiteContent.query.filter_by(key=css_key).first()
        
        if css_content_obj:
            css_content_obj.value = css_content
        else:
            css_content_obj = SiteContent(key=css_key, value=css_content)
            db.session.add(css_content_obj)
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        app.logger.error(f"Error saving visual edit: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/get_media')
def get_media():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Not authorized'})
    
    try:
        media_files = MediaFile.query.all()
        media_list = []
        
        for media in media_files:
            media_list.append({
                'id': media.id,
                'filename': media.filename,
                'original_filename': media.original_filename,
                'file_path': media.file_path,
                'file_type': media.file_type,
                'description': media.description,
                'upload_date': media.upload_date.strftime('%Y-%m-%d %H:%M:%S') if media.upload_date else None
            })
        
        return jsonify({'success': True, 'media': media_list})
    except Exception as e:
        app.logger.error(f"Error getting media: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/media/upload_ajax', methods=['POST'])
def upload_media_ajax():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Not authorized'})
    
    try:
        file = request.files.get('file')
        description = request.form.get('description', '')
        
        if not file:
            return jsonify({'success': False, 'message': 'No file provided'})
            
        # Check if file is an image
        if not file.content_type.startswith('image/'):
            return jsonify({'success': False, 'message': 'Only image files are allowed'})
        
        # Generate a unique filename
        original_filename = secure_filename(file.filename)
        file_ext = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        
        # Determine file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file position
        
        # Save file to upload directory
        upload_path = os.path.join('static', 'uploads')
        file_path = os.path.join(upload_path, unique_filename)
        
        # Ensure directory exists
        os.makedirs(upload_path, exist_ok=True)
        
        file.save(file_path)
        
        # Create database record
        media_file = MediaFile(
            filename=unique_filename,
            original_filename=original_filename,
            file_path=f"/static/uploads/{unique_filename}",
            file_type=file.content_type,
            file_size=file_size,
            description=description
        )
        
        db.session.add(media_file)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'file_path': f"/static/uploads/{unique_filename}",
            'original_filename': original_filename,
            'description': description
        })
        
    except Exception as e:
        app.logger.error(f"Error uploading media via AJAX: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/save_inline_edit', methods=['POST'])
def save_inline_edit():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Not authorized'})
    
    try:
        data = request.get_json()
        page_url = data.get('pageUrl', '')
        changed_elements = data.get('changedElements', [])
        removed_ids = data.get('removedIds', [])
        added_elements = data.get('addedElements', [])
        
        # Determine which page we're editing
        page_name = page_url.strip('/') or 'index'
        if page_name.startswith('p/'):
            # Custom page
            slug = page_name[2:]
            page = PageTemplate.query.filter_by(slug=slug).first()
            if page:
                # Get the current content
                current_content = page.content
                # TODO: Implement the logic to update the content with the changes
                # For now, just save the raw changes log
                changes_log = SiteContent.query.filter_by(key=f"{page.slug}_changes").first()
                if changes_log:
                    changes_log.value = str(data)
                else:
                    changes_log = SiteContent(key=f"{page.slug}_changes", value=str(data))
                    db.session.add(changes_log)
                
                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Page not found'})
        else:
            # Standard page
            # Save the changes to the database for future rendering
            changes_log = SiteContent.query.filter_by(key=f"{page_name}_inline_changes").first()
            if changes_log:
                changes_log.value = str(data)
            else:
                changes_log = SiteContent(key=f"{page_name}_inline_changes", value=str(data))
                db.session.add(changes_log)
            
            db.session.commit()
            return jsonify({'success': True})
            
    except Exception as e:
        app.logger.error(f"Error saving inline edits: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

# Modo de edición inline para cualquier página
@app.route('/edit-mode/<path:page_path>')
def enter_edit_mode(page_path=''):
    if not session.get('is_admin'):
        flash('You need to login first', 'error')
        return redirect(url_for('admin_login'))
    
    # Set edit mode in session
    session['edit_mode'] = True
    
    # Redirect to the page to edit
    target_url = f"/{page_path}"
    return redirect(target_url)

# Salir del modo de edición
@app.route('/exit-edit-mode')
def exit_edit_mode():
    # Remove edit mode from session
    session.pop('edit_mode', None)
    
    # Redirect back to the previous page or home
    return redirect(request.referrer or url_for('index'))

# Route para cambiar el idioma
@app.route('/set-language/<language>')
def set_language(language):
    # Verificar que el idioma es válido
    supported_locales = ['en', 'es', 'it', 'pt', 'de']
    if language in supported_locales:
        # Guardar el idioma en la sesión
        session['language'] = language
        # Configurar locale para Flask-Babel
        g.locale = language
    
    # Obtener la URL de referencia o usar la página de inicio
    referrer = request.referrer or url_for('index')
    
    # Limpiar la caché para forzar la actualización de la página
    response = redirect(referrer)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response
