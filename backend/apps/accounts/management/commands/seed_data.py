"""
BLACK LIGHT Collective — Pełne dane przykładowe
Użycie: python manage.py seed_data
        python manage.py seed_data --flush  (wyczyść i załaduj od nowa)
"""
from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import CustomUser, UserAddress
from apps.portfolio.models import Festival, TeamMember, Project, ProjectImage, Testimonial
from apps.configurator.models import SceneTemplate, ComponentCategory, Component, Order, OrderItem
from apps.shop.models import ProductCategory, Product, ProductImage as ShopProductImage, Coupon, ShopOrder, ShopOrderItem


class Command(BaseCommand):
    help = 'Ładuje przykładowe dane do bazy BLACK LIGHT Collective'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='Wyczyść istniejące dane przed załadowaniem',
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write(self.style.WARNING('⚠️  Czyszczenie istniejących danych...'))
            self._flush()

        self.stdout.write(self.style.NOTICE('🚀 Ładowanie danych BLACK LIGHT Collective...'))
        self._create_users()
        self._create_team()
        self._create_festivals()
        self._create_projects()
        self._create_testimonials()
        self._create_configurator()
        self._create_shop()
        self._create_orders()
        self.stdout.write(self.style.SUCCESS('✅ Dane załadowane pomyślnie!'))

    def _flush(self):
        """Wyczyść wszystkie dane (oprócz superuserów)."""
        ShopOrderItem.objects.all().delete()
        ShopOrder.objects.all().delete()
        Coupon.objects.all().delete()
        ShopProductImage.objects.all().delete()
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Component.objects.all().delete()
        ComponentCategory.objects.all().delete()
        SceneTemplate.objects.all().delete()
        Testimonial.objects.all().delete()
        ProjectImage.objects.all().delete()
        Project.objects.all().delete()
        Festival.objects.all().delete()
        TeamMember.objects.all().delete()
        UserAddress.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()
        self.stdout.write('   Dane wyczyszczone.')

    # =========================================================================
    # USERS
    # =========================================================================
    def _create_users(self):
        self.stdout.write('👤 Tworzenie użytkowników...')

        # Admin
        self.admin, _ = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.pl',
                'first_name': 'Admin',
                'last_name': 'BLACK LIGHT',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'phone': '+48 500 100 200',
                'bio': 'Główny administrator platformy BLACK LIGHT Collective.',
                'company': 'BLACK LIGHT Collective',
                'website': 'https://blacklight-collective.pl',
            }
        )
        self.admin.set_password('admin123!')
        self.admin.save()

        # Członkowie zespołu
        members_data = [
            {
                'username': 'kasia.led',
                'email': 'kasia@blacklight-collective.pl',
                'first_name': 'Katarzyna',
                'last_name': 'Ledóchowska',
                'role': 'member',
                'phone': '+48 501 111 111',
                'bio': 'Lead Light Designer z 8-letnim doświadczeniem w projektowaniu oświetlenia festiwalowego. Specjalizacja: systemy laserowe i mapping.',
                'company': 'BLACK LIGHT Collective',
            },
            {
                'username': 'marek.bass',
                'email': 'marek@blacklight-collective.pl',
                'first_name': 'Marek',
                'last_name': 'Basiewicz',
                'role': 'member',
                'phone': '+48 502 222 222',
                'bio': 'Sound Engineer & Stage Designer. 10 lat doświadczenia z systemami Funktion-One, d&b audiotechnik.',
                'company': 'BLACK LIGHT Collective',
            },
            {
                'username': 'ola.deko',
                'email': 'ola@blacklight-collective.pl',
                'first_name': 'Aleksandra',
                'last_name': 'Dekowska',
                'role': 'member',
                'phone': '+48 503 333 333',
                'bio': 'Art Director & Decoration Designer. Tworzę immersyjne przestrzenie festiwalowe łączące naturę z technologią.',
                'company': 'BLACK LIGHT Collective',
            },
            {
                'username': 'piotr.vfx',
                'email': 'piotr@blacklight-collective.pl',
                'first_name': 'Piotr',
                'last_name': 'Visualski',
                'role': 'member',
                'phone': '+48 504 444 444',
                'bio': 'VFX Artist & Projection Mapper. Tworzę wizualizacje real-time w TouchDesigner i Resolume.',
                'company': 'BLACK LIGHT Collective',
            },
        ]

        self.members = []
        for data in members_data:
            user, _ = CustomUser.objects.get_or_create(
                username=data['username'],
                defaults=data,
            )
            user.set_password('member123!')
            user.save()
            self.members.append(user)

        # Klienci
        clients_data = [
            {
                'username': 'jan.kowalski',
                'email': 'jan.kowalski@festmanager.pl',
                'first_name': 'Jan',
                'last_name': 'Kowalski',
                'role': 'client',
                'phone': '+48 600 111 222',
                'bio': 'Organizator festiwali muzycznych od 15 lat.',
                'company': 'FestManager Sp. z o.o.',
                'website': 'https://festmanager.pl',
            },
            {
                'username': 'anna.nowak',
                'email': 'anna.nowak@bassculture.pl',
                'first_name': 'Anna',
                'last_name': 'Nowak',
                'role': 'client',
                'phone': '+48 601 333 444',
                'bio': 'CEO Bass Culture Events. Organizujemy eventy techno i house w całej Polsce.',
                'company': 'Bass Culture Events',
                'website': 'https://bassculture.pl',
            },
            {
                'username': 'tomek.dj',
                'email': 'tomek@nightowl.pl',
                'first_name': 'Tomasz',
                'last_name': 'Nocny',
                'role': 'client',
                'phone': '+48 602 555 666',
                'bio': 'DJ i promotor eventów. Szukam wyjątkowych scenografii.',
                'company': 'Night Owl Events',
            },
        ]

        self.clients = []
        for data in clients_data:
            user, _ = CustomUser.objects.get_or_create(
                username=data['username'],
                defaults=data,
            )
            user.set_password('client123!')
            user.save()
            self.clients.append(user)

        # Adresy
        addresses = [
            (self.clients[0], 'Biuro', 'ul. Festiwalowa 15', 'Warszawa', '00-001'),
            (self.clients[0], 'Magazyn', 'ul. Składowa 42', 'Łódź', '90-001'),
            (self.clients[1], 'Siedziba', 'ul. Basowa 7/3', 'Kraków', '30-001'),
            (self.clients[2], 'Dom', 'ul. Nocna 23', 'Wrocław', '50-001'),
        ]
        for user, label, street, city, postal in addresses:
            UserAddress.objects.get_or_create(
                user=user, label=label,
                defaults={'street': street, 'city': city, 'postal_code': postal, 'is_default': label in ('Biuro', 'Siedziba', 'Dom')},
            )

        self.stdout.write(f'   ✅ {CustomUser.objects.count()} użytkowników, {UserAddress.objects.count()} adresów')

    # =========================================================================
    # TEAM MEMBERS (portfolio)
    # =========================================================================
    def _create_team(self):
        self.stdout.write('🎭 Tworzenie członków zespołu...')

        team_data = [
            {
                'name': 'Katarzyna Ledóchowska',
                'role': 'Lead Light Designer',
                'bio': 'Kasia to serce naszego działu oświetlenia. Z 8-letnim doświadczeniem w projektowaniu systemów laserowych i oświetlenia architektonicznego, tworzy niezapomniane pokazy świetlne na największych festiwalach w Europie. Absolwentka ASP w Krakowie, łączy artystyczną wrażliwość z techniczną precyzją.',
                'email': 'kasia@blacklight-collective.pl',
                'instagram': 'https://instagram.com/kasia.lights',
                'behance': 'https://behance.net/kasialedochowska',
                'order': 1,
            },
            {
                'name': 'Marek Basiewicz',
                'role': 'Sound Engineer & Stage Architect',
                'bio': 'Marek projektuje sceny od fundamentów po wieże dźwiękowe. Certyfikowany inżynier Funktion-One i d&b audiotechnik. Zrealizował ponad 200 scen na festiwalach w Polsce, Niemczech i Holandii. Pasjonat psychoakustyki i systemów wielokanałowych.',
                'email': 'marek@blacklight-collective.pl',
                'instagram': 'https://instagram.com/marek.bass',
                'linkedin': 'https://linkedin.com/in/marekbasiewicz',
                'order': 2,
            },
            {
                'name': 'Aleksandra Dekowska',
                'role': 'Art Director & Decoration Designer',
                'bio': 'Ola zamienia festiwalowe pola w magiczne krainy. Specjalizuje się w dekoracjach UV, instalacjach kinetycznych i scenografiach inspirowanych naturą. Współpracowała z Burning Man, Fusion Festival i Audioriver.',
                'email': 'ola@blacklight-collective.pl',
                'instagram': 'https://instagram.com/ola.deko.art',
                'behance': 'https://behance.net/oladekowska',
                'order': 3,
            },
            {
                'name': 'Piotr Visualski',
                'role': 'VFX Artist & Projection Mapper',
                'bio': 'Piotr tworzy wizualizacje real-time, które żyją w rytm muzyki. Ekspert TouchDesigner, Resolume Arena i Notch. Jego projection mappingi pokryły elewacje budynków w 12 krajach. Twórca autorskiego systemu generatywnych wizualizacji SYNTH_VIS.',
                'email': 'piotr@blacklight-collective.pl',
                'instagram': 'https://instagram.com/piotr.vfx',
                'linkedin': 'https://linkedin.com/in/piotrvisualski',
                'order': 4,
            },
            {
                'name': 'Zuza Woltażowa',
                'role': 'Technical Producer & Project Manager',
                'bio': 'Zuza koordynuje całe produkcje — od koncepcji po demontaż. Z wykształcenia inżynier elektryk, z powołania — strażniczka terminów i budżetów. Zarządza logistyką sprzętu wartego miliony złotych.',
                'email': 'zuza@blacklight-collective.pl',
                'instagram': 'https://instagram.com/zuza.blacklight',
                'linkedin': 'https://linkedin.com/in/zuzawoltazowa',
                'order': 5,
            },
            {
                'name': 'Bartek Pyroński',
                'role': 'Pyrotechnics & Special Effects',
                'bio': 'Bartek to nasz specjalista od efektów specjalnych — ogień, CO2, confetti, zimne ognie. Licencjonowany pirotechnik z uprawnieniami do widowisk scenicznych. Dba o to, żeby każdy drop na festiwalu miał swoje WOW.',
                'email': 'bartek@blacklight-collective.pl',
                'instagram': 'https://instagram.com/bartek.pyro',
                'order': 6,
            },
        ]

        for data in team_data:
            TeamMember.objects.get_or_create(name=data['name'], defaults=data)

        self.stdout.write(f'   ✅ {TeamMember.objects.count()} członków zespołu')

    # =========================================================================
    # FESTIVALS
    # =========================================================================
    def _create_festivals(self):
        self.stdout.write('🎪 Tworzenie festiwali...')

        festivals_data = [
            {
                'name': 'Audioriver Festival',
                'location': 'Płock, Polska',
                'website': 'https://audioriver.pl',
                'description': 'Jeden z największych festiwali muzyki elektronicznej w Polsce, odbywający się nad Wisłą w Płocku. Trzy dni, cztery sceny, tysiące uczestników.',
            },
            {
                'name': 'Up To Date Festival',
                'location': 'Białystok, Polska',
                'website': 'https://uptodate.pl',
                'description': 'Festiwal muzyki elektronicznej i sztuki w Białymstoku. Znany z eksperymentalnego podejścia do scenografii i programu artystycznego.',
            },
            {
                'name': 'Tauron Nowa Muzyka',
                'location': 'Katowice, Polska',
                'website': 'https://nowamuzyka.pl',
                'description': 'Festiwal w postindustrialnych przestrzeniach Katowic. Łączy muzykę elektroniczną z awangardą, sztuką współczesną i architekturą.',
            },
            {
                'name': 'Instytut Festival',
                'location': 'Państwowe Muzeum Auschwitz, Oświęcim → przeniesiony do Krakowa',
                'website': 'https://instytutfestival.pl',
                'description': 'Kameralny festiwal techno znany z wyjątkowej atmosfery i dbałości o detale scenograficzne.',
            },
            {
                'name': 'Sunrise Festival',
                'location': 'Kołobrzeg, Polska',
                'website': 'https://sunrisefestival.pl',
                'description': 'Największy festiwal muzyki tanecznej nad polskim morzem. Epickie sceny, pokazy laserowe i fajerwerki.',
            },
            {
                'name': 'Fest Festival',
                'location': 'Chorzów, Polska',
                'website': 'https://festfestival.pl',
                'description': 'Wielogatunkowy festiwal w Parku Śląskim z mocnym line-upem elektronicznym i spektakularnymi scenami.',
            },
            {
                'name': 'Unsound Festival',
                'location': 'Kraków, Polska',
                'website': 'https://unsound.pl',
                'description': 'Awangardowy festiwal muzyki elektronicznej i eksperymentalnej. Międzynarodowa renoma, unikalne lokacje.',
            },
            {
                'name': 'Sonar Festival',
                'location': 'Barcelona, Hiszpania',
                'website': 'https://sonar.es',
                'description': 'Legendarny festiwal muzyki elektronicznej i sztuki cyfrowej w Barcelonie. Punkt odniesienia dla całej branży.',
            },
        ]

        self.festivals = []
        for data in festivals_data:
            fest, _ = Festival.objects.get_or_create(name=data['name'], defaults=data)
            self.festivals.append(fest)

        self.stdout.write(f'   ✅ {Festival.objects.count()} festiwali')

    # =========================================================================
    # PROJECTS
    # =========================================================================
    def _create_projects(self):
        self.stdout.write('🎨 Tworzenie projektów portfolio...')

        today = date.today()
        projects_data = [
            {
                'title': 'NEON CATHEDRAL — Main Stage Audioriver 2025',
                'slug': 'neon-cathedral-audioriver-2025',
                'description': 'Monumentalna scena główna inspirowana gotycką architekturą, przetworzona przez pryzmat cyberpunku. 30-metrowa konstrukcja z 500 ruchomymi głowicami LED, systemem laserowym 80W i projection mappingiem na 400m² powierzchni. Konstrukcja zawierała 12 łuków świetlnych tworzących "nawę" katedry, w której publiczność stawała się częścią instalacji.',
                'short_description': 'Gotycki cyberpunk — 30m scena z 500 LED-ami i mappingiem 400m²',
                'festival': self.festivals[0],
                'client': 'FestManager Sp. z o.o.',
                'date': today - timedelta(days=120),
                'category': 'main_stage',
                'is_featured': True,
                'technologies': 'Martin MAC Aura XB ×120, Robe MegaPointe ×60, Kvant laser 80W RGB ×4, Disguise D3 ×2, TouchDesigner, Funktion-One Vero VX ×48, konstrukcja aluminiowa Prolyte H40V 180t',
            },
            {
                'title': 'DEEP FOREST — Techno Stage Up To Date',
                'slug': 'deep-forest-utd-2025',
                'description': 'Organiczna scena techno zanurzona w leśnej scenerii. Żywe drzewa wplecione w konstrukcję stalową, oświetlenie UV reagujące na dźwięk, mgła niskopoziomowa i system ambisoniczny 360°. Dekoracje z recyklingowanych materiałów — stare kable, płyty CD, elementy elektroniczne tworzące "technologiczny las".',
                'short_description': 'Organiczna scena techno w leśnej scenerii z UV i dźwiękiem 360°',
                'festival': self.festivals[1],
                'client': 'Bass Culture Events',
                'date': today - timedelta(days=90),
                'category': 'full_production',
                'is_featured': True,
                'technologies': 'Chauvet COLORado ×80, UV flood 400W ×40, Antari HZ-500 ×8, d&b audiotechnik SL-Series ambisonic, Resolume Arena 7, DMX pixel tape 2000m',
            },
            {
                'title': 'VOID CHAMBER — Instalacja Tauron Nowa Muzyka',
                'slug': 'void-chamber-tnm-2025',
                'description': 'Immersyjna instalacja artystyczna w postindustrialnej hali. Pokój o wymiarach 15×15×8m, w pełni pokryty czarnym materiałem, z 2000 punktowych źródeł LED sterowanych algorytmicznie. Dźwięk przestrzenny 22.2 tworzący wrażenie "wnętrza maszyny". Publiczność wchodzi w absolutną ciemność, a światło i dźwięk budują narrację.',
                'short_description': 'Immersyjna instalacja — 2000 LED-ów, dźwięk 22.2, absolutna ciemność',
                'festival': self.festivals[2],
                'client': 'Tauron Nowa Muzyka',
                'date': today - timedelta(days=60),
                'category': 'art_installation',
                'is_featured': True,
                'technologies': 'Pixel LED WS2812B ×2000, Teensy 4.1 ×32, Max/MSP, Meyer Sound Constellation 22.2, custom Python controllers, Arduino DMX shields',
            },
            {
                'title': 'PRISM — Scena Laserowa Instytut Festival',
                'slug': 'prism-instytut-2025',
                'description': 'Minimalistyczna scena techno z naciskiem na geometrię laserową. 6 laserów 30W tworzących trójwymiarowe struktury świetlne synchronizowane z BPM. Bez tradycyjnych dekoracji — czysty dialog między dźwiękiem a światłem. Mgła przemysłowa jako medium projekcji laserowej.',
                'short_description': 'Minimalistyczna geometria laserowa — 6×30W synchronized z BPM',
                'festival': self.festivals[3],
                'client': 'Instytut Collective',
                'date': today - timedelta(days=180),
                'category': 'lighting',
                'is_featured': False,
                'technologies': 'Kvant Spectrum 30W ×6, Pangolin BEYOND Ultimate, Antari HZ-500 ×12, Pioneer DJ CDJ-3000 MIDI sync, custom BPM analyzer',
            },
            {
                'title': 'OCEAN PULSE — Main Stage Sunrise Festival',
                'slug': 'ocean-pulse-sunrise-2025',
                'description': 'Morska scena główna z 40-metrową falą LED nad DJ-em. Kinetyczne elementy imitujące fale oceaniczne, wodne kurtyny z projection mappingiem, pirotechnika morska. Konstrukcja dla 25 000 osób z systemem dźwiękowym pokrywającym 300m.',
                'short_description': '40m fala LED, wodne kurtyny z mappingiem, pirotechnika dla 25k osób',
                'festival': self.festivals[4],
                'client': 'Sunrise Events',
                'date': today - timedelta(days=30),
                'category': 'main_stage',
                'is_featured': True,
                'technologies': 'ROE Visual CB5 LED panels ×400, Kinesys automation ×16 points, ETC Gio @5 ×2, JBL VTX A12 ×96, water screens ×4, Le Maitre pyro ×200 cues',
            },
            {
                'title': 'BINARY GARDEN — Side Stage Fest Festival',
                'slug': 'binary-garden-fest-2025',
                'description': 'Kameralna scena house/disco w otoczeniu interaktywnego ogrodu LED. Instalacje reagujące na obecność ludzi (czujniki PIR), świecące rośliny, ścieżki LED prowadzące do sceny. Ciepła, zachęcająca atmosfera kontrastująca z agresywnymi scenami techno.',
                'short_description': 'Interaktywny ogród LED reagujący na ruch, scena house/disco',
                'festival': self.festivals[5],
                'client': 'Fest Festival',
                'date': today - timedelta(days=200),
                'category': 'side_stage',
                'is_featured': False,
                'technologies': 'Astera AX1 PixelTubes ×200, PIR sensors ×80, Raspberry Pi 4 ×20, LED neon flex 5000m, Madrix control, Void Acoustics Incubus ×12',
            },
            {
                'title': 'ECHO DIMENSION — Instalacja dźwiękowa Unsound',
                'slug': 'echo-dimension-unsound-2025',
                'description': 'Przestrzenna instalacja audio-wizualna eksplorująca granice percepcji. 64 niezależne głośniki rozmieszczone sferycznie wokół publiczności. Wizualizacje generatywne reagujące na dane z analizy dźwięku w czasie rzeczywistym. Współpraca z artystami z Akademii Sztuk Pięknych w Krakowie.',
                'short_description': 'Sferyczny system 64 głośników z generatywnymi wizualizacjami',
                'festival': self.festivals[6],
                'client': 'Unsound Festival',
                'date': today - timedelta(days=45),
                'category': 'art_installation',
                'is_featured': True,
                'technologies': 'Genelec 8030C ×64, RME MADI ×4, SuperCollider, openFrameworks, custom C++ spatial audio engine, projectors Epson EB-PU2220B ×8',
            },
        ]

        self.projects = []
        for data in projects_data:
            proj, _ = Project.objects.get_or_create(
                slug=data['slug'], defaults=data,
            )
            self.projects.append(proj)

        self.stdout.write(f'   ✅ {Project.objects.count()} projektów')

    # =========================================================================
    # TESTIMONIALS
    # =========================================================================
    def _create_testimonials(self):
        self.stdout.write('💬 Tworzenie opinii klientów...')

        testimonials_data = [
            {
                'author': 'Jan Kowalski',
                'role': 'CEO, FestManager Sp. z o.o.',
                'content': 'BLACK LIGHT Collective to najlepszy zespół scenograficzny, z jakim pracowaliśmy. Neon Cathedral na Audioriver przeszła nasze najśmielsze oczekiwania. Profesjonalizm, terminowość i kreatywność na najwyższym poziomie. Publiczność do dziś o tym mówi!',
                'project': self.projects[0],
                'rating': 5,
            },
            {
                'author': 'Anna Nowak',
                'role': 'CEO, Bass Culture Events',
                'content': 'Deep Forest na Up To Date to był strzał w dziesiątkę. Połączenie natury z technologią, dźwięk 360° — ludzie mówili, że to najlepsza scena techno w Polsce w 2025 roku. BLACK LIGHT rozumie muzykę elektroniczną jak nikt inny.',
                'project': self.projects[1],
                'rating': 5,
            },
            {
                'author': 'Michał Krawczyk',
                'role': 'Dyrektor artystyczny, Tauron Nowa Muzyka',
                'content': 'Void Chamber to dzieło sztuki. Nie spodziewałem się, że można stworzyć tak intensywne doświadczenie z samego światła i dźwięku. Instalacja idealnie wpisała się w naszą wizję festiwalu. Zdecydowanie wracamy do współpracy.',
                'project': self.projects[2],
                'rating': 5,
            },
            {
                'author': 'Paweł Rytm',
                'role': 'Founder, Instytut Collective',
                'content': 'Prism to dowód, że mniej znaczy więcej. Lasery zsynchronizowane z BPM, zero bałaganu wizualnego — czysta energia. Idealne dla naszego minimalistycznego podejścia do techno. Budżet, terminowość, jakość — wszystko na 5.',
                'project': self.projects[3],
                'rating': 5,
            },
            {
                'author': 'Karolina Morska',
                'role': 'Production Manager, Sunrise Events',
                'content': 'Scena Ocean Pulse to było coś niesamowitego! 25 tysięcy ludzi pod wrażeniem fali LED i pirotechniki. BLACK LIGHT dostarczyli wszystko na czas mimo trudnych warunków pogodowych. Profesjonaliści w każdym calu.',
                'project': self.projects[4],
                'rating': 5,
            },
            {
                'author': 'Tomasz Nocny',
                'role': 'DJ & Promoter, Night Owl Events',
                'content': 'Pierwszy raz skorzystałem z usług BLACK LIGHT przy mniejszym evencie i byłem pod wrażeniem. Nawet przy ograniczonym budżecie potrafili stworzyć magiczną atmosferę. Na pewno wrócę z większym projektem!',
                'rating': 4,
            },
            {
                'author': 'Dr Alicja Sztuka',
                'role': 'Kuratorka, Unsound Festival',
                'content': 'Echo Dimension to jedno z najambitniejszych dzieł, które prezentowaliśmy na Unsound. Sferyczny system dźwiękowy i generatywne wizualizacje stworzyły naprawdę transcendentne doświadczenie. Artyści z ASP byli zachwyceni współpracą z zespołem BLACK LIGHT.',
                'project': self.projects[6],
                'rating': 5,
            },
        ]

        for data in testimonials_data:
            project = data.pop('project', None)
            Testimonial.objects.get_or_create(
                author=data['author'],
                defaults={**data, 'project': project},
            )

        self.stdout.write(f'   ✅ {Testimonial.objects.count()} opinii')

    # =========================================================================
    # CONFIGURATOR
    # =========================================================================
    def _create_configurator(self):
        self.stdout.write('⚙️ Tworzenie szablonów i komponentów konfiguratora...')

        # Scene Templates
        templates_data = [
            {
                'name': 'Main Stage Classic',
                'slug': 'main-stage-classic',
                'description': 'Klasyczna scena główna dla dużych festiwali. Solidna konstrukcja aluminiowa, pełna infrastruktura oświetleniowa i dźwiękowa. Pojemność: 10 000–30 000 osób. Idealna jako punkt centralny każdego festiwalu.',
                'base_price': Decimal('75000.00'),
                'width': Decimal('30.00'),
                'depth': Decimal('15.00'),
                'height': Decimal('12.00'),
            },
            {
                'name': 'Techno Bunker',
                'slug': 'techno-bunker',
                'description': 'Industrialna scena techno. Surowa, betonowa estetyka z agresywnym oświetleniem stroboskopowym i potężnym systemem basowym. Pojemność: 3 000–8 000 osób. Dla prawdziwych techno heads.',
                'base_price': Decimal('45000.00'),
                'width': Decimal('18.00'),
                'depth': Decimal('12.00'),
                'height': Decimal('8.00'),
            },
            {
                'name': 'Forest Stage',
                'slug': 'forest-stage',
                'description': 'Organiczna scena leśna. Dekoracje UV, świecące instalacje w drzewach, naturalna sceneria. Pojemność: 2 000–5 000 osób. Magiczna atmosfera dla psytrance, progressive i deep techno.',
                'base_price': Decimal('35000.00'),
                'width': Decimal('15.00'),
                'depth': Decimal('10.00'),
                'height': Decimal('6.00'),
            },
            {
                'name': 'Minimal Black Box',
                'slug': 'minimal-black-box',
                'description': 'Minimalistyczna czarna scena skupiona na laserach i dźwięku. Zero dekoracji — czysty dialog światło-muzyka. Pojemność: 500–2 000 osób. Idealna do techno, dub techno i ambient.',
                'base_price': Decimal('25000.00'),
                'width': Decimal('10.00'),
                'depth': Decimal('8.00'),
                'height': Decimal('5.00'),
            },
            {
                'name': 'Beach Paradise',
                'slug': 'beach-paradise',
                'description': 'Scena plażowa z tropikalną estetyką. Bambusowe konstrukcje, LED palmy, wodne efekty. Pojemność: 5 000–15 000 osób. Na house, disco i melodic techno pod gołym niebem.',
                'base_price': Decimal('55000.00'),
                'width': Decimal('25.00'),
                'depth': Decimal('12.00'),
                'height': Decimal('10.00'),
            },
        ]

        self.templates = []
        for data in templates_data:
            tmpl, _ = SceneTemplate.objects.get_or_create(slug=data['slug'], defaults=data)
            self.templates.append(tmpl)

        # Component Categories
        categories_data = [
            {'name': 'Oświetlenie', 'slug': 'oswietlenie', 'icon': '💡', 'description': 'Głowice ruchome, LED bary, lasery, stroboskopy, UV', 'order': 1},
            {'name': 'Dźwięk', 'slug': 'dzwiek', 'icon': '🔊', 'description': 'Systemy nagłośnienia, subwoofery, monitory, procesory', 'order': 2},
            {'name': 'Dekoracje', 'slug': 'dekoracje', 'icon': '🎨', 'description': 'Tkaniny UV, instalacje, kwiaty, rzeźby, elementy scenograficzne', 'order': 3},
            {'name': 'Efekty specjalne', 'slug': 'efekty-specjalne', 'icon': '🔥', 'description': 'Pirotechnika, CO2, confetti, mgła, woda, bańki', 'order': 4},
            {'name': 'Wizualizacje', 'slug': 'wizualizacje', 'icon': '🖥️', 'description': 'Projektory, ekrany LED, media serwery, mapping', 'order': 5},
            {'name': 'Konstrukcja', 'slug': 'konstrukcja', 'icon': '🏗️', 'description': 'Kratownice, podesty, rigging, zadaszenie', 'order': 6},
        ]

        self.categories = []
        for data in categories_data:
            cat, _ = ComponentCategory.objects.get_or_create(slug=data['slug'], defaults=data)
            self.categories.append(cat)

        # Components
        components_data = [
            # Oświetlenie
            {'category': self.categories[0], 'name': 'Martin MAC Aura XB', 'slug': 'martin-mac-aura-xb', 'description': 'Kompaktowa głowica wash LED z zoomem 11°-58°. 1220 lm, RGBW, piękne kolory pastele i mocne nasycone barwy.', 'price': Decimal('180.00'), 'power_consumption': 450, 'weight_kg': Decimal('6.8'), 'specs': {'type': 'moving_head_wash', 'lumens': 1220, 'zoom': '11-58°'}},
            {'category': self.categories[0], 'name': 'Robe MegaPointe', 'slug': 'robe-megapointe', 'description': 'Hybrydowa głowica beam/spot/wash. Niezwykle jasna, ostre belki i gobo. Standard na dużych scenach.', 'price': Decimal('250.00'), 'power_consumption': 550, 'weight_kg': Decimal('17.5'), 'specs': {'type': 'moving_head_hybrid', 'lumens': 36000, 'zoom': '1.8-22°'}},
            {'category': self.categories[0], 'name': 'Kvant Spectrum 30W Laser', 'slug': 'kvant-spectrum-30w', 'description': 'Profesjonalny laser pokazowy 30W full color RGB. Idealne do efektów tunelowych i geometrycznych.', 'price': Decimal('800.00'), 'power_consumption': 1500, 'weight_kg': Decimal('25.0'), 'specs': {'type': 'laser', 'power': '30W', 'colors': 'RGB full color'}},
            {'category': self.categories[0], 'name': 'Stroboskop Atomic 3000 LED', 'slug': 'atomic-3000-led', 'description': 'Potężny stroboskop LED z efektem koloru. Ikoniczny na scenach techno.', 'price': Decimal('120.00'), 'power_consumption': 300, 'weight_kg': Decimal('8.0'), 'specs': {'type': 'strobe', 'lumens': 55000}},
            {'category': self.categories[0], 'name': 'UV Bar 1m LED', 'slug': 'uv-bar-1m', 'description': 'Belka UV LED 1 metr. Idealna do oświetlenia dekoracji fluorescencyjnych.', 'price': Decimal('45.00'), 'power_consumption': 80, 'weight_kg': Decimal('3.0'), 'specs': {'type': 'uv_bar', 'length': '1m'}},

            # Dźwięk
            {'category': self.categories[1], 'name': 'Funktion-One Vero VX (para)', 'slug': 'f1-vero-vx', 'description': 'Topowy system line array. Krystalicznie czysty dźwięk od 55Hz, pokrycie do 100m.', 'price': Decimal('1200.00'), 'power_consumption': 2000, 'weight_kg': Decimal('45.0'), 'specs': {'type': 'line_array', 'freq': '55Hz-20kHz', 'spl': '139dB'}},
            {'category': self.categories[1], 'name': 'Funktion-One F221 Bass (para)', 'slug': 'f1-f221-bass', 'description': 'Legendarny subwoofer 2×21". Głęboki, fizyczny bas, który czujesz w klatce piersiowej.', 'price': Decimal('800.00'), 'power_consumption': 3000, 'weight_kg': Decimal('110.0'), 'specs': {'type': 'subwoofer', 'drivers': '2x21"', 'freq': '28-100Hz'}},
            {'category': self.categories[1], 'name': 'd&b audiotechnik SL-Sub', 'slug': 'db-sl-sub', 'description': 'Kardioidalny subwoofer z rodziny SL. Precyzyjna kontrola kierunkowości basu.', 'price': Decimal('600.00'), 'power_consumption': 2400, 'weight_kg': Decimal('75.0'), 'specs': {'type': 'subwoofer', 'drivers': '2x21"', 'cardioid': True}},
            {'category': self.categories[1], 'name': 'Monitor wedge d&b M4', 'slug': 'db-m4-monitor', 'description': 'Kompaktowy monitor sceniczny. Czysty dźwięk dla DJ-a/artysty.', 'price': Decimal('150.00'), 'power_consumption': 600, 'weight_kg': Decimal('22.0'), 'specs': {'type': 'monitor', 'freq': '62Hz-18kHz'}},

            # Dekoracje
            {'category': self.categories[2], 'name': 'Tkanina UV Lycra 5m²', 'slug': 'tkanina-uv-5m2', 'description': 'Elastyczna tkanina fluorescencyjna, świeci pod UV. Różne wzory i kolory.', 'price': Decimal('85.00'), 'power_consumption': 0, 'weight_kg': Decimal('2.0'), 'specs': {'type': 'uv_fabric', 'area': '5m²'}},
            {'category': self.categories[2], 'name': 'Instalacja kinetyczna "Wave" 3m', 'slug': 'instalacja-wave-3m', 'description': 'Ruchoma instalacja z elementami odbijającymi światło. Napędzana silnikami sterowanymi DMX.', 'price': Decimal('1500.00'), 'power_consumption': 200, 'weight_kg': Decimal('35.0'), 'specs': {'type': 'kinetic', 'dmx_channels': 8}},
            {'category': self.categories[2], 'name': 'LED Neon Flex RGB (10m)', 'slug': 'led-neon-flex-10m', 'description': 'Elastyczny neon LED RGB, DMX sterowany. Do konturowania scen i dekoracji.', 'price': Decimal('120.00'), 'power_consumption': 80, 'weight_kg': Decimal('3.0'), 'specs': {'type': 'led_neon', 'length': '10m', 'pixels_per_m': 60}},
            {'category': self.categories[2], 'name': 'Rzeźba LED "Totem" 4m', 'slug': 'rzezba-led-totem-4m', 'description': 'Wolnostojąca rzeźba LED o wysokości 4m. Wbudowane LED pixele, programowalna DMX/Art-Net.', 'price': Decimal('3500.00'), 'power_consumption': 500, 'weight_kg': Decimal('80.0'), 'specs': {'type': 'sculpture', 'height': '4m', 'leds': 2000}},

            # Efekty specjalne
            {'category': self.categories[3], 'name': 'CO2 Jet Cryo Cannon', 'slug': 'co2-jet-cryo', 'description': 'Wystrzał CO2 do 8m wysokości. Efektowny biały słup gazu — must-have na drop.', 'price': Decimal('350.00'), 'power_consumption': 50, 'weight_kg': Decimal('12.0'), 'specs': {'type': 'co2_jet', 'height': '8m'}},
            {'category': self.categories[3], 'name': 'Confetti Blaster (jednorazowy)', 'slug': 'confetti-blaster', 'description': 'Wystrzał konfetti metalicznego. Różne kolory. Efekt WOW na finał seta.', 'price': Decimal('95.00'), 'power_consumption': 0, 'weight_kg': Decimal('3.0'), 'specs': {'type': 'confetti', 'range': '15m'}},
            {'category': self.categories[3], 'name': 'Flame Machine DMX', 'slug': 'flame-machine-dmx', 'description': 'Kontrolowana maszyna ogniowa. Płomienie do 3m, sterowane DMX. Wymaga pirotechnika.', 'price': Decimal('500.00'), 'power_consumption': 100, 'weight_kg': Decimal('18.0'), 'specs': {'type': 'flame', 'height': '3m', 'fuel': 'propane'}},
            {'category': self.categories[3], 'name': 'Antari HZ-500 Hazer', 'slug': 'antari-hz500', 'description': 'Profesjonalna wytwornica mgły na bazie oleju. Delikatna, równomierna mgła idealna do laserów.', 'price': Decimal('75.00'), 'power_consumption': 575, 'weight_kg': Decimal('9.0'), 'specs': {'type': 'hazer', 'fluid': 'oil-based'}},

            # Wizualizacje
            {'category': self.categories[4], 'name': 'Ekran LED P3.9 Indoor (1m²)', 'slug': 'ekran-led-p39', 'description': 'Moduł ekranu LED o pikselacji 3.9mm. Jasny, wyraźny obraz. Łączenie w dowolne kształty.', 'price': Decimal('200.00'), 'power_consumption': 800, 'weight_kg': Decimal('8.0'), 'specs': {'type': 'led_screen', 'pixel_pitch': '3.9mm', 'brightness': '5000 nits'}},
            {'category': self.categories[4], 'name': 'Projektor Epson 20K lumen', 'slug': 'projektor-epson-20k', 'description': 'Profesjonalny projektor laserowy do projection mappingu. WUXGA, 24/7, ciche chłodzenie.', 'price': Decimal('450.00'), 'power_consumption': 900, 'weight_kg': Decimal('30.0'), 'specs': {'type': 'projector', 'lumens': 20000, 'resolution': 'WUXGA'}},
            {'category': self.categories[4], 'name': 'Disguise D3 Media Server', 'slug': 'disguise-d3', 'description': 'Topowy media serwer do projection mappingu i sterowania treścią wideo. Standard w branży.', 'price': Decimal('1500.00'), 'power_consumption': 800, 'weight_kg': Decimal('15.0'), 'specs': {'type': 'media_server', 'outputs': 16, 'resolution': '8K'}},

            # Konstrukcja
            {'category': self.categories[5], 'name': 'Kratownica aluminiowa H40V (1m)', 'slug': 'kratownica-h40v-1m', 'description': 'Ciężka kratownica aluminiowa 40×40cm. Nośność 2000kg na 12m. Standard festiwalowy.', 'price': Decimal('35.00'), 'power_consumption': 0, 'weight_kg': Decimal('12.0'), 'specs': {'type': 'truss', 'size': '400x400mm', 'load': '2000kg/12m'}},
            {'category': self.categories[5], 'name': 'Podest sceniczny 2×1m', 'slug': 'podest-sceniczny-2x1m', 'description': 'Regulowana wysokość 0.4-1.8m. Nośność 750kg/m². Antypoślizgowa powierzchnia.', 'price': Decimal('50.00'), 'power_consumption': 0, 'weight_kg': Decimal('35.0'), 'specs': {'type': 'stage_deck', 'size': '2x1m', 'height': '0.4-1.8m'}},
            {'category': self.categories[5], 'name': 'Chain Hoist 1T (łańcuchowy)', 'slug': 'chain-hoist-1t', 'description': 'Elektryczny wciągnik łańcuchowy 1 tona. Do podnoszenia kratownic z oświetleniem i dźwiękiem.', 'price': Decimal('120.00'), 'power_consumption': 1500, 'weight_kg': Decimal('30.0'), 'specs': {'type': 'hoist', 'capacity': '1000kg', 'speed': '4m/min'}},
        ]

        for data in components_data:
            Component.objects.get_or_create(slug=data['slug'], defaults=data)

        self.stdout.write(f'   ✅ {SceneTemplate.objects.count()} szablonów, {ComponentCategory.objects.count()} kategorii, {Component.objects.count()} komponentów')

    # =========================================================================
    # SHOP
    # =========================================================================
    def _create_shop(self):
        self.stdout.write('🛒 Tworzenie produktów sklepu...')

        # Product Categories
        shop_cats_data = [
            {'name': 'Odzież', 'slug': 'odziez', 'description': 'Koszulki, bluzy, czapki z logo BLACK LIGHT', 'order': 1},
            {'name': 'Akcesoria', 'slug': 'akcesoria', 'description': 'Torby, plecaki, breloki, naklejki', 'order': 2},
            {'name': 'Elementy sceniczne', 'slug': 'elementy-sceniczne', 'description': 'Mniejsze elementy dekoracyjne na własne eventy', 'order': 3},
            {'name': 'Druki artystyczne', 'slug': 'druki-artystyczne', 'description': 'Plakaty, printy zdjęć z festiwali, grafiki limitowane', 'order': 4},
        ]

        shop_cats = []
        for data in shop_cats_data:
            cat, _ = ProductCategory.objects.get_or_create(slug=data['slug'], defaults=data)
            shop_cats.append(cat)

        # Products
        products_data = [
            # Odzież
            {'name': 'T-shirt BLACK LIGHT "Neon Cathedral" Ed.', 'slug': 'tshirt-neon-cathedral', 'category': shop_cats[0], 'description': 'Limitowana koszulka upamiętniająca projekt Neon Cathedral na Audioriver 2025. 100% bawełna organiczna, nadruk UV-reaktywny — świeci pod ultafioletem na festiwalu! Unisex, regular fit.', 'short_description': 'Limitowana koszulka z nadrukiem UV-reaktywnym', 'price': Decimal('129.00'), 'compare_price': Decimal('159.00'), 'sku': 'TSH-NC-001', 'stock': 150, 'is_featured': True, 'weight_kg': Decimal('0.25'), 'tags': 'koszulka,uv,neon,audioriver,limitowana'},
            {'name': 'Bluza Hoodie BLACK LIGHT Classic Black', 'slug': 'bluza-blacklight-classic', 'category': shop_cats[0], 'description': 'Klasyczna czarna bluza z kapturem i haftowanym logo BLACK LIGHT. 80% bawełna, 20% poliester, 320g/m². Kangurka, sznurek w kapturze. Idealny festiwalowy must-have na chłodne noce.', 'short_description': 'Czarna bluza z haftowanym logo', 'price': Decimal('249.00'), 'sku': 'BLZ-CL-001', 'stock': 80, 'is_featured': True, 'weight_kg': Decimal('0.55'), 'tags': 'bluza,hoodie,classic,logo'},
            {'name': 'Czapka Snapback BLACK LIGHT Glow', 'slug': 'czapka-blacklight-glow', 'category': shop_cats[0], 'description': 'Czapka snapback z odblaskowym logo BLACK LIGHT. Świeci w błyskach stroboskopu! Regulowany rozmiar, płaski daszek.', 'short_description': 'Snapback z odblaskowym logo', 'price': Decimal('89.00'), 'sku': 'CZP-GL-001', 'stock': 120, 'weight_kg': Decimal('0.12'), 'tags': 'czapka,snapback,glow,odblask'},
            {'name': 'Tank Top BLACK LIGHT Techno Black', 'slug': 'tanktop-techno-black', 'category': shop_cats[0], 'description': 'Lekki tank top na festiwalowe upały. Minimalistyczny design z małym logo na piersi. 100% bawełna.', 'short_description': 'Lekki tank top z logo', 'price': Decimal('79.00'), 'sku': 'TNK-TB-001', 'stock': 200, 'weight_kg': Decimal('0.15'), 'tags': 'tanktop,techno,lato,festiwal'},

            # Akcesoria
            {'name': 'Plecak BLACK LIGHT Utility 25L', 'slug': 'plecak-blacklight-utility', 'category': shop_cats[1], 'description': 'Wodoodporny plecak festiwalowy z kieszenią na laptop, ukrytą kieszenią antykradzieżową i odblaskowym logo. Objętość 25L, pasek piersiowy, port USB do powerbanku.', 'short_description': 'Wodoodporny plecak 25L z portem USB', 'price': Decimal('199.00'), 'sku': 'PLK-UT-001', 'stock': 45, 'is_featured': True, 'weight_kg': Decimal('0.8'), 'tags': 'plecak,festiwal,wodoodporny,usb'},
            {'name': 'Zestaw naklejek BLACK LIGHT (10 szt.)', 'slug': 'naklejki-blacklight-set', 'category': shop_cats[1], 'description': '10 naklejek winylowych z grafikami BLACK LIGHT. Wodoodporne, UV-odporne. Idealnie na laptop, skrzynię na sprzęt czy samochód.', 'short_description': '10 naklejek winylowych wodoodpornych', 'price': Decimal('29.00'), 'sku': 'NAK-ST-001', 'stock': 500, 'weight_kg': Decimal('0.05'), 'tags': 'naklejki,vinyl,zestaw'},
            {'name': 'Brelok LED BLACK LIGHT (USB-C)', 'slug': 'brelok-led-blacklight', 'category': shop_cats[1], 'description': 'Mini brelok z podświetlanym logo BLACK LIGHT. Ładowanie USB-C, 3 tryby świecenia (stały, pulsujący, stroboskop). Bateria na 48h.', 'short_description': 'Brelok z podświetlanym logo, USB-C', 'price': Decimal('49.00'), 'sku': 'BRL-LED-001', 'stock': 300, 'weight_kg': Decimal('0.03'), 'tags': 'brelok,led,usb-c,gadżet'},

            # Elementy sceniczne
            {'name': 'Mini LED Totem 1.5m (DIY Kit)', 'slug': 'mini-led-totem-diy', 'category': shop_cats[2], 'description': 'Zestaw do samodzielnego złożenia totemu LED o wysokości 1.5m. Zawiera: profil aluminiowy, taśmę LED WS2812B 300px, kontroler ESP32 z WiFi, zasilacz 5V/10A, instrukcję montażu i kod Arduino do sterowania. Idealny na domówki i małe eventy.', 'short_description': 'Zestaw DIY — totem LED 1.5m z ESP32', 'price': Decimal('449.00'), 'compare_price': Decimal('549.00'), 'sku': 'TOT-DIY-001', 'stock': 25, 'is_featured': True, 'weight_kg': Decimal('5.0'), 'tags': 'totem,led,diy,esp32,arduino'},
            {'name': 'UV Tape Fluorescencyjna (50m)', 'slug': 'uv-tape-50m', 'category': shop_cats[2], 'description': 'Taśma fluorescencyjna świecąca pod UV. 50 metrów, szerokość 19mm. Do dekorowania ścian, sufitów, mebli. 6 kolorów do wyboru.', 'short_description': 'Taśma UV 50m — 6 kolorów', 'price': Decimal('39.00'), 'sku': 'UVT-50M-001', 'stock': 200, 'weight_kg': Decimal('0.3'), 'tags': 'uv,tape,dekoracja,fluor'},
            {'name': 'Pixel LED Strip WS2812B (5m, 60/m)', 'slug': 'pixel-led-strip-5m', 'category': shop_cats[2], 'description': 'Adresowalna taśma LED z 300 pixelami na 5 metrów. Kompatybilna z Arduino, ESP32, WLED. IP65 wodoodporna. Idealna do DIY instalacji świetlnych.', 'short_description': 'Taśma LED 300px, IP65, WLED compatible', 'price': Decimal('89.00'), 'sku': 'PXL-5M-001', 'stock': 150, 'weight_kg': Decimal('0.4'), 'tags': 'led,pixel,ws2812b,wled,arduino'},

            # Druki artystyczne
            {'name': 'Plakat "Neon Cathedral" 70×100cm', 'slug': 'plakat-neon-cathedral', 'category': shop_cats[3], 'description': 'Oficjalny plakat projektu Neon Cathedral (Audioriver 2025). Druk na papierze fotograficznym 250g/m², nasycone kolory. Limitowana edycja numerowana, 200 sztuk.', 'short_description': 'Limitowany plakat 70×100cm, druk foto', 'price': Decimal('149.00'), 'sku': 'PLK-NC-001', 'stock': 200, 'is_featured': True, 'weight_kg': Decimal('0.3'), 'tags': 'plakat,print,neon,audioriver,limitowany'},
            {'name': 'Zestaw 3 printów "Best of 2025" A3', 'slug': 'printy-best-of-2025', 'category': shop_cats[3], 'description': '3 druki artystyczne A3 przedstawiające najlepsze realizacje BLACK LIGHT z sezonu 2025. Neon Cathedral, Deep Forest, Ocean Pulse. Papier matowy 200g/m².', 'short_description': '3 printy A3 — top projekty 2025', 'price': Decimal('199.00'), 'compare_price': Decimal('249.00'), 'sku': 'PRT-BO-2025', 'stock': 100, 'weight_kg': Decimal('0.5'), 'tags': 'print,zestaw,2025,a3,artystyczny'},
        ]

        for data in products_data:
            Product.objects.get_or_create(slug=data['slug'], defaults=data)

        # Coupons
        now = timezone.now()
        coupons_data = [
            {'code': 'BLACK LIGHT10', 'discount_type': 'percentage', 'discount_value': Decimal('10.00'), 'min_order_amount': Decimal('100.00'), 'max_uses': 500, 'valid_from': now, 'valid_until': now + timedelta(days=90)},
            {'code': 'FIRSTORDER', 'discount_type': 'percentage', 'discount_value': Decimal('15.00'), 'min_order_amount': Decimal('50.00'), 'max_uses': 1000, 'valid_from': now, 'valid_until': now + timedelta(days=365)},
            {'code': 'FESTIWAL50', 'discount_type': 'fixed', 'discount_value': Decimal('50.00'), 'min_order_amount': Decimal('300.00'), 'max_uses': 100, 'valid_from': now, 'valid_until': now + timedelta(days=60)},
            {'code': 'VIP25', 'discount_type': 'percentage', 'discount_value': Decimal('25.00'), 'min_order_amount': Decimal('200.00'), 'max_uses': 50, 'valid_from': now, 'valid_until': now + timedelta(days=180)},
        ]

        for data in coupons_data:
            Coupon.objects.get_or_create(code=data['code'], defaults=data)

        self.stdout.write(f'   ✅ {Product.objects.count()} produktów, {Coupon.objects.count()} kuponów')

    # =========================================================================
    # SAMPLE ORDERS
    # =========================================================================
    def _create_orders(self):
        self.stdout.write('📋 Tworzenie przykładowych zamówień...')
        today = date.today()

        # === CONFIGURATOR ORDERS ===
        components = list(Component.objects.all())

        orders_data = [
            {
                'user': self.clients[0],
                'template': self.templates[0],
                'status': 'completed',
                'event_name': 'Summer Bass Festival 2025',
                'event_date': today + timedelta(days=90),
                'event_location': 'Łódź, Park Poniatowskiego',
                'expected_audience': 15000,
                'notes': 'Potrzebujemy dodatkowego zasilania 400A. Scena ma być gotowa 2 dni przed eventem.',
            },
            {
                'user': self.clients[1],
                'template': self.templates[1],
                'status': 'in_progress',
                'event_name': 'Underground Techno Night',
                'event_date': today + timedelta(days=45),
                'event_location': 'Kraków, Hala Wisły',
                'expected_audience': 3000,
                'notes': 'Minimalistyczne podejście. Nacisk na lasery i stroboskopy. Bez dekoracji UV.',
            },
            {
                'user': self.clients[2],
                'template': self.templates[2],
                'status': 'quoted',
                'event_name': 'Forest Rave Wrocław',
                'event_date': today + timedelta(days=120),
                'event_location': 'Las Osobowicki, Wrocław',
                'expected_audience': 2000,
                'notes': 'Potrzebujemy dekoracji UV w drzewach + ścieżkę LED do sceny. Prąd z agregatów.',
            },
            {
                'user': self.clients[0],
                'template': self.templates[4],
                'status': 'submitted',
                'event_name': 'Plaża Beats 2026',
                'event_date': today + timedelta(days=200),
                'event_location': 'Sopot, Plaża',
                'expected_audience': 8000,
                'notes': 'Scena plażowa, ale z mocniejszym systemem dźwiękowym niż standard. VIP zone z osobnym nagłośnieniem.',
            },
        ]

        for i, data in enumerate(orders_data):
            order, created = Order.objects.get_or_create(
                event_name=data['event_name'],
                defaults=data,
            )
            if created and components:
                # Dodaj losowe komponenty
                import random
                selected = random.sample(components, min(len(components), random.randint(4, 8)))
                for comp in selected:
                    qty = random.randint(1, 20)
                    OrderItem.objects.create(
                        order=order,
                        component=comp,
                        quantity=qty,
                        unit_price=comp.price,
                        subtotal=comp.price * qty,
                    )
                order.recalculate_total()

        # === SHOP ORDERS ===
        products = list(Product.objects.all())
        if products and self.clients:
            shop_orders_data = [
                {
                    'user': self.clients[0],
                    'status': 'delivered',
                    'shipping_name': 'Jan Kowalski',
                    'shipping_street': 'ul. Festiwalowa 15',
                    'shipping_city': 'Warszawa',
                    'shipping_postal_code': '00-001',
                    'shipping_cost': Decimal('15.00'),
                    'notes': 'Proszę o paczkę na firmę z fakturą.',
                },
                {
                    'user': self.clients[1],
                    'status': 'shipped',
                    'shipping_name': 'Anna Nowak',
                    'shipping_street': 'ul. Basowa 7/3',
                    'shipping_city': 'Kraków',
                    'shipping_postal_code': '30-001',
                    'shipping_cost': Decimal('12.00'),
                    'tracking_number': 'PL1234567890',
                },
                {
                    'user': self.clients[2],
                    'status': 'pending',
                    'shipping_name': 'Tomasz Nocny',
                    'shipping_street': 'ul. Nocna 23',
                    'shipping_city': 'Wrocław',
                    'shipping_postal_code': '50-001',
                    'shipping_cost': Decimal('0.00'),
                    'notes': 'Odbiór osobisty we Wrocławiu.',
                },
            ]

            import random
            for data in shop_orders_data:
                total = Decimal('0.00')
                order, created = ShopOrder.objects.get_or_create(
                    user=data['user'],
                    status=data['status'],
                    defaults={**data, 'total': Decimal('0.00')},
                )
                if created:
                    selected = random.sample(products, min(len(products), random.randint(2, 5)))
                    for prod in selected:
                        qty = random.randint(1, 3)
                        subtotal = prod.price * qty
                        total += subtotal
                        ShopOrderItem.objects.create(
                            order=order,
                            product=prod,
                            product_name=prod.name,
                            quantity=qty,
                            unit_price=prod.price,
                            subtotal=subtotal,
                        )
                    order.total = total
                    order.save()

        self.stdout.write(f'   ✅ {Order.objects.count()} zamówień scen, {ShopOrder.objects.count()} zamówień sklepowych')
