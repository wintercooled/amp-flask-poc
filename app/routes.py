from flask import render_template, request, flash, redirect, url_for

from app import app
from app.api_data_access import BlockstreamAMPAPI
from app.forms import RegisteredUserForm

PERMISSION_DENIED = 'You do not have permission to view this page.'
GENERAL_ERROR = 'An error occured, please try again later.'
PAGE_NOT_FOUND = 'Page not found'
APPLICATION_ERROR = 'An application error occured, please try again later or contact amp-developers@blockstream.com if the problem persists.'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=PAGE_NOT_FOUND)


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', error=APPLICATION_ERROR)


@app.route('/')
@app.route('/index')
@app.route('/assets')
def assets():
    assets = BlockstreamAMPAPI.assets()
    return render_template('assets.html', title='Assets', assets=assets)


@app.route('/asset_summary')
def asset_summary():
    try:
        asset_uuid = request.args.get('asset_uuid')
        asset = BlockstreamAMPAPI.asset(asset_uuid)
        summary = BlockstreamAMPAPI.asset_summary(asset_uuid)
        activities = BlockstreamAMPAPI.asset_activities(asset_uuid)
        balance = BlockstreamAMPAPI.asset_balance(asset_uuid)
        utxos = BlockstreamAMPAPI.asset_utxos(asset_uuid)
        circulating_amount = summary['issued'] + summary['reissued'] - summary['burned'] - summary['blacklisted']
    except PermissionError:
        return render_template('error.html', error=PERMISSION_DENIED)
    return render_template('asset_summary.html', title='Asset Summary', asset=asset,
        circulating_amount=circulating_amount, activities=activities, balance=balance, utxos=utxos)


@app.route('/registered_users')
def registered_users():
    investors = BlockstreamAMPAPI.investors()
    return render_template('registered_users.html', title='Registered Users', investors=investors)


@app.route('/registered_user')
def registered_user():
    investor_id = request.args.get('registered_user_id')
    try:
        investor = BlockstreamAMPAPI.investor(investor_id)
        gaid = None
        balances = None
        if investor['GAID']:
            gaid = investor['GAID']
            balances = BlockstreamAMPAPI.gaid_balance(gaid)
    except PermissionError:
        return render_template('error.html', error=PERMISSION_DENIED)
    return render_template('registered_user.html', title='Registered User', investor=investor, balances=balances)


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form = RegisteredUserForm()
    name = None
    if form.validate_on_submit():
        gaid = form.gaid.data
        name = form.name.data
        try:
            new_investor = BlockstreamAMPAPI.investors_add(name, gaid)
        except ValueError as e:
            if 'An error occured. An investor with that GAID was already created.' == str(e):
                return render_template('register_user.html', title='Register GAID', form=form, name=name, already_registered=True)
            else:
                flash(str(e), 'error')
                return redirect(url_for('register_user'))
    return render_template('register_user.html', title='Register GAID', form=form, name=name, already_registered=False)

