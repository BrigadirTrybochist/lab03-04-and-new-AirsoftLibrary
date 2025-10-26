from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Weapon, Module
from forms import WeaponForm, ModuleForm
from sqlalchemy import func
import logging

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Головна сторінка з меню вибору"""
    stats = get_collection_stats()
    return render_template('index.html', stats=stats)


@bp.route('/weapon/<int:id>')
def weapon_detail(id):
    """Детальна сторінка зброї"""
    weapon = Weapon.query.get_or_404(id)
    return render_template('weapon_detail.html', weapon=weapon)


@bp.route('/weapons')
def weapons():
    """Сторінка зі списком зброї з фільтрами"""
    sort_by = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    
    # Валідні поля для сортування
    valid_sorts = {
        'name': Weapon.name,
        'brand': Weapon.brand,
        'created_at': Weapon.created_at,
        'purchase_date': Weapon.purchase_date,
        'purchase_price': Weapon.purchase_price
    }
    
    if sort_by not in valid_sorts:
        sort_by = 'created_at'
    
    sort_field = valid_sorts[sort_by]
    if order == 'asc':
        weapons = Weapon.query.order_by(sort_field.asc()).all()
    else:
        weapons = Weapon.query.order_by(sort_field.desc()).all()
    
    stats = get_collection_stats()
    return render_template('weapons.html', weapons=weapons, stats=stats, sort_by=sort_by, order=order)


@bp.route('/modules')
def modules():
    """Сторінка зі списком модулів з фільтрами"""
    sort_by = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    
    valid_sorts = {
        'name': Module.name,
        'module_type': Module.module_type,
        'brand': Module.brand,
        'created_at': Module.created_at,
        'purchase_date': Module.purchase_date,
        'purchase_price': Module.purchase_price
    }
    
    if sort_by not in valid_sorts:
        sort_by = 'created_at'
    
    sort_field = valid_sorts[sort_by]
    if order == 'asc':
        modules = Module.query.order_by(sort_field.asc()).all()
    else:
        modules = Module.query.order_by(sort_field.desc()).all()
    
    stats = get_collection_stats()
    return render_template('modules.html', modules=modules, stats=stats, sort_by=sort_by, order=order)


@bp.route('/add_weapon', methods=['GET', 'POST'])
def add_weapon():
    """Додавання нової зброї"""
    form = WeaponForm()
    
    if form.validate_on_submit():
        try:
            weapon = Weapon(
                name=form.name.data,
                brand=form.brand.data,
                model=form.model.data,
                weapon_type=form.weapon_type.data,
                fps=form.fps.data,
                joules=form.joules.data,
                is_tuned=form.is_tuned.data,
                purchase_date=form.purchase_date.data,
                purchase_price=form.purchase_price.data,
                notes=form.notes.data
            )
            db.session.add(weapon)
            db.session.commit()
            flash(f'Зброю "{weapon.name}" успішно додано до колекції!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding weapon: {e}")
            flash('Помилка при додаванні зброї. Спробуйте ще раз.', 'error')
    
    return render_template('add_weapon.html', form=form)


@bp.route('/add_module', methods=['GET', 'POST'])
def add_module():
    """Додавання нового модуля"""
    form = ModuleForm()
    
    # Populate weapon choices
    weapons = Weapon.query.all()
    form.weapon_id.choices = [(0, 'Не прикріплено')] + [(w.id, f"{w.brand} {w.model}") for w in weapons]
    
    if form.validate_on_submit():
        try:
            weapon_id = form.weapon_id.data if form.weapon_id.data != 0 else None
            module = Module(
                name=form.name.data,
                module_type=form.module_type.data,
                brand=form.brand.data,
                is_used=form.is_used.data,
                weapon_id=weapon_id,
                purchase_date=form.purchase_date.data,
                purchase_price=form.purchase_price.data,
                notes=form.notes.data
            )
            db.session.add(module)
            db.session.commit()
            flash(f'Модуль "{module.name}" успішно додано!', 'success')
            return redirect(url_for('main.modules'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding module: {e}")
            flash('Помилка при додаванні модуля. Спробуйте ще раз.', 'error')
    
    return render_template('add_module.html', form=form)


def get_collection_stats():
    """Отримання статистики колекції"""
    weapons_count = Weapon.query.count()
    modules_count = Module.query.count()
    
    # Загальна сума зброї
    weapons_total = db.session.query(func.sum(Weapon.purchase_price)).filter(
        Weapon.purchase_price.isnot(None)
    ).scalar() or 0
    
    # Загальна сума модулів
    modules_total = db.session.query(func.sum(Module.purchase_price)).filter(
        Module.purchase_price.isnot(None)
    ).scalar() or 0
    
    total_value = weapons_total + modules_total
    
    return {
        'weapons_count': weapons_count,
        'modules_count': modules_count,
        'total_value': total_value,
        'weapons_total': weapons_total,
        'modules_total': modules_total
    }

@bp.route('/weapon/<int:id>/edit', methods=['GET', 'POST'])
def edit_weapon(id):
    """Редагування зброї"""
    weapon = Weapon.query.get_or_404(id)
    form = WeaponForm(obj=weapon)
    
    if form.validate_on_submit():
        try:
            weapon.name = form.name.data
            weapon.brand = form.brand.data
            weapon.model = form.model.data
            weapon.weapon_type = form.weapon_type.data
            weapon.fps = form.fps.data
            weapon.joules = form.joules.data
            weapon.is_tuned = form.is_tuned.data
            weapon.purchase_date = form.purchase_date.data
            weapon.purchase_price = form.purchase_price.data
            weapon.notes = form.notes.data
            
            db.session.commit()
            flash(f'Зброю "{weapon.name}" успішно оновлено!', 'success')
            return redirect(url_for('main.weapon_detail', id=weapon.id))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating weapon: {e}")
            flash('Помилка при оновленні зброї. Спробуйте ще раз.', 'error')
    
    return render_template('add_weapon.html', form=form, weapon=weapon)

@bp.route('/weapon/<int:id>/delete', methods=['POST'])
def delete_weapon(id):
    """Видалення зброї"""
    weapon = Weapon.query.get_or_404(id)
    try:
        name = weapon.name
        db.session.delete(weapon)
        db.session.commit()
        flash(f'Зброю "{name}" видалено з колекції.', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting weapon: {e}")
        flash('Помилка при видаленні зброї.', 'error')
    return redirect(url_for('main.weapons'))

@bp.route('/weapon/<int:id>/toggle_tuned', methods=['POST'])
def toggle_weapon_tuned(id):
    """Змінити статус налагодження зброї"""
    weapon = Weapon.query.get_or_404(id)
    try:
        weapon.is_tuned = not weapon.is_tuned
        db.session.commit()
        status = "налагоджено" if weapon.is_tuned else "не налагоджено"
        flash(f'Статус зброї "{weapon.name}" змінено на {status}.', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error toggling weapon status: {e}")
        flash('Помилка при зміні статусу зброї.', 'error')
    return redirect(url_for('main.weapons'))

@bp.route('/module/<int:id>/edit', methods=['GET', 'POST'])
def edit_module(id):
    """Редагування модуля"""
    module = Module.query.get_or_404(id)
    form = ModuleForm(obj=module)
    
    # Populate weapon choices
    weapons = Weapon.query.all()
    form.weapon_id.choices = [(0, 'Не прикріплено')] + [(w.id, f"{w.brand} {w.model}") for w in weapons]
    
    if form.validate_on_submit():
        try:
            module.name = form.name.data
            module.module_type = form.module_type.data
            module.brand = form.brand.data
            module.is_used = form.is_used.data
            module.weapon_id = form.weapon_id.data if form.weapon_id.data != 0 else None
            module.purchase_date = form.purchase_date.data
            module.purchase_price = form.purchase_price.data
            module.notes = form.notes.data
            
            db.session.commit()
            flash(f'Модуль "{module.name}" успішно оновлено!', 'success')
            return redirect(url_for('main.modules'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating module: {e}")
            flash('Помилка при оновленні модуля. Спробуйте ще раз.', 'error')
    
    # Set current weapon_id
    if module.weapon_id:
        form.weapon_id.data = module.weapon_id
    else:
        form.weapon_id.data = 0
    
    return render_template('add_module.html', form=form, module=module)

@bp.route('/module/<int:id>/delete', methods=['POST'])
def delete_module(id):
    """Видалення модуля"""
    module = Module.query.get_or_404(id)
    try:
        name = module.name
        db.session.delete(module)
        db.session.commit()
        flash(f'Модуль "{name}" видалено.', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting module: {e}")
        flash('Помилка при видаленні модуля.', 'error')
    return redirect(url_for('main.modules'))

@bp.route('/module/<int:id>/toggle_used', methods=['POST'])
def toggle_module_used(id):
    """Змінити статус використання модуля"""
    module = Module.query.get_or_404(id)
    try:
        module.is_used = not module.is_used
        db.session.commit()
        status = "використовується" if module.is_used else "не використовується"
        flash(f'Статус модуля "{module.name}" змінено на {status}.', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error toggling module status: {e}")
        flash('Помилка при зміні статусу модуля.', 'error')
    return redirect(url_for('main.modules'))

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('base.html', title='Сторінку не знайдено'), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html', title='Внутрішня помилка сервера'), 500