import os
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, 
                    SelectField, TextAreaField, IntegerField, DateField, FloatField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask_migrate import Migrate
from sqlalchemy import func, desc, or_

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Nikhil%40260405@localhost/blood_donation_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Custom Jinja2 filters
@app.template_filter('time_ago')
def time_ago_filter(dt):
    """Convert datetime to human-readable relative time"""
    if not dt:
        return 'N/A'
    
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return 'just now'
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours} hour{"s" if hours != 1 else ""} ago'
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f'{days} day{"s" if days != 1 else ""} ago'
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f'{weeks} week{"s" if weeks != 1 else ""} ago'
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f'{months} month{"s" if months != 1 else ""} ago'
    else:
        years = int(seconds / 31536000)
        return f'{years} year{"s" if years != 1 else ""} ago'

@app.template_filter('date_format')
def date_format_filter(dt, format_string='%b %d, %Y'):
    """Format datetime with custom format string"""
    if not dt:
        return 'N/A'
    # If it's already a string, return it as-is
    if isinstance(dt, str):
        return dt
    # If it's a datetime object, format it
    return dt.strftime(format_string)

# Database Models
class User(UserMixin, db.Model):
    __tablename__ = 'user'  # Explicitly set table name
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    blood_type = db.Column(db.String(5))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default='United States')
    profile_image = db.Column(db.String(200))
    is_donor = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    last_donation = db.Column(db.DateTime)
    donation_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships with explicit foreign keys
    donations = db.relationship('Donation', foreign_keys='Donation.donor_id', backref=db.backref('donor', lazy=True), lazy=True)
    blood_requests = db.relationship('BloodRequest', foreign_keys='BloodRequest.requester_id', backref=db.backref('requester', lazy=True), lazy=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        if self.date_of_birth:
            today = datetime.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def get_profile_completion(self):
        """Calculate profile completion percentage"""
        required_fields = [
            self.first_name, self.last_name, self.email, self.phone, 
            self.blood_type, self.date_of_birth, self.gender, 
            self.address, self.city, self.state, self.postal_code
        ]
        
        completed = sum(1 for field in required_fields if field)
        total = len(required_fields)
        return int((completed / total) * 100) if total > 0 else 0

class Donation(db.Model):
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Changed from 'users.id' to 'user.id'
    blood_type = db.Column(db.String(5), nullable=False)
    units = db.Column(db.Float, nullable=False)
    donation_date = db.Column(db.DateTime, nullable=False)
    next_eligible_date = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled, no_show
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'donor_id': self.donor_id,
            'blood_type': self.blood_type,
            'units': self.units,
            'donation_date': self.donation_date.isoformat() if self.donation_date else None,
            'next_eligible_date': self.next_eligible_date.isoformat() if self.next_eligible_date else None,
            'location': self.location,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class BloodRequest(db.Model):
    __tablename__ = 'blood_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_age = db.Column(db.Integer)
    patient_gender = db.Column(db.String(20))
    blood_type = db.Column(db.String(5), nullable=False)
    units_required = db.Column(db.Integer, nullable=False)
    required_by = db.Column(db.DateTime, nullable=False)
    hospital_name = db.Column(db.String(200), nullable=False)
    hospital_address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(15), nullable=False)
    additional_notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_name': self.patient_name,
            'blood_type': self.blood_type,
            'units_required': self.units_required,
            'hospital_name': self.hospital_name,
            'city': self.city,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class BloodInventory(db.Model):
    __tablename__ = 'blood_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(5), nullable=False)
    blood_bank_name = db.Column(db.String(100), nullable=False, default='Main Blood Bank')
    units_available = db.Column(db.Integer, default=0)
    units_reserved = db.Column(db.Integer, default=0)
    target_level = db.Column(db.Float, default=100.0)
    critical_level = db.Column(db.Float, default=10.0)
    last_updated = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'blood_type': self.blood_type,
            'units_available': self.units_available,
            'units_reserved': self.units_reserved,
            'target_level': self.target_level,
            'critical_level': self.critical_level,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
        
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationship is defined in User model via backref or we can define it here
    # user = db.relationship('User', backref=db.backref('notifications', lazy=True))

# Routes
# Sign Up Form
class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='Passwords must match'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    blood_type = SelectField('Blood Type', choices=[
        ('', 'Select Blood Type'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ])
    is_donor = BooleanField('I want to be a blood donor')
    accept_terms = BooleanField('I accept the Terms and Conditions', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

# Contact Form
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

# Main routes
@app.route('/')
def index():
    # Mock data for the frontend
    return render_template('index.html', 
                         total_donors=100,
                         total_donations=500,
                         lives_saved=1000,
                         active_campaigns=5)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Here you would typically send an email or save the message to a database
        # For now, we'll just show a success message
        flash('Your message has been sent successfully! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blood-banks')
def blood_banks():
    return render_template('blood_banks.html')

# Add missing routes
@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/become_donor')
def become_donor():
    return redirect(url_for('signup'))  # Redirect to signup page for now

@app.route('/donors')
@login_required
def donors():
    # Mock donor data
    mock_donors = [
        {'first_name': 'John', 'last_name': 'Doe', 'blood_type': 'O+', 'city': 'Sample City'},
        {'first_name': 'Jane', 'last_name': 'Smith', 'blood_type': 'A+', 'city': 'Sample City'}
    ]
    return render_template('donors.html', donors=mock_donors)

class BloodRequestForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[DataRequired()])
    blood_type = SelectField('Blood Type', choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ], validators=[DataRequired()])
    units_required = IntegerField('Units Required', validators=[DataRequired(), NumberRange(min=1)])
    required_date = DateField('Required Date', format='%Y-%m-%d', validators=[DataRequired()])
    hospital_name = StringField('Hospital Name', validators=[DataRequired()])
    hospital_address = TextAreaField('Hospital Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    contact_name = StringField('Contact Person', validators=[DataRequired()])
    contact_phone = StringField('Contact Phone', validators=[DataRequired()])
    contact_email = StringField('Contact Email', validators=[Optional(), Email()])
    submit = SubmitField('Submit Request')


@app.route('/inventory')
def inventory():
    inventory_data = BloodInventory.query.all()
    
    # Calculate stats
    total_units = sum(i.units_available for i in inventory_data)
    total_reserved = sum(i.units_reserved for i in inventory_data)
    critical_types = sum(1 for i in inventory_data if i.units_available < i.critical_level)
    
    return render_template('inventory.html', inventory=inventory_data, 
                           total_units=total_units, 
                           total_reserved=total_reserved, 
                           critical_types=critical_types)

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        flash('Thank you for your interest in donating blood!', 'success')
        return redirect(url_for('index'))
    return render_template('donate.html')

# Authentication routes
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('Logged in successfully!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = SignUpForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))
            
        # Create new user
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password,
            blood_type=form.blood_type.data if form.blood_type.data else None,
            is_donor=form.is_donor.data,
            created_at=datetime.utcnow()
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            print(f"Error creating user: {e}")
            import traceback
            traceback.print_exc()
    else:
        # Print form validation errors
        if request.method == 'POST':
            print("Form validation failed!")
            print(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'danger')
            
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

# Placeholder routes for future features
class DonationForm(FlaskForm):
    donation_date = DateField('Preferred Date', format='%Y-%m-%d', validators=[DataRequired()])
    location = SelectField('Donation Center', choices=[
        ('Rotary Bangalore TTK Blood Bank - Indiranagar', 'Rotary Bangalore TTK Blood Bank - Indiranagar'),
        ('Rashtrotthana Blood Bank - Jayanagar', 'Rashtrotthana Blood Bank - Jayanagar'),
        ('Lions Blood Bank - Malleswaram', 'Lions Blood Bank - Malleswaram'),
        ('Red Cross Blood Bank - MG Road', 'Red Cross Blood Bank - MG Road'),
        ('Victoria Hospital Blood Bank - City Market', 'Victoria Hospital Blood Bank - City Market'),
        ('Home Visit', 'Home Visit (We come to you)'),
        ('Other', 'Other (Please specify in notes)')
    ], validators=[DataRequired()])
    home_address = TextAreaField('Home Address (For Home Visit)')
    notes = TextAreaField('Notes (Optional)')
    submit = SubmitField('Schedule Donation')

@app.route('/api/search-donors')
def search_donors():
    blood_type = request.args.get('blood_type')
    location = request.args.get('location')
    
    query = User.query.filter_by(is_donor=True)
    
    if blood_type:
        query = query.filter_by(blood_type=blood_type)
    
    if location:
        query = query.filter(or_(User.city.ilike(f'%{location}%'), User.state.ilike(f'%{location}%'), User.postal_code.ilike(f'%{location}%'), User.address.ilike(f'%{location}%')))
        
    donors = query.all()
    
    return jsonify([{
        'id': d.id,
        'name': d.full_name,
        'blood_type': d.blood_type,
        'location': f"{d.address}, {d.city} - {d.postal_code}" if d.city else "Unknown",
        'last_donation': d.last_donation.strftime('%Y-%m-%d') if d.last_donation else 'Never',
        'donation_count': d.donation_count,
        'phone': d.phone,
        'email': d.email,
        'profile_image': d.profile_image or 'https://randomuser.me/api/portraits/lego/1.jpg'
    } for d in donors])

@app.route('/request-blood', methods=['GET', 'POST'])
@login_required
def request_blood():
    form = BloodRequestForm()
    if request.method == 'GET' and request.args.get('blood_type'):
        form.blood_type.data = request.args.get('blood_type')
        
    if form.validate_on_submit():
        blood_request = BloodRequest(
            requester_id=current_user.id,
            patient_name=form.patient_name.data,
            blood_type=form.blood_type.data,
            units_required=form.units_required.data,
            required_by=datetime.combine(form.required_date.data, datetime.min.time()),
            hospital_name=form.hospital_name.data,
            hospital_address=form.hospital_address.data,
            city=form.city.data,
            contact_name=form.contact_name.data,
            contact_phone=form.contact_phone.data,
            status='Open'
        )
        db.session.add(blood_request)
        
        # Notify matching donors
        matching_donors = User.query.filter_by(
            is_donor=True, 
            blood_type=form.blood_type.data
        ).filter(User.id != current_user.id).all()
        
        for donor in matching_donors:
            notification = Notification(
                user_id=donor.id,
                message=f"{form.patient_name.data} has requested {form.units_required.data} units of blood. Contact {form.contact_phone.data} if you are interested in donating.",
                is_read=False
            )
            db.session.add(notification)
            
        db.session.commit()
        flash(f'Blood request submitted! {len(matching_donors)} potential donors have been notified.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('request_blood.html', form=form)

@app.route('/schedule-donation', methods=['GET', 'POST'])
@login_required
def schedule_donation():
    form = DonationForm()
    if form.validate_on_submit():
        # Determine location string
        loc = form.location.data
        if loc == 'Home Visit':
            if form.home_address.data:
                loc = f"Home Visit at: {form.home_address.data}"
            else:
                # Fallback if they didn't fill it, though UI should enforce it
                loc = f"Home Visit at: {current_user.address or 'Address not provided'}"
        
        donation = Donation(
            donor_id=current_user.id,
            blood_type=current_user.blood_type or 'Unknown',
            units=0,  # Will be updated after donation
            donation_date=datetime.combine(form.donation_date.data, datetime.min.time()),
            location=loc,
            status='scheduled',
            notes=form.notes.data
        )
        db.session.add(donation)
        
        # Create notification
        msg = f"Your donation at {loc} has been scheduled for {form.donation_date.data}."
        notification = Notification(
            user_id=current_user.id,
            message=msg
        )
        db.session.add(notification)
        
        db.session.commit()
        flash('Donation scheduled successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('schedule_donation.html', form=form)

@app.route('/api/notifications')
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(10).all()
    return jsonify([{
        'id': n.id,
        'message': n.message,
        'is_read': n.is_read,
        'created_at': n.created_at.strftime('%Y-%m-%d %H:%M')
    } for n in notifications])

@app.route('/api/notifications/mark-read', methods=['POST'])
@login_required
def mark_notifications_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return jsonify({'success': True})

@app.route('/donation-tips')
def donation_tips():
    return render_template('donation_tips.html')

@app.route('/donation-history')
@login_required
def donation_history():
    """Placeholder for donation history feature"""
    donations = Donation.query.filter_by(donor_id=current_user.id)\
        .order_by(Donation.donation_date.desc())\
        .all()
    return render_template('donation_history.html', donations=donations)

@app.route('/certificate/<int:donation_id>')
@login_required
def certificate(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    # Ensure the user owns this donation
    if donation.donor_id != current_user.id:
        flash('You do not have permission to view this certificate.', 'danger')
        return redirect(url_for('donation_history'))
    
    return render_template('certificate.html', 
                           donor_name=current_user.full_name, 
                           donation_date=donation.donation_date.strftime('%B %d, %Y'))


# User dashboard and profile
@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's recent donations
    recent_donations = Donation.query.filter_by(donor_id=current_user.id)\
        .order_by(Donation.donation_date.desc())\
        .limit(5)\
        .all()
    
    # Get user's blood requests
    blood_requests = BloodRequest.query.filter_by(requester_id=current_user.id)\
        .order_by(BloodRequest.created_at.desc())\
        .limit(5)\
        .all()
    
    # Mock upcoming donations (in real app, would come from appointments table)
    upcoming_donations = []
    
    # Calculate stats
    total_donations = Donation.query.filter_by(donor_id=current_user.id).count()
    lives_saved = total_donations * 3  # Each donation can save up to 3 lives
    
    stats = {
        'total_donations': total_donations,
        'lives_saved': lives_saved,
        'blood_type': current_user.blood_type or 'Not Set',
        'next_eligible': 'Check with doctor'
    }
    
    # Get recent activities
    recent_activities = []
    
    # Add donation activities
    for donation in recent_donations[:3]:
        recent_activities.append({
            'icon': 'fas fa-tint',
            'title': 'Blood Donation',
            'description': f'Donated {donation.blood_type} blood',
            'time_ago': f'{(datetime.utcnow() - donation.donation_date).days} days ago'
        })
    
    # Add request activities
    for request in blood_requests[:2]:
        recent_activities.append({
            'icon': 'fas fa-hand-holding-medical',
            'title': 'Blood Request',
            'description': f'Requested {request.blood_type} blood - {request.status}',
            'time_ago': f'{(datetime.utcnow() - request.created_at).days} days ago'
        })
    
    # Calculate profile completion percentage
    profile_completion = current_user.get_profile_completion()
    
    return render_template('dashboard.html',
                         recent_donations=recent_donations,
                         blood_requests=blood_requests,
                         upcoming_donations=upcoming_donations,
                         stats=stats,
                         recent_activities=recent_activities,
                         profile_completion=profile_completion)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Update profile information
        current_user.first_name = request.form.get('first_name', current_user.first_name)
        current_user.last_name = request.form.get('last_name', current_user.last_name)
        current_user.phone = request.form.get('phone', current_user.phone)
        current_user.blood_type = request.form.get('blood_type', current_user.blood_type)
        current_user.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d') if request.form.get('date_of_birth') else None
        current_user.gender = request.form.get('gender', current_user.gender)
        current_user.address = request.form.get('address', current_user.address)
        current_user.city = request.form.get('city', current_user.city)
        current_user.state = request.form.get('state', current_user.state)
        current_user.postal_code = request.form.get('postal_code', current_user.postal_code)
        current_user.country = request.form.get('country', current_user.country)
        
        # Handle profile picture upload
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{current_user.id}_{int(datetime.utcnow().timestamp())}.{file.filename.rsplit('.', 1)[1].lower()}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    file.save(filepath)
                    current_user.profile_image = f"uploads/profiles/{filename}"
        
        try:
            db.session.commit()
            flash('Your profile has been updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error updating profile: {str(e)}')
            flash('An error occurred while updating your profile. Please try again.', 'danger')
        
        return redirect(url_for('profile'))
    
    return render_template('profile.html')

# API Endpoints
@app.route('/api/blood-types')
def get_blood_types():
    blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    return jsonify(blood_types)

@app.route('/api/donors')
def get_donors():
    blood_type = request.args.get('blood_type')
    location = request.args.get('location', '').lower()
    
    query = User.query.filter_by(is_donor=True)
    
    if blood_type:
        query = query.filter_by(blood_type=blood_type)
    
    if location:
        query = query.filter(
            (User.city.ilike(f'%{location}%')) | 
            (User.state.ilike(f'%{location}%')) |
            (User.address.ilike(f'%{location}%'))
        )
    
    donors = query.all()
    
    donors_data = [{
        'id': donor.id,
        'name': donor.full_name,
        'blood_type': donor.blood_type,
        'location': f"{donor.city}, {donor.state}" if donor.city and donor.state else 'Location not specified',
        'last_donation': donor.last_donation.strftime('%Y-%m-%d') if donor.last_donation else 'Never',
        'donation_count': donor.donation_count or 0,
        'profile_image': url_for('static', filename=donor.profile_image) if donor.profile_image else url_for('static', filename='images/default-avatar.png')
    } for donor in donors]
    
    return jsonify(donors_data)

@app.route('/api/inventory')
def get_inventory():
    inventory = BloodInventory.query.all()
    return jsonify([item.to_dict() for item in inventory])

@app.route('/fix-donors')
def fix_donors():
    try:
        import datetime
        
        # 1. Get Users
        admin = User.query.filter_by(email='admin@gmail.com').first()
        ff = User.query.filter_by(email='ff@gmail.com').first()

        if not admin: return "Error: admin@gmail.com not found."
        if not ff: return "Error: ff@gmail.com not found."

        # 2. Ensure Admin is a Donor and A+
        if not admin.is_donor:
            admin.is_donor = True
        admin.blood_type = 'A+'
        db.session.add(admin)

        # 3. Find FF's Last Request
        last_req = BloodRequest.query.filter_by(requester_id=ff.id).order_by(BloodRequest.created_at.desc()).first()
        
        if not last_req:
            # If no request exists, create one
            req = BloodRequest(
                requester_id=ff.id,
                patient_name="Demo Patient (Created by System)",
                blood_type="A+",
                units_required=2,
                required_by=datetime.datetime.now() + datetime.timedelta(days=2),
                hospital_name="City Hospital",
                hospital_address="123 Main St",
                city="Bangalore",
                contact_name=ff.first_name,
                contact_phone=ff.phone,
                status="Open",
                created_at=datetime.datetime.now()
            )
            db.session.add(req)
            last_req = req
            status_msg = "Created new request as none existed."
        else:
            status_msg = f"Found existing request for {last_req.patient_name}."

        # 4. DELETE OLD NOTIFICATIONS
        Notification.query.filter_by(user_id=admin.id).delete()

        # 5. CREATE NEW NOTIFICATION
        msg = f"{last_req.patient_name} has requested {last_req.units_required} units of blood. Contact {last_req.contact_phone} if you are interested in donating."
        notif = Notification(
            user_id=admin.id,
            message=msg,
            is_read=False,
            created_at=datetime.datetime.now()
        )
        db.session.add(notif)

        db.session.commit()
        return f"SUCCESS! {status_msg} Notification sent: '{msg}'. <a href='/dashboard'>Go to Dashboard</a>"
    except Exception as e:
        return f"Error: {str(e)}"

def create_tables():
    """Create database tables."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

def init_db():
    """Initialize the database with default data."""
    with app.app_context():
        try:
            # Create admin user if not exists
            admin = User.query.filter_by(email='admin@bloodbridge.com').first()
            if not admin:
                admin = User(
                    first_name='Admin',
                    last_name='User',
                    email='admin@bloodbridge.com',
                    password=generate_password_hash('admin123'),
                    phone='1234567890',
                    is_admin=True,
                    is_verified=True,
                    created_at=datetime.utcnow()
                )
                db.session.add(admin)
            
            # Initialize blood inventory if empty
            blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
            for blood_type in blood_types:
                if not BloodInventory.query.filter_by(blood_type=blood_type).first():
                    inventory = BloodInventory(
                        blood_type=blood_type,
                        units_available=0,
                        units_reserved=0,
                        target_level=100.0,
                        critical_level=10.0
                    )
                    db.session.add(inventory)
            
            db.session.commit()
            print("Database initialized with default data!")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {e}")
        finally:
            db.session.close()

# Create error templates directory if it doesn't exist
errors_dir = os.path.join(app.root_path, 'templates', 'errors')
os.makedirs(errors_dir, exist_ok=True)

# Create default error pages if they don't exist
def create_error_page(status_code):
    error_file = os.path.join(errors_dir, f"{status_code}.html")
    if not os.path.exists(error_file):
        with open(error_file, 'w') as f:
            f.write(f"""{{
% extends "base.html" %}}

{{% block title %}}{status_code} Error - Blood Bridge{{% endblock %}}

{{% block content %}}
<div class="container my-5">
    <div class="row justify-content-center">
        <div class="col-md-8 text-center">
            <h1 class="display-1 text-danger">{status_code}</h1>
            <h2 class="mb-4">
                {{% if status_code == 404 %}}
                    Page Not Found
                {{% elif status_code == 403 %}}
                    Access Forbidden
                {{% elif status_code == 500 %}}
                    Server Error
                {{% else %}}
                    Something went wrong
                {{% endif %}}
            </h2>
            <p class="lead mb-4">
                {{% if status_code == 404 %}}
                    The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
                {{% elif status_code == 403 %}}
                    You don't have permission to access this page.
                {{% elif status_code == 500 %}}
                    We're experiencing some technical difficulties. Please try again later.
                {{% else %}}
                    An unexpected error has occurred. Please try again later.
                {{% endif %}}
            </p>
            <a href="{{{{ url_for('index') }}}}" class="btn btn-primary btn-lg">
                <i class="fas fa-home me-2"></i> Go to Homepage
            </a>
        </div>
    </div>
</div>
{{% endblock %}}
""")

# Create error pages for common HTTP errors
for code in [400, 401, 403, 404, 405, 408, 413, 429, 500, 502, 503, 504]:
    create_error_page(code)

if __name__ == '__main__':
    # Create database tables first
    print("Creating database tables...")
    create_tables()
    
    # Then initialize with default data
    print("Initializing database with default data...")
    init_db()
    
    # Start the development server
    print("Starting development server...")
    app.run(debug=True, port=5000)
