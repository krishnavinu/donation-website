from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Donation, User, NGO, PickupRequest
from app.forms import DonationForm, PickupRequestForm
from app import db
from flask_login import login_required, current_user

donations = Blueprint('donations', __name__)

@donations.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    form = DonationForm()
    ngos = NGO.query.all()
    form.ngo.choices = [(ngo.ngo_id, ngo.name) for ngo in ngos]
    if form.validate_on_submit():
        donation = Donation(
            user_id=current_user.user_id,
            ngo_id=form.ngo.data,
            amount=form.amount.data,
            type=form.type.data,
            status='pending',
        )
        db.session.add(donation)
        db.session.commit()
        flash('Thank you for your donation!', 'success')
        return redirect(url_for('donations.list_donations'))
    return render_template('main/donate.html', form=form)

@donations.route('/donations')
def list_donations():
    all_donations = Donation.query.order_by(Donation.donation_date.desc()).all()
    return render_template('donations/donation.html', donations=all_donations)

@donations.route('/my_donations')
@login_required
def my_donations():
    user_donations = Donation.query.filter_by(user_id=current_user.user_id).order_by(Donation.donation_date.desc()).all()
    return render_template('user/my_donations.html', donations=user_donations)

@donations.route('/my_pickups')
@login_required
def my_pickups():
    pickups = PickupRequest.query.filter_by(user_id=current_user.user_id).order_by(PickupRequest.pickup_time.desc()).all()
    return render_template('user/my_pickups.html', pickups=pickups)

@donations.route('/pickup_request', methods=['GET', 'POST'])
@login_required
def pickup_request():
    donation_id = request.args.get('donation_id', type=int)
    form = PickupRequestForm()
    ngos = NGO.query.all()
    form.ngo.choices = [(ngo.ngo_id, ngo.name) for ngo in ngos]
    if donation_id:
        donation = Donation.query.get(donation_id)
        if donation and donation.user_id == current_user.user_id:
            if request.method == 'GET':
                form.items.data = f"Donation for NGO: {donation.ngo.name if donation.ngo else ''}, Amount: {donation.amount}, Type: {donation.type}"
                form.ngo.data = donation.ngo_id
    if form.validate_on_submit():
        pickup = PickupRequest(
            user_id=current_user.user_id,
            ngo_id=form.ngo.data,
            address=form.address.data,
            items=form.items.data,
            pickup_time=form.pickup_time.data,
            status='pending'
        )
        db.session.add(pickup)
        db.session.commit()
        flash('Pickup request submitted!', 'success')
        return redirect(url_for('donations.my_pickups'))
    return render_template('donations/pickup_request.html', form=form) 