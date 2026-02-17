import logging
import os
import random
import hashlib
from sqlalchemy import select
from db.tables import truncate_table


def add_admin(conn, users_table):
    admin_password = hashlib.sha1(os.getenv("STAND_PASSWORD").encode("utf-8")).hexdigest()

    admin_user = {
        "id": 1,
        "unit": 1,
        "name": "admin",
        "password": admin_password,
        "outputName": "Администратор",
        "permissions": 5,
        "language": "ru",
        "blocked": 0,
        "params": """{"basemap":"googleTer","lastPage":"","panel":1,"weather":true,"weather_points":false,"layers":[],"fires":true,"maxicmp":100,"sound":true,"searchPanel":true,"cameraPosition":{"x":10,"y":10},"capabilities":true,"devicecapabilities":true,"gptlservice":false,"thermopoints":false,"mcsfires":false,"mcsburn":false,"meteoeye":false,"archivefires":false,"deforestation":true,"userobjects":true,"filtermap":false,"chatAvailable":true,"chat":false,"chatpos":{"top":50,"left":50},"chatsize":{"width":900,"height":460},"chatCurrentTab":"contacts","sipvideopos":{"top":50,"left":50},"sipvideosize":{"width":500,"height":400},"chatcurrentdialog":"","layersUnAccessible":{"base":[],"user":[]},"userMonitoring":true,"userFires":true,"userTransport":true,"userDeforest":true,"userMapLayers":true,"userExtRights":true,"userExtRightsHours":"","userRightsConfirmed":true,"mediaCollections":true,"currentUserService":"cameras","userRecursions":true,"meteostationslayer":false,"userduty":false,"sectors":true,"balloons":true,"layerRemoteDevices":false,"lightningmaps":false,"layerThermopointsTerra":false,"layerThermopointsAqua":false,"layerThermopointsSNPP":false,"layerThermopointsNOAA":false,"layerFireSafety":false,"airRoutes":{},"groundRoutes":{},"canEditKPO":true,"canEditForestriesKPO":[],"canEditAirbasesKPO":[],"workspace":"/view.php","legendState":[1001,1002,1003,1005,1007,1010,1019],"opticalVisibility":false,"quadrator":16,"filterMapObjectsByForestries":false,"canRemoveEvents":true,"masterplan_button":true,"detection_time_exceeded":0,"fires_isdm":false,"forestriesWithFireClass":false,"meteorological":false,"accessToArchive":false,"accessToReports":false,"telegramFireSummaryNotify":false,"telegramReportNotify":false,"lightingFinder":false,"muted_chats":[],"layerCamsCover":false,"canAccessAnalytics":true,"canAccessWideoWall":true,"coordFormat":0,"camerasPanel":true}""",
        "layoutColumns": 3,
        "layoutRows": 2,
        "close_session": 0,
        "extent": "",
        "allowPrivateMessages": 1,
    }

    conn.execute(users_table.insert().values(admin_user))

def load_users(conn, tables, rows: list[dict]) -> None:
    units = tables["units"]
    users = tables["users"]

    truncate_table(conn, "users")
    add_admin(conn, users)

    unit_ids = [
        r[0]
        for r in conn.execute(
            select(units.c.id)
        ).fetchall()
    ]

    if not unit_ids:
        raise RuntimeError("units пуст — users некуда привязывать")

    for row in rows:
        row["unit"] = random.choice(unit_ids)

    conn.execute(users.insert().values(rows))
    logging.info(f"Таблица users заполнена тестовыми данными в количестве {len(rows)} шт.")
