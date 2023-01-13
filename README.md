# Térháló alkotás 3D LIDAR pontfelhő alapján

**Leírás:**
A feladat a Széchenyi István Egyetem központi campus 3D modelljének megalkotása LIDAR mérések alapján. Elsődleges szempont, hogy a modell segítséget nyújtson önvezető autók szimulációs feladatai során. Ezért hangsúlyos a mérethelyesség. A modellnek emellett felismerhető részletességűnek kell lennie, de tárhelyigényét tekintve kis mérettel kell rendelkeznie, ezt alacsony poligonszámmal biztosítva.
Részfeladatok:
- Pontfelhő létrehozása LIDAR mérések alapján. Szakirodalmi áttekintés. LIDAR + GPS vagy LIDAR + IMU alapján történő pontfelhő létrehozás vizsgálata. A bemeneti adatokat az egyetem biztosítja rosbag fájlok formájában.
- A létrehozott pontfelhőből mesh (térháló) készítése automatikus és kézi módszerrel.
- A két módszerrel készült mesh összehasonlítása, objektív és szubjektív szempontok alapján (Ajánlott Blender/CloudCompare/Python script)
- A modell feltöltése OpenStreetMap-re, generikus CAD fájl kimenet létrehozása.

A szakdolgozat elkészítéséhez segédletnek létrehozott státusztábla és a hozzá kapcsolódó források:
https://docs.google.com/spreadsheets/d/1eU2DpAmq5Aa4l-W5WdOUBwwwMSZWgDM9zuSsYl-_ekU/edit#gid=0
