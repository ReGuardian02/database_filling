import random

# ---- Статичные названия лесничеств ----

FORESTRY_NAMES = [
    "Волоколамское",
    "Дмитровское",
    "Клинское",
    "Московское учебно-опытное",
    "Орехово-Зуевское",
    "Подольское",
    "Шатурское",
    "Наро-Фоминское",
    "Ногинское",
    "Ступинское",
    "Талдомское",
    "Сергиево-Посадское",
    "Бородинское",
    "Русский лес",
    "Егорьевское",
    "Звенигородское",
    "Виноградовское",
    "Истринское",
    "Луховицкое",
    "Лосиный остров",
    "Завидово",
    "Приоксо-Террасный",
    "Костеревское МО",
    "Московское МО",
]

# ---- Генерация WKT MULTIPOLYGON ----

def generate_multipolygon_wkt(center_lat: float, center_lon: float, points: int = 8, radius: float = 0.01) -> str:
    coords = []
    for _ in range(points):
        lat = center_lat + random.uniform(-radius, radius)
        lon = center_lon + random.uniform(-radius, radius)
        coords.append(f"{lon} {lat}")
    coords.append(coords[0])  # замыкаем полигон
    polygon_body = ", ".join(coords)
    return f"MULTIPOLYGON ((({polygon_body})))"

# ---- Генерация набора записей ----

def generate_forestries(count: int) -> list[dict]:
    if count > len(FORESTRY_NAMES):
        raise ValueError(f"count ({count}) не может быть больше количества названий ({len(FORESTRY_NAMES)})")
    if count > 99:
        raise ValueError("count не может быть больше 99 (уникальные code_lv)")

    selected_names = FORESTRY_NAMES[:count]
    code_lvs = random.sample(range(1, 100), k=count)

    rows = []
    for name, lv in zip(selected_names, code_lvs):
        code_lv = f"{lv:02d}"
        code_oiv = "016"
        code = f"{code_oiv}{code_lv}"
        center_lat = random.uniform(54.0, 60.0)
        center_lon = random.uniform(30.0, 40.0)
        rows.append({
            "name": name,
            "code": code,
            "code_lv": code_lv,
            "code_oiv": code_oiv,
            "polygon": generate_multipolygon_wkt(center_lat, center_lon),
        })
    return rows
