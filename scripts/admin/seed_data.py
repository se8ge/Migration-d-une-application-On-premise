import os, sys, random
from datetime import datetime, date, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database import SessionLocal
from app import models

db = SessionLocal()

# ── Stores ────────────────────────────────────────────────────────────────────
stores_data = [
    ("Magasin Principal",  "M01", "01 40 00 10 00", "12 Rue de Rivoli, 75001 Paris"),
    ("Magasin Lyon",       "M02", "04 72 00 20 00", "8 Rue de la République, 69001 Lyon"),
    ("Magasin Marseille",  "M03", "04 91 00 30 00", "15 La Canebière, 13001 Marseille"),
]

stores = []
for name, code, phone, addr in stores_data:
    existing = db.query(models.Store).filter(models.Store.store_code == code).first()
    if not existing:
        s = models.Store(store_name=name, store_code=code, store_phone=phone,
                         store_address=addr, createby="seed", isactive=True)
        db.add(s)
        db.flush()
        stores.append(s)
        print(f"  Store créé : {name}")
    else:
        stores.append(existing)
db.commit()
stores = db.query(models.Store).all()

# ── Suppliers ─────────────────────────────────────────────────────────────────
suppliers_data = [
    ("SUP001", "Apple Distribution France",  "1 Rue de la Paix, 75001 Paris",          "01 40 10 11 12", "contact@apple-dist.fr",   "Jean Dupont",    "06 10 11 12 13"),
    ("SUP002", "Samsung Electronics France", "15 Av. des Champs-Élysées, 75008 Paris", "01 41 20 21 22", "b2b@samsung.fr",          "Marie Martin",   "06 20 21 22 23"),
    ("SUP003", "Sony France",               "45 Bd Haussmann, 75009 Paris",            "01 42 30 31 32", "pro@sony.fr",             "Pierre Bernard", "06 30 31 32 33"),
    ("SUP004", "LG Electronics",            "20 Rue du Commerce, 75015 Paris",         "01 43 40 41 42", "pro@lg.fr",               "Sophie Leroy",   "06 40 41 42 43"),
    ("SUP005", "Huawei Technologies",       "10 Rue Lafayette, 75010 Paris",           "01 44 50 51 52", "business@huawei.fr",      "Thomas Moreau",  "06 50 51 52 53"),
    ("SUP006", "HP France",                 "80 Quai Voltaire, 75007 Paris",           "01 45 60 61 62", "hpb2b@hp.fr",             "Camille Petit",  "06 60 61 62 63"),
    ("SUP007", "Lenovo France",             "5 Rue Saint-Honoré, 75001 Paris",         "01 46 70 71 72", "pro@lenovo.fr",           "Lucas Durand",   "06 70 71 72 73"),
    ("SUP008", "Logitech EMEA",             "30 Rue du Louvre, 75001 Paris",           "01 47 80 81 82", "b2b@logitech.fr",         "Emma Girard",    "06 80 81 82 83"),
    ("SUP009", "Philips France",            "3 Bd Saint-Germain, 75005 Paris",         "01 48 90 91 92", "pro@philips.fr",          "Noah Roux",      "06 90 91 92 93"),
    ("SUP010", "Asus France",               "22 Rue Beaubourg, 75003 Paris",           "01 49 00 01 02", "business@asus.fr",        "Chloé Blanc",    "06 00 01 02 03"),
]

admin_user = db.query(models.User).first()
admin_id = admin_user.id if admin_user else 1

for code, name, addr, phone, email, contact, c_p in suppliers_data:
    if not db.query(models.Supplier).filter(models.Supplier.supplier_code == code).first():
        s = models.Supplier(supplier_code=code, supplier_name=name, address=addr,
                            phone=phone, email=email, contact_per_name=contact,
                            c_p_contact=c_p, isactive=True, createby=admin_id)
        db.add(s)
        print(f"  Fournisseur créé : {name}")
db.commit()

# ── Products ──────────────────────────────────────────────────────────────────
products_data = [
    # Smartphones
    ("PRD001","iPhone 15 Pro 256Go",       "Smartphones","Apple",    "Pièce","A3090","Smartphone Apple 256Go Titane",          899.00,1199.00,5),
    ("PRD002","iPhone 15 128Go",           "Smartphones","Apple",    "Pièce","A2846","Smartphone Apple 128Go Noir",             699.00, 899.00,5),
    ("PRD003","Samsung Galaxy S24 Ultra",  "Smartphones","Samsung",  "Pièce","S928B","Smartphone Samsung 512Go Titanium",      899.00,1299.00,5),
    ("PRD004","Samsung Galaxy A55",        "Smartphones","Samsung",  "Pièce","A556B","Smartphone Samsung 128Go Bleu",           349.00, 449.00,8),
    ("PRD005","Huawei P60 Pro",            "Smartphones","Huawei",   "Pièce","LNA-L29","Smartphone Huawei 256Go Noir",         699.00, 899.00,5),
    ("PRD006","Xiaomi 14 Pro",             "Smartphones","Xiaomi",   "Pièce","2312DPK50G","Smartphone Xiaomi 512Go Blanc",     699.00, 999.00,5),
    ("PRD007","Google Pixel 8 Pro",        "Smartphones","Google",   "Pièce","GC3VE","Smartphone Google 128Go Obsidian",       699.00, 999.00,5),
    ("PRD008","OnePlus 12",                "Smartphones","OnePlus",  "Pièce","CPH2573","Smartphone OnePlus 256Go Noir",        599.00, 799.00,5),
    # Tablettes
    ("PRD009","iPad Pro 12.9 M2",          "Tablettes",  "Apple",    "Pièce","MNXF3NF","Tablette Apple 256Go WiFi",           899.00,1199.00,3),
    ("PRD010","iPad Air 5 64Go",           "Tablettes",  "Apple",    "Pièce","MM9D3NF","Tablette Apple 64Go WiFi Bleu",       549.00, 749.00,5),
    ("PRD011","Samsung Galaxy Tab S9",     "Tablettes",  "Samsung",  "Pièce","X710NZAAEUB","Tablette Samsung 256Go WiFi",     649.00, 849.00,5),
    ("PRD012","Huawei MatePad Pro 13.2",   "Tablettes",  "Huawei",   "Pièce","MRX-W09","Tablette Huawei 256Go WiFi",          599.00, 799.00,3),
    # Laptops
    ("PRD013","MacBook Air M2 256Go",      "Laptops",    "Apple",    "Pièce","MLXW3FN","Laptop Apple M2 8Go RAM 256Go SSD",  999.00,1299.00,3),
    ("PRD014","MacBook Pro 14 M3",         "Laptops",    "Apple",    "Pièce","MRX33FN","Laptop Apple M3 Pro 18Go 512Go",    1799.00,2299.00,2),
    ("PRD015","Dell XPS 15 OLED",          "Laptops",    "Dell",     "Pièce","9530-7842","Laptop Dell i7 16Go 512Go SSD",   1199.00,1599.00,3),
    ("PRD016","HP Spectre x360 14",        "Laptops",    "HP",       "Pièce","2V9M4EA","Laptop HP i7 16Go 512Go Argent",    1099.00,1499.00,3),
    ("PRD017","Lenovo ThinkPad X1 Carbon", "Laptops",    "Lenovo",   "Pièce","21HM000EFR","Laptop Lenovo i7 16Go 512Go",    1299.00,1699.00,3),
    ("PRD018","Asus ZenBook 14 OLED",      "Laptops",    "Asus",     "Pièce","UM3402YA","Laptop Asus Ryzen 7 16Go 512Go",    799.00,1099.00,3),
    ("PRD019","Acer Swift 3",              "Laptops",    "Acer",     "Pièce","NX.A4BEF","Laptop Acer i5 8Go 512Go SSD",      499.00, 699.00,5),
    ("PRD020","MSI Prestige 14",           "Laptops",    "MSI",      "Pièce","9S7-14C612","Laptop MSI i7 16Go 1To SSD",      899.00,1199.00,3),
    # Accessoires téléphonie
    ("PRD021","AirPods Pro 2e gen",        "Audio",      "Apple",    "Pièce","MQDB3RN","Écouteurs Apple ANC USB-C",           199.00, 279.00,10),
    ("PRD022","Samsung Galaxy Buds2 Pro",  "Audio",      "Samsung",  "Pièce","SM-R510","Écouteurs Samsung ANC Bora Purple",   149.00, 229.00,10),
    ("PRD023","Sony WH-1000XM5",           "Audio",      "Sony",     "Pièce","WH1000XM5","Casque Sony ANC Bluetooth Noir",   279.00, 399.00,5),
    ("PRD024","Bose QuietComfort 45",      "Audio",      "Bose",     "Pièce","866724-0100","Casque Bose ANC Blanc",           249.00, 349.00,5),
    ("PRD025","Jabra Evolve2 85",          "Audio",      "Jabra",    "Pièce","28599-999-989","Casque Pro ANC UC",             299.00, 449.00,5),
    # Enceintes
    ("PRD026","HomePod mini",              "Audio",      "Apple",    "Pièce","MY5H2FN","Enceinte Apple Smart Gris Sidéral",   89.00,  99.00,8),
    ("PRD027","Sonos Era 100",             "Audio",      "Sonos",    "Pièce","E10G1EU1BLK","Enceinte Sonos WiFi Noir",       199.00, 249.00,5),
    ("PRD028","JBL Charge 5",              "Audio",      "JBL",      "Pièce","JBLCHARGE5BLU","Enceinte JBL Waterproof Bleu", 129.00, 179.00,8),
    # Écrans
    ("PRD029","LG UltraWide 34 WQHD",     "Écrans",     "LG",       "Pièce","34WP85C-B","Écran 34 pouces WQHD IPS 144Hz",   449.00, 599.00,3),
    ("PRD030","Samsung Odyssey G5 27",     "Écrans",     "Samsung",  "Pièce","LC27G55TQ","Écran Gaming 27 QHD 144Hz",        249.00, 349.00,5),
    ("PRD031","Dell UltraSharp U2722D",    "Écrans",     "Dell",     "Pièce","210-AZZV","Écran 27 4K USB-C Hub",             399.00, 549.00,3),
    ("PRD032","BenQ PD2725U",              "Écrans",     "BenQ",     "Pièce","9H.LLFLB.QBE","Écran 27 4K Thunderbolt",      549.00, 749.00,3),
    # Périphériques
    ("PRD033","Magic Keyboard Touch ID",   "Périphériques","Apple",  "Pièce","MK2C3FN","Clavier Apple Wireless AZERTY",      109.00, 149.00,8),
    ("PRD034","Logitech MX Keys",          "Périphériques","Logitech","Pièce","920-009415","Clavier sans fil rétroéclairé",    79.00, 119.00,10),
    ("PRD035","Logitech MX Master 3S",     "Périphériques","Logitech","Pièce","910-006559","Souris Ergonomique Wireless",      79.00, 109.00,10),
    ("PRD036","Apple Magic Mouse",         "Périphériques","Apple",  "Pièce","MK2E3ZM","Souris Apple Multi-Touch Blanc",      69.00,  99.00,8),
    ("PRD037","Razer DeathAdder V3",       "Périphériques","Razer",  "Pièce","RZ01-0480","Souris Gaming 30000 DPI",           59.00,  89.00,8),
    ("PRD038","Corsair K100 RGB",          "Périphériques","Corsair","Pièce","CH-912A01A","Clavier Gaming Mécanique RGB",    149.00, 199.00,5),
    # Stockage
    ("PRD039","SSD Samsung 990 Pro 1To",   "Stockage",   "Samsung",  "Pièce","MZ-V9P1T0BW","SSD NVMe M.2 PCIe 4.0 1To",     79.00, 129.00,10),
    ("PRD040","WD Black SN850X 2To",       "Stockage",   "WD",       "Pièce","WDS200T2X0E","SSD NVMe PCIe 4.0 2To",          129.00, 189.00,8),
    ("PRD041","Seagate BarraCuda 4To",     "Stockage",   "Seagate",  "Pièce","ST4000DM004","Disque Dur 3.5 SATA 5400RPM",     59.00,  89.00,10),
    ("PRD042","SanDisk Extreme Pro 1To",   "Stockage",   "SanDisk",  "Pièce","SDSSDE81-1T","SSD Externe USB 3.2 1To",         79.00, 119.00,8),
    # Réseau
    ("PRD043","Ubiquiti UniFi AP WiFi 6",  "Réseau",     "Ubiquiti", "Pièce","U6-LR-EU","Point d'accès WiFi 6 LR",           99.00, 149.00,5),
    ("PRD044","TP-Link Archer AX73",       "Réseau",     "TP-Link",  "Pièce","ARCHER AX73","Routeur WiFi 6 AX5400",           99.00, 149.00,5),
    ("PRD045","Netgear Nighthawk AX12",    "Réseau",     "Netgear",  "Pièce","RAX200-100EUS","Routeur WiFi 6 12 flux",       299.00, 399.00,3),
    ("PRD046","Switch TP-Link 8P PoE",     "Réseau",     "TP-Link",  "Pièce","TL-SG108PE","Switch 8 ports Gigabit PoE",       49.00,  79.00,8),
    ("PRD047","Câble RJ45 Cat6 10m",       "Réseau",     "Goobay",   "Pièce","96200","Câble réseau Cat6 UTP 10m",              3.00,   8.00,50),
    # Gaming
    ("PRD048","PlayStation 5 Standard",    "Gaming",     "Sony",     "Pièce","CFI-1216A","Console Sony PS5 BluRay",          399.00, 549.00,3),
    ("PRD049","Xbox Series X",             "Gaming",     "Microsoft","Pièce","RRT-00010","Console Microsoft 1To SSD",         399.00, 549.00,3),
    ("PRD050","Nintendo Switch OLED",      "Gaming",     "Nintendo", "Pièce","HEG-001","Console Portable Nintendo 64Go",     299.00, 349.00,5),
    ("PRD051","DualSense PS5 Blanc",       "Gaming",     "Sony",     "Pièce","CFI-ZCT1W","Manette PS5 Haptic Blanc",          54.00,  74.00,10),
    ("PRD052","Xbox Wireless Controller",  "Gaming",     "Microsoft","Pièce","QAT-00002","Manette Xbox Carbon Black",         44.00,  64.00,10),
    ("PRD053","Razer Kraken V3 Pro",       "Gaming",     "Razer",    "Pièce","RZ04-0445","Casque Gaming ANC WiFi",            99.00, 149.00,8),
    # Smartphones milieu de gamme
    ("PRD054","Samsung Galaxy A54",        "Smartphones","Samsung",  "Pièce","SM-A546B","Smartphone Samsung 128Go Violet",   299.00, 399.00,10),
    ("PRD055","Xiaomi Redmi Note 13 Pro",  "Smartphones","Xiaomi",   "Pièce","23090RA98G","Smartphone Xiaomi 256Go Noir",    249.00, 349.00,10),
    ("PRD056","OPPO Find X7",              "Smartphones","OPPO",     "Pièce","CPH2599","Smartphone OPPO 256Go Noir",         599.00, 799.00,5),
    ("PRD057","Motorola Edge 40 Pro",      "Smartphones","Motorola", "Pièce","PAWO0011FR","Smartphone Motorola 256Go Noir",  499.00, 699.00,5),
    # Électroménager connecté
    ("PRD058","Aspirateur Dyson V15",      "Électroménager","Dyson", "Pièce","394647-01","Aspirateur Balai sans fil V15",    499.00, 649.00,3),
    ("PRD059","Robot Roomba j9+",          "Électroménager","iRobot","Pièce","R975840","Robot aspirateur Auto-Vidage",       599.00, 799.00,3),
    ("PRD060","Thermomix TM6",             "Électroménager","Vorwerk","Pièce","TM6","Robot Cuiseur Multifonction",         1099.00,1249.00,2),
    # Smartwatch
    ("PRD061","Apple Watch Series 9 45mm", "Montres",    "Apple",    "Pièce","MRMC3NF","Montre Connectée GPS Aluminium",    379.00, 449.00,5),
    ("PRD062","Samsung Galaxy Watch6",     "Montres",    "Samsung",  "Pièce","SM-R930","Montre Connectée 44mm Graphite",    199.00, 299.00,5),
    ("PRD063","Garmin Fenix 7X Pro",       "Montres",    "Garmin",   "Pièce","010-02778-11","Montre Sport GPS Premium",      599.00, 799.00,3),
    ("PRD064","Fitbit Sense 2",            "Montres",    "Fitbit",   "Pièce","FB521BKBK","Montre Santé ECG GPS",            199.00, 249.00,5),
    # Imprimantes
    ("PRD065","HP LaserJet Pro M404n",     "Imprimantes","HP",       "Pièce","W1A52A","Imprimante Laser Monochrome Réseau",  199.00, 279.00,3),
    ("PRD066","Canon PIXMA TS8351a",       "Imprimantes","Canon",    "Pièce","4167C006","Imprimante Photo Multifonction",    99.00, 149.00,5),
    ("PRD067","Epson EcoTank ET-4850",     "Imprimantes","Epson",    "Pièce","C11CJ29401","Imprimante Jet d'encre Réservoir",199.00, 299.00,5),
    # Câbles & Accessoires
    ("PRD068","Câble USB-C MagSafe 2m",    "Accessoires","Apple",    "Pièce","MQLN3ZM","Câble Apple USB-C vers MagSafe 3",   39.00,  59.00,20),
    ("PRD069","Chargeur Apple 96W USB-C",  "Accessoires","Apple",    "Pièce","MX0J2ZM","Adaptateur secteur USB-C 96W",       69.00,  89.00,15),
    ("PRD070","Hub USB-C CalDigit TS4",    "Accessoires","CalDigit", "Pièce","500756","Station d'accueil Thunderbolt 4",     199.00, 299.00,5),
    ("PRD071","Câble HDMI 2.1 3m",         "Accessoires","Belkin",   "Pièce","AV10175bt3M","Câble HDMI 4K 120Hz 3m",         19.00,  39.00,30),
    ("PRD072","Chargeur Anker 140W GaN",   "Accessoires","Anker",    "Pièce","A2077111","Chargeur GaN 3 ports USB-C+A",       49.00,  79.00,15),
    # Sécurité
    ("PRD073","Caméra Arlo Pro 4",         "Sécurité",   "Arlo",     "Pièce","VMC4050P","Caméra 2K Sans Fil Color Night",   149.00, 219.00,5),
    ("PRD074","Ring Video Doorbell 4",     "Sécurité",   "Ring",     "Pièce","8DDBP8-0EU0","Sonnette Vidéo WiFi 1080p",       89.00, 129.00,5),
    ("PRD075","Yale Linus Smart Lock",     "Sécurité",   "Yale",     "Pièce","YL-MDL","Serrure Connectée Bluetooth",         149.00, 219.00,5),
    # PC Composants
    ("PRD076","Processeur Intel i7-14700K","Composants", "Intel",    "Pièce","BX8071514700K","CPU 20 cœurs 3.4GHz LGA1700", 319.00, 449.00,5),
    ("PRD077","RAM Corsair 32Go DDR5",     "Composants", "Corsair",  "Pièce","CMK32GX5M2B","Kit 2x16Go DDR5 6000MHz",        99.00, 149.00,8),
    ("PRD078","RTX 4070 Ti Super",         "Composants", "ASUS",     "Pièce","TUF-RTX4070TIS","Carte Graphique GDDR6X 16Go",599.00, 849.00,3),
    ("PRD079","Alimentation EVGA 850W",    "Composants", "EVGA",     "Pièce","220-G6-0850","PSU 80+ Gold Modulaire",          99.00, 149.00,5),
    ("PRD080","Boitier Fractal North",     "Composants", "Fractal",  "Pièce","FD-C-NOR1C","Boitier Mid-Tower ATX Verre",      89.00, 139.00,5),
    # Photo & Vidéo
    ("PRD081","Sony Alpha 7 IV",           "Photo",      "Sony",     "Pièce","ILCE-7M4","Appareil Photo Hybride 33MP",     2199.00,2799.00,2),
    ("PRD082","Canon EOS R6 Mark II",      "Photo",      "Canon",    "Pièce","5666C003","Appareil Photo Hybride 24.2MP",   2199.00,2699.00,2),
    ("PRD083","DJI Mini 4 Pro",            "Photo",      "DJI",      "Pièce","CP.MA.00000732","Drone 4K HDR 249g GPS",       679.00, 899.00,3),
    ("PRD084","GoPro Hero12 Black",        "Photo",      "GoPro",    "Pièce","CHDHX-121","Caméra Sport 5.3K HDR",            299.00, 399.00,5),
    # Éclairage connecté
    ("PRD085","Philips Hue Starter Pack",  "Domotique",  "Philips",  "Pièce","8719514291720","Kit 3 ampoules E27 + Bridge",  99.00, 149.00,8),
    ("PRD086","Nanoleaf Lines 9 Smarts",   "Domotique",  "Nanoleaf", "Pièce","NL59-0002LW-9PK","Panneaux LED connectés",    149.00, 229.00,5),
    # Consommables
    ("PRD087","Toner HP LaserJet 59A",     "Consommables","HP",      "Pièce","CF259A","Cartouche Toner Noire 3000 pages",    49.00,  79.00,20),
    ("PRD088","Encre Canon PG-560XL",      "Consommables","Canon",   "Pièce","3712C001","Cartouche Noire Grande Capacité",   12.00,  22.00,30),
    ("PRD089","Papier HP Premium 500f",    "Consommables","HP",       "Rame","CHP871","Papier Laser A4 160g 500 feuilles",    14.00,  24.00,50),
    ("PRD090","Film Protection iPhone 15", "Consommables","Belkin",  "Pièce","OVA130ZZ","Verre Trempé Anti-traces",           8.00,  18.00,50),
    # Mobilier & Ergonomie
    ("PRD091","Bras Écran Ergotron LX",    "Ergonomie",  "Ergotron", "Pièce","45-241-026","Support Bras Articulé Noir",      79.00, 119.00,5),
    ("PRD092","Repose-poignet Logitech",   "Ergonomie",  "Logitech", "Pièce","956-000001","Repose-Poignet Gel Clavier",      14.00,  24.00,20),
    ("PRD093","Webcam Logitech C920 HD",   "Périphériques","Logitech","Pièce","960-001055","Webcam 1080p 30fps",              59.00,  89.00,10),
    ("PRD094","Microphone Blue Yeti",      "Audio",      "Blue",     "Pièce","988-000100","Microphone USB Condensateur",    109.00, 149.00,5),
    ("PRD095","Lampe LED Bureau BenQ",     "Ergonomie",  "BenQ",     "Pièce","9H.LN8LB.QB2","Lampe LED Moniteur ScreenBar",  69.00,  99.00,8),
    # Cloud / Services (clés physiques)
    ("PRD096","YubiKey 5 NFC",             "Sécurité",   "Yubico",   "Pièce","5060408461426","Clé Sécurité USB-A NFC FIDO2", 45.00,  69.00,10),
    ("PRD097","SSD Portable Samsung T7",   "Stockage",   "Samsung",  "Pièce","MU-PC1T0H","SSD Externe USB 3.2 1To Gris",     79.00, 119.00,10),
    ("PRD098","Station Charge Belkin 15W", "Accessoires","Belkin",   "Pièce","WIZ016vfWH","Chargeur Sans Fil Qi2 15W Blanc",  39.00,  59.00,15),
    ("PRD099","Apple TV 4K 128Go WiFi6E",  "Domotique",  "Apple",    "Pièce","MN893FD","Box Multimédia 4K HDR",             119.00, 149.00,5),
    ("PRD100","Kindle Paperwhite 16Go",    "Tablettes",  "Amazon",   "Pièce","B095J2F139","Liseuse 6.8 pouces 300ppi",       119.00, 149.00,5),
]

created_products = []
for code, name, cat, brand, unit, model, details, pp, rp, min_s in products_data:
    if not db.query(models.Product).filter(models.Product.product_code == code).first():
        p = models.Product(product_code=code, product_name=name, category=cat,
                           brand=brand, unit=unit, model=model,
                           product_details=details, purchase_price=pp,
                           retail_price=rp, min_stock=min_s,
                           isactive=True, createby="seed")
        db.add(p)
        created_products.append(code)
db.commit()
print(f"  {len(created_products)} produits créés")

# ── Store Stock ───────────────────────────────────────────────────────────────
all_products = db.query(models.Product).all()
all_stores   = db.query(models.Store).all()

for store in all_stores:
    for prod in all_products:
        existing = db.query(models.StoreStock).filter_by(
            StoreID=store.store_id, ProdID=prod.product_id).first()
        if not existing:
            in_qty = random.randint(prod.min_stock + 5, prod.min_stock + 80)
            # 15% chance de stock bas
            if random.random() < 0.15:
                in_qty = random.randint(1, prod.min_stock - 1)
            out_qty = random.randint(0, max(0, in_qty - 2))
            ss = models.StoreStock(StoreID=store.store_id, ProdID=prod.product_id,
                                   InQty=in_qty, OutQty=out_qty)
            db.add(ss)
db.commit()
print("  Stocks initialisés pour tous les magasins")

# ── Stock Movements ───────────────────────────────────────────────────────────
today = date.today()
prods_ids = [p.product_id for p in all_products]
store_ids  = [s.store_id for s in all_stores]

movements_created = 0
for i in range(1, 21):
    code = f"MV{str(i).zfill(4)}"
    if db.query(models.StockMovement).filter_by(proposal_code=code).first():
        continue

    from_s = random.choice(store_ids)
    to_s   = random.choice([s for s in store_ids if s != from_s])
    days_ago = random.randint(0, 60)
    d = today - timedelta(days=days_ago)
    approved = random.random() > 0.3
    received = approved and random.random() > 0.4

    mv = models.StockMovement(
        proposal_code=code,
        issue_code=f"IS{str(i).zfill(4)}" if approved else None,
        for_store_id=to_s, from_store_id=from_s,
        proposal_datetime=d, proposal_by=admin_id,
        issue_datetime=d, issue_by=admin_id,
        is_approved=approved, is_received=received
    )
    db.add(mv)
    db.flush()

    nb_prods = random.randint(1, 5)
    chosen = random.sample(prods_ids, nb_prods)
    for pid in chosen:
        db.add(models.StockMovementDetails(
            movement_id=mv.movement_id,
            product_id=pid,
            received_qty=random.randint(5, 50)
        ))
    movements_created += 1

db.commit()
print(f"  {movements_created} mouvements créés")
print("\nSeed terminé avec succès !")
db.close()
