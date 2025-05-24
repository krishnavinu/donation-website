from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models import Donation, NGO, PickupRequest
from app.forms import DonationForm, PickupRequestForm
from datetime import datetime

donations = Blueprint('donations', __name__)

@donations.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    form = DonationForm()
    # Populate NGO choices
    form.ngo.choices = [(ngo.ngo_id, ngo.name) for ngo in NGO.query.filter_by(verified=True).all()]
    
    if form.validate_on_submit():
        donation = Donation(
            user_id=current_user.user_id,
            ngo_id=form.ngo.data,
            amount=form.amount.data if form.type.data == 'monetary' else None,
            type=form.type.data,
            status='pending'
        )
        db.session.add(donation)
        
        # If it's a goods donation, create a pickup request
        if form.type.data == 'goods':
            pickup = PickupRequest(
                user_id=current_user.user_id,
                items=form.items.data,
                status='pending'
            )
            db.session.add(pickup)
        
        db.session.commit()
        
        # Add reward points for the donation
        points = 50 if form.type.data == 'monetary' else 30
        current_user.reward_points += points
        db.session.commit()
        
        flash('Thank you for your donation!', 'success')
        return redirect(url_for('donations.my_donations'))
    
    return render_template('donations/donate.html', title='Make a Donation', form=form)

@donations.route('/my-donations')
@login_required
def my_donations():
    donations = Donation.query.filter_by(user_id=current_user.user_id)\
                            .order_by(Donation.donation_date.desc()).all()
    return render_template('donations/my_donations.html', 
                         title='My Donations', 
                         donations=donations)

@donations.route('/pickup-request', methods=['GET', 'POST'])
@login_required
def request_pickup():
    form = PickupRequestForm()
    if form.validate_on_submit():
        pickup = PickupRequest(
            user_id=current_user.user_id,
            address=form.address.data,
            items=form.items.data,
            pickup_time=datetime.strptime(form.pickup_time.data, '%Y-%m-%d %H:%M'),
            status='pending'
        )
        db.session.add(pickup)
        db.session.commit()
        
        flash('Pickup request submitted successfully!', 'success')
        return redirect(url_for('donations.my_pickups'))
    
    return render_template('donations/pickup_request.html', 
                         title='Request Item Pickup', 
                         form=form)

@donations.route('/my-pickups')
@login_required
def my_pickups():
    pickups = PickupRequest.query.filter_by(user_id=current_user.user_id)\
                                .order_by(PickupRequest.pickup_time.desc()).all()
    return render_template('donations/my_pickups.html', 
                         title='My Pickup Requests', 
                         pickups=pickups) 
