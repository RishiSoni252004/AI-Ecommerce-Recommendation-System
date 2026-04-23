import time, random, os, sys

# Ensure imports work both when run directly inside database/ and from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.mongo_client import db_client

# Every product has a SPECIFIC image URL that matches what it actually is.
# Images sourced from Unsplash (free, no API key needed).

PRODUCTS = [
  {
    "title": "Apple MacBook Air M2",
    "category": "Laptops",
    "price": 99900,
    "brand": "Apple",
    "description": "13.6-inch Liquid Retina display, M2 chip, 8GB RAM, 256GB SSD",
    "image": "/images/apple-macbook-air-m2.jpg"
  },
  {
    "title": "Apple MacBook Pro 14-inch",
    "category": "Laptops",
    "price": 169900,
    "brand": "Apple",
    "description": "M3 Pro chip, 18GB RAM, 512GB SSD, Liquid Retina XDR display",
    "image": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-m3-pro-max-silver-select-202310?wid=800&hei=800&fmt=jpeg&qlt=90"
  },
  {
    "title": "Dell XPS 13 Plus",
    "category": "Laptops",
    "price": 124990,
    "brand": "Dell",
    "description": "13.4-inch FHD+, Intel Core i7, 16GB RAM, 512GB SSD",
    "image": "/images/dell-xps-13-plus.jpg"
  },
  {
    "title": "HP Spectre x360 14",
    "category": "Laptops",
    "price": 139990,
    "brand": "HP",
    "description": "2-in-1 convertible, 13.5-inch 3K OLED, Intel Core i7",
    "image": "/images/hp-spectre-x360-14.jpg"
  },
  {
    "title": "Lenovo ThinkPad X1 Carbon",
    "category": "Laptops",
    "price": 154990,
    "brand": "Lenovo",
    "description": "14-inch 2.8K OLED, Intel Core i7, 16GB RAM, 1TB SSD",
    "image": "/images/lenovo-thinkpad-x1-carbon.jpg"
  },
  {
    "title": "ASUS ZenBook 14 OLED",
    "category": "Laptops",
    "price": 89990,
    "brand": "ASUS",
    "description": "14-inch 2.8K OLED, AMD Ryzen 7, 16GB RAM, 512GB SSD",
    "image": "/images/asus-zenbook-14-oled.jpg"
  },
  {
    "title": "Acer Swift 5",
    "category": "Laptops",
    "price": 79990,
    "brand": "Acer",
    "description": "14-inch FHD IPS, Intel Core i5, 16GB RAM, 512GB SSD",
    "image": "/images/acer-swift-5.jpg"
  },
  {
    "title": "MSI Gaming GF63 Thin",
    "category": "Laptops",
    "price": 64990,
    "brand": "MSI",
    "description": "15.6-inch FHD 144Hz, i5-12450H, RTX 2050, 8GB RAM",
    "image": "/images/msi-gaming-gf63-thin.jpg"
  },
  {
    "title": "Apple iPhone 15 Pro Max",
    "category": "Smartphones",
    "price": 159900,
    "brand": "Apple",
    "description": "6.7-inch Super Retina XDR, A17 Pro chip, 256GB, Titanium",
    "image": "/images/apple-iphone-15-pro-max.jpg"
  },
  {
    "title": "Samsung Galaxy S24 Ultra",
    "category": "Smartphones",
    "price": 129999,
    "brand": "Samsung",
    "description": "6.8-inch QHD+, Snapdragon 8 Gen 3, 200MP camera, S Pen",
    "image": "/images/samsung-galaxy-s24-ultra.jpg"
  },
  {
    "title": "OnePlus 12",
    "category": "Smartphones",
    "price": 64999,
    "brand": "OnePlus",
    "description": "6.82-inch 2K LTPO, Snapdragon 8 Gen 3, 50MP Hasselblad",
    "image": "/images/oneplus-12.jpg"
  },
  {
    "title": "Google Pixel 8 Pro",
    "category": "Smartphones",
    "price": 106999,
    "brand": "Google",
    "description": "6.7-inch LTPO OLED, Tensor G3, 50MP camera, 7 years updates",
    "image": "/images/google-pixel-8-pro.jpg"
  },
  {
    "title": "Xiaomi 14 Ultra",
    "category": "Smartphones",
    "price": 99999,
    "brand": "Xiaomi",
    "description": "6.73-inch 2K LTPO, Snapdragon 8 Gen 3, Leica optics",
    "image": "/images/xiaomi-14-ultra.jpg"
  },
  {
    "title": "Samsung Galaxy A54 5G",
    "category": "Smartphones",
    "price": 32999,
    "brand": "Samsung",
    "description": "6.4-inch Super AMOLED, Exynos 1380, 50MP triple camera",
    "image": "https://images.samsung.com/is/image/samsung/p6pim/in/sm-a546ezkdins/gallery/in-galaxy-a54-5g-sm-a546-sm-a546ezkdins-thumb-535287234?$650_519_PNG$"
  },
  {
    "title": "Realme GT 5 Pro",
    "category": "Smartphones",
    "price": 36999,
    "brand": "Realme",
    "description": "6.78-inch 2K AMOLED 144Hz, Snapdragon 8 Gen 3, 50MP Sony",
    "image": "https://image01.realme.net/general/20231127/1701078840285.png"
  },
  {
    "title": "Nothing Phone 2",
    "category": "Smartphones",
    "price": 44999,
    "brand": "Nothing",
    "description": "6.7-inch LTPO OLED, Snapdragon 8+ Gen 1, Glyph Interface",
    "image": "/images/nothing-phone-2.jpg"
  },
  {
    "title": "Apple iPad Air M2",
    "category": "Tablets",
    "price": 74900,
    "brand": "Apple",
    "description": "11-inch Liquid Retina, M2 chip, 128GB, Wi-Fi + 5G",
    "image": "/images/apple-ipad-air-m2.jpg"
  },
  {
    "title": "Samsung Galaxy Tab S9 FE",
    "category": "Tablets",
    "price": 44999,
    "brand": "Samsung",
    "description": "10.9-inch TFT LCD, Exynos 1380, 128GB, S Pen included",
    "image": "/images/samsung-galaxy-tab-s9-fe.jpg"
  },
  {
    "title": "Apple iPad Pro 12.9-inch",
    "category": "Tablets",
    "price": 112900,
    "brand": "Apple",
    "description": "12.9-inch Liquid Retina XDR, M2 chip, 256GB, Face ID",
    "image": "/images/apple-ipad-pro-12-9-inch.jpg"
  },
  {
    "title": "Lenovo Tab P12 Pro",
    "category": "Tablets",
    "price": 49990,
    "brand": "Lenovo",
    "description": "12.6-inch 2K AMOLED 120Hz, Snapdragon 870, 8GB RAM",
    "image": "/images/lenovo-tab-p12-pro.jpg"
  },
  {
    "title": "OnePlus Pad",
    "category": "Tablets",
    "price": 37999,
    "brand": "OnePlus",
    "description": "11.61-inch 2.8K LCD 144Hz, Dimensity 9000, 8GB RAM",
    "image": "/images/oneplus-pad.jpg"
  },
  {
    "title": "Sony WH-1000XM5",
    "category": "Headphones",
    "price": 26990,
    "brand": "Sony",
    "description": "Wireless noise cancelling over-ear, 30hr battery, LDAC",
    "image": "/images/sony-wh-1000xm5.jpg"
  },
  {
    "title": "Apple AirPods Pro 2",
    "category": "Headphones",
    "price": 24900,
    "brand": "Apple",
    "description": "Active Noise Cancellation, Adaptive Transparency, USB-C",
    "image": "/images/apple-airpods-pro-2.jpg"
  },
  {
    "title": "Bose QuietComfort Ultra",
    "category": "Headphones",
    "price": 29900,
    "brand": "Bose",
    "description": "Spatial audio, world-class noise cancellation, 24hr battery",
    "image": "/images/bose-quietcomfort-ultra.jpg"
  },
  {
    "title": "JBL Tune 770NC",
    "category": "Headphones",
    "price": 4999,
    "brand": "JBL",
    "description": "Wireless over-ear with ANC, JBL Pure Bass, 44hr battery",
    "image": "/images/jbl-tune-770nc.jpg"
  },
  {
    "title": "Samsung Galaxy Buds2 Pro",
    "category": "Headphones",
    "price": 17999,
    "brand": "Samsung",
    "description": "True wireless earbuds, 360 Audio, ANC, IPX7 waterproof",
    "image": "/images/samsung-galaxy-buds2-pro.jpg"
  },
  {
    "title": "Sennheiser Momentum 4",
    "category": "Headphones",
    "price": 24990,
    "brand": "Sennheiser",
    "description": "Wireless over-ear, 60hr battery, adaptive ANC, aptX",
    "image": "/images/sennheiser-momentum-4.jpg"
  },
  {
    "title": "OnePlus Buds Pro 2",
    "category": "Headphones",
    "price": 9999,
    "brand": "OnePlus",
    "description": "True wireless with ANC, LHDC 5.0, 39hr total battery",
    "image": "/images/oneplus-buds-pro-2.jpg"
  },
  {
    "title": "boAt Airdopes 141",
    "category": "Headphones",
    "price": 1299,
    "brand": "boAt",
    "description": "True wireless earbuds, 42hr playback, IPX4, low latency",
    "image": "/images/boat-airdopes-141.jpg"
  },
  {
    "title": "Canon EOS R50",
    "category": "Cameras",
    "price": 74990,
    "brand": "Canon",
    "description": "24.2MP APS-C mirrorless, 4K video, Dual Pixel CMOS AF II",
    "image": "/images/canon-eos-r50.jpg"
  },
  {
    "title": "Sony Alpha A7 IV",
    "category": "Cameras",
    "price": 198990,
    "brand": "Sony",
    "description": "33MP full-frame mirrorless, 4K 60fps, 759-point AF",
    "image": "/images/sony-alpha-a7-iv.jpg"
  },
  {
    "title": "Nikon Z50",
    "category": "Cameras",
    "price": 76990,
    "brand": "Nikon",
    "description": "20.9MP APS-C mirrorless, 4K UHD video, 209-point AF",
    "image": "/images/nikon-z50.jpg"
  },
  {
    "title": "GoPro Hero 12 Black",
    "category": "Cameras",
    "price": 44490,
    "brand": "GoPro",
    "description": "5.3K60 video, 27MP photos, HyperSmooth 6.0, waterproof",
    "image": "/images/gopro-hero-12-black.jpg"
  },
  {
    "title": "Fujifilm X-T5",
    "category": "Cameras",
    "price": 169999,
    "brand": "Fujifilm",
    "description": "40.2MP APS-C, 6.2K video, film simulations, IBIS",
    "image": "/images/fujifilm-x-t5.jpg"
  },
  {
    "title": "Canon PowerShot G7 X Mark III",
    "category": "Cameras",
    "price": 54995,
    "brand": "Canon",
    "description": "20.1MP compact, 4K video, YouTube live streaming, f/1.8",
    "image": "/images/canon-powershot-g7-x-mark-iii.jpg"
  },
  {
    "title": "DJI Osmo Action 4",
    "category": "Cameras",
    "price": 27490,
    "brand": "DJI",
    "description": "1/1.3-inch sensor, 4K 120fps, 160-min battery, waterproof",
    "image": "/images/dji-osmo-action-4.jpg"
  },
  {
    "title": "Logitech MX Keys S",
    "category": "Keyboards",
    "price": 9995,
    "brand": "Logitech",
    "description": "Wireless illuminated keyboard, smart backlight, multi-device",
    "image": "/images/logitech-mx-keys-s.jpg"
  },
  {
    "title": "Keychron K2 V2 Mechanical",
    "category": "Keyboards",
    "price": 6999,
    "brand": "Keychron",
    "description": "75% wireless mechanical, Gateron switches, RGB backlit",
    "image": "/images/keychron-k2-v2-mechanical.jpg"
  },
  {
    "title": "Razer BlackWidow V4",
    "category": "Keyboards",
    "price": 14999,
    "brand": "Razer",
    "description": "Mechanical gaming keyboard, Razer Green switches, RGB",
    "image": "/images/razer-blackwidow-v4.jpg"
  },
  {
    "title": "Apple Magic Keyboard",
    "category": "Keyboards",
    "price": 13900,
    "brand": "Apple",
    "description": "Wireless with Touch ID, numeric keypad, USB-C charging",
    "image": "/images/apple-magic-keyboard.jpg"
  },
  {
    "title": "Corsair K100 RGB",
    "category": "Keyboards",
    "price": 22999,
    "brand": "Corsair",
    "description": "Optical-mechanical gaming, iCUE control wheel, PBT caps",
    "image": "/images/corsair-k100-rgb.jpg"
  },
  {
    "title": "HyperX Alloy Origins 60",
    "category": "Keyboards",
    "price": 7999,
    "brand": "HyperX",
    "description": "60% compact mechanical, HyperX Red switches, RGB per-key",
    "image": "/images/hyperx-alloy-origins-60.jpg"
  },
  {
    "title": "Logitech MX Master 3S",
    "category": "Mice",
    "price": 8995,
    "brand": "Logitech",
    "description": "Wireless ergonomic mouse, 8K DPI, MagSpeed scroll, USB-C",
    "image": "/images/logitech-mx-master-3s.jpg"
  },
  {
    "title": "Razer DeathAdder V3 Pro",
    "category": "Mice",
    "price": 12999,
    "brand": "Razer",
    "description": "Wireless gaming mouse, 30K DPI Focus Pro sensor, 63g",
    "image": "/images/razer-deathadder-v3-pro.jpg"
  },
  {
    "title": "Apple Magic Mouse",
    "category": "Mice",
    "price": 7500,
    "brand": "Apple",
    "description": "Wireless multi-touch surface, Lightning rechargeable",
    "image": "/images/apple-magic-mouse.jpg"
  },
  {
    "title": "Logitech G502 X PLUS",
    "category": "Mice",
    "price": 13995,
    "brand": "Logitech",
    "description": "Wireless RGB gaming mouse, HERO 25K sensor, LIGHTSPEED",
    "image": "/images/logitech-g502-x-plus.jpg"
  },
  {
    "title": "SteelSeries Aerox 5 Wireless",
    "category": "Mice",
    "price": 10999,
    "brand": "SteelSeries",
    "description": "Ultra-lightweight gaming, 18K CPI TrueMove sensor, 180hr",
    "image": "/images/steelseries-aerox-5-wireless.jpg"
  },
  {
    "title": "Apple Watch Series 9",
    "category": "Watches",
    "price": 41900,
    "brand": "Apple",
    "description": "45mm, Always-On Retina, S9 chip, Double Tap gesture",
    "image": "/images/apple-watch-series-9.jpg"
  },
  {
    "title": "Samsung Galaxy Watch 6 Classic",
    "category": "Watches",
    "price": 37999,
    "brand": "Samsung",
    "description": "47mm, rotating bezel, BioActive sensor, Wear OS",
    "image": "/images/samsung-galaxy-watch-6-classic.jpg"
  },
  {
    "title": "Casio G-Shock GA-2100",
    "category": "Watches",
    "price": 10995,
    "brand": "Casio",
    "description": "Carbon Core Guard, 200m water resistance, world time",
    "image": "/images/casio-g-shock-ga-2100.jpg"
  },
  {
    "title": "Fossil Gen 6 Smartwatch",
    "category": "Watches",
    "price": 22995,
    "brand": "Fossil",
    "description": "44mm, Snapdragon 4100+, SpO2, GPS, Wear OS by Google",
    "image": "/images/fossil-gen-6-smartwatch.jpg"
  },
  {
    "title": "Titan Classique Analog",
    "category": "Watches",
    "price": 5995,
    "brand": "Titan",
    "description": "Stainless steel case, leather strap, Japanese quartz",
    "image": "/images/titan-classique-analog.jpg"
  },
  {
    "title": "Noise ColorFit Pro 5",
    "category": "Watches",
    "price": 3999,
    "brand": "Noise",
    "description": "1.85-inch AMOLED, Bluetooth calling, 150+ watch faces",
    "image": "/images/noise-colorfit-pro-5.jpg"
  },
  {
    "title": "Garmin Venu 3",
    "category": "Watches",
    "price": 49990,
    "brand": "Garmin",
    "description": "AMOLED display, advanced health monitoring, 14-day battery",
    "image": "/images/garmin-venu-3.jpg"
  },
  {
    "title": "Ajanta Quartz Wall Clock",
    "category": "Wall Clocks",
    "price": 899,
    "brand": "Ajanta",
    "description": "12-inch silent sweep, ABS plastic frame, clear numerals",
    "image": "/images/ajanta-quartz-wall-clock.jpg"
  },
  {
    "title": "Seiko Pendulum Wall Clock",
    "category": "Wall Clocks",
    "price": 7500,
    "brand": "Seiko",
    "description": "Decorative pendulum, Westminster chime, oak finish",
    "image": "/images/seiko-pendulum-wall-clock.jpg"
  },
  {
    "title": "Casio Digital Wall Clock",
    "category": "Wall Clocks",
    "price": 2499,
    "brand": "Casio",
    "description": "LED digital display, temperature, calendar, auto-light",
    "image": "/images/casio-digital-wall-clock.jpg"
  },
  {
    "title": "IKEA PUGG Wall Clock",
    "category": "Wall Clocks",
    "price": 999,
    "brand": "IKEA",
    "description": "Minimalist Scandinavian design, 25cm diameter, stainless steel",
    "image": "/images/ikea-pugg-wall-clock.jpg"
  },
  {
    "title": "Vintage Wooden Wall Clock",
    "category": "Wall Clocks",
    "price": 3499,
    "brand": "Craftel",
    "description": "Handcrafted solid wood, Roman numerals, silent movement",
    "image": "/images/vintage-wooden-wall-clock.jpg"
  },
  {
    "title": "Nike Air Max 270",
    "category": "Shoes",
    "price": 12995,
    "brand": "Nike",
    "description": "Men's lifestyle shoe, Max Air 270 unit, mesh upper",
    "image": "/images/nike-air-max-270.jpg"
  },
  {
    "title": "Adidas Ultraboost 23",
    "category": "Shoes",
    "price": 16999,
    "brand": "Adidas",
    "description": "Running shoe, BOOST midsole, Continental rubber outsole",
    "image": "/images/adidas-ultraboost-23.jpg"
  },
  {
    "title": "Puma RS-X Reinvention",
    "category": "Shoes",
    "price": 8999,
    "brand": "Puma",
    "description": "Retro chunky sneaker, RS cushioning, mesh upper",
    "image": "/images/puma-rs-x-reinvention.jpg"
  },
  {
    "title": "New Balance 574 Classic",
    "category": "Shoes",
    "price": 7999,
    "brand": "New Balance",
    "description": "Heritage sneaker, ENCAP midsole, suede/mesh upper",
    "image": "/images/new-balance-574-classic.jpg"
  },
  {
    "title": "Converse Chuck Taylor All Star",
    "category": "Shoes",
    "price": 4499,
    "brand": "Converse",
    "description": "Classic high-top canvas sneaker, vulcanized rubber sole",
    "image": "/images/converse-chuck-taylor-all-star.jpg"
  },
  {
    "title": "Nike Air Jordan 1 Mid",
    "category": "Shoes",
    "price": 10795,
    "brand": "Nike",
    "description": "Iconic basketball sneaker, Air-Sole cushioning, leather",
    "image": "/images/nike-air-jordan-1-mid.jpg"
  },
  {
    "title": "Reebok Classic Leather",
    "category": "Shoes",
    "price": 5999,
    "brand": "Reebok",
    "description": "Retro lifestyle shoe, soft leather upper, EVA midsole",
    "image": "/images/reebok-classic-leather.jpg"
  },
  {
    "title": "Woodland Outdoor Boots",
    "category": "Shoes",
    "price": 4495,
    "brand": "Woodland",
    "description": "Genuine leather hiking boots, rubber sole, water-resistant",
    "image": "/images/woodland-outdoor-boots.jpg"
  },
  {
    "title": "Levi's Classic Denim Shirt",
    "category": "Clothing",
    "price": 2999,
    "brand": "Levi's",
    "description": "Western snap-front denim shirt, 100% cotton",
    "image": "/images/levi-s-classic-denim-shirt.jpg"
  },
  {
    "title": "H&M Slim Fit Oxford Shirt",
    "category": "Clothing",
    "price": 1499,
    "brand": "H&M",
    "description": "Button-down collar, chest pocket, regular fit",
    "image": "/images/h-m-slim-fit-oxford-shirt.jpg"
  },
  {
    "title": "Zara Linen Blend Shirt",
    "category": "Clothing",
    "price": 2790,
    "brand": "Zara",
    "description": "Relaxed fit, linen-cotton blend, lapel collar",
    "image": "/images/zara-linen-blend-shirt.jpg"
  },
  {
    "title": "Nike Dri-FIT Training T-Shirt",
    "category": "Clothing",
    "price": 1795,
    "brand": "Nike",
    "description": "Moisture-wicking, lightweight, crew neck athletic tee",
    "image": "/images/nike-dri-fit-training-t-shirt.jpg"
  },
  {
    "title": "Uniqlo AIRism Polo Shirt",
    "category": "Clothing",
    "price": 1490,
    "brand": "Uniqlo",
    "description": "Quick-dry, stretch, anti-odor, UV protection technology",
    "image": "/images/uniqlo-airism-polo-shirt.jpg"
  },
  {
    "title": "Allen Solly Formal Blazer",
    "category": "Clothing",
    "price": 5999,
    "brand": "Allen Solly",
    "description": "Slim fit, 2-button closure, notch lapel, polyester blend",
    "image": "/images/allen-solly-formal-blazer.jpg"
  },
  {
    "title": "US Polo Assn. Chino Trousers",
    "category": "Clothing",
    "price": 2199,
    "brand": "US Polo",
    "description": "Slim fit chinos, stretch cotton, flat front",
    "image": "/images/us-polo-assn-chino-trousers.jpg"
  },
  {
    "title": "Adidas Originals Track Jacket",
    "category": "Clothing",
    "price": 4999,
    "brand": "Adidas",
    "description": "Classic track jacket, 3-stripes, full zip, recycled poly",
    "image": "/images/adidas-originals-track-jacket.jpg"
  },
  {
    "title": "Peter England Formal Shirt",
    "category": "Clothing",
    "price": 1299,
    "brand": "Peter England",
    "description": "Regular fit, wrinkle-free, easy-care cotton blend",
    "image": "/images/peter-england-formal-shirt.jpg"
  },
  {
    "title": "Roadster Jogger Pants",
    "category": "Clothing",
    "price": 999,
    "brand": "Roadster",
    "description": "Relaxed fit joggers, elasticated waist, side pockets",
    "image": "/images/roadster-jogger-pants.jpg"
  },
  {
    "title": "IKEA MARKUS Office Chair",
    "category": "Furniture",
    "price": 15990,
    "brand": "IKEA",
    "description": "Ergonomic swivel chair, mesh back, adjustable headrest",
    "image": "/images/ikea-markus-office-chair.jpg"
  },
  {
    "title": "Nilkamal Freedom Bookshelf",
    "category": "Furniture",
    "price": 5999,
    "brand": "Nilkamal",
    "description": "5-tier bookshelf, engineered wood, walnut finish",
    "image": "/images/nilkamal-freedom-bookshelf.jpg"
  },
  {
    "title": "Wakefit Orion Coffee Table",
    "category": "Furniture",
    "price": 4499,
    "brand": "Wakefit",
    "description": "Rectangular coffee table, engineered wood, storage shelf",
    "image": "/images/wakefit-orion-coffee-table.jpg"
  },
  {
    "title": "Urban Ladder TV Unit",
    "category": "Furniture",
    "price": 14999,
    "brand": "Urban Ladder",
    "description": "Solid wood TV stand, 2 drawers, cable management, teak",
    "image": "/images/urban-ladder-tv-unit.jpg"
  },
  {
    "title": "Amazon Basics Study Desk",
    "category": "Furniture",
    "price": 6999,
    "brand": "Amazon Basics",
    "description": "L-shaped computer desk, metal frame, engineered wood top",
    "image": "/images/amazon-basics-study-desk.jpg"
  },
  {
    "title": "SleepyCat Sofa Cum Bed",
    "category": "Furniture",
    "price": 24999,
    "brand": "SleepyCat",
    "description": "3-seater convertible sofa bed, fabric upholstery, storage",
    "image": "/images/sleepycat-sofa-cum-bed.jpg"
  },
  {
    "title": "Aesthetic Wall Art Canvas Set",
    "category": "Home Decor",
    "price": 1499,
    "brand": "Art Street",
    "description": "Set of 5 abstract canvas prints, ready to hang, framed",
    "image": "/images/aesthetic-wall-art-canvas-set.jpg"
  },
  {
    "title": "Mason Home Ceramic Vase",
    "category": "Home Decor",
    "price": 1299,
    "brand": "Mason Home",
    "description": "Handcrafted ceramic flower vase, matte finish, 30cm",
    "image": "/images/mason-home-ceramic-vase.jpg"
  },
  {
    "title": "Philips Hue Table Lamp",
    "category": "Home Decor",
    "price": 8999,
    "brand": "Philips",
    "description": "Smart LED table lamp, 16 million colors, voice control",
    "image": "/images/philips-hue-table-lamp.jpg"
  },
  {
    "title": "Artificial Monstera Plant",
    "category": "Home Decor",
    "price": 899,
    "brand": "Fourwalls",
    "description": "Faux monstera plant with pot, 60cm height, evergreen",
    "image": "/images/artificial-monstera-plant.jpg"
  },
  {
    "title": "Decorative Throw Pillow Set",
    "category": "Home Decor",
    "price": 1599,
    "brand": "Pepperfry",
    "description": "Set of 5 cushion covers, 16x16 inch, cotton blend",
    "image": "/images/decorative-throw-pillow-set.jpg"
  },
  {
    "title": "Macram\u00e9 Wall Hanging",
    "category": "Home Decor",
    "price": 799,
    "brand": "Boho Living",
    "description": "Handwoven macram\u00e9 tapestry, cotton rope, bohemian style",
    "image": "/images/macrame-wall-hanging.jpg"
  },
  {
    "title": "Philips Air Fryer HD9252",
    "category": "Kitchen",
    "price": 7495,
    "brand": "Philips",
    "description": "4.1L capacity, Rapid Air technology, 1400W, digital",
    "image": "/images/philips-air-fryer-hd9252.jpg"
  },
  {
    "title": "Prestige 3L Pressure Cooker",
    "category": "Kitchen",
    "price": 1799,
    "brand": "Prestige",
    "description": "Svachh pressure cooker, stainless steel, induction base",
    "image": "/images/prestige-3l-pressure-cooker.jpg"
  },
  {
    "title": "Borosil Chef Knife Set",
    "category": "Kitchen",
    "price": 2499,
    "brand": "Borosil",
    "description": "6-piece stainless steel knife set with wooden block",
    "image": "/images/borosil-chef-knife-set.jpg"
  },
  {
    "title": "InstantPot Duo 7-in-1",
    "category": "Kitchen",
    "price": 8999,
    "brand": "InstantPot",
    "description": "Electric pressure cooker, slow cook, steam, saut\u00e9, 6Qt",
    "image": "/images/instantpot-duo-7-in-1.jpg"
  },
  {
    "title": "KitchenAid Classic Stand Mixer",
    "category": "Kitchen",
    "price": 34990,
    "brand": "KitchenAid",
    "description": "4.5-quart tilt-head mixer, 10 speeds, multiple attachments",
    "image": "/images/kitchenaid-classic-stand-mixer.jpg"
  },
  {
    "title": "American Tourister Laptop Backpack",
    "category": "Bags",
    "price": 2499,
    "brand": "American Tourister",
    "description": "15.6-inch laptop compartment, water-resistant, 28L",
    "image": "/images/american-tourister-laptop-backpack.jpg"
  },
  {
    "title": "Skybags Brat Daypack",
    "category": "Bags",
    "price": 1199,
    "brand": "Skybags",
    "description": "22L casual backpack, 2 compartments, padded straps",
    "image": "/images/skybags-brat-daypack.jpg"
  },
  {
    "title": "Wildcraft Hiking Backpack 45L",
    "category": "Bags",
    "price": 3999,
    "brand": "Wildcraft",
    "description": "45L trekking pack, rain cover, hip belt, hydration sleeve",
    "image": "/images/wildcraft-hiking-backpack-45l.jpg"
  },
  {
    "title": "Samsonite Spinner Luggage 55cm",
    "category": "Bags",
    "price": 7990,
    "brand": "Samsonite",
    "description": "Cabin trolley, hardside, 4 wheels, TSA lock, expandable",
    "image": "/images/samsonite-spinner-luggage-55cm.jpg"
  },
  {
    "title": "Nike Brasilia Gym Duffel",
    "category": "Bags",
    "price": 2795,
    "brand": "Nike",
    "description": "41L training bag, shoe compartment, padded shoulder strap",
    "image": "/images/nike-brasilia-gym-duffel.jpg"
  },
  {
    "title": "Atomic Habits by James Clear",
    "category": "Books",
    "price": 499,
    "brand": "Penguin",
    "description": "An easy & proven way to build good habits & break bad ones",
    "image": "/images/atomic-habits-by-james-clear.jpg"
  },
  {
    "title": "Sapiens by Yuval Noah Harari",
    "category": "Books",
    "price": 599,
    "brand": "Vintage",
    "description": "A brief history of humankind \u2014 global bestseller",
    "image": "/images/sapiens-by-yuval-noah-harari.jpg"
  },
  {
    "title": "The Psychology of Money",
    "category": "Books",
    "price": 350,
    "brand": "Jaico",
    "description": "Morgan Housel \u2014 timeless lessons on wealth and happiness",
    "image": "/images/the-psychology-of-money.jpg"
  },
  {
    "title": "Rich Dad Poor Dad",
    "category": "Books",
    "price": 399,
    "brand": "Plata",
    "description": "Robert Kiyosaki \u2014 what the rich teach their kids about money",
    "image": "/images/rich-dad-poor-dad.jpg"
  },
  {
    "title": "Ikigai: The Japanese Secret",
    "category": "Books",
    "price": 299,
    "brand": "Penguin",
    "description": "The Japanese secret to a long and happy life",
    "image": "/images/ikigai-the-japanese-secret.jpg"
  },
  {
    "title": "Boldfit Yoga Mat 6mm",
    "category": "Fitness",
    "price": 599,
    "brand": "Boldfit",
    "description": "Anti-slip NBR material, 6mm thick, with carry strap",
    "image": "/images/boldfit-yoga-mat-6mm.jpg"
  },
  {
    "title": "Kore 20kg PVC Dumbbell Set",
    "category": "Fitness",
    "price": 1699,
    "brand": "Kore",
    "description": "20kg combo, PVC plates, 2 rods, gym gloves included",
    "image": "/images/kore-20kg-pvc-dumbbell-set.jpg"
  },
  {
    "title": "Fitbit Charge 6 Fitness Tracker",
    "category": "Fitness",
    "price": 14999,
    "brand": "Fitbit",
    "description": "GPS, heart rate, SpO2, stress management, 7-day battery",
    "image": "/images/fitbit-charge-6-fitness-tracker.jpg"
  },
  {
    "title": "Adidas Resistance Band Set",
    "category": "Fitness",
    "price": 1299,
    "brand": "Adidas",
    "description": "3-pack resistance bands, light/medium/heavy, latex-free",
    "image": "/images/adidas-resistance-band-set.jpg"
  },
  {
    "title": "Cockatoo Treadmill CT-01",
    "category": "Fitness",
    "price": 24999,
    "brand": "Cockatoo",
    "description": "2HP motorized treadmill, 12 programs, heart rate monitor",
    "image": "/images/cockatoo-treadmill-ct-01.jpg"
  },
  {
    "title": "Davidoff Cool Water EDT",
    "category": "Fragrances",
    "price": 2500,
    "brand": "Davidoff",
    "description": "125ml Eau De Toilette, fresh aquatic fragrance for men",
    "image": "/images/davidoff-cool-water-edt.jpg"
  },
  {
    "title": "Park Avenue Voyage Perfume",
    "category": "Fragrances",
    "price": 599,
    "brand": "Park Avenue",
    "description": "100ml EDP, oriental woody fragrance, long lasting",
    "image": "/images/park-avenue-voyage-perfume.jpg"
  },
  {
    "title": "Fogg Xtremo Scent",
    "category": "Fragrances",
    "price": 399,
    "brand": "Fogg",
    "description": "100ml body spray, no gas deodorant, intense fragrance",
    "image": "/images/fogg-xtremo-scent.jpg"
  },
  {
    "title": "Versace Pour Homme EDT",
    "category": "Fragrances",
    "price": 5500,
    "brand": "Versace",
    "description": "100ml Eau De Toilette, Mediterranean-inspired masculine scent",
    "image": "/images/versace-pour-homme-edt.jpg"
  },
  {
    "title": "Wild Stone Red Perfume",
    "category": "Fragrances",
    "price": 449,
    "brand": "Wild Stone",
    "description": "100ml EDP, seductive spicy-floral-musky fragrance",
    "image": "/images/wild-stone-red-perfume.jpg"
  },
  {
    "title": "Anker PowerCore 20000mAh",
    "category": "Electronics",
    "price": 3499,
    "brand": "Anker",
    "description": "Portable charger, 20W USB-C PD, dual output, PowerIQ",
    "image": "/images/anker-powercore-20000mah.jpg"
  },
  {
    "title": "Belkin USB-C Hub 7-in-1",
    "category": "Electronics",
    "price": 5999,
    "brand": "Belkin",
    "description": "4K HDMI, SD card, 100W pass-through charging, USB 3.0",
    "image": "/images/belkin-usb-c-hub-7-in-1.jpg"
  },
  {
    "title": "JBL Flip 6 Portable Speaker",
    "category": "Electronics",
    "price": 9999,
    "brand": "JBL",
    "description": "Wireless Bluetooth speaker, IP67 waterproof, 12hr battery",
    "image": "/images/jbl-flip-6-portable-speaker.jpg"
  },
  {
    "title": "Amazon Echo Dot 5th Gen",
    "category": "Electronics",
    "price": 4499,
    "brand": "Amazon",
    "description": "Smart speaker with Alexa, improved audio, motion detection",
    "image": "/images/amazon-echo-dot-5th-gen.jpg"
  },
  {
    "title": "Fire TV Stick 4K Max",
    "category": "Electronics",
    "price": 6499,
    "brand": "Amazon",
    "description": "4K streaming, Wi-Fi 6E, Dolby Vision/Atmos, ambient display",
    "image": "/images/fire-tv-stick-4k-max.jpg"
  },
  {
    "title": "TP-Link Deco X55 Mesh Router",
    "category": "Electronics",
    "price": 11999,
    "brand": "TP-Link",
    "description": "AX3000 Wi-Fi 6 mesh system, 3-pack, 6500 sq ft coverage",
    "image": "/images/tp-link-deco-x55-mesh-router.jpg"
  },
  {
    "title": "Sony PS5 DualSense Controller",
    "category": "Gaming",
    "price": 5990,
    "brand": "Sony",
    "description": "Wireless controller, haptic feedback, adaptive triggers",
    "image": "/images/sony-ps5-dualsense-controller.jpg"
  },
  {
    "title": "Xbox Series X Console",
    "category": "Gaming",
    "price": 49990,
    "brand": "Microsoft",
    "description": "12 TF GPU, 1TB SSD, 4K 120fps gaming, Quick Resume",
    "image": "/images/xbox-series-x-console.jpg"
  },
  {
    "title": "Nintendo Switch OLED",
    "category": "Gaming",
    "price": 34999,
    "brand": "Nintendo",
    "description": "7-inch OLED screen, 64GB, detachable Joy-Cons, tabletop mode",
    "image": "https://assets.nintendo.com/image/upload/ar_16:9,c_lpad,w_656/b_white/f_auto/q_auto/ncom/en_US/articles/2021/announcing-nintendo-switch-oled-model/Nintendo_Switch-OLED_Model-platform.png"
  },
  {
    "title": "Razer Kraken V3 Gaming Headset",
    "category": "Gaming",
    "price": 7999,
    "brand": "Razer",
    "description": "50mm TriForce drivers, THX 7.1 surround, HyperClear mic",
    "image": "/images/razer-kraken-v3-gaming-headset.jpg"
  },
  {
    "title": "SteelSeries QcK Gaming Mousepad",
    "category": "Gaming",
    "price": 999,
    "brand": "SteelSeries",
    "description": "Large cloth mousepad, micro-woven surface, non-slip rubber",
    "image": "/images/steelseries-qck-gaming-mousepad.jpg"
  },
  {
    "title": "Philips OneBlade Pro Trimmer",
    "category": "Grooming",
    "price": 3495,
    "brand": "Philips",
    "description": "Hybrid electric trimmer & shaver, 14 length settings",
    "image": "/images/philips-oneblade-pro-trimmer.jpg"
  },
  {
    "title": "Dyson Supersonic Hair Dryer",
    "category": "Grooming",
    "price": 34900,
    "brand": "Dyson",
    "description": "V9 digital motor, intelligent heat control, 5 attachments",
    "image": "/images/dyson-supersonic-hair-dryer.jpg"
  },
  {
    "title": "mCaffeine Coffee Face Wash",
    "category": "Grooming",
    "price": 349,
    "brand": "mCaffeine",
    "description": "100ml, coffee arabica extract, deep cleansing, all skin types",
    "image": "https://www.mcaffeine.com/cdn/shop/products/Coffee-Face-Wash-main.jpg?v=1234567890"
  },
  {
    "title": "Nivea Men Dark Spot Reduction",
    "category": "Grooming",
    "price": 269,
    "brand": "Nivea",
    "description": "Face moisturizer, SPF 30, 10x vitamin C, oily skin",
    "image": "/images/nivea-men-dark-spot-reduction.jpg"
  },
  {
    "title": "Oral-B Smart 6 Electric Toothbrush",
    "category": "Grooming",
    "price": 8999,
    "brand": "Oral-B",
    "description": "Bluetooth connected, 5 cleaning modes, pressure sensor",
    "image": "/images/oral-b-smart-6-electric-toothbrush.jpg"
  },
  {
    "title": "Tanishq Gold Stud Earrings",
    "category": "Jewellery",
    "price": 12999,
    "brand": "Tanishq",
    "description": "18K gold, 0.05ct diamond accent, butterfly back",
    "image": "/images/tanishq-gold-stud-earrings.jpg"
  },
  {
    "title": "Swarovski Crystal Pendant",
    "category": "Jewellery",
    "price": 7999,
    "brand": "Swarovski",
    "description": "Rhodium-plated, blue crystal pendant with chain",
    "image": "/images/swarovski-crystal-pendant.jpg"
  },
  {
    "title": "Malabar Gold Chain 22K",
    "category": "Jewellery",
    "price": 45999,
    "brand": "Malabar Gold",
    "description": "22K yellow gold, 18-inch, Italian design chain",
    "image": "/images/malabar-gold-chain-22k.jpg"
  },
  {
    "title": "GIVA Silver Ring Set",
    "category": "Jewellery",
    "price": 1299,
    "brand": "GIVA",
    "description": "Set of 3, 925 sterling silver, adjustable, anti-tarnish",
    "image": "/images/giva-silver-ring-set.jpg"
  },
  {
    "title": "CaratLane Diamond Bracelet",
    "category": "Jewellery",
    "price": 24999,
    "brand": "CaratLane",
    "description": "18K rose gold, 0.15ct diamond cluster, toggle clasp",
    "image": "/images/caratlane-diamond-bracelet.jpg"
  }
]

def generate_data():
    print("🗑️  Clearing database...")
    db_client.clear_db()

    # ─── Users ─────────────────────────────────────────────
    print("👤 Generating users...")
    users = [
        {"user_id": "user_001", "name": "Aarav Sharma",  "email": "aarav@example.com",  "password": "password123", "age": 24, "location": "Mumbai",    "avatar": "👨‍💻"},
        {"user_id": "user_002", "name": "Priya Patel",   "email": "priya@example.com",  "password": "password123", "age": 28, "location": "Bangalore", "avatar": "👩‍🎨"},
        {"user_id": "user_003", "name": "Rahul Verma",   "email": "rahul@example.com",  "password": "password123", "age": 32, "location": "Delhi",     "avatar": "👨‍🔧"},
        {"user_id": "user_004", "name": "Sneha Reddy",   "email": "sneha@example.com",  "password": "password123", "age": 22, "location": "Hyderabad", "avatar": "👩‍🎓"},
        {"user_id": "user_005", "name": "Vikram Singh",  "email": "vikram@example.com", "password": "password123", "age": 35, "location": "Pune",      "avatar": "👨‍💼"},
        {"user_id": "user_006", "name": "Ananya Gupta",  "email": "ananya@example.com", "password": "password123", "age": 27, "location": "Chennai",   "avatar": "👩‍⚕️"},
        {"user_id": "user_007", "name": "Rohit Kumar",   "email": "rohit@example.com",  "password": "password123", "age": 30, "location": "Kolkata",   "avatar": "👨‍🏫"},
        {"user_id": "user_008", "name": "Meera Joshi",   "email": "meera@example.com",  "password": "password123", "age": 26, "location": "Jaipur",    "avatar": "👩‍🍳"},
    ]
    db_client.insert_users(users)

    # ─── Items ─────────────────────────────────────────────
    print(f"🛍️  Inserting {len(PRODUCTS)} hand-curated real products...")
    items = []
    for idx, p in enumerate(PRODUCTS):
        items.append({
            "item_id": f"item_{idx+1:03d}",
            "title": p["title"],
            "category": p["category"],
            "rating": round(random.uniform(3.5, 5.0), 1),
            "price": p["price"],
            "image": p["image"],
            "description": p["description"],
            "brand": p["brand"],
        })
    db_client.insert_items(items)

    item_ids = [i["item_id"] for i in items]

    # ─── Interactions ──────────────────────────────────────
    print("🔗 Generating user interactions...")
    cat_items = {}
    for item in items:
        cat_items.setdefault(item["category"], []).append(item["item_id"])
    
    categories = list(cat_items.keys())
    interactions = []
    actions = ["view", "click", "purchase"]
    weights = [0.5, 0.3, 0.2]

    for u in users:
        primary = random.sample(categories, min(3, len(categories)))
        for _ in range(40):
            cat = random.choice(primary)
            interactions.append({
                "user_id": u["user_id"],
                "item_id": random.choice(cat_items[cat]),
                "action_type": random.choices(actions, weights=weights)[0],
                "timestamp": time.time() - random.randint(0, 30*24*3600)
            })
        for _ in range(10):
            interactions.append({
                "user_id": u["user_id"],
                "item_id": random.choice(item_ids),
                "action_type": random.choices(actions, weights=weights)[0],
                "timestamp": time.time() - random.randint(0, 30*24*3600)
            })

    db_client.insert_interactions(interactions)

    cats = sorted(set(i["category"] for i in items))
    brands = sorted(set(i["brand"] for i in items))
    print(f"\n✅ Done! {len(items)} real products, {len(cats)} categories, {len(brands)} brands")
    print(f"   Categories: {', '.join(cats)}")
    print(f"   Sample brands: {', '.join(brands[:12])}...")
    print(f"   {len(users)} users, {len(interactions)} interactions")


if __name__ == "__main__":
    generate_data()
