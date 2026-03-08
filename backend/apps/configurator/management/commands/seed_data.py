"""
Seed data — realistyczne moduly Black Light Collective.
Uruchom: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.configurator.models import (
    SceneTemplate, ComponentCategory, Component, Order, OrderItem,
)
from apps.portfolio.models import (
    TeamMember, Festival, Project, ProjectImage, Testimonial,
)
from apps.shop.models import ProductCategory, Product, Coupon
from decimal import Decimal
from datetime import date, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = "Zaladuj przykladowe dane Black Light Collective"

    def handle(self, *args, **options):
        self.stdout.write("Laduje dane Black Light Collective...")
        self._users()
        self._team()
        self._festivals()
        self._projects()
        self._testimonials()
        self._configurator()
        self._shop()
        self._orders()
        self.stdout.write(self.style.SUCCESS("Dane zaladowane!"))

    # ---------- USERS ----------
    def _users(self):
        self.stdout.write("  Uzytkownicy...")
        a, _ = User.objects.get_or_create(username="admin", defaults={
            "email": "admin@blacklight-collective.pl", "role": "admin",
            "first_name": "Admin", "last_name": "Black Light",
            "is_staff": True, "is_superuser": True,
        })
        a.set_password("admin123!"); a.save()
        for u, e, fn, ln in [
            ("kasia.led","kasia@blacklight.pl","Katarzyna","Swietlna"),
            ("marek.bass","marek@blacklight.pl","Marek","Basski"),
            ("ola.deko","ola@blacklight.pl","Aleksandra","Dekowska"),
            ("piotr.vfx","piotr@blacklight.pl","Piotr","Efektowski"),
        ]:
            o, _ = User.objects.get_or_create(username=u, defaults={"email":e,"first_name":fn,"last_name":ln,"role":"member"})
            o.set_password("member123!"); o.save()
        for u, e, fn, ln in [
            ("jan.kowalski","jan@fest.pl","Jan","Kowalski"),
            ("anna.nowak","anna@bass.pl","Anna","Nowak"),
            ("tomek.dj","tomek@night.pl","Tomek","Sowinski"),
        ]:
            o, _ = User.objects.get_or_create(username=u, defaults={"email":e,"first_name":fn,"last_name":ln,"role":"client"})
            o.set_password("client123!"); o.save()

    # ---------- TEAM ----------
    def _team(self):
        self.stdout.write("  Zespol...")
        for t in [
            {"name":"Jakub Black Light","role":"Founder & Creative Director","bio":"Zalozyciel Black Light Collective. 12 lat doswiadczenia w scenografiach festiwalowych.","order":0},
            {"name":"Katarzyna Swietlna","role":"Light Designer","bio":"Specjalistka od oswietlenia z 8-letnim doswiadczeniem.","order":1},
            {"name":"Marek Basski","role":"Sound & Stage Engineer","bio":"Inzynier dzwieku i konstruktor scen.","order":2},
            {"name":"Aleksandra Dekowska","role":"Art Director","bio":"Projektantka dekoracji scenicznych.","order":3},
            {"name":"Piotr Efektowski","role":"VFX & Laser Artist","bio":"Artysta laserowy i specjalista od efektow.","order":4},
            {"name":"Weronika Pixel","role":"LED & Mapping Specialist","bio":"Projektantka mappingu video i instalacji LED.","order":5},
        ]:
            TeamMember.objects.get_or_create(name=t["name"], defaults=t)

    # ---------- FESTIVALS ----------
    def _festivals(self):
        self.stdout.write("  Festiwale...")
        for f in [
            {"name":"Audioriver","location":"Plock, Polska"},
            {"name":"Up To Date","location":"Bialystok, Polska"},
            {"name":"Tauron Nowa Muzyka","location":"Katowice, Polska"},
            {"name":"Unsound","location":"Krakow, Polska"},
            {"name":"Instytut Festival","location":"Warszawa, Polska"},
            {"name":"Fest Festival","location":"Chorzow, Polska"},
            {"name":"Plotzlich am Meer","location":"Rostock, Niemcy"},
            {"name":"Contrast Festival","location":"Wroclaw, Polska"},
        ]:
            Festival.objects.get_or_create(name=f["name"], defaults=f)

    # ---------- PROJECTS ----------
    def _projects(self):
        self.stdout.write("  Projekty...")
        fests = {f.name: f for f in Festival.objects.all()}
        for p in [
            {"title":"Neon Cathedral","slug":"neon-cathedral","short_description":"Main stage Audioriver 2024","description":"Monumentalna instalacja swietlna inspirowana gotyckimi katedrami. 200m LED strips, 40 ruchomych glowic.","festival":fests.get("Audioriver"),"date":date(2024,7,26),"category":"main_stage","is_featured":True,"technologies":"LED RGBW, Moving Heads, Laser RGB 10W, Truss H8"},
            {"title":"Deep Forest Stage","slug":"deep-forest-stage","short_description":"Side stage Up To Date 2024","description":"Immersyjna scena lesna z 30 sztucznymi drzewami LED, systemem mgly i UV.","festival":fests.get("Up To Date"),"date":date(2024,9,6),"category":"side_stage","is_featured":True,"technologies":"Custom LED Trees, Low Fog, UV"},
            {"title":"Void Chamber","slug":"void-chamber","short_description":"Laserowa komora techno","description":"Minimalistyczna przestrzen techno — 80 laserow i gesta mgla.","festival":fests.get("Instytut Festival"),"date":date(2024,11,15),"category":"full_production","is_featured":True,"technologies":"Laser RGB 5W x80, Hazer"},
            {"title":"Ocean Pulse","slug":"ocean-pulse","short_description":"Scena nadmorska PAM 2024","description":"Nadmorska scena z falujacymi panelami LED imitujacymi ocean.","festival":fests.get("Plotzlich am Meer"),"date":date(2024,8,10),"category":"main_stage","is_featured":False,"technologies":"Flexible LED, Water FX"},
            {"title":"Neon Jungle","slug":"neon-jungle","short_description":"Neonowa dzungla Tauron 2024","description":"Tropikalna dzungla w neonowych kolorach z gigantycznymi liscmi z RGB LED.","festival":fests.get("Tauron Nowa Muzyka"),"date":date(2024,8,23),"category":"art_installation","is_featured":True,"technologies":"Custom LED flora, EL Wire, UV"},
            {"title":"Crystal Grid","slug":"crystal-grid","short_description":"Unsound 2024","description":"Geometryczna instalacja z 500 akrylowych pryzmatow.","festival":fests.get("Unsound"),"date":date(2024,10,12),"category":"art_installation","is_featured":False,"technologies":"Acrylic prisms, Addressable LED"},
            {"title":"Bass Bunker","slug":"bass-bunker","short_description":"Contrast 2024","description":"Surowa industrialna scena bass music.","festival":fests.get("Contrast Festival"),"date":date(2024,10,5),"category":"full_production","is_featured":False,"technologies":"Industrial structures, Strobes"},
        ]:
            Project.objects.get_or_create(slug=p["slug"], defaults=p)

    # ---------- TESTIMONIALS ----------
    def _testimonials(self):
        self.stdout.write("  Opinie...")
        projects = list(Project.objects.all())
        for i, t in enumerate([
            {"author":"Michal Kowalczyk","role":"Dyr. artystyczny, Audioriver","content":"Black Light to najlepsza ekipa od scenografii w Polsce.","rating":5},
            {"author":"Agata Wisniewska","role":"Organizatorka, Up To Date","content":"Deep Forest Stage byl absolutnym hitem festiwalu.","rating":5},
            {"author":"Tomek DJ Owl","role":"Rezydent, Instytut","content":"Granie w Void Chamber to doswiadczenie nie z tego swiata.","rating":5},
            {"author":"Hans Mueller","role":"Founder, PAM","content":"Polish team, German precision. Ocean Pulse was amazing.","rating":5},
            {"author":"Kinga Zielinska","role":"PR, Tauron NM","content":"Neon Jungle to instalacja ktora zyje wlasnym zyciem.","rating":4},
        ]):
            t["project"] = projects[i] if i < len(projects) else None
            Testimonial.objects.get_or_create(author=t["author"], defaults=t)

    # ---------- CONFIGURATOR ----------
    def _configurator(self):
        self.stdout.write("  Konfigurator...")
        # Templates
        for t in [
            {"name":"Main Stage","slug":"main-stage","description":"Glowna scena festiwalowa","base_price":Decimal("5000"),"width":30,"depth":20,"height":10},
            {"name":"Techno Bunker","slug":"techno-bunker","description":"Zamknieta ciemna przestrzen na raw techno","base_price":Decimal("3000"),"width":15,"depth":12,"height":5},
            {"name":"Forest Stage","slug":"forest-stage","description":"Scena lesna na ambient i organic house","base_price":Decimal("4000"),"width":20,"depth":15,"height":8},
            {"name":"Beach Stage","slug":"beach-stage","description":"Otwarta scena plazowa","base_price":Decimal("3500"),"width":25,"depth":18,"height":6},
        ]:
            SceneTemplate.objects.get_or_create(slug=t["slug"], defaults=t)

        # Categories
        cats = {}
        for c in [
            {"name":"Obiekty UFO","slug":"ufo","icon":"\U0001f6f8","color":"#00ff88","order":1,"description":"Podwieszane obiekty UFO z LED"},
            {"name":"Las / Drzewa","slug":"las","icon":"\U0001f332","color":"#22c55e","order":2,"description":"Sztuczne drzewa i rosliny z LED"},
            {"name":"Lasery","slug":"lasery","icon":"\u2728","color":"#ef4444","order":3,"description":"Systemy laserowe"},
            {"name":"Oswietlenie LED","slug":"led","icon":"\U0001f4a1","color":"#8b5cf6","order":4,"description":"Panele LED, wash, strip, pixel tubes"},
            {"name":"Konstrukcje","slug":"konstrukcje","icon":"\U0001f527","color":"#f59e0b","order":5,"description":"Trussy, totemy, konstrukcje"},
            {"name":"Efekty specjalne","slug":"efekty","icon":"\U0001f4a8","color":"#06b6d4","order":6,"description":"Mgla, dym, CO2, confetti"},
        ]:
            obj, _ = ComponentCategory.objects.get_or_create(slug=c["slug"], defaults=c)
            cats[c["slug"]] = obj

        # Components (modules)
        modules = [
            # UFO
            {"category":cats["ufo"],"name":"Ufo 1","slug":"ufo-1","description":"Maly obiekt UFO diam.2m z LED RGB. Idealny jako element dekoracyjny.","short_desc":"Maly UFO diam.2m, LED RGB","price":Decimal("1500"),"icon_name":"ufo","color":"#00ff88","width_m":2,"depth_m":2,"power_consumption":200,"weight_kg":15,"max_quantity":10,"specs":{"diameter":"2m","led":"RGB"}},
            {"category":cats["ufo"],"name":"Ufo 2","slug":"ufo-2","description":"Duzy obiekt UFO diam.4m z LED RGBW + laser. Glowny element wizualny sceny.","short_desc":"Duzy UFO diam.4m, RGBW+laser","price":Decimal("3500"),"icon_name":"ufo","color":"#00ffaa","width_m":4,"depth_m":4,"power_consumption":500,"weight_kg":45,"max_quantity":6,"specs":{"diameter":"4m","led":"RGBW","laser":"1W"}},
            {"category":cats["ufo"],"name":"Ufo 3 Mega","slug":"ufo-3-mega","description":"Mega UFO diam.6m — flagowy obiekt Black Light. Full RGBW, laser 3W, rotacja.","short_desc":"Mega UFO diam.6m, full show","price":Decimal("6000"),"icon_name":"ufo","color":"#00ffcc","width_m":6,"depth_m":6,"power_consumption":1200,"weight_kg":80,"max_quantity":3,"specs":{"diameter":"6m","led":"RGBW","laser":"3W","rotation":True}},
            # LAS
            {"category":cats["las"],"name":"Las 1","slug":"las-1","description":"Maly set lesny — 3 drzewa LED (wys. 3m) z pniami i konarami.","short_desc":"3 drzewa LED, 3m","price":Decimal("2000"),"icon_name":"tree","color":"#22c55e","width_m":4,"depth_m":3,"power_consumption":300,"weight_kg":60,"max_quantity":8,"specs":{"trees":3,"height":"3m"}},
            {"category":cats["las"],"name":"Las 2","slug":"las-2","description":"Duzy set lesny — 6 drzew LED (3-5m) z gestymi koronami.","short_desc":"6 drzew LED, 3-5m","price":Decimal("4500"),"icon_name":"tree","color":"#16a34a","width_m":6,"depth_m":5,"power_consumption":600,"weight_kg":140,"max_quantity":5,"specs":{"trees":6,"height":"3-5m"}},
            {"category":cats["las"],"name":"Las 3 Enchanted","slug":"las-3-enchanted","description":"Enchanted Forest — 10 drzew LED + mgla + UV + pixel tubes.","short_desc":"10 drzew + mgla + UV","price":Decimal("8000"),"icon_name":"tree","color":"#15803d","width_m":10,"depth_m":8,"power_consumption":1500,"weight_kg":300,"max_quantity":2,"specs":{"trees":10,"fog":True,"uv":True}},
            # LASERY
            {"category":cats["lasery"],"name":"Laser RGB Compact","slug":"laser-rgb-compact","description":"Kompaktowy laser RGB 1W — idealny do malych scen.","short_desc":"Laser RGB 1W","price":Decimal("800"),"icon_name":"laser","color":"#ef4444","width_m":1,"depth_m":1,"power_consumption":150,"weight_kg":5,"max_quantity":20,"specs":{"power":"1W","color":"RGB"}},
            {"category":cats["lasery"],"name":"Laser Show 5W","slug":"laser-show-5w","description":"Profesjonalny laser show 5W Full Color.","short_desc":"Laser show 5W","price":Decimal("2500"),"icon_name":"laser","color":"#dc2626","width_m":1,"depth_m":1,"power_consumption":400,"weight_kg":12,"max_quantity":10,"specs":{"power":"5W","color":"Full RGBYW"}},
            {"category":cats["lasery"],"name":"Laser Bar Multi","slug":"laser-bar-multi","description":"Listwa laserowa z 8 glowicami — sciana laserow.","short_desc":"8-glowicowa listwa","price":Decimal("3000"),"icon_name":"laser","color":"#f87171","width_m":3,"depth_m":1,"power_consumption":600,"weight_kg":18,"max_quantity":6,"specs":{"heads":8}},
            # LED
            {"category":cats["led"],"name":"Panel LED P3.9","slug":"panel-led-p39","description":"Indoor LED panel 50x50cm do VJ contentu.","short_desc":"Panel LED 50x50cm","price":Decimal("600"),"icon_name":"led-panel","color":"#8b5cf6","width_m":1,"depth_m":1,"power_consumption":200,"weight_kg":8,"max_quantity":50,"specs":{"pixel_pitch":"3.9mm"}},
            {"category":cats["led"],"name":"LED Wash 360","slug":"led-wash-360","description":"Ruchoma glowica LED wash RGBW z zoomem.","short_desc":"Moving Head Wash","price":Decimal("900"),"icon_name":"led-wash","color":"#a78bfa","width_m":1,"depth_m":1,"power_consumption":350,"weight_kg":14,"max_quantity":20,"specs":{"led":"19x15W RGBW"}},
            {"category":cats["led"],"name":"Pixel Tube 1m","slug":"pixel-tube-1m","description":"Pikselowa tuba LED 1m — reaguje na muzyke.","short_desc":"Tuba LED 1m","price":Decimal("200"),"icon_name":"pixel-tube","color":"#c4b5fd","width_m":1,"depth_m":1,"power_consumption":20,"weight_kg":1,"max_quantity":100,"specs":{"pixels":16}},
            {"category":cats["led"],"name":"LED Strip RGBW 5m","slug":"led-strip-5m","description":"Tasma LED RGBW 5m IP65.","short_desc":"Tasma RGBW 5m","price":Decimal("150"),"icon_name":"led-strip","color":"#7c3aed","width_m":5,"depth_m":1,"power_consumption":60,"weight_kg":Decimal("0.5"),"max_quantity":100,"specs":{"length":"5m","ip":"IP65"}},
            # KONSTRUKCJE
            {"category":cats["konstrukcje"],"name":"Truss kwadrat 3x3m","slug":"truss-kwadrat-3x3","description":"Aluminiowa kratownica 3x3m.","short_desc":"Kratownica 3x3m","price":Decimal("800"),"icon_name":"truss","color":"#f59e0b","width_m":3,"depth_m":3,"power_consumption":0,"weight_kg":50,"max_quantity":10,"specs":{"material":"Aluminium"}},
            {"category":cats["konstrukcje"],"name":"Truss luk 6m","slug":"truss-luk-6m","description":"Lukowa konstrukcja trussowa 6m.","short_desc":"Luk trussowy 6m","price":Decimal("1500"),"icon_name":"truss-arch","color":"#d97706","width_m":6,"depth_m":2,"power_consumption":0,"weight_kg":80,"max_quantity":4,"specs":{"span":"6m","height":"4m"}},
            {"category":cats["konstrukcje"],"name":"Totem LED 3m","slug":"totem-led-3m","description":"Wolnostojacy totem z panelami LED.","short_desc":"Totem LED 3m","price":Decimal("1200"),"icon_name":"totem","color":"#fbbf24","width_m":1,"depth_m":1,"power_consumption":300,"weight_kg":35,"max_quantity":12,"specs":{"height":"3m","sides":4}},
            # EFEKTY
            {"category":cats["efekty"],"name":"Wytwornica dymu","slug":"wytwornica-dymu","description":"Profesjonalna wytwornica dymu 3000W.","short_desc":"Hazer 3000W","price":Decimal("400"),"icon_name":"fog","color":"#06b6d4","width_m":1,"depth_m":1,"power_consumption":3000,"weight_kg":15,"max_quantity":10,"specs":{"power":"3000W"}},
            {"category":cats["efekty"],"name":"Mgla ciezka (Low Fog)","slug":"low-fog","description":"Generator mgly ciezkiej — efekt dymu przy podlodze.","short_desc":"Low fog","price":Decimal("600"),"icon_name":"low-fog","color":"#0891b2","width_m":2,"depth_m":1,"power_consumption":1500,"weight_kg":25,"max_quantity":6,"specs":{"type":"Low Fog"}},
            {"category":cats["efekty"],"name":"CO2 Jet","slug":"co2-jet","description":"Wyrzutnia CO2 — slup bialego gazu do 8m.","short_desc":"CO2 cryo jet 8m","price":Decimal("500"),"icon_name":"co2","color":"#67e8f9","width_m":1,"depth_m":1,"power_consumption":50,"weight_kg":10,"max_quantity":10,"specs":{"height":"8m"}},
            {"category":cats["efekty"],"name":"Confetti Launcher","slug":"confetti-launcher","description":"Wyrzutnia konfetti.","short_desc":"Confetti elektryczne","price":Decimal("350"),"icon_name":"confetti","color":"#22d3ee","width_m":1,"depth_m":1,"power_consumption":100,"weight_kg":5,"max_quantity":8,"specs":{"range":"12m"}},
        ]
        for m in modules:
            Component.objects.get_or_create(slug=m["slug"], defaults=m)

    # ---------- SHOP ----------
    def _shop(self):
        self.stdout.write("  Sklep...")
        for c in [
            {"name":"Odziez","slug":"odziez","description":"Koszulki, bluzy Black Light"},
            {"name":"Akcesoria","slug":"akcesoria","description":"Naklejki, plakaty"},
        ]:
            ProductCategory.objects.get_or_create(slug=c["slug"], defaults=c)
        cats = {c.slug: c for c in ProductCategory.objects.all()}
        for p in [
            {"name":"T-shirt Black Light Logo","slug":"tshirt-logo","category":cats.get("odziez"),"description":"Czarny t-shirt z neonowym logo","price":Decimal("89"),"sku":"TSH-001","stock":50,"is_featured":True},
            {"name":"Hoodie Neon Grid","slug":"hoodie-neon","category":cats.get("odziez"),"description":"Bluza z kapturem neon grid","price":Decimal("189"),"sku":"HOD-001","stock":30,"is_featured":True},
            {"name":"Sticker Pack","slug":"sticker-pack","category":cats.get("akcesoria"),"description":"10 holograficznych naklejek","price":Decimal("25"),"sku":"STK-001","stock":200},
        ]:
            Product.objects.get_or_create(slug=p["slug"], defaults=p)
        Coupon.objects.get_or_create(code="BLACK LIGHT10", defaults={"discount_percent":10,"is_active":True,"valid_from":date.today(),"valid_until":date.today()+timedelta(days=365)})

    # ---------- ORDERS ----------
    def _orders(self):
        self.stdout.write("  Zamowienia...")
        jan = User.objects.filter(username="jan.kowalski").first()
        if not jan: return
        tmpl = SceneTemplate.objects.first()
        comps = list(Component.objects.all()[:4])
        order, created = Order.objects.get_or_create(
            user=jan, event_name="Sylwester w Hangarze",
            defaults={"template":tmpl,"status":"submitted","event_date":date(2025,12,31),"event_location":"Hangar 646, Warszawa","expected_audience":2000,"notes":"Duze UFO + las po bokach"}
        )
        if created:
            for c in comps:
                OrderItem.objects.create(order=order,component=c,quantity=2,unit_price=c.price,subtotal=c.price*2)
            order.recalculate_total()
