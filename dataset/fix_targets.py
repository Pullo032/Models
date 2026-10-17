import json
from pathlib import Path

BASE = Path(__file__).parent

FIXES = {
    ("batch_02_p3.jsonl", 48): "Un duplex de 5 pièces de 120 m² au 4e étage, à découvrir sans attendre ! Il compte 2 salles de bains, une cave, et affiche un DPE E. Construit en 1932, il est proposé à 498 000 € : contactez-nous pour organiser une visite.",
    ("batch_04.jsonl", 46): "Costume deux pièces gris anthracite, taille 50 FR. Acheté en 2019, il a été porté pour 3 mariages seulement. La veste et le pantalon sont fournis. Le prix est de 150 €.",
    ("batch_05_p1.jsonl", 12): "Zelda Breath of the Wild sur Nintendo Switch, version européenne avec boîte et notice, en excellent état, classé PEGI 12, pour 35 €. Une occasion à saisir.",
    ("batch_05_p1.jsonl", 13): "Vous cherchez Zelda Breath of the Wild ? Cette version européenne pour Nintendo Switch, avec boîte et notice, est en excellent état, classée PEGI 12 et affichée à 35 € ! Contactez-moi vite pour en profiter.",
    ("batch_05_p2.jsonl", 10): "Clavier Casio CT-S300 de 2015 à 61 touches, avec pupitre et adaptateur secteur, très bon état pour un poids de 4,8 kg. Proposé à 110 €.",
    ("batch_05_p2.jsonl", 21): "Ampli guitare Marshall MG15CFX de 2019, 15 W, avec câble jack, très bon état, 30 x 26 x 20 cm et 6 kg. Tu l'as pour 120 € !",
    ("batch_05_p2.jsonl", 37): "Une basse Ibanez GSR200 de 2017, à 4 cordes, avec sa housse. Poids 4,2 kg, petite rayure sur le vernis, proposée à 165 €.",
    ("batch_05_p2.jsonl", 44): "Pédale d'overdrive Ibanez TS9 de 2012, avec boîte d'origine, qui fonctionne parfaitement. 12 x 7 x 5 cm, 0,5 kg, proposée à 45 €.",
    ("batch_05_p2.jsonl", 45): "Vous cherchez une pédale d'overdrive ? Cette Ibanez TS9 de 2012 est vendue avec sa boîte d'origine et fonctionne parfaitement. Dimensions 12 x 7 x 5 cm, 0,5 kg, proposée à 45 € : contactez-moi !",
    ("batch_05_p2.jsonl", 46): "Accordéon diatonique à 2 rangées et 21 touches, de 2005, avec housse. Légères usures aux coins, 3,8 kg, 390 €.",
    ("batch_05_p3.jsonl", 3): "Tondeuse thermique Honda HRN216 de 2019, largeur de coupe 53 cm, avec bac de ramassage. Elle fonctionne et pèse 36 kg, pour 320 € !",
    ("batch_05_p3.jsonl", 21): "Ponceuse excentrique Festool ETS 125 de 2016, 350 W, avec sa valisette, très bon état. Elle pèse 1,6 kg, et je la propose à 210 €.",
    ("batch_05_p3.jsonl", 32): "Le taille-haie électrique Bosch AHS 55-20 date de 2017. Sa puissance est de 550 W et sa lame mesure 55 cm. Il pèse 3,2 kg, est rangé et en bon état, et il est proposé à 60 €.",
    ("batch_05_p3.jsonl", 35): "Un taille-haie électrique Bosch AHS 55-20 de 2017, à 550 W, avec une lame de 55 cm, rangé et en bon état. Je le propose à 60 €, il pèse 3,2 kg.",
    ("batch_05_p3.jsonl", 44): "Établi de bricolage Workmate Black & Decker de 2014, pliable, plateau de 60 cm, dimensions 90 x 60 x 80 cm, jamais utilisé. 55 €.",
    ("batch_05_p3.jsonl", 46): "Scie circulaire Makita HS7601 de 2019, 1400 W, lame de 190 mm. Elle fonctionne et pèse 4,7 kg. Prix : 85 €.",
    ("batch_05_p4.jsonl", 3): "Une poussette canne Maclaren Techno XT de 2019, pliable, avec capote et panier. Très bon état, 7 kg : tu peux l'avoir pour 180 €.",
    ("batch_05_p4.jsonl", 19): "Un tapis d'éveil Fisher-Price de 2021 avec arche et jouets suspendus, à partir de 0 mois, en bon état. 35 €.",
    ("batch_05_p4.jsonl", 35): "Arbre à chat de 150 cm avec 3 plateformes et griffoir en sisal, de 2021 ! 60 x 50 cm, un peu poussiéreux, 40 €.",
    ("batch_05_p4.jsonl", 46): "Transporteur pour chat taille S de 2021, 48 x 32 x 32 cm, en bon état. 1,8 kg, proposé à 22 €.",
}

by_file = {}
for (name, lineno), text in FIXES.items():
    by_file.setdefault(name, {})[lineno] = text

for name, fixes in by_file.items():
    path = BASE / name
    lines = path.read_text(encoding="utf-8").splitlines()
    for lineno, text in fixes.items():
        obj = json.loads(lines[lineno - 1])
        obj["target_text"] = text
        lines[lineno - 1] = json.dumps(obj, ensure_ascii=False)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{name} : {len(fixes)} ligne(s) corrigée(s)")
