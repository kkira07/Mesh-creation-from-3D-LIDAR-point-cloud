# Térháló alkotás 3D LIDAR pontfelhő alapján
<p>
<b>Leírás:</b>
A feladat a Széchenyi István Egyetem központi campus 3D modelljének megalkotása LIDAR mérések alapján. Elsődleges szempont, hogy a modell segítséget nyújtson önvezető autók szimulációs feladatai során. Ezért hangsúlyos a mérethelyesség. A modellnek emellett felismerhető részletességűnek kell lennie, de tárhelyigényét tekintve kis mérettel kell rendelkeznie, ezt alacsony poligonszámmal biztosítva.
Részfeladatok:
- Pontfelhő létrehozása LIDAR mérések alapján. Szakirodalmi áttekintés. LIDAR + GPS vagy LIDAR + IMU alapján történő pontfelhő létrehozás vizsgálata. A bemeneti adatokat az egyetem biztosítja rosbag fájlok formájában.
- A létrehozott pontfelhőből mesh (térháló) készítése automatikus és kézi módszerrel.
- A két módszerrel készült mesh összehasonlítása, objektív és szubjektív szempontok alapján (Ajánlott Blender/CloudCompare/Python script)
- A modell feltöltése OpenStreetMap-re, generikus CAD fájl kimenet létrehozása.
</p>
<p>
Jelen repository az automatikus módszer kódját tartalmazza. Elsősorban viszonylag sík területek felszíni méréssel készült leképezésének feldolgozására fókuszál.
<b>A futtatáshoz szükséges előkészületek és eszközök:</b>
- Python 3.10 virtuális környezet
- NumPy
- Open3D
- PyVista
- CUDA kompatibilis GPU
- legalább 8-16GB RAM
</p>
A kód a futás során szétválasztja a pontfelhőt földi és föld feletti pontokra, majd több tisztítási és zajszűrési lépésen keresztül különálló épületekre bontja a föld feletti ponthalmazt. Ezután Alphashape metódussal és Delaunay-triangulációval létrehozza a térhálót.
<p>
<b>English version:</b>
</p>


<p align="center">
<img src="https://github.com/kkira07/Szakdolgozat/blob/main/output/separation.png?raw=true" width="400" height="240" alt="Separation of ground points and buildings">
<img src="https://github.com/kkira07/Szakdolgozat/blob/main/output/segmentation.png?raw=true" width="400" height="240" alt="Building segmentation">
</p>
<p align="center">
Separation of ground and buildings (left), and building segmentation (right).
</p>
<p>
<b>Results:</b>
</p>
<p align="center">
<img src="https://github.com/kkira07/Szakdolgozat/blob/main/output/cloud.png?raw=true" width="400" height="240" alt="The original point cloud">
<img src="https://github.com/kkira07/Szakdolgozat/blob/main/output/handmade_model.png?raw=true" width="400" height="240" alt="Handmade model">
<img src="https://github.com/kkira07/Szakdolgozat/blob/main/output/code_model.png?raw=true" width="600" height="360" alt="Model produced by the code">
</p>
<p align="center">
The original point cloud (upper left), the model made by hand in Blender (upper right), and the model produced by this code (bottom).
</p>
