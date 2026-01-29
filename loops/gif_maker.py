from PIL import Image
import glob
import os

# ────────────────────────────────────────────────
# USTAWIENIA – zmień tylko te linie jeśli trzeba
folder = "loops\outputs"              # nazwa Twojego folderu ze zdjęciami
output_gif = "loops\graf_animacja.gif"   # nazwa pliku wynikowego
czas_na_klatke = 800            # milisekundy (800 = 0,8 s na klatkę)
# odwrotna_kolejnosc = True       # True = od ostatniego do pierwszego pliku
# ────────────────────────────────────────────────

# Znajdujemy wszystkie pliki .png w folderze
sciezki = glob.glob(os.path.join(folder, "*.png"))

if not sciezki:
    print("Nie znaleziono żadnych plików .png w folderze", folder)
    exit()

# Sortujemy alfabetycznie (ważne przy numerowanych nazwach typu 001.png)
sciezki.sort()

# Jeśli chcesz odwróconą kolejność
# if odwrotna_kolejnosc:
#     sciezki = sciezki[::-1]

print(f"Znaleziono {len(sciezki)} obrazków. Tworzę GIF...")

# Wczytujemy pierwszy obrazek
obrazki = []
pierwszy = Image.open(sciezki[0])
pierwszy = pierwszy.convert("RGBA")   # GIF-y lepiej działają z RGBA

for sciezka in sciezki[1:]:
    img = Image.open(sciezka).convert("RGBA")
    obrazki.append(img)

# Zapisujemy animację
pierwszy.save(
    output_gif,
    save_all=True,
    append_images=obrazki,
    duration=czas_na_klatke,      # czas trwania każdej klatki
    loop=0,                       # 0 = nieskończona pętla
    disposal=2                    # 2 = usuń poprzednią klatkę (najczęściej najlepszy efekt)
)

print(f"Gotowe! Plik: {output_gif}")
print(f"Rozmiar animacji: {len(sciezki)} klatek, każda widoczna przez {czas_na_klatke} ms")
