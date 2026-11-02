import re
from app import db
from app.models import User
from app.messages import (
    EMAIL_EXISTS, UNAUTHORIZED, ACCOUNT_LOCKED, PASSWORD_MISMATCH,
    PASSWORD_WEAK, PASSWORD_LENGTH, NAME_LENGTH, PHONE_INVALID,
    CANNOT_LOCK_SELF, USER_NOT_FOUND, USER_LOCKED_SUCCESS
)
from flask_jwt_extended import create_access_token

def validate_register_data(data):
    email = data.get('email', '').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    full_name = data.get('full_name', '').strip()
    phone = data.get('phone', '').strip()

    if not email or len(email) > 100 or '@' not in email:
        return 'Email không hợp lệ'
    
    existing = User.query.filter(db.func.lower(User.email) == email.lower()).first()
    if existing:
        return EMAIL_EXISTS

    if not (8 <= len(password) <= 32):
        return PASSWORD_LENGTH
    if not (re.search(r'[A-Za-z]', password) and re.search(r'\d', password)):
        return PASSWORD_WEAK

    if password != confirm_password:
        return PASSWORD_MISMATCH

    if not (2 <= len(full_name) <= 50):
        return NAME_LENGTH

    if not re.match(r'^0\d{9}$', phone):
        return PHONE_INVALID

    return None

def register_user(data):
    err = validate_register_data(data)
    if err:
        return {"error": {"message": err}}, 400

    user = User(
        email=data['email'].strip().lower(),
        full_name=data['full_name'].strip(),
        phone=data['phone'].strip(),
        role='customer',
        locked=False
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role}, 201

def login_user(data):
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    user = User.query.filter(db.func.lower(User.email) == email).first()
    if not user or not user.check_password(password):
        return {"error": {"message": UNAUTHORIZED}}, 401

    if user.locked:
        return {"error": {"message": ACCOUNT_LOCKED}}, 403

    token = create_access_token(identity=str(user.id))
    return {
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    }, 200

def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": {"message": USER_NOT_FOUND}}, 404
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "role": user.role,
        "locked": user.locked
    }, 200

def update_user_profile(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return {"error": {"message": USER_NOT_FOUND}}, 404

    full_name = data.get('full_name', '').strip()
    phone = data.get('phone', '').strip()

    if full_name:
        if not (2 <= len(full_name) <= 50):
            return {"error": {"message": NAME_LENGTH}}, 400
        user.full_name = full_name

    if phone:
        if not re.match(r'^0\d{9}$', phone):
            return {"error": {"message": PHONE_INVALID}}, 400
        user.phone = phone

    db.session.commit()
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "role": user.role
    }, 200

def update_password(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return {"error": {"message": USER_NOT_FOUND}}, 404

    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')

    if not user.check_password(old_password):
        return {"error": {"message": UNAUTHORIZED}}, 400

    if not (8 <= len(new_password) <= 32):
        return {"error": {"message": PASSWORD_LENGTH}}, 400
    if not (re.search(r'[A-Za-z]', new_password) and re.search(r'\d', new_password)):
        return {"error": {"message": PASSWORD_WEAK}}, 400

    if new_password != confirm_password:
        return {"error": {"message": PASSWORD_MISMATCH}}, 400

    user.set_password(new_password)
    db.session.commit()
    return {"message": "Cập nhật mật khẩu thành công"}, 200

def admin_get_users(query_params):
    q = query_params.get('q', '').strip()
    page = int(query_params.get('page', 1))
    size = int(query_params.get('size', 12))

    if page < 1:
        return {"error": {"message": "Trang không hợp lệ"}}, 422

    query = User.query
    if q:
        query = query.filter(
            db.or_(
                User.email.ilike(f'%{q}%'),
                User.full_name.ilike(f'%{q}%'),
                User.phone.ilike(f'%{q}%')
            )
        )

    pagination = query.paginate(page=page, per_page=size, error_out=False)
    items = [{
        "id": u.id,
        "email": u.email,
        "full_name": u.full_name,
        "phone": u.phone,
        "role": u.role,
        "locked": u.locked
    } for u in pagination.items]

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": pagination.total
    }, 200

def admin_toggle_lock_user(admin_id, target_user_id, data):
    if admin_id == target_user_id:
        return {"error": {"message": CANNOT_LOCK_SELF}}, 400

    target = User.query.get(target_user_id)
    if not target:
        return {"error": {"message": USER_NOT_FOUND}}, 404

    locked = data.get('locked')
    if locked is not None:
        target.locked = bool(locked)
        db.session.commit()

    return {
        "id": target.id,
        "email": target.email,
        "locked": target.locked,
        "message": USER_LOCKED_SUCCESS
    }, 200
