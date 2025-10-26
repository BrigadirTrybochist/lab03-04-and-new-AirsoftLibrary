# Звіт з лабораторної роботи 3

## Розробка базового вебпроєкту

### Інформація про команду
- Назва команди: Ті самі "Програмісти"

- Учасники:
  - Антонюк Андрій - Створює основу на чому буде робота
  - Терещук Дмитро - Візуал та робота над ХТМЛ
  - Корець Ярослав - робота з базами данних

## Завдання
Створити веб застосунок на Фласк(Пайтон)
### Обрана предметна область

Опишіть обрану предметну область для вашого вебзастосунку (наприклад: онлайн-бібліотека, каталог товарів, портфоліо, блог тощо).
Онлайн бібліотека airsoft зброї та її редагування і список модулів до неї

### Реалізовані вимоги

Вкажіть, які рівні завдань було виконано:

- [Реалізовано] Рівень 1: Створено Головну сторінку де вказано кількість вашої зброї та модулів а також їх додавання
- [Частково_реалізовано] Рівень 2: Додано в перегляді вашої зброї\модулів редагування\видалення\перегляду

## Хід виконання роботи
Спочатку розбиралися як створити і редагувати. Потім по ходу робили код (з допомогою різних ресурсів та ші) Спочатку створювалися пробні файли але були видалені через помилки та не актуальність. По ходу створили app.py forms.py models і routes. Далі було створенно самі коди ХТМЛ для роботи сайту та база данних де зберігаються створені зброя та модулі.
### Підготовка середовища розробки

Опишіть процес встановлення та налаштування:

Версія пайтон яка була використана 3.14. Фласк встановленно успішно після деяких помилок при встановлені. Також використано програму для створення\редагування VCS Visual Code Studio. Встановлено аддони до вкс на пайтон джава скрипт хтмл і деякі інші.

### Структура проєкту

Наведіть структуру файлів та директорій вашого проєкту:

```
Lab03-flaskProject/
├──__pycache__
    ├── app.cpython-314.pyc
    ├── forms.cpython-314.pyc
    ├── models.cpython-314.pyc
    └── routes.cpython-314.pyc
├── app.py
├── templates/
│   ├── add_weapon.html
│   ├── base.html
│   ├── index.html
│   ├── modules.html
│   ├── stats_widget.html
│   ├── weapon_detail.html
│   └── weapons.html
├── static/
│   └──  js/
        └── main.js
└── lab-reports/
    └── lab03-report-АнтонюкАндрій-ІПЗ-21.md
```

### Опис реалізованих сторінок
Сторінка список зброї\модулів
Сторінка редагування зброї\модулів
Сторінка детального перегляду зброї\модулів
#### Головна сторінка

Перегляд кількості зброї та модулів і перегляд ціни на все це

#### Сторінка Детального перегляду зброї\модулів

перегляд всієї інформації щодо предмету

#### Сторінка Редагування

Редагування деякої інформації про предмет

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

- Антонюк Андрій: створено файли на основі пайтон та подальше редагування для коректної роботи і допомога в редагуванні інших файлів
- Терещук Дмитро: створено файли на основі хтмл та подільше редагування для коректної роботи
- Корець Ярослав: створено файл на основі SQL для зберігання інформації про предмети

## Скріншоти

Додайте скріншоти основних сторінок вашого вебзастосунку:

https://www.reddit.com/user/Master-Priority4609/comments/1ogq4ls/%D0%BD%D0%B5%D0%B4%D0%BE%D0%B3%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D1%96_%D1%81%D0%BA%D1%80%D1%96%D0%BD%D0%B8/
https://www.reddit.com/user/Master-Priority4609/comments/1ogq38h/%D1%81%D0%BA%D1%80%D1%96%D0%BD%D1%88%D0%BE%D1%82%D0%B8_%D0%B4%D0%BB%D1%8F_%D0%B7%D0%B2%D1%96%D1%82%D1%83/

### Висновки

Реалізовано список для перегляду добавленої зброї та модулів. Також їх редагування. Детальний перегляд. Видалення предметів. Встановлення статусу налагодження зброї(інформація чи зброя була обслугована). Також дизайн та сама основа була деколи використана з минулих рабораторних а точніше з першої про створення сайту на репліт. Через сльози та піт були виправлені помилки та створення самого сайту.

Очікувана оцінка: 9 або 11 балів

Обґрунтування: В багатьох моментах було використано допомогу ші але з роз'ясненням. Також за загальне старання над роботою. Надіюсь старання пройшли не просто так. В самому процесі нас зацікавив сам процес роботи, пізнавання нового досвіду думаю покращить подальшу роботу з лабораторними та іншими проєктами
