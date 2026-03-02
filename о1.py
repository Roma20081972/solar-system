import tkinter as tk
from tkinter import ttk
import math
from PIL import Image, ImageTk, ImageDraw
import os
import random
from datetime import datetime


class SolarSystemSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("СОЛНЕЧНАЯ СИСТЕМА - КОСМИЧЕСКИЙ СИМУЛЯТОР")
        self.root.geometry("1400x900")

        # Настройка стиля
        self.setup_styles()

        # Основные параметры
        self.AU = 149.6e6  # Астрономическая единица в км
        self.SCALE = 3  # Масштаб отображения
        self.center_x = 700
        self.center_y = 400
        self.time = 0
        self.time_scale = 1.0
        self.target_time_scale = 1.0
        self.zoom = 0.4
        self.target_zoom = 0.4
        self.show_orbits = True
        self.show_labels = True
        self.animation_speed = 50  # мс
        self.paused = False

        # Данные планет с расширенной информацией
        self.planets = self.create_planets_data()

        # Изображения
        self.images = {}
        self.hover_images = {}
        self.background_stars = []

        # Загрузка ресурсов
        self.load_images()
        self.generate_stars()
        self.setup_ui()
        self.animate()

    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TScale", background='#2a2a2a', troughcolor='#444',
                        slidercolor='#ffaa00')
        style.configure("TButton", background='#444', foreground='white',
                        borderwidth=0, focuscolor='none')
        style.map("TButton",
                  background=[('active', '#666'), ('pressed', '#333')])

    def create_planets_data(self):
        """Создание расширенных данных о планетах"""
        return [
            {
                "name": "СОЛНЦЕ",
                "dist": 0,
                "size": 109,
                "period": 0,
                "color": "#ffdd00",
                "color2": "#ffaa00",
                "emoji": "☀️",
                "info": "СОЛНЦЕ - ЗВЕЗДА\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                        "📏 РАЗМЕРЫ: Диаметр 1.4 млн км (109× Земли)\n"
                        "⚖️ МАССА: 1.99×10^30 кг (99.8% всей системы)\n"
                        "🌡️ ТЕМПЕРАТУРА: Ядро 15 млн°C, поверхность 5500°C\n"
                        "⏳ ВОЗРАСТ: 4.6 млрд лет\n"
                        "🔬 СОСТАВ: Водород 73%, Гелий 25%\n"
                        "💫 КЛАСС: Желтый карлик G2V\n"
                        "⚡ МОЩНОСТЬ: 3.8×10^26 Вт\n"
                        "🔄 ВРАЩЕНИЕ: 25 дней на экваторе\n"
                        "✨ ФАКТ: Каждую секунду сжигает 4 млн тонн водорода"
            },
            {
                "name": "МЕРКУРИЙ",
                "dist": 0.39,
                "size": 0.38,
                "period": 88,
                "color": "#a5a5a5",
                "color2": "#8a8a8a",
                "emoji": "☿",
                "info": "МЕРКУРИЙ - ПЕРВАЯ ПЛАНЕТА\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                        "📏 ДИАМЕТР: 4879 км (0.38 Земли)\n"
                        "⚖️ МАССА: 3.30×10^23 кг (0.055 от Земли)\n"
                        "🌡️ ТЕМПЕРАТУРА: +430°C днем, -180°C ночью\n"
                        "🪐 РАССТОЯНИЕ: 58 млн км (0.39 AU)\n"
                        "⏳ ГОД: 88 земных дней\n"
                        "⏰ СУТКИ: 59 земных дней\n"
                        "🌪️ АТМОСФЕРА: Почти отсутствует\n"
                        "🛰️ СПУТНИКИ: 0\n"
                        "🏔️ ОСОБЕННОСТЬ: Самый большой перепад температур\n"
                        "✨ ФАКТ: Медленнее всех вращается вокруг оси"
            },
            {
                "name": "ВЕНЕРА",
                "dist": 0.72,
                "size": 0.95,
                "period": 225,
                "color": "#e6b800",
                "color2": "#cc9900",
                "emoji": "♀",
                "info": "ВЕНЕРА - УТРЕННЯЯ ЗВЕЗДА\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                        "📏 ДИАМЕТР: 12104 км (0.95 Земли)\n"
                        "⚖️ МАССА: 4.87×10^24 кг (0.82 от Земли)\n"
                        "🌡️ ТЕМПЕРАТУРА: +470°C (самая горячая планета)\n"
                        "🪐 РАССТОЯНИЕ: 108 млн км (0.72 AU)\n"
                        "⏳ ГОД: 225 дней\n"
                        "⏰ СУТКИ: 243 дня (длиннее года!)\n"
                        "🌪️ АТМОСФЕРА: CO2 96%, давление 90 атм\n"
                        "🛰️ СПУТНИКИ: 0\n"
                        "✨ ФАКТ: Вращается в обратную сторону"
            },
            {
                "name": "ЗЕМЛЯ",
                "dist": 1.0,
                "size": 1.0,
                "period": 365,
                "color": "#4d94ff",
                "color2": "#2d74df",
                "emoji": "🌍",
                "info": "ЗЕМЛЯ - ГОЛУБАЯ ПЛАНЕТА\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                        "📏 ДИАМЕТР: 12742 км (эталон)\n"
                        "⚖️ МАССА: 5.97×10^24 кг\n"
                        "🌡️ ТЕМПЕРАТУРА: Средняя +15°C\n"
                        "🪐 РАССТОЯНИЕ: 150 млн км (1 AU)\n"
                        "⏳ ГОД: 365 дней\n"
                        "⏰ СУТКИ: 24 часа\n"
                        "🌪️ АТМОСФЕРА: N2 78%, O2 21%\n"
                        "🛰️ СПУТНИКИ: 1 (Луна)\n"
                        "🌊 ВОДА: 71% поверхности\n"
                        "✨ ФАКТ: Единственная известная жизнь"
            },
            {
                "name": "МАРС",
                "dist": 1.52,
                "size": 0.53,
                "period": 687,
                "color": "#ff6666",
                "color2": "#cc3333",
                "emoji": "♂",
                "info": "МАРС - КРАСНАЯ ПЛАНЕТА\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                        "📏 ДИАМЕТР: 6779 км (0.53 Земли)\n"
                        "⚖️ МАССА: 6.42×10^23 кг (0.107 от Земли)\n"
                        "🌡️ ТЕМПЕРАТУРА: Средняя -60°C\n"
                        "🪐 РАССТОЯНИЕ: 228 млн км (1.52 AU)\n"
                        "⏳ ГОД: 687 дней\n"
                        "⏰ СУТКИ: 24ч 37мин\n"
                        "🌪️ АТМОСФЕРА: CO2 95%\n"
                        "🛰️ СПУТНИКИ: 2 (Фобос, Деймос)\n"
                        "🏔️ ВУЛКАН: Олимп (27 км высота)\n"
                        "✨ ФАКТ: Красный цвет из-за оксида железа"
            },
            {
                "name": "ЮПИТЕР",
                "dist": 5.2,
                "size": 11.2,
                "period": 4333,
                "color": "#d2b48c",
                "color2": "#b89470",
                "emoji": "♃",
                "info": "ЮПИТЕР - ЦАРЬ ПЛАНЕТ\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                        "📏 ДИАМЕТР: 139820 км (11.2× Земли)\n"
                        "⚖️ МАССА: 1.90×10^27 кг (318× Земли)\n"
                        "🌡️ ТЕМПЕРАТУРА: -110°C\n"
                        "🪐 РАССТОЯНИЕ: 778 млн км (5.2 AU)\n"
                        "⏳ ГОД: 11.9 лет\n"
                        "⏰ СУТКИ: 9.9 часа\n"
                        "🌪️ АТМОСФЕРА: H2 90%, He 10%\n"
                        "🛰️ СПУТНИКИ: 79\n"
                        "🎯 ПЯТНО: Шторм размером 3× Земли\n"
                        "✨ ФАКТ: Мог стать звездой"
            },
            {
                "name": "САТУРН",
                "dist": 9.5,
                "size": 9.5,
                "period": 10759,
                "color": "#f0e68c",
                "color2": "#ddd06a",
                "emoji": "♄",
                "rings": True,
                "info": "САТУРН - ВЛАСТЕЛИН КОЛЕЦ\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                        "📏 ДИАМЕТР: 116460 км (9.5× Земли)\n"
                        "⚖️ МАССА: 5.68×10^26 кг (95× Земли)\n"
                        "🌡️ ТЕМПЕРАТУРА: -140°C\n"
                        "🪐 РАССТОЯНИЕ: 1.4 млрд км (9.5 AU)\n"
                        "⏳ ГОД: 29.5 лет\n"
                        "⏰ СУТКИ: 10.7 часа\n"
                        "💫 КОЛЬЦА: Ширина 300 тыс км, толщина 1 км\n"
                        "🛰️ СПУТНИКИ: 82 (больше всех)\n"
                        "🌊 ПЛОТНОСТЬ: Меньше воды (будет плавать)\n"
                        "✨ ФАКТ: Шестиугольный шторм на полюсе"
            },
            {
                "name": "УРАН",
                "dist": 19.2,
                "size": 4.0,
                "period": 30687,
                "color": "#b0e0e6",
                "color2": "#90c0d6",
                "emoji": "⛢",
                "info": "УРАН - ЛЕЖАЧАЯ ПЛАНЕТА\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                        "📏 ДИАМЕТР: 50724 км (4× Земли)\n"
                        "⚖️ МАССА: 8.68×10^25 кг (14.5× Земли)\n"
                        "🌡️ ТЕМПЕРАТУРА: -224°C (самый холодный)\n"
                        "🪐 РАССТОЯНИЕ: 2.9 млрд км (19.2 AU)\n"
                        "⏳ ГОД: 84 года\n"
                        "⏰ СУТКИ: 17.2 часа\n"
                        "🌀 НАКЛОН: 98° (катится по орбите)\n"
                        "🛰️ СПУТНИКИ: 27\n"
                        "💫 КОЛЬЦА: 13 темных колец\n"
                        "✨ ФАКТ: Полюс 42 года освещен, 42 в темноте"
            },
            {
                "name": "НЕПТУН",
                "dist": 30.1,
                "size": 3.9,
                "period": 60190,
                "color": "#4682b4",
                "color2": "#2d6294",
                "emoji": "♆",
                "info": "НЕПТУН - ВЕТРЕНАЯ ПЛАНЕТА\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                        "📏 ДИАМЕТР: 49244 км (3.9× Земли)\n"
                        "⚖️ МАССА: 1.02×10^26 кг (17× Земли)\n"
                        "🌡️ ТЕМПЕРАТУРА: -220°C\n"
                        "🪐 РАССТОЯНИЕ: 4.5 млрд км (30.1 AU)\n"
                        "⏳ ГОД: 165 лет\n"
                        "⏰ СУТКИ: 16 часов\n"
                        "🌪️ ВЕТЕР: 2100 км/ч (самый сильный)\n"
                        "🛰️ СПУТНИКИ: 14\n"
                        "💫 КОЛЬЦА: 5 тонких колец\n"
                        "✨ ФАКТ: Алмазные дожди в атмосфере"
            }
        ]

    def generate_stars(self, count=300):
        """Генерация фоновых звезд с мерцанием"""
        for _ in range(count):
            self.background_stars.append({
                'x': random.randint(0, 2000),
                'y': random.randint(0, 2000),
                'size': random.uniform(0.5, 2),
                'brightness': random.randint(100, 255),
                'twinkle_speed': random.uniform(0.01, 0.05)
            })

    def load_images(self):
        """Загрузка изображений планет"""
        image_paths = {
            "СОЛНЦЕ": "sun.png",
            "МЕРКУРИЙ": "mercury.png",
            "ВЕНЕРА": "venus.png",
            "ЗЕМЛЯ": "earth.png",
            "МАРС": "mars.png",
            "ЮПИТЕР": "jupiter.png",
            "САТУРН": "saturn.png",
            "УРАН": "uranus.png",
            "НЕПТУН": "neptune.png"
        }

        # Создаем папку для изображений, если её нет
        if not os.path.exists('images'):
            os.makedirs('images')
            self.create_default_images()

        # Загружаем изображения
        for name, path in image_paths.items():
            try:
                if os.path.exists(path):
                    img = Image.open(path)

                    for p in self.planets:
                        if p["name"] == name:
                            # Обычный размер
                            normal_size = int(25 * p["size"])
                            normal_size = max(15, min(120, normal_size))
                            normal_img = img.resize((normal_size, normal_size), Image.Resampling.LANCZOS)
                            self.images[name] = ImageTk.PhotoImage(normal_img)

                            # Увеличенный размер
                            hover_img = img.resize((200, 200), Image.Resampling.LANCZOS)
                            self.hover_images[name] = ImageTk.PhotoImage(hover_img)
                            break
            except Exception as e:
                print(f"Не удалось загрузить {path}: {e}")

    def create_default_images(self):
        """Создание изображений по умолчанию, если файлы не найдены"""
        for planet in self.planets:
            img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Рисуем планету
            center = 100
            radius = 80
            draw.ellipse((center - radius, center - radius, center + radius, center + radius),
                         fill=planet["color"], outline='white', width=2)

            # Добавляем детали
            if planet["name"] == "САТУРН":
                draw.ellipse((center - 120, center - 20, center + 120, center + 20),
                             outline='#aaa', width=3)
            elif planet["name"] == "ЮПИТЕР":
                draw.arc((center - 70, center - 70, center + 70, center + 70),
                         0, 180, fill='#8B4513', width=5)

            # Сохраняем
            img.save(f'images/{planet["name"].lower()}.png')

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Холст для планет
        canvas_frame = tk.Frame(main_frame, bg='black')
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg='black', highlightthickness=0, cursor='cross')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Панель информации
        self.create_info_panel(main_frame)

        # Панель управления
        self.create_control_panel()

        # Привязка событий
        self.setup_bindings()

    def create_info_panel(self, parent):
        """Создание панели информации"""
        info_panel = tk.Frame(parent, bg='#1a1a1a', width=400, relief=tk.RAISED, bd=1)
        info_panel.pack(side=tk.RIGHT, fill=tk.Y)
        info_panel.pack_propagate(False)

        # Заголовок с текущим временем
        title_frame = tk.Frame(info_panel, bg='#1a1a1a')
        title_frame.pack(fill=tk.X, pady=10)

        tk.Label(title_frame, text="🪐 ИНФОРМАЦИЯ", fg='#ffaa00',
                 bg='#1a1a1a', font=('Arial', 16, 'bold')).pack()

        self.time_label = tk.Label(title_frame, text="", fg='#88ccff',
                                   bg='#1a1a1a', font=('Arial', 10))
        self.time_label.pack()

        # Изображение планеты
        self.create_image_display(info_panel)

        # Текст информации
        self.create_text_display(info_panel)

    def create_image_display(self, parent):
        """Создание области для изображения планеты"""
        self.image_frame = tk.Frame(parent, bg='#2a2a2a', height=220,
                                    relief=tk.SUNKEN, bd=1)
        self.image_frame.pack(fill=tk.X, padx=10, pady=5)
        self.image_frame.pack_propagate(False)

        self.planet_image_label = tk.Label(self.image_frame, bg='#2a2a2a')
        self.planet_image_label.pack(expand=True)

    def create_text_display(self, parent):
        """Создание текстовой области с прокруткой"""
        text_frame = tk.Frame(parent, bg='#1a1a1a')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Добавляем поиск
        search_frame = tk.Frame(text_frame, bg='#1a1a1a')
        search_frame.pack(fill=tk.X, pady=(0, 5))

        tk.Label(search_frame, text="🔍 Поиск:", fg='#aaa',
                 bg='#1a1a1a').pack(side=tk.LEFT)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_planets)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                bg='#333', fg='white', insertbackground='white')
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Текстовое поле
        text_container = tk.Frame(text_frame, bg='#1a1a1a')
        text_container.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.info_text = tk.Text(text_container,
                                 yscrollcommand=scrollbar.set,
                                 bg='#2a2a2a', fg='white',
                                 font=('Consolas', 10),
                                 wrap=tk.WORD, bd=0, padx=10, pady=10)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.info_text.yview)
        self.show_welcome_message()

    def create_control_panel(self):
        """Создание панели управления"""
        control = tk.Frame(self.root, bg='#2a2a2a', height=120)
        control.pack(fill=tk.X, side=tk.BOTTOM)
        control.pack_propagate(False)

        # Верхняя линия с ползунками
        self.create_sliders(control)

        # Нижняя линия с кнопками
        self.create_buttons(control)

        # Статус бар
        self.create_status_bar(control)

    def create_sliders(self, parent):
        """Создание ползунков управления"""
        sliders_frame = tk.Frame(parent, bg='#2a2a2a')
        sliders_frame.pack(fill=tk.X, padx=20, pady=5)

        # Скорость
        speed_frame = tk.Frame(sliders_frame, bg='#2a2a2a')
        speed_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(speed_frame, text="⚡ СКОРОСТЬ", fg='#ffaa00',
                 bg='#2a2a2a', font=('Arial', 9, 'bold')).pack()

        speed_controls = tk.Frame(speed_frame, bg='#2a2a2a')
        speed_controls.pack()

        tk.Button(speed_controls, text="−", command=lambda: self.adjust_speed(-0.5),
                  bg='#444', fg='white', width=2).pack(side=tk.LEFT)

        self.speed_var = tk.DoubleVar(value=1.0)
        speed_slider = ttk.Scale(speed_controls, from_=0.1, to=100,
                                 variable=self.speed_var,
                                 orient=tk.HORIZONTAL,
                                 command=self.update_speed,
                                 length=150)
        speed_slider.pack(side=tk.LEFT, padx=5)

        tk.Button(speed_controls, text="+", command=lambda: self.adjust_speed(0.5),
                  bg='#444', fg='white', width=2).pack(side=tk.LEFT)

        self.speed_label = tk.Label(speed_frame, text="1.0x", fg='#ffaa00',
                                    bg='#2a2a2a', font=('Arial', 10, 'bold'))
        self.speed_label.pack()

        # Масштаб
        zoom_frame = tk.Frame(sliders_frame, bg='#2a2a2a')
        zoom_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(zoom_frame, text="🔍 МАСШТАБ", fg='#00ccff',
                 bg='#2a2a2a', font=('Arial', 9, 'bold')).pack()

        zoom_controls = tk.Frame(zoom_frame, bg='#2a2a2a')
        zoom_controls.pack()

        tk.Button(zoom_controls, text="−", command=lambda: self.adjust_zoom(-0.1),
                  bg='#444', fg='white', width=2).pack(side=tk.LEFT)

        self.zoom_var = tk.DoubleVar(value=0.4)
        zoom_slider = ttk.Scale(zoom_controls, from_=0.1, to=2.0,
                                variable=self.zoom_var,
                                orient=tk.HORIZONTAL,
                                command=self.update_zoom,
                                length=150)
        zoom_slider.pack(side=tk.LEFT, padx=5)

        tk.Button(zoom_controls, text="+", command=lambda: self.adjust_zoom(0.1),
                  bg='#444', fg='white', width=2).pack(side=tk.LEFT)

        self.zoom_label = tk.Label(zoom_frame, text="40%", fg='#00ccff',
                                   bg='#2a2a2a', font=('Arial', 10, 'bold'))
        self.zoom_label.pack()

    def create_buttons(self, parent):
        """Создание кнопок управления"""
        buttons_frame = tk.Frame(parent, bg='#2a2a2a')
        buttons_frame.pack(pady=5)

        buttons = [
            ("⏯ ПАУЗА", self.toggle_pause),
            ("🌌 ВСЯ СИСТЕМА", self.fit_all),
            ("🔄 СБРОС", self.reset_view),
            ("🛸 ЦЕНТРИРОВАТЬ", self.center_view),
            ("📡 ОРБИТЫ", self.toggle_orbits),
            ("🏷 МЕТКИ", self.toggle_labels)
        ]

        for text, command in buttons:
            btn = tk.Button(buttons_frame, text=text, command=command,
                            bg='#444', fg='white', font=('Arial', 9),
                            padx=10, relief=tk.RAISED, bd=1)
            btn.pack(side=tk.LEFT, padx=2)

            # Эффект наведения
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#666'))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#444'))

    def create_status_bar(self, parent):
        """Создание строки состояния"""
        self.status_bar = tk.Frame(parent, bg='#1a1a1a', height=20)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(self.status_bar, bg='#1a1a1a',
                                     fg='#aaa', font=('Arial', 8))
        self.status_label.pack(side=tk.LEFT, padx=10)

    def setup_bindings(self):
        """Настройка привязок событий"""
        self.canvas.bind("<ButtonPress-1>", self.pan_start)
        self.canvas.bind("<B1-Motion>", self.pan_move)
        self.canvas.bind("<MouseWheel>", self.wheel_zoom)
        self.canvas.bind("<Motion>", self.mouse_move)
        self.canvas.bind("<Configure>", self.on_resize)

        # Горячие клавиши
        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("<Key-plus>", lambda e: self.adjust_zoom(0.1))
        self.root.bind("<Key-minus>", lambda e: self.adjust_zoom(-0.1))
        self.root.bind("<r>", lambda e: self.reset_view())
        self.root.bind("<f>", lambda e: self.fit_all())
        self.root.bind("<o>", lambda e: self.toggle_orbits())
        self.root.bind("<l>", lambda e: self.toggle_labels())

        self.pan_start_x = 0
        self.pan_start_y = 0

    def adjust_speed(self, delta):
        """Регулировка скорости"""
        new_speed = self.speed_var.get() + delta
        if 0.1 <= new_speed <= 100:
            self.speed_var.set(new_speed)
            self.update_speed(None)

    def adjust_zoom(self, delta):
        """Регулировка масштаба"""
        new_zoom = self.zoom_var.get() + delta
        if 0.1 <= new_zoom <= 2.0:
            self.zoom_var.set(new_zoom)
            self.update_zoom(None)

    def toggle_pause(self):
        """Пауза/возобновление анимации"""
        self.paused = not self.paused
        self.update_status()

    def toggle_orbits(self):
        """Включение/выключение отображения орбит"""
        self.show_orbits = not self.show_orbits
        self.update_status()

    def toggle_labels(self):
        """Включение/выключение отображения меток"""
        self.show_labels = not self.show_labels
        self.update_status()

    def center_view(self):
        """Центрирование вида на Солнце"""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.center_x = w // 2
        self.center_y = h // 2

    def update_status(self):
        """Обновление строки состояния"""
        status = f"Скорость: {self.time_scale:.1f}x | "
        status += f"Масштаб: {self.zoom * 100:.0f}% | "
        status += f"Орбиты: {'✓' if self.show_orbits else '✗'} | "
        status += f"Метки: {'✓' if self.show_labels else '✗'} | "
        status += f"Пауза: {'✓' if self.paused else '✗'}"
        self.status_label.config(text=status)

    def update_speed(self, e):
        """Обновление скорости"""
        self.target_time_scale = self.speed_var.get()
        self.speed_label.config(text=f"{self.target_time_scale:.1f}x")
        self.update_status()

    def update_zoom(self, e):
        """Обновление масштаба"""
        self.target_zoom = self.zoom_var.get()
        self.zoom_label.config(text=f"{int(self.target_zoom * 100)}%")
        self.update_status()

    def fit_all(self):
        """Подгонка масштаба под всю систему"""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w > 1 and h > 1:
            max_dist = max(p["dist"] for p in self.planets if p["dist"] > 0)
            new_zoom = (min(w, h) * 0.4) / (max_dist * self.AU / 1e6 * self.SCALE)
            new_zoom = max(0.1, min(2.0, new_zoom))
            self.zoom_var.set(new_zoom)
            self.update_zoom(None)
            self.center_view()

    def reset_view(self):
        """Сброс вида"""
        self.zoom_var.set(0.4)
        self.update_zoom(None)
        self.center_view()
        self.speed_var.set(1.0)
        self.update_speed(None)

    def on_resize(self, e):
        """Обработка изменения размера окна"""
        if not hasattr(self, '_resize_delay'):
            self.center_view()

    def pan_start(self, e):
        """Начало перемещения"""
        self.pan_start_x = e.x
        self.pan_start_y = e.y
        self.canvas.config(cursor='fleur')

    def pan_move(self, e):
        """Перемещение вида"""
        dx = e.x - self.pan_start_x
        dy = e.y - self.pan_start_y
        self.center_x += dx
        self.center_y += dy
        self.pan_start_x = e.x
        self.pan_start_y = e.y

    def wheel_zoom(self, e):
        """Масштабирование колесиком"""
        if e.delta > 0:
            self.zoom_var.set(self.zoom_var.get() * 1.1)
        else:
            self.zoom_var.set(self.zoom_var.get() * 0.9)
        self.update_zoom(None)

    def mouse_move(self, e):
        """Обработка движения мыши"""
        if self.paused:
            return

        x, y = e.x, e.y

        # Проверяем наведение на планеты
        for p in self.planets:
            planet_x, planet_y = self.get_planet_position(p)
            size = self.get_planet_size(p)

            if planet_x is not None:
                distance = math.sqrt((x - planet_x) ** 2 + (y - planet_y) ** 2)
                if distance <= size:
                    self.show_info(p)
                    return

        # Если не навели ни на одну планету
        self.show_info(None)

    def get_planet_position(self, planet):
        """Получение координат планеты"""
        if planet["dist"] == 0:
            return self.center_x, self.center_y

        angle = (self.time / planet["period"]) * 2 * math.pi
        d = planet["dist"] * self.AU / 1e6 * self.SCALE * self.zoom
        x = self.center_x + math.cos(angle) * d
        y = self.center_y + math.sin(angle) * d
        return x, y

    def get_planet_size(self, planet):
        """Получение размера планеты для отображения"""
        if planet["dist"] == 0:
            size = 25 * 109 * self.zoom
            return min(200, size)
        else:
            size = 20 * planet["size"] * self.zoom
            return max(5, min(80, size))

    def search_planets(self, *args):
        """Поиск планет"""
        search_term = self.search_var.get().upper()
        if not search_term:
            self.show_info(None)
            return

        for planet in self.planets:
            if search_term in planet["name"]:
                self.show_info(planet)
                break

    def show_welcome_message(self):
        """Показ приветственного сообщения"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert('1.0',
                              "🌟 ДОБРО ПОЖАЛОВАТЬ В КОСМОС!\n"
                              "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n\n"
                              "🪐 Наведите курсор на планету\n"
                              "📊 Управляйте скоростью и масштабом\n"
                              "🔄 Перемещайте вид мышью\n"
                              "⌨️ Горячие клавиши:\n"
                              "   • Пробел - пауза\n"
                              "   • +/- - масштаб\n"
                              "   • R - сброс вида\n"
                              "   • F - вся система\n"
                              "   • O - орбиты\n"
                              "   • L - метки\n\n"
                              "🚀 Приятного путешествия!")
        self.info_text.config(state=tk.DISABLED)

    def show_info(self, planet):
        """Отображение информации о планете"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete('1.0', tk.END)

        if planet:
            # Показываем изображение
            if planet["name"] in self.hover_images:
                self.planet_image_label.config(image=self.hover_images[planet["name"]])
                self.planet_image_label.image = self.hover_images[planet["name"]]
            else:
                # Создаем изображение планеты
                img = self.create_planet_image(planet)
                self.planet_image_label.config(image=img)
                self.planet_image_label.image = img

            # Показываем информацию
            self.info_text.insert('1.0', planet["info"])

            # Добавляем дополнительную информацию о текущем положении
            if planet["dist"] > 0:
                angle = (self.time / planet["period"]) * 360
                self.info_text.insert(tk.END,
                                      f"\n\n📍 ТЕКУЩЕЕ ПОЛОЖЕНИЕ:\n   Угол: {angle:.1f}°\n")
        else:
            self.planet_image_label.config(image='')
            self.show_welcome_message()

        self.info_text.config(state=tk.DISABLED)
        self.update_time_display()

    def create_planet_image(self, planet):
        """Создание изображения планеты"""
        img_size = 200
        img = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Рисуем планету
        center = img_size // 2
        radius = 80
        draw.ellipse((center - radius, center - radius, center + radius, center + radius),
                     fill=planet["color"], outline='white', width=3)

        # Добавляем детали в зависимости от планеты
        if planet["name"] == "ЮПИТЕР":
            # Полосы Юпитера
            draw.arc((center - 70, center - 60, center + 70, center + 60),
                     0, 180, fill='#8B4513', width=8)
            draw.arc((center - 70, center - 20, center + 70, center + 20),
                     0, 180, fill='#CD853F', width=8)
        elif planet["name"] == "САТУРН":
            # Кольца Сатурна
            draw.ellipse((center - 120, center - 25, center + 120, center + 25),
                         outline='#aaa', width=4)
        elif planet["name"] == "ЗЕМЛЯ":
            # Континенты (упрощенно)
            draw.ellipse((center - 20, center - 30, center + 20, center + 30),
                         fill='#228B22')
            draw.ellipse((center + 20, center - 10, center + 40, center + 10),
                         fill='#228B22')
        elif planet["name"] == "МАРС":
            # Полярные шапки
            draw.ellipse((center - 30, center - 70, center + 30, center - 40),
                         fill='white')
            draw.ellipse((center - 30, center + 40, center + 30, center + 70),
                         fill='white')

        # Добавляем название планеты
        draw.text((center, img_size - 20), planet["name"],
                  fill='white', anchor='mm')

        return ImageTk.PhotoImage(img)

    def update_time_display(self):
        """Обновление отображения времени"""
        years = self.time / 365
        self.time_label.config(text=f"Время: {years:.1f} лет")

    def draw_stars(self, w, h):
        """Отрисовка звезд с мерцанием"""
        for star in self.background_stars:
            # Мерцание звезд
            star['brightness'] += random.uniform(-5, 5)
            star['brightness'] = max(100, min(255, star['brightness']))

            x = (star['x'] + self.center_x * 0.1) % w
            y = (star['y'] + self.center_y * 0.1) % h

            color = f'#{int(star["brightness"]):02x}{int(star["brightness"]):02x}{int(star["brightness"]):02x}'
            self.canvas.create_oval(x, y,
                                    x + star['size'], y + star['size'],
                                    fill=color, outline='')

    def draw(self):
        """Основная функция отрисовки"""
        self.canvas.delete("all")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            return

        # Рисуем звезды
        self.draw_stars(w, h)

        # Рисуем орбиты
        if self.show_orbits:
            self.draw_orbits()

        # Рисуем планеты
        self.draw_planets()

    def draw_orbits(self):
        """Отрисовка орбит планет"""
        for p in self.planets:
            if p["dist"] > 0:
                d = p["dist"] * self.AU / 1e6 * self.SCALE * self.zoom
                # Рисуем орбиту
                self.canvas.create_oval(self.center_x - d, self.center_y - d,
                                        self.center_x + d, self.center_y + d,
                                        outline='#333', width=1, dash=(2, 4))

                # Добавляем метку расстояния
                if self.zoom > 0.3:
                    self.canvas.create_text(self.center_x, self.center_y - d - 15,
                                            text=f"{p['dist']} AU", fill='#555',
                                            font=('Arial', 7))

    def draw_planets(self):
        """Отрисовка планет"""
        for p in self.planets:
            if p["dist"] == 0:
                self.draw_sun(p)
            else:
                self.draw_planet(p)

    def draw_sun(self, sun):
        """Отрисовка Солнца"""
        size = self.get_planet_size(sun)

        if "СОЛНЦЕ" in self.images:
            self.canvas.create_image(self.center_x, self.center_y,
                                     image=self.images["СОЛНЦЕ"])
        else:
            # Рисуем Солнце с короной
            for i in range(15, 0, -1):
                s = size * (1 + i * 0.05)
                alpha = int(100 / i)
                color = f'#ffff{99 - i * 3:02d}'
                self.canvas.create_oval(self.center_x - s, self.center_y - s,
                                        self.center_x + s, self.center_y + s,
                                        fill=color, outline='', stipple='gray50')

        # Добавляем лучи
        for i in range(8):
            angle = i * 45
            x1 = self.center_x + math.cos(math.radians(angle)) * size * 1.2
            y1 = self.center_y + math.sin(math.radians(angle)) * size * 1.2
            x2 = self.center_x + math.cos(math.radians(angle)) * size * 1.5
            y2 = self.center_y + math.sin(math.radians(angle)) * size * 1.5
            self.canvas.create_line(x1, y1, x2, y2, fill='#ffaa00', width=1)

        # Метка
        if self.show_labels:
            self.canvas.create_text(self.center_x, self.center_y - size - 25,
                                    text=f"☀️ {sun['name']}", fill='#ffaa00',
                                    font=('Arial', 10, 'bold'))

    def draw_planet(self, planet):
        """Отрисовка планеты"""
        angle = (self.time / planet["period"]) * 2 * math.pi
        d = planet["dist"] * self.AU / 1e6 * self.SCALE * self.zoom
        x = self.center_x + math.cos(angle) * d
        y = self.center_y + math.sin(angle) * d
        size = self.get_planet_size(planet)

        # Рисуем планету
        if planet["name"] in self.images:
            self.canvas.create_image(x, y, image=self.images[planet["name"]])
        else:
            # Планета с градиентом
            for i in range(5, 0, -1):
                s = size * (1 - i * 0.03)
                self.canvas.create_oval(x - s, y - s, x + s, y + s,
                                        fill=planet["color" if i % 2 else "color2"],
                                        outline='white', width=1)

        # Кольца для Сатурна
        if planet.get("rings"):
            self.canvas.create_oval(x - size * 1.5, y - size / 3,
                                    x + size * 1.5, y + size / 3,
                                    outline='#aaa', width=1, dash=(3, 2))

        # Метка с названием
        if self.show_labels:
            self.canvas.create_text(x, y - size - 15,
                                    text=f"{planet['emoji']} {planet['name']}",
                                    fill='white', font=('Arial', 8))

    def animate(self):
        """Анимация"""
        if not self.paused:
            # Плавное изменение параметров
            self.time_scale += (self.target_time_scale - self.time_scale) * 0.05
            self.zoom += (self.target_zoom - self.zoom) * 0.05
            self.time += self.time_scale * 0.1  # Замедляем время для плавности

        self.draw()
        self.update_time_display()
        self.root.after(self.animation_speed, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = SolarSystemSimulator(root)
    root.mainloop()