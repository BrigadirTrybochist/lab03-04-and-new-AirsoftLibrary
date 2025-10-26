from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Weapon, Module
from forms import WeaponForm, ModuleForm
from sqlalchemy import func
import logging

@app.route('/')
def index():
    """Головна сторінка з меню вибору"""
    stats = get_collection_stats()
    return render_template('index.html', stats=stats)

@app.route('/weapon/<int:id>')
def weapon_detail(id):
    """Детальна сторінка зброї"""
    weapon = Weapon.query.get_or_404(id)
    return render_template('weapon_detail.html', weapon=weapon)

@app.route('/add_weapon', methods=['GET', 'POST'])
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
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding weapon: {e}")
            flash('Помилка при додаванні зброї. Спробуйте ще раз.', 'error')
    
    return render_template('add_weapon.html', form=form)

@app.route('/edit_weapon/<int:id>', methods=['GET', 'POST'])
def edit_weapon(id):
    """Редагування зброї"""
    weapon = Weapon.query.get_or_404(id)
    form = WeaponForm(obj=weapon)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(weapon)
            db.session.commit()
            flash(f'Зброю "{weapon.name}" успішно оновлено!', 'success')
            return redirect(url_for('weapon_detail', id=weapon.id))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating weapon: {e}")
            flash('Помилка при оновленні зброї. Спробуйте ще раз.', 'error')
    
    return render_template('add_weapon.html', form=form, weapon=weapon)

@app.route('/delete_weapon/<int:id>', methods=['POST'])
def delete_weapon(id):
    """Видалення зброї"""
    weapon = Weapon.query.get_or_404(id)
    try:
        weapon_name = weapon.name
        db.session.delete(weapon)
        db.session.commit()
        flash(f'Зброю "{weapon_name}" видалено з колекції.', 'info')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting weapon: {e}")
        flash('Помилка при видаленні зброї. Спробуйте ще раз.', 'error')
    
    return redirect(url_for('index'))

@app.route('/toggle_weapon_tuned/<int:id>', methods=['POST'])
def toggle_weapon_tuned(id):
    """Перемикання статусу налагодження зброї"""
    weapon = Weapon.query.get_or_404(id)
    try:
        weapon.is_tuned = not weapon.is_tuned
        db.session.commit()
        status = "налагоджена" if weapon.is_tuned else "не налагоджена"
        flash(f'Зброю "{weapon.name}" позначено як {status}.', 'info')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error toggling weapon tuned status: {e}")
        flash('Помилка при оновленні статусу. Спробуйте ще раз.', 'error')
    
    return redirect(request.referrer or url_for('index'))

@app.route('/modules')
def modules():
    """Сторінка зі списком модулів з фільтрами"""
    sort_by = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    
    # Валідні поля для сортування
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

@app.route('/add_module', methods=['GET', 'POST'])
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
            return redirect(url_for('modules'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding module: {e}")
            flash('Помилка при додаванні модуля. Спробуйте ще раз.', 'error')
    
    return render_template('add_module.html', form=form)

@app.route('/edit_module/<int:id>', methods=['GET', 'POST'])
def edit_module(id):
    """Редагування модуля"""
    module = Module.query.get_or_404(id)
    form = ModuleForm(obj=module)
    
    # Populate weapon choices
    weapons = Weapon.query.all()
    form.weapon_id.choices = [(0, 'Не прикріплено')] + [(w.id, f"{w.brand} {w.model}") for w in weapons]
    
    if not form.weapon_id.data:
        form.weapon_id.data = 0
    
    if form.validate_on_submit():
        try:
            weapon_id = form.weapon_id.data if form.weapon_id.data != 0 else None
            form.populate_obj(module)
            module.weapon_id = weapon_id
            db.session.commit()
            flash(f'Модуль "{module.name}" успішно оновлено!', 'success')
            return redirect(url_for('modules'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating module: {e}")
            flash('Помилка при оновленні модуля. Спробуйте ще раз.', 'error')
    
    return render_template('add_module.html', form=form, module=module)

@app.route('/delete_module/<int:id>', methods=['POST'])
def delete_module(id):
    """Видалення модуля"""
    module = Module.query.get_or_404(id)
    try:
        module_name = module.name
        db.session.delete(module)
        db.session.commit()
        flash(f'Модуль "{module_name}" видалено.', 'info')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting module: {e}")
        flash('Помилка при видаленні модуля. Спробуйте ще раз.', 'error')
    
    return redirect(url_for('modules'))

@app.route('/toggle_module_used/<int:id>', methods=['POST'])
def toggle_module_used(id):
    """Перемикання статусу використання модуля"""
    module = Module.query.get_or_404(id)
    try:
        module.is_used = not module.is_used
        db.session.commit()
        status = "використовується" if module.is_used else "не використовується"
        flash(f'Модуль "{module.name}" позначено як {status}.', 'info')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error toggling module used status: {e}")
        flash('Помилка при оновленні статусу. Спробуйте ще раз.', 'error')
    
    return redirect(request.referrer or url_for('modules'))

# API Endpoints
@app.route('/api/weapons', methods=['GET'])
def api_get_weapons():
    """API: Отримання списку всієї зброї"""
    weapons = Weapon.query.all()
    return jsonify([{
        'id': w.id,
        'name': w.name,
        'brand': w.brand,
        'model': w.model,
        'weapon_type': w.weapon_type,
        'fps': w.fps,
        'joules': w.joules,
        'is_tuned': w.is_tuned,
        'purchase_date': w.purchase_date.isoformat() if w.purchase_date else None,
        'purchase_price': w.purchase_price,
        'notes': w.notes,
        'created_at': w.created_at.isoformat(),
        'modules_count': len(w.modules)
    } for w in weapons])

@app.route('/api/weapons/<int:id>', methods=['GET'])
def api_get_weapon(id):
    """API: Отримання деталей зброї"""
    weapon = Weapon.query.get_or_404(id)
    return jsonify({
        'id': weapon.id,
        'name': weapon.name,
        'brand': weapon.brand,
        'model': weapon.model,
        'weapon_type': weapon.weapon_type,
        'fps': weapon.fps,
        'joules': weapon.joules,
        'is_tuned': weapon.is_tuned,
        'purchase_date': weapon.purchase_date.isoformat() if weapon.purchase_date else None,
        'purchase_price': weapon.purchase_price,
        'notes': weapon.notes,
        'created_at': weapon.created_at.isoformat(),
        'modules': [{
            'id': m.id,
            'name': m.name,
            'module_type': m.module_type,
            'brand': m.brand,
            'is_used': m.is_used
        } for m in weapon.modules]
    })

@app.route('/api/modules', methods=['GET'])
def api_get_modules():
    """API: Отримання списку всіх модулів"""
    modules = Module.query.all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'module_type': m.module_type,
        'brand': m.brand,
        'is_used': m.is_used,
        'weapon_id': m.weapon_id,
        'weapon_name': f"{m.weapon.brand} {m.weapon.model}" if m.weapon else None,
        'purchase_date': m.purchase_date.isoformat() if m.purchase_date else None,
        'purchase_price': m.purchase_price,
        'notes': m.notes,
        'created_at': m.created_at.isoformat()
    } for m in modules])

@app.route('/api/modules/<int:id>', methods=['GET'])
def api_get_module(id):
    """API: Отримання деталей модуля"""
    module = Module.query.get_or_404(id)
    return jsonify({
        'id': module.id,
        'name': module.name,
        'module_type': module.module_type,
        'brand': module.brand,
        'is_used': module.is_used,
        'weapon_id': module.weapon_id,
        'weapon_name': f"{module.weapon.brand} {module.weapon.model}" if module.weapon else None,
        'purchase_date': module.purchase_date.isoformat() if module.purchase_date else None,
        'purchase_price': module.purchase_price,
        'notes': module.notes,
        'created_at': module.created_at.isoformat()
    })

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

@app.route('/weapons')
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

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html', title='Сторінку не знайдено'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html', title='Внутрішня помилка сервера'), 500
