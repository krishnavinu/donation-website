from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models import User, NGO, Donation, PickupRequest, Request
from app.forms import NGORegistrationForm
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_ngos': NGO.query.count(),
        'total_donations': Donation.query.count(),
        'pending_pickups': PickupRequest.query.filter_by(status='pending').count()
    }
    recent_donations = Donation.query.order_by(Donation.donation_date.desc()).limit(5).all()
    pending_ngos = NGO.query.filter_by(verified=False).all()
    
    return render_template('admin/dashboard.html', 
                         title='Admin Dashboard',
                         stats=stats,
                         recent_donations=recent_donations,
                         pending_ngos=pending_ngos)

@admin.route('/admin/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', title='Manage Users', users=users)

@admin.route('/admin/ngos')
@login_required
@admin_required
def manage_ngos():
    ngos = NGO.query.all()
    return render_template('admin/ngos.html', title='Manage NGOs', ngos=ngos)

@admin.route('/admin/ngo/<int:ngo_id>/verify')
@login_required
@admin_required
def verify_ngo(ngo_id):
    ngo = NGO.query.get_or_404(ngo_id)
    ngo.verified = True
    db.session.commit()
    flash(f'NGO {ngo.name} has been verified.', 'success')
    return redirect(url_for('admin.manage_ngos'))

@admin.route('/admin/donations')
@login_required
@admin_required
def manage_donations():
    donations = Donation.query.order_by(Donation.donation_date.desc()).all()
    return render_template('admin/donations.html', 
                         title='Manage Donations',
                         donations=donations)

@admin.route('/admin/pickups')
@login_required
@admin_required
def manage_pickups():
    pickups = PickupRequest.query.order_by(PickupRequest.pickup_time.desc()).all()
    return render_template('admin/pickups.html',
                         title='Manage Pickups',
                         pickups=pickups)

@admin.route('/admin/pickup/<int:pickup_id>/status', methods=['POST'])
@login_required
@admin_required
def update_pickup_status(pickup_id):
    pickup = PickupRequest.query.get_or_404(pickup_id)
    status = request.form.get('status')
    if status in ['pending', 'scheduled', 'completed', 'cancelled']:
        pickup.status = status
        db.session.commit()
        flash(f'Pickup request status updated to {status}.', 'success')
    return redirect(url_for('admin.manage_pickups'))

@admin.route('/admin/reports')
@login_required
@admin_required
def reports():
    # Add your reporting logic here
    return render_template('admin/reports.html', title='Reports') 
