import logging
import random
from sqlalchemy import select, insert, text
from db.tables import truncate_table


def load_cameras(conn, tables, rows: list[dict]) -> None:
    cameras = tables["cameras"]
    truncate_table(conn, "cameras")

    # regions = [r[0] for r in conn.execute(select(tables["regions"].c.id))]
    # models = [r[0] for r in conn.execute(select(tables["camera_models"].c.id))]
    # streams = [r[0] for r in conn.execute(select(tables["stream_servers"].c.id))]
    # units = [r[0] for r in conn.execute(select(tables["units"].c.id))]
    # users = [r[0] for r in conn.execute(select(tables["users"].c.id))]
    #
    # if not all([regions, models, streams, units]):
    #     raise RuntimeError("Недостаточно FK-данных для cameras")
    #
    # for row in rows:
    #     row["region"] = random.choice(regions)
    #     row["model"] = random.choice(models)
    #     row["streamServer"] = random.choice(streams)
    #     row["unit"] = random.choice(units)
    #
    #     if row["locked"] == 1:
    #         row["lockuid"] = random.choice(users)
    #     else:
    #         row["lockuid"] = -1
    #
    #     row["zbxhttpitemid"] = row["zbxicmpitemid"] - 1
    #
    # conn.execute(insert(cameras).values(rows))

    # Вставляем одну запись
    insert_query = text("""
         INSERT INTO `cameras` (
             `uuid`, `id`, `streamName`, `localAddress`, `localMask`, `localGateway`, 
             `name`, `userName`, `password`, `latitude`, `longitude`, `manageUrl`, 
             `deviceIpAddressCamera`, `height`, `locked`, `archiveIdentify`, `maintenance`, 
             `remoteTourServerAddress`, `remoteTourServer`, `ownerInformation`, 
             `zbxicmpitemid`, `zbxhttpitemid`, `operator`, `rtspPort`, `orderIndex`, 
             `state`, `streamInput`, `serialNumber`, `ethernetHardwareType`, 
             `infoMountAddress`, `infoInverter`, `installationDate`, `warrantyPeriod`, 
             `region`, `model`, `streamServer`, `unit`, `lockuid`
         ) VALUES (
             :uuid, :id, :streamName, :localAddress, :localMask, :localGateway,
             :name, :userName, :password, :latitude, :longitude, :manageUrl,
             :deviceIpAddressCamera, :height, :locked, :archiveIdentify, :maintenance,
             :remoteTourServerAddress, :remoteTourServer, :ownerInformation,
             :zbxicmpitemid, :zbxhttpitemid, :operator, :rtspPort, :orderIndex,
             :state, :streamInput, :serialNumber, :ethernetHardwareType,
             :infoMountAddress, :infoInverter, :installationDate, :warrantyPeriod,
             :region, :model, :streamServer, :unit, :lockuid
         )
     """)

    row = {
        "uuid": "403742e4-b29f-4954-9c58-794903d3c1f4",
        "id": 1165,
        "streamName": "RU.01.1165",
        "localAddress": "192.168.201.249",
        "localMask": "",
        "localGateway": "192.168.0.1",
        "name": "Стенд - низ - Тесно",
        "userName": "iraida20",
        "password": "hor9LyJM$5",
        "latitude": 56.767367444288,
        "longitude": 33.349603931413,
        "manageUrl": "http://192.168.201.249:487",
        "deviceIpAddressCamera": "",
        "height": 24,
        "locked": 0,
        "archiveIdentify": "RU.01.1165",
        "maintenance": 0,
        "remoteTourServerAddress": "",
        "remoteTourServer": 0,
        "ownerInformation": "Солнце увеличиваться песня факультет способ остановить экзамен.",
        "zbxicmpitemid": 38621,
        "zbxhttpitemid": 38620,
        "operator": 1,
        "rtspPort": "487",
        "orderIndex": 0,
        "state": 1,
        "streamInput": "rtsp://iraida20:hor9LyJM$5@192.168.201.249:487/axis-media/media.amp",
        "serialNumber": "",
        "ethernetHardwareType": 0,
        "infoMountAddress": "д. Пушкинские Горы, алл. Линейная, д. 277, 417253",
        "infoInverter": 0,
        "installationDate": "2025-10-22",
        "warrantyPeriod": "2026-05-25",
        "region": 1,
        "model": 6,
        "streamServer": 1,
        "unit": 2,
        "lockuid": -1
    }

    conn.execute(insert_query, row)
    logging.info(f"Таблица cameras заполнена тестовыми данными в количестве {len(rows)} шт.")
