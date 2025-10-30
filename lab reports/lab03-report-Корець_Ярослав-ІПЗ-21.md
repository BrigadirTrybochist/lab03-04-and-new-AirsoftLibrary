# Звіт з лабораторної роботи 3

## Розробка базового вебпроєкту

### Інформація про команду
- Назва команди: Ті самі "Програмісти"

- Учасники:
  - Корець Ярослав - Робота з базою данних
  - Антонюк Андрій - Створення основи для вебзастосунку
  - Терещук Дмитро - Візуал та робота над ХТМЛ

## Завдання
Створення веб-застосунок на Flask(Python)

### Обрана предметна область

Онлайн бібліотека airsoft зброї та її редагування і список модулів до неї

### Реалізовані вимоги

Вкажіть, які рівні завдань було виконано:

- [+] Рівень 1: Створено сторінки "Головна" та "Про нас"
- [+-] Рівень 2: Додано мінімум дві додаткові статичні сторінки з меню та адаптивною версткою

## Хід виконання роботи
Обговорення ідей щодо застосунку, поділ ролей, напис коду за допомогою інших ресурсів + ШІ. Спочатку створили основу для роботи а потім оформили візуал та БД

### Підготовка середовища розробки

Опишіть процес встановлення та налаштування:

- Версія Python 3.14
- Встановлення Flask
- Інші використані інструменти: VS Code (прога де писали код), JS, HTML

### Структура проєкту

Наведіть структуру файлів та директорій вашого проєкту:

```
lab03-04-and-new-AirsoftLibrary/
├── app.py
├── apps.py
├── forms.py
├── models.py
├── routes.py
├── README.md
├── templates/
│   ├── add_weapon.html
│   ├── base.html
│   ├── index.html
│   ├── modules.html
|   ├── stats_widget.html
|   ├── weapon_detail.html
|   └── weapons.html
├── instances/
│   ├── airsoft_collection.db/
├── _pycache_
|   ├── app.cpython-314.pyc
|   ├── forms.cpython-314.pyc
|   ├── models.cpython-314.pyc
|   └── routes.cpython-314.pyc
├── static/
|   ├── js/
|       ├── main.js
└── lab-reports/
    └── ...
```

### Опис реалізованих сторінок

#### Головна сторінка

Перегляд арсеналу зброї, модулів та їх ціни

#### Додаткові сторінки (якщо реалізовано)

#### Сторінка редагування

Зміна інформації про предмет

#### Сторінка Детального перегляду

Перегляд ПОВНОЇ інформації зброї

## Ключові фрагменти коду

### Маршрутизація в Flask

Наведіть приклад налаштування маршрутів у файлі `app.py`:

```python
@app.route('/')
def index():
    """Головна сторінка з меню вибору"""
    stats = get_collection_stats()
    return render_template('index.html', stats=stats)

@app.route('/weapon/<int:id>', methods=['GET'])
def weapon_detail(id):
    """Детальна сторінка зброї"""
    weapon = Weapon.query.get_or_404(id)
    return render_template('weapon_detail.html', weapon=weapon)

@app.route('/add_weapon', methods=['GET', 'POST'])
def add_weapon():
    """Додавання нової зброї"""
    form = WeaponForm()
    if form.validate_on_submit():
        weapon = Weapon(
            name=form.name.data,
            brand=form.brand.data,
            model=form.model.data
        )
        db.session.add(weapon)
        db.session.commit()
        flash(f'Зброю "{weapon.name}" успішно додано!', 'success')
        return redirect(url_for('index'))
    return render_template('add_weapon.html', form=form)
```

### Базовий шаблон

Наведіть фрагмент базового шаблону `base.html`:

```html
<!DOCTYPE html>
<html lang="uk" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Колекція страйкбольної зброї{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    <!-- Font Awesome Icons -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <style>
        .weapon-card {
            transition: transform 0.2s;
        }
        .weapon-card:hover {
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <i class="fas fa-crosshairs me-2"></i>
                Колекція страйкболу
            </a>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('index') }}">
                            <i class="fas fa-home me-1"></i>Головна
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('weapons') }}">
                            <i class="fas fa-gun me-1"></i>Зброя
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container mt-4 mb-5">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

## Розподіл обов'язків у команді

Опишіть внесок кожного учасника команди:

- Корець Ярослав: Створення БД
- Антонюк Андрій: Створення основи робочої частини сайту
- Терещук Дмитро: Створення візуальної частини сайту

## Скріншоти

Додайте скріншоти основних сторінок вашого вебзастосунку:

### Головна сторінка

![Головна сторінка] https://drive.google.com/file/d/1yTX-uy7-fpbvFG7Ul1JonTXdRESFWqEk/view?usp=sharing


### Додаткові сторінки

![Додаткова сторінка] https://drive.google.com/drive/folders/1RxidoNMuCAtVjh2-W6WjQRRIpGaCvd54?usp=sharing


### Висновки

Опишіть:

- Що вдалося реалізувати успішно: Головну сторінку, декілька додаткових, базу данних
- З якими труднощами зіткнулися: 
- Які навички та знання отримали: Робота з Flask, JS, HTML
- Які можливості для вдосконалення проєкту бачите: Додавання нових категорій арсеналу АКА броня, гаджети, дрони тощо.

Очікувана оцінка: 9 Балів

Обґрунтування: Хоча й код було написано з допомогою ШІ, ідея була нашою, ми вносили поправки в коді, перевіряли його роботу та зібрали все докупи.
