import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

#definicija ravnina
normala_ravnine = [None, None, None]
tocka_ravnine = [None, None, None]

normala_ravnine[0] = np.array([1, 0, 0])
tocka_ravnine[0] = np.array([60, 0, 0])

normala_ravnine[1] = np.array([1, 0, 0])
tocka_ravnine[1] = np.array([80, 0, 0])

normala_ravnine[2] = np.array([1, 0, 0])
tocka_ravnine[2] = np.array([100, 0, 0])

def presjek_ravnina_trokut(normala_ravnine, tocka_ravnine, vrhovi_trokuta):
    tocke_presjeka = []
    
    for i in range(3):
        #izracun koeficijenata u jednadzbi ravnine
        a, b, c = normala_ravnine
        d = -np.dot(normala_ravnine, tocka_ravnine)

        #izracun presjeka s ravninom
        t = (-d - np.dot(normala_ravnine, vrhovi_trokuta[i])) / np.dot(normala_ravnine, vrhovi_trokuta[(i + 1) % 3] - vrhovi_trokuta[i])
        tocka_presjeka = vrhovi_trokuta[i] + t * (vrhovi_trokuta[(i + 1) % 3] - vrhovi_trokuta[i])

        u = vrhovi_trokuta[(i + 1) % 3] - vrhovi_trokuta[i]
        
        w = tocka_presjeka - vrhovi_trokuta[i]

        #provjera je li tocka presjeka u trokutu
        if np.dot(u,u)>np.dot(w,w):
            tocke_presjeka.append(tocka_presjeka)
    
    return tocke_presjeka if len(tocke_presjeka) == 2 else None

#ucitavanje stl datoteke
stl_datoteka = "model.stl"
model = mesh.Mesh.from_file(stl_datoteka)

#vizualizacija
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#vizualizacija 3D modela
mesh = Poly3DCollection(model.vectors, facecolors='gray', alpha=0.6)
ax.add_collection3d(mesh)

#postavljanje limita
scale = model.points.flatten()
ax.auto_scale_xyz(scale, scale, scale)

for i in range(0,3):
    #izracun koeficijenata u jednadzbi ravnine
    a, b, c = normala_ravnine[i]
    d = -np.dot(normala_ravnine[i], tocka_ravnine[i])

    #vizualni prikaz ravnine
    yy, zz = np.meshgrid(np.linspace(-20, 60, 100), np.linspace(-20, 60, 100))
    xx = 0*yy + tocka_ravnine[i][0]
    ax.plot_surface(xx, yy, zz, alpha=0.4)

    #vizualni prikaz presjeka (ako postoji)
    for x in model.vectors:
        vrhovi_trokuta = [x[0], x[1], x[2]]
        tocke_presjeka = presjek_ravnina_trokut(normala_ravnine[i], tocka_ravnine[i], vrhovi_trokuta)

        if tocke_presjeka is not None:
                pravac = np.array(tocke_presjeka)
                ax.plot(pravac[:, 0], pravac[:, 1], pravac[:, 2], c='red', label='Pravac kroz tocke presjeka', alpha=1)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

#prikaz
plt.show()