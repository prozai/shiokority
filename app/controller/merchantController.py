# controllers/merchantController.py
from app.models.merchant import db, Merchant
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

def createAccount(form_data):
    email = form_data.get('email')
    if Merchant.query.filter_by(email=email).first():
        return {'success': False, 'message': 'Email is already in use'}

    try:
        merchant = Merchant(
            name=form_data.get('name'),
            email=email,
            business_name=form_data.get('business_name'),
            password=generate_password_hash(form_data.get('password'))
        )
        db.session.add(merchant)
        db.session.commit()
        return {'success': True, 'message': 'Account created successfully'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': str(e)}
    
def authenticateMerchant(email, password):
    merchant = Merchant.query.filter_by(email=email).first()
    if merchant and check_password_hash(merchant.password, password):
        return merchant
    return None
