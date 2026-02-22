# Kompletní hloubkový rozbor projektu: Apartment Market Analyzer

Tento dokument slouží jako ultimátní průvodce celým projektem. Je napsán tak, abys po jeho přečtení dokonale rozuměl každému rozhodnutí, které bylo učiněno, věděl, proč byly použity konkrétní technologie, a chápal projekt do nejmenšího detailu, jako bys ho od nuly napsal sám.

## 1. Architektura a Workflow (Jak to celé funguje dohromady)

Projekt je rozdělen do tří naprosto oddělených logických celků (komponent), které na sebe navazují sekvenčně:

1. **Scraper (`src/scraper`)**: Otevře reálný web, "nakliká" stránky, přečte inzeráty a surová data (texty, lokace, ceny jako stringy) uloží do CSV souboru (`data/raw/apartments_raw_data.csv`).
2. **Model a Trénink (`src/model/train_model.py`)**: Vezme toto hrubé CSV, vyčistí ho (odstraní nesmysly, převede text na čísla), natrénuje algoritmus umělé inteligence a výsledek uloží do "zmraženého" stavu (`.pkl` soubory) a zároveň vypíše zjištěná metadata (např. seznam použitých krajů) do `apartment_metadata.json`.
3. **GUI aplikace (`src/app/gui_app.py` & `src/model/inference.py`)**: Grafické rozhraní, které model probudí k životu. Načte `.pkl` soubory z předchozího kroku, vezme parametry od uživatele a provede odhad ceny. Zobrazí výsledek a vykreslí graf.

Vše je spojeno univerzálním konfiguračním souborem `config.json`, díky kterému lze měnit chování aplikace bez zásahu do samotného Python kódu.

---

## 2. Detailní rozbor kódů (Soubor po souboru)

### A. Konfigurace (`config.json` & `src/utils/config_loader.py`)

**Proč bylo použito toto řešení:**
Mít parametry přímo v kódu (hardcoding) je špatná praxe. Když chceme změnit barvu tlačítka, nebo URL adresu scraperu, museli bychom hledat na 50 místech v kódu. Napsali jsme třídu `ConfigLoader`.

- **`config_loader.py`**: Aplikuje návrhový vzor "Singleton". Znamená to, že soubor se načte z disku pouze jednou při prvním zavolání a uloží se do paměti (proměnná `_config`). Zbytek aplikace k němu přistupuje bleskově. Cesty jsou zde řešeny pomocí relativních přesunů `os.path.dirname`, aby aplikace vždy našla `config.json` v kořeni projektu, ať už ji spouštíš z jakéhokoliv adresáře.
- **Pseudo-komentáře v `config.json`**: Jelikož čistý formát JSON neakceptuje tradiční komentáře (jako `//` v C++ nebo `#` v Pythonu), byl v souboru uplatněn trik. Jsou tam přidány neaktivní klíče začínající `"_comment"`. Aplikace je při parsování prostě překročí, ale pro administrátora slouží jako detailní anglický návod (přímo v souboru), co která proměnná dělá a jak ji bezpečně měnit (např. limity GUI, rychlost delayů u scraperu apod.).

### B. Extrakce dat (`src/scraper/reality_scraper.py`)

**Proč Selenium a ne třeba Beautiful Soup nebo Requests?**
Moderní weby (jako reality.idnes.cz) nenačítají inzeráty rovnou v HTML, ale stahují je dynamicky na pozadí pomocí JavaScriptu (tzv. asynchronní načítání/React/Angular). Obyčejný HTTP požadavek by vrátil prázdnou stránku. Selenium reálně spustí prohlížeč Chrome, nechá JavaScript doběhnout a simuluje skutečného uživatele.

**Hlavní funkce a proč tu jsou:**
- **`setup_driver(config)`**: Inicializuje Chrome prohlížeč. Záměrně posílá reálný User-Agent string (z konfigurace), aby se náš bot tvářil jako běžný uživatel. Odstraňuje flag `AutomationControlled`, abychom minimalizovali šanci, že nás web zablokuje pomocí Captchy.
- **`extract_apartment_data()`**: Zde vybíráme HTML prvky na základě jejich CSS tříd (`c-products__title`, `c-products__price`). Kód je nutně obalen v `try-except` blocích, protože weby nejsou perfektní – někdy chybí lokace, jindy cena, a my nechceme, aby nám pád jednoho inzerátu shodil dvouhodinové stahování.
- **`save_state()` a `load_state()`**: Toto je velmi užitečná funkcionalita (soubor `scraper_state_apartments.json`). Pokud ti padne internet po scrapování 200. stránky, při dalším spuštění skript začne na straně 201 a stáhne zbytek. Obrovská úspora času a datového provozu. Ukládá se iterativně uvnitř hlavní smyčky po každé stránce.
- **Manuální intervence v `main()`**: Dnes se stává standardem nevyhnutelné okno pro "Souhlas se soubory Cookies". Robot neumí vždy přesně trefit toto okno (často se mění rozložení webu). Záměrně se zde kód zastaví (`input()`), otevře se grafické okno, ty odklikáš GDPR a pak v terminálu odentruješ, že má bot pokračovat.

### C. Zpracování a "Inteligence" (`src/model/train_model.py`)

**Jaká je motivace tohoto kódu:**
Máme `apartments_raw_data.csv`. Vypadá asi takto: "Prodej bytu 2+kk 52 m²", cena: "5 400 000 Kč", lokace: "Tepelného, Beroun". Z tohoto se žádná umělá inteligence nic nenaučí. Musíme text "PŘELOŽIT" na čísla a standardizované hodnoty. Tomu se říká "Feature extraction" (Těžba příznaků).

- **`parse_area(title)` a `parse_disposition(title)`**: Čisté regulární výrazy (RegEx). Hledají jakékoliv číslo těsně před "m2" nebo "m²" a ukládají ho. Podobně pro dispozici, hledá vzor bloku jako `"číslo + kk"` atd.
- **`clean_region(location)`**: Obrovský a nejdůležitější blok čištění. Algoritmus nemá rád obrovské množství lokací, kde má ke každé 2 inzeráty (např. Malá Lhota). Model by selhal při tréninku. Proto zde bereme desítky českých městských částí a "komprimujeme" je do 14 krajů nebo Prahy. Zjišťujeme také zahraničí (Slovensko, Egypt), které pak vyřazujeme (Zahraničí).
- **One-Hot Encoding (`pd.get_dummies`)**: Model Random Forest spolkne pouze čísla, ne slovo "Praha". Tento proces vezme sloupec `region` a rozdělí jej na sloupce `region_Praha`, `region_Plzeňský kraj` apod., které obsahují boolean hodnoty (0 nebo 1). Pro byt v Praze bude všude `0`, jen ve sloupci `region_Praha` bude `1`.

**Proč Random Forest Regressor?**
Použili jsme algoritmus ze scikit-learn zvaný "Náhodný les". Je to soubor stovek rozhodovacích stromů. Je geniální na realitní data, protože nelineární vtahy (např. byt v Praze o ploše 30m stoupá na ceně jinak než v Ústí nad Labem o ploše 100m) řeší stromy obrovskou sérií otázek a rozhodnutí. Je velmi odolný proti ojedinělým chybám v ceně (outliers).

Kód po natrénování uloží model na disk přes knihovnu `joblib`. Také vezme vyčištěné kategorie a parametry a zapíše je do `apartment_metadata.json`, aby o nich GUI hned po startu vědělo (tato metadata udávají, co má být v dropdownech na frontendu aplikacie).

### D. Mozek Aplikace: Inference (`src/model/inference.py`)

Předchozí kód model pouze postavil. Tento jej využívá uvnitř aplikace.

- **`PricePredictor` (Třída)**: Při startu GUI vytvoříme instanci této třídy. V metodě `__init__` se provede čtení dříve vygenerovaných souborů `.pkl` a jsonu obsahujících sloupce.
- **`predict_price()`**: Nejsložitější funkce pro nováčka. Ve stejném tvaru, jaký byl předložen modelu při trénování, musíme nyní připravit prediktivní vzorek (řádek).
  Vezmeme všechny očekávané sloupce a naplníme je `0`. Pak se zeptáme na "Area" a vpíšeme přesnou plochu. U dispozice a regionu najdeme string (např. `"Praha"`), k němu přilepíme předponu `"region_"` -> `"region_Praha"` a hledáme tento přesný název sloupce. Když ho najdeme, přepíšeme zde nulu na `1`. Takto zpracovaný "dummy" řádek pak pošleme metodě `model.predict()`, která vrátí magické číslo - přesnou tržní predikci nemovitosti.
- **`calculate_future_value()`**: Obslužná funkce, která vezme současnou cenu bytu, využije roční růstový úrok (pevně 4 % formou `growth_rate = 0.04`) a pomocí for-loopu aplikuje složené úročení. Vygeneruje seznam ceníků za další roky, které se dál pošlou ke grafické vizualizaci na Frontend.

### E. Uživatelské rozhraní (`src/app/gui_app.py`)

Aplikace je vizualizována za pomocí knihovny Tkinter. 

**Proč Tkinter?**
Tkinter je přímo obsažen v základu jazyka Python. Stačí ho importovat a funguje bez instalace napříč Mac, Windows i Linux systémem. Byly použity vizuální prvky `ttk` (Themed Tkinter), což je novější knihovna překrývající starý nevzhledný design a napojující se na nativní vykreslování operačního systému.

**Rozložení a Flow:**
1. **Při načtení (metoda `__init__`)**: Načteme konfiguraci (pro globální stylování: barvy z `config.json`), inicializujeme okno a z `inference.py` zjistíme možné oblasti a dispoziční tvary pro dropdown menu, načež vše poskládáme metodou `create_widgets()`.
2. **Uživatelská Validace (`validate_inputs()`)**: Klíčový bezpečnostní prvek. Místo toho abychom se ptali modelu na nesmysl, před predikcí proběhne validace proti hardkódovaným prahům. Chtít odhadnout miniaturní 20m² ale roztáhnutou na 6+kk je zřejmě překlep uživatele. GUI nabídne standardní varovný dialog (pop-up).
3. **Výstup a Vizualizace (`plot_future_trend()`)**: Skvělý "Wau" efekt projektu na uživatele. Využívá se zde framework Matplotlib. K tomu, aby se graf zobrazil přímo do okna programu (a nikoliv do externího generovaného popup okna), se používá interní tk bridge `FigureCanvasTkAgg`. Tento objekt graf vyrenderuje a doslova připlácne do framu uvnitř tkinter aplikace. Funkce `currency_formatter` v grafu se stará o to, že místo milionů (např. `5500000.00`) graf ukazuje přátelské štítky na osách, např. `5.5M`, respektive v českém pojetí vizuálu.

## Shrnutí 
Aplikace je napsaná nesmírně čistě na architekturu **End-to-End**. Máme data z webu -> Přípravu & Učení -> Logiku odhadu -> Prezentaci uživateli. Kód nevyužívá takřka žádné globální stavové proměnné (vše se točí uvnitř ohraničených tříd), má oddělené logické zodpovědnosti (Solid Princip) a pro svou lehkost plně odpovídá profesionálním firemním softwarovým zvyklostem moderního Python developera.
