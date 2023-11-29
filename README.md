# Térháló alkotás 3D LIDAR pontfelhő alapján - Mesh creation based on 3D LIDAR point cloud
<p>
<b>Szakdolgozat téma leírása:</b>
</p>
<p>
A feladat a Széchenyi István Egyetem központi campus 3D modelljének megalkotása LIDAR mérések alapján. Elsődleges szempont, hogy a modell segítséget nyújtson önvezető autók szimulációs feladatai során. Ezért hangsúlyos a mérethelyesség. A modellnek emellett felismerhető részletességűnek kell lennie, de tárhelyigényét tekintve kis mérettel kell rendelkeznie, ezt alacsony poligonszámmal biztosítva.
<p><b>Részfeladatok:</b></p>
<ul>
  <li>Pontfelhő létrehozása LIDAR mérések alapján. Szakirodalmi áttekintés. LIDAR + GPS vagy LIDAR + IMU alapján történő pontfelhő létrehozás vizsgálata. A bemeneti adatokat az egyetem biztosítja rosbag fájlok formájában.</li>
  <li>A létrehozott pontfelhőből mesh (térháló) készítése automatikus és kézi módszerrel.</li>
  <li>A két módszerrel készült mesh összehasonlítása, objektív és szubjektív szempontok alapján (Ajánlott Blender/CloudCompare/Python script)</li>
  <li>A modell feltöltése OpenStreetMap-re, generikus CAD fájl kimenet létrehozása.</li>
</ul>
</p>
<p>
Jelen repository az automatikus módszer kódját tartalmazza. Elsősorban viszonylag sík területek felszíni méréssel készült leképezésének feldolgozására fókuszál.
</p>
<p>
<b>A futtatáshoz szükséges előkészületek és eszközök:</b>
<ul>
  <li>Python 3.10 virtuális környezet</li>
  <li>NumPy</li>
  <li>Open3D</li>
  <li>PyVista</li>
  <li>CUDA kompatibilis GPU</li>
  <li>legalább 8-16 GB RAM</li>
</ul>
</p>
<p>
A kód a futás során szétválasztja a pontfelhőt földi és föld feletti pontokra, majd több tisztítási és zajszűrési lépésen keresztül különálló épületekre bontja a föld feletti ponthalmazt. Ezután Alphashape metódussal és Delaunay-triangulációval létrehozza a térhálót.
</p>
<p>
<b>English version:</b>
</p>
<p>
<b>Description of the thesis:</b>
</p>
<p>
The purpose of the project is to create the 3D mesh of the Széchenyi István University Central Campus, based on LIDAR data. The primary focus is to help in the research of simulating the behaviour of self-driving vehicles. For this reason, dimensional accuracy is important. Apart from this, the model needs to be high resolution enough to be recognizable, however it can't take up too much storage space, therefore its polygon number needs to stay as low as possible.
<p><b>Subtasks:</b></p>
<ul>
  <li>Producing a point cloud based on LIDAR data. Literature review. Research of producing point cloud based on LIDAR + GPS or LIDAR + IMU. The input data is provided by the university in the form of rosbag files.</li>
  <li>Mesh creation from the point cloud, using both manual and automatic tools.</li>
  <li>Comparing the meshes created by the two methods, based on objective and subjective aspects (Recommended: Blender/CloudCompare/Python scrilt)</li>
  <li>Uploading the model to OpenStreetMap, producing generic CAD file output (.obj file)</li>
</ul>
</p>
<p>
This repository contains the code for the automatic method. It is primarily used for processing surface-level measurements of fairly flat and noisy areas.
</p>
<p>
<b>Preparations and tools for running the code:</b>
<ul>
  <li>Python 3.10 virtual environment</li>
  <li>NumPy</li>
  <li>Open3D</li>
  <li>PyVista</li>
  <li>CUDA compatible GPU</li>
  <li>at least 8-16 GB RAM</li>
</ul>
</p>
<p>
During the process, the code separates the ground points from the ponts of the buildings and other objects, then, through multiple cleaning and noise filtering steps, it segments the buildings into clusters. As the final steps, it uses Alphashape and Delaunay-triangulation to create the mesh.
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
