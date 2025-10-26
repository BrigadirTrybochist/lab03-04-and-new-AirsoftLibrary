from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Optional, NumberRange, Length

class WeaponForm(FlaskForm):
    name = StringField('Назва зброї', validators=[DataRequired(), Length(min=1, max=100)],
                      render_kw={"placeholder": "Наприклад: M4A1 Assault Rifle"})
    brand = StringField('Бренд', validators=[DataRequired(), Length(min=1, max=50)],
                       render_kw={"placeholder": "Наприклад: Tokyo Marui"})
    model = StringField('Модель', validators=[DataRequired(), Length(min=1, max=50)],
                       render_kw={"placeholder": "Наприклад: M4A1 SOPMOD"})
    weapon_type = SelectField('Тип зброї', 
                             choices=[
                                 ('AEG', 'AEG (Automatic Electric Gun)'),
                                 ('GBB', 'GBB (Gas Blow Back)'),
                                 ('GBBR', 'GBBR (Gas Blow Back Rifle)'),
                                 ('Spring', 'Spring (Пружинна)'),
                                 ('HPA', 'HPA (High Pressure Air)'),
                                 ('CO2', 'CO2'),
                                 ('Other', 'Інше')
                             ],
                             validators=[DataRequired()])
    fps = IntegerField('FPS', validators=[Optional(), NumberRange(min=0, max=1000)],
                      render_kw={"placeholder": "Швидкість кулі в футах на секунду"})
    joules = FloatField('Джоулі', validators=[Optional(), NumberRange(min=0, max=10)],
                       render_kw={"placeholder": "Енергія пострілу в джоулях"})
    is_tuned = BooleanField('Налагоджена')
    purchase_date = DateField('Дата придбання', validators=[Optional()])
    purchase_price = FloatField('Ціна придбання (грн)', validators=[Optional(), NumberRange(min=0)],
                               render_kw={"placeholder": "Ціна в гривнях"})
    notes = TextAreaField('Примітки', validators=[Optional(), Length(max=1000)],
                         render_kw={"rows": 4, "placeholder": "Додаткова інформація, модифікації тощо"})

class ModuleForm(FlaskForm):
    name = StringField('Назва модуля', validators=[DataRequired(), Length(min=1, max=100)],
                      render_kw={"placeholder": "Наприклад: Red Dot Sight"})
    module_type = SelectField('Тип модуля',
                             choices=[
                                 ('Optics', 'Оптика'),
                                 ('Grip', 'Рукоятка'),
                                 ('Barrel', 'Ствол'),
                                 ('Stock', 'Приклад'),
                                 ('Silencer', 'Глушник'),
                                 ('Magazine', 'Магазин'),
                                 ('Battery', 'Акумулятор'),
                                 ('Hop-up', 'Hop-up'),
                                 ('Gearbox', 'Редуктор'),
                                 ('Motor', 'Мотор'),
                                 ('Spring', 'Пружина'),
                                 ('BB', 'Кульки'),
                                 ('Accessory', 'Аксесуар'),
                                 ('Other', 'Інше')
                             ],
                             validators=[DataRequired()])
    brand = StringField('Бренд', validators=[Optional(), Length(max=50)],
                       render_kw={"placeholder": "Виробник модуля"})
    is_used = BooleanField('Використовується')
    weapon_id = SelectField('Прикріплено до зброї', coerce=int, validators=[Optional()])
    purchase_date = DateField('Дата придбання', validators=[Optional()])
    purchase_price = FloatField('Ціна придбання (грн)', validators=[Optional(), NumberRange(min=0)],
                               render_kw={"placeholder": "Ціна в гривнях"})
    notes = TextAreaField('Примітки', validators=[Optional(), Length(max=1000)],
                         render_kw={"rows": 3, "placeholder": "Додаткова інформація"})
