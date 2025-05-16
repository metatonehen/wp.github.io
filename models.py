from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relations
    courses = db.relationship('Course', backref='instructor', lazy='dynamic')
    services = db.relationship('Service', backref='provider', lazy='dynamic')
    blog_posts = db.relationship('BlogPost', backref='author', lazy='dynamic')
    events = db.relationship('Event', backref='host', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    duration = db.Column(db.String(50))  # e.g., "6 weeks"
    difficulty_level = db.Column(db.String(20))  # e.g., "Beginner", "Intermediate", "Advanced"
    image_url = db.Column(db.String(255))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Course {self.title}>'

class CourseModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer)
    
    # Foreign Keys
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    
    # Relations
    course = db.relationship('Course', backref='modules')
    lessons = db.relationship('Lesson', backref='module', lazy='dynamic')
    
    def __repr__(self):
        return f'<CourseModule {self.title}>'

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    duration = db.Column(db.String(50))  # e.g., "45 minutes"
    order = db.Column(db.Integer)
    video_url = db.Column(db.String(255))
    
    # Foreign Keys
    module_id = db.Column(db.Integer, db.ForeignKey('course_module.id'))
    
    def __repr__(self):
        return f'<Lesson {self.title}>'

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))  # e.g., "Coaching", "Astrology", "Human Design"
    price = db.Column(db.Float)
    duration = db.Column(db.String(50))  # e.g., "60 minutes"
    image_url = db.Column(db.String(255))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relations
    bookings = db.relationship('Booking', backref='service', lazy='dynamic')
    
    def __repr__(self):
        return f'<Service {self.title}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, canceled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Astrology specific fields
    birth_date = db.Column(db.Date)
    birth_time = db.Column(db.Time)
    birth_city = db.Column(db.String(100))
    
    # Foreign Keys
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relations
    user = db.relationship('User', backref='bookings')
    
    def __repr__(self):
        return f'<Booking {self.id} for {self.service_id}>'

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    excerpt = db.Column(db.Text)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    
    # Foreign Keys
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))  # e.g., "Retreat", "Workshop", "Ceremony"
    location = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float)
    capacity = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Event {self.title}>'

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100))  # e.g., "Course Graduate", "Retreat Participant"
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5 stars
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Optional foreign keys for related services/courses
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    
    # Relations
    course = db.relationship('Course', backref='testimonials')
    service = db.relationship('Service', backref='testimonials')
    event = db.relationship('Event', backref='testimonials')
    
    def __repr__(self):
        return f'<Testimonial by {self.name}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<ContactMessage from {self.name}>'

class NewsletterSubscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<NewsletterSubscriber {self.email}>'

class MembershipPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., "Platinum", "Electrum"
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(20), default='monthly')  # monthly, quarterly, yearly
    benefits = db.Column(db.Text)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Relations
    user_memberships = db.relationship('UserMembership', backref='plan', lazy='dynamic')
    
    def __repr__(self):
        return f'<MembershipPlan {self.name}>'

class UserMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, expired, canceled
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('membership_plan.id'))
    
    # Relations
    user = db.relationship('User', backref='memberships')
    
    def __repr__(self):
        return f'<UserMembership {self.id} for user {self.user_id}>'

class SiteContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SiteContent {self.key}>'

class MediaFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    description = db.Column(db.String(200))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MediaFile {self.original_filename}>'
        
class PageTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PageTemplate {self.name}>'