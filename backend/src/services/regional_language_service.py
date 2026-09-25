"""
Project ORCA — Regional Coastal Language Engine & Vernacular Fish Nomenclature
Supports:
1. Native Indic Scripts: Hindi (Devanagari), Tamil, Malayalam, Marathi, Bengali, Telugu, Gujarati.
2. Transliterated Romanized Input: Hinglish, Marathlish, Tanglish, Malayalam-English.
3. Vernacular Coastal Fish Directory: Regional names across Indian coastal states (Bangda, Surmai, Ayala, Mathi, Paplet, etc.).
"""
from typing import Dict, Any, List, Optional, Tuple
import re
import os
import json

# Comprehensive Vernacular Coastal Fish Directory
VERNACULAR_FISH_DIRECTORY: Dict[str, Dict[str, str]] = {
    "indian mackerel": {
        "en": "Indian Mackerel",
        "scientific": "Rastrelliger kanagurta",
        "hi": "Bangda (बांगडा)",
        "mr": "Bangda (बांगडा)",
        "ml": "Ayala (അയല)",
        "ta": "Kumla / Kanangeluthi (கானாங்கெளுத்தி)",
        "te": "Kanagarthalu (కానగంతలు)",
        "bn": "Bangda (বাংড়া)",
        "gu": "Bangdi (બાંગડી)",
        "kn": "Bangude (ಬಂಗುಡೆ)"
    },
    "mackerel": {
        "en": "Indian Mackerel",
        "scientific": "Rastrelliger kanagurta",
        "hi": "Bangda (बांगडा)",
        "mr": "Bangda (बांगडा)",
        "ml": "Ayala (അയല)",
        "ta": "Kumla (கானாங்கெளுத்தி)",
        "te": "Kanagarthalu (కానగంతలు)",
        "bn": "Bangda (বাংড়া)",
        "gu": "Bangdi (બાંગડી)",
        "kn": "Bangude (ಬಂಗುಡೆ)"
    },
    "seer fish": {
        "en": "Seer Fish / King Mackerel",
        "scientific": "Scomberomorus commerson",
        "hi": "Surmai (सुरमई)",
        "mr": "Surmai (सुरमई)",
        "ml": "Neymeen / Ayakoora (നെയ്മീൻ)",
        "ta": "Vanjaram (வஞ்சிரம்)",
        "te": "Vanjaram (వంజరం)",
        "bn": "Surmai",
        "gu": "Surmai",
        "kn": "Anjal (ಅಂಜಲ್)"
    },
    "kingfish": {
        "en": "Seer Fish / King Mackerel",
        "scientific": "Scomberomorus commerson",
        "hi": "Surmai (सुरमई)",
        "mr": "Surmai (सुरमई)",
        "ml": "Neymeen / Ayakoora (നെയ്മീൻ)",
        "ta": "Vanjaram (வஞ்சிரம்)",
        "te": "Vanjaram (వంజరం)",
        "bn": "Surmai",
        "gu": "Surmai",
        "kn": "Anjal (ಅಂಜಲ್)"
    },
    "yellowfin tuna": {
        "en": "Yellowfin Tuna",
        "scientific": "Thunnus albacares",
        "hi": "Gedar",
        "mr": "Gedar / Khavlya",
        "ml": "Kera / Choora (ചൂര)",
        "ta": "Surai (சூரை)",
        "te": "Soora (సూర)",
        "bn": "Tuna (টুনা)",
        "gu": "Gedar",
        "kn": "Kera Choora"
    },
    "tuna": {
        "en": "Yellowfin Tuna",
        "scientific": "Thunnus albacares",
        "hi": "Gedar / Tuna",
        "mr": "Gedar / Khavlya",
        "ml": "Choora (ചൂര)",
        "ta": "Surai (சூரை)",
        "te": "Soora (సూర)",
        "bn": "Tuna (টুনা)",
        "gu": "Gedar",
        "kn": "Choora"
    },
    "oil sardine": {
        "en": "Indian Oil Sardine",
        "scientific": "Sardinella longiceps",
        "hi": "Tarli (तारली)",
        "mr": "Tarli (तारली)",
        "ml": "Mathi / Chaala (മത്തി)",
        "ta": "Kavalai (கவலை)",
        "te": "Kavallu (కవళ్ళు)",
        "bn": "Khaira",
        "gu": "Tarli",
        "kn": "Boothai (ಭೂತಾಯಿ)"
    },
    "sardine": {
        "en": "Indian Oil Sardine",
        "scientific": "Sardinella longiceps",
        "hi": "Tarli (तारली)",
        "mr": "Tarli (तारली)",
        "ml": "Mathi / Chaala (മത്തി)",
        "ta": "Kavalai (கவலை)",
        "te": "Kavallu (కవళ్ళు)",
        "bn": "Khaira",
        "gu": "Tarli",
        "kn": "Boothai (ಭೂತಾಯಿ)"
    },
    "silver pomfret": {
        "en": "Silver Pomfret",
        "scientific": "Pampus argenteus",
        "hi": "Paplet (पापलेट)",
        "mr": "Paplet / Saranga (पापलेट)",
        "ml": "Vellavoli (വെള്ളവോലി)",
        "ta": "Vawaal (வாவல்)",
        "te": "Tella Chanduva (తెల్ల చందువ)",
        "bn": "Rupchanda (রূপচাঁদা)",
        "gu": "Vichuda (વિચુડા)",
        "kn": "Bili Manji"
    },
    "pomfret": {
        "en": "Silver Pomfret",
        "scientific": "Pampus argenteus",
        "hi": "Paplet (पापलेट)",
        "mr": "Paplet (पापलेट)",
        "ml": "Aavoli / Vellavoli (ആവോലി)",
        "ta": "Vawaal (வாவல்)",
        "te": "Chanduva (చందువ)",
        "bn": "Rupchanda (রূপচাঁদা)",
        "gu": "Vichuda",
        "kn": "Manji"
    },
    "skipjack tuna": {
        "en": "Skipjack Tuna",
        "scientific": "Katsuwonus pelamis",
        "hi": "Kuppa Gedar",
        "mr": "Kuppa Gedar",
        "ml": "Kuppa Choora (കുപ്പച്ചൂര)",
        "ta": "Kandayan Surai (கண்டையன் சூரை)",
        "te": "Gora Soora",
        "bn": "Skipjack Tuna",
        "gu": "Kuppa",
        "kn": "Kuppa Choora"
    },
    "hilsa": {
        "en": "Hilsa / River Shad",
        "scientific": "Tenualosa ilisha",
        "hi": "Palla (पल्ला)",
        "mr": "Palla (पल्ला)",
        "ml": "Hilsa",
        "ta": "Ullam (உள்ளம்)",
        "te": "Palasa (పలస)",
        "bn": "Ilish (ইলিশ)",
        "gu": "Palla / Chaksi",
        "kn": "Palla"
    },
    "threadfin bream": {
        "en": "Threadfin Bream",
        "scientific": "Nemipterus japonicus",
        "hi": "Lal Machli",
        "mr": "Rani / Tamb (राणी)",
        "ml": "Kilimeen / Chutta (കിളിമീൻ)",
        "ta": "Sankara (சங்கரா)",
        "te": "Chitti Mathi",
        "bn": "Rani",
        "gu": "Lal Machli",
        "kn": "Kempu Meenu"
    },
    "squid": {
        "en": "Squid / Cuttlefish",
        "scientific": "Loligo spp.",
        "hi": "Makul",
        "mr": "Ghol / Makul",
        "ml": "Koonthal / Kanava (കൂന്തൽ)",
        "ta": "Oosi Kanawa (கணவா)",
        "te": "Kalava",
        "bn": "Calmari",
        "gu": "Narsinga",
        "kn": "Bondaas",
        "ja": "Ika / Aori-ika (アオリイカ / 烏賊)",
        "zh": "Youyu (鱿鱼)",
        "es": "Calamar",
        "fr": "Calmar",
        "nl": "Pijlinktvis",
        "de": "Kalmar",
        "no": "Akkar / Blekksprut",
        "id": "Cumi-cumi",
        "ar": "حبار (Habbar)"
    },
    "ribbonfish": {
        "en": "Ribbonfish / Hairtail",
        "scientific": "Trichiurus lepturus",
        "hi": "Champa / Bala",
        "mr": "Bala / Piti (बाळा)",
        "ml": "Vaala (വാള)",
        "ta": "Savala (சவாலா)",
        "te": "Savalalu",
        "bn": "Churi (ছুরি)",
        "gu": "Piti",
        "kn": "Haalu Meenu",
        "ja": "Tachiuo (タチウオ / 太刀魚)",
        "zh": "Daiyu (带鱼)",
        "es": "Pez cinta",
        "fr": "Poisson-ruban",
        "nl": "Deegenvis",
        "de": "Haarschwanz",
        "no": "Hårstjert",
        "id": "Ikan Layur",
        "ar": "سمك السيف (Sayf)"
    },
    "sea bass": {
        "en": "Japanese Sea Bass / Suzuki",
        "scientific": "Lateolabrax japonicus",
        "hi": "Bhetki / Sea Bass",
        "mr": "Khajura / Bhetki",
        "ml": "Kalanchi",
        "ta": "Koduva (கொடுவா)",
        "te": "Pandugappa",
        "bn": "Bhetki (ভেটকি)",
        "gu": "Dangara",
        "kn": "Kurinji",
        "ja": "Suzuki (スズキ / 鱸)",
        "zh": "Luyu (鲈鱼)",
        "es": "Lubina",
        "fr": "Bar commun",
        "nl": "Zeebaars",
        "de": "Wolfsbarsch",
        "no": "Havabbor",
        "id": "Kakap Putih",
        "ar": "قاروص (Qaroos)"
    },
    "suzuki": {
        "en": "Japanese Sea Bass / Suzuki",
        "scientific": "Lateolabrax japonicus",
        "hi": "Sea Bass",
        "mr": "Bhetki",
        "ml": "Kalanchi",
        "ta": "Koduva",
        "te": "Pandugappa",
        "bn": "Bhetki",
        "gu": "Dangara",
        "kn": "Kurinji",
        "ja": "Suzuki (スズキ / 鱸)",
        "zh": "Luyu (鲈鱼)",
        "es": "Lubina",
        "fr": "Bar",
        "nl": "Zeebaars",
        "de": "Wolfsbarsch",
        "no": "Havabbor",
        "id": "Kakap Putih",
        "ar": "قاروص"
    },
    "horse mackerel": {
        "en": "Japanese Horse Mackerel / Aji",
        "scientific": "Trachurus japonicus",
        "hi": "Bangda / Kankada",
        "mr": "Kankada",
        "ml": "Paara / Ayala",
        "ta": "Paarai (பாறை)",
        "te": "Para",
        "bn": "Horse Mackerel",
        "gu": "Bangdi",
        "kn": "Kankada",
        "ja": "Ma-Aji (マアジ / 真鯵)",
        "zh": "Zhujiaoyu (竹荚鱼)",
        "es": "Jurel",
        "fr": "Chinchard",
        "nl": "Horsmakreel",
        "de": "Bastardmakrele",
        "no": "Hestmakrell",
        "id": "Ikan Selar",
        "ar": "شاخورة (Shakhura)"
    },
    "aji": {
        "en": "Japanese Horse Mackerel / Aji",
        "scientific": "Trachurus japonicus",
        "hi": "Bangda",
        "mr": "Kankada",
        "ml": "Paara",
        "ta": "Paarai",
        "te": "Para",
        "bn": "Horse Mackerel",
        "gu": "Bangdi",
        "kn": "Kankada",
        "ja": "Ma-Aji (マアジ / 真鯵)",
        "zh": "Zhujiaoyu (竹荚鱼)",
        "es": "Jurel",
        "fr": "Chinchard",
        "nl": "Horsmakreel",
        "de": "Bastardmakrele",
        "no": "Hestmakrell",
        "id": "Ikan Selar",
        "ar": "شاخورة"
    },
    "yellowtail": {
        "en": "Japanese Amberjack / Yellowtail / Buri",
        "scientific": "Seriola quinqueradiata",
        "hi": "Surmai / Amberjack",
        "mr": "Modaka / Buri",
        "ml": "Poomeen",
        "ta": "Pannai (பண்ணை)",
        "te": "Panna",
        "bn": "Amberjack",
        "gu": "Modaka",
        "kn": "Buri",
        "ja": "Buri / Hamachi (ブリ / 鰤)",
        "zh": "Shiyu (鰤鱼 / 黄尾鲼)",
        "es": "Pez limón / Seriola",
        "fr": "Sériole du Japon",
        "nl": "Geelstaartmakreel",
        "de": "Gelbschwanzmakrele",
        "no": "Gulhale",
        "id": "Ikan Kuwe",
        "ar": "سريولا (Seriola)"
    },
    "buri": {
        "en": "Japanese Amberjack / Yellowtail / Buri",
        "scientific": "Seriola quinqueradiata",
        "hi": "Amberjack",
        "mr": "Buri",
        "ml": "Poomeen",
        "ta": "Pannai",
        "te": "Panna",
        "bn": "Amberjack",
        "gu": "Modaka",
        "kn": "Buri",
        "ja": "Buri / Hamachi (ブリ / 鰤)",
        "zh": "Shiyu (鰤鱼)",
        "es": "Pez limón",
        "fr": "Sériole",
        "nl": "Geelstaartmakreel",
        "de": "Gelbschwanz",
        "no": "Gulhale",
        "id": "Ikan Kuwe",
        "ar": "سريولا"
    },
    "red sea bream": {
        "en": "Red Sea Bream / Madai",
        "scientific": "Pagrus major",
        "hi": "Lal Machli",
        "mr": "Tamb / Rani",
        "ml": "Kilimeen",
        "ta": "Sankara",
        "te": "Erra Chanduva",
        "bn": "Rani",
        "gu": "Lal Machli",
        "kn": "Kempu Meenu",
        "ja": "Madai (マダイ / 真鯛)",
        "zh": "Zhendiao (真鲷)",
        "es": "Dorada japonesa",
        "fr": "Daurade rouge",
        "nl": "Rode zeebrasem",
        "de": "Rote Meerbrasse",
        "no": "Rød havabbor",
        "id": "Ikan Kakap Merah",
        "ar": "دنيس أحمر (Danees)"
    },
    "tai": {
        "en": "Red Sea Bream / Madai",
        "scientific": "Pagrus major",
        "hi": "Lal Machli",
        "mr": "Tamb",
        "ml": "Kilimeen",
        "ta": "Sankara",
        "te": "Erra Chanduva",
        "bn": "Rani",
        "gu": "Lal Machli",
        "kn": "Kempu Meenu",
        "ja": "Madai (マダイ / 真鯛)",
        "zh": "Zhendiao (真鲷)",
        "es": "Dorada",
        "fr": "Daurade",
        "nl": "Zeebrasem",
        "de": "Meerbrasse",
        "no": "Havbrasme",
        "id": "Kakap Merah",
        "ar": "دنيس"
    },
    "pacific saury": {
        "en": "Pacific Saury / Sanma",
        "scientific": "Cololabis saira",
        "hi": "Tarli / Saury",
        "mr": "Bala / Sanma",
        "ml": "Mathi",
        "ta": "Savala",
        "te": "Savalalu",
        "bn": "Saury",
        "gu": "Piti",
        "kn": "Haalu Meenu",
        "ja": "Sanma (サンマ / 秋刀魚)",
        "zh": "Qiudaoyu (秋刀鱼)",
        "es": "Paparda del Pacífico",
        "fr": "Balaou du Japon",
        "nl": "Makreelgeep",
        "de": "Pazifischer Makrelenhecht",
        "no": "Stillehavsmakrellgjedde",
        "id": "Ikan Sanma",
        "ar": "صوري الهادئ"
    },
    "sanma": {
        "en": "Pacific Saury / Sanma",
        "scientific": "Cololabis saira",
        "hi": "Saury",
        "mr": "Sanma",
        "ml": "Mathi",
        "ta": "Savala",
        "te": "Savalalu",
        "bn": "Saury",
        "gu": "Piti",
        "kn": "Haalu Meenu",
        "ja": "Sanma (サンマ / 秋刀魚)",
        "zh": "Qiudaoyu (秋刀鱼)",
        "es": "Paparda",
        "fr": "Balaou",
        "nl": "Makreelgeep",
        "de": "Makrelenhecht",
        "no": "Makrellgjedde",
        "id": "Ikan Sanma",
        "ar": "صوري"
    },
    "cod": {
        "en": "Atlantic / Pacific Cod",
        "scientific": "Gadus morhua",
        "hi": "Gobro / Cod",
        "mr": "Gobro / Ghol",
        "ml": "Kalava",
        "ta": "Koduva",
        "te": "Kalava",
        "bn": "Cod",
        "gu": "Ghol",
        "kn": "Ghol",
        "ja": "Tara / Ma-dara (タラ / 真鱈)",
        "zh": "Xueyu (鳕鱼)",
        "es": "Bacalao",
        "fr": "Morue / Cabillaud",
        "nl": "Kabeljauw",
        "de": "Kabeljauw / Dorsch",
        "no": "Torsk",
        "id": "Ikan Kod",
        "ar": "سمك القد (Qadd)"
    },
    "salmon": {
        "en": "Pacific / Atlantic Salmon",
        "scientific": "Salmo salar / Oncorhynchus",
        "hi": "Ravas / Salmon",
        "mr": "Ravas (रावस)",
        "ml": "Salmon",
        "ta": "Kaala Meen",
        "te": "Maga Chepa",
        "bn": "Gurjali",
        "gu": "Ravas",
        "kn": "Ravas",
        "ja": "Sake / Sake-masu (サケ / 鮭)",
        "zh": "Sanwenyu (三文鱼 / 鲑鱼)",
        "es": "Salmón",
        "fr": "Saumon",
        "nl": "Zalm",
        "de": "Lachs",
        "no": "Laks",
        "id": "Ikan Salmon",
        "ar": "سلمون (Salmon)"
    }
}

# Dynamically load expanded marine species taxonomy dataset if available
TAXONOMY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "marine_species_taxonomy.json")
if os.path.exists(TAXONOMY_PATH):
    try:
        with open(TAXONOMY_PATH, "r", encoding="utf-8") as _tax_f:
            _tax_data = json.load(_tax_f)
            for _item in _tax_data.get("species", []):
                _common_en = _item.get("en", "")
                _sci = _item.get("scientific", "")
                _vern = _item.get("vernacular", {})
                _entry = {
                    "en": _common_en,
                    "scientific": _sci,
                    **_vern
                }
                VERNACULAR_FISH_DIRECTORY[_common_en.lower()] = _entry
                VERNACULAR_FISH_DIRECTORY[_item.get("id", "").replace("_", " ")] = _entry
                for _lang_code, _name_str in _vern.items():
                    _clean_local = re.sub(r'[\(\)]', '', _name_str).split('/')[0].strip().lower()
                    if _clean_local and _clean_local not in VERNACULAR_FISH_DIRECTORY:
                        VERNACULAR_FISH_DIRECTORY[_clean_local] = _entry
    except Exception:
        pass


class RegionalLanguageService:
    """
    Detects regional Indian coastal languages and transliterated Romanized inquiries,
    enriches advisories with vernacular fish names, and formats localized responses.
    """

    # Transliteration keyword patterns
    HINGLISH_PATTERNS = [
        r'\baaj\b', r'\bmausam\b', r'\bkaisa\b', r'\bkaise\b', r'\bhawa\b', r'\bkitna\b', r'\bkitni\b',
        r'\bsamundar\b', r'\bsamudra\b', r'\bpani\b', r'\bmachli\b', r'\bmachhli\b', r'\bpakadne\b',
        r'\bjaana\b', r'\bjaa\s+sakte\b', r'\blahrein\b', r'\blaharein\b', r'\btoofan\b', r'\bbaarish\b',
        r'\bbatao\b', r'\bbataye\b', r'\bkya\b', r'\bhain\b', r'\bhai\b', r'\bnahi\b', r'\bjaayen\b',
        r'\bjana\b', r'\bbangda\b', r'\bsurmai\b', r'\bpaplet\b', r'\bbombil\b', r'\bjhinga\b', r'\bkripya\b',
        r'\bkahani\b', r'\bfilam\b', r'\bgaana\b', r'\bkhana\b', r'\bkuch\b', r'\bbata\b'
    ]

    MARATHLISH_PATTERNS = [
        r'\bkasa\b', r'\bkase\b', r'\bahe\b', r'\bdaryavar\b', r'\bdaryat\b', r'\bjaycha\b', r'\bka\b',
        r'\baajche\b', r'\bvatavaran\b', r'\bwaryacha\b', r'\bwara\b', r'\bveg\b', r'\bmachhimari\b',
        r'\bbandar\b', r'\bkiti\b', r'\blamb\b', r'\bantar\b', r'\btarli\b', r'\bkinara\b', r'\bmanje\b',
        r'\bbombil\b', r'\bsaranga\b', r'\bkolambi\b', r'\bchimbori\b', r'\bgosht\b', r'\bsang\b'
    ]

    TANGLISH_PATTERNS = [
        r'\binniku\b', r'\bkadal\b', r'\bkaaththu\b', r'\bkaatru\b', r'\bepdi\b', r'\beppadi\b',
        r'\birukku\b', r'\bmeen\b', r'\bpidikka\b', r'\bpogalama\b', r'\bpoga\b', r'\balai\b',
        r'\balagal\b', r'\bvegam\b', r'\bsollunga\b', r'\bkadalukku\b', r'\bvanjaram\b', r'\bayala\b',
        r'\bkumla\b', r'\beral\b', r'\bnandu\b', r'\benna\b', r'\bpannalam\b'
    ]

    MALAYALAM_ENG_PATTERNS = [
        r'\binnathe\b', r'\bkaatu\b', r'\bkaatte\b', r'\bkadalil\b', r'\bpokamo\b', r'\bmeen\b',
        r'\bpidikkan\b', r'\bengane\b', r'\bchoora\b', r'\bmathi\b', r'\bkadal\b', r'\bshanthamano\b',
        r'\bchala\b', r'\bkarimeen\b', r'\bchemmeen\b', r'\bayala\b'
    ]

    BENGLISH_PATTERNS = [
        r'\baajke\b', r'\bmaachh\b', r'\bmach\b', r'\bdhorbo\b', r'\bdhora\b', r'\bilish\b',
        r'\bkothay\b', r'\bkemon\b', r'\bkemon\s+ache\b', r'\bobostha\b', r'\bbondor\b', r'\bbheshe\b'
    ]

    GUJLISH_PATTERNS = [
        r'\bkem\s+chho\b', r'\bdariya\b', r'\bdariyo\b', r'\bmachhli\b', r'\bbundar\b', r'\bhawa\b',
        r'\bjay\b', r'\bsakay\b', r'\bketlo\b', r'\bketli\b', r'\bkaro\b'
    ]

    ENGLISH_PATTERNS = [
        r'\b(?:what|where|when|which|how|is|are|the|near|off|today|tomorrow|safe|condition|conditions|weather|forecast|fishing|vessel|zone|zones|port|harbor)\b'
    ]

    # Global Port Language Patterns (Romanized / Native Keywords)
    JAPANESE_ROMANIZED_PATTERNS = [
        r'\b(?:tokyo|wan|tokyowan|sakana|maguro|saba|aji|iwashi|suzuki|tai|buri|sanma|gyojo|nami|kaze|donna|nan|imasu|desu|arimasu|ka|shukko)\b'
    ]
    CHINESE_PINYIN_PATTERNS = [
        r'\b(?:shanghai|kaohsiung|yuchang|buyu|fenglang|chaoxi|haishang|yulei|shenme|zainar|zenmeyang)\b'
    ]
    SPANISH_PATTERNS = [
        r'\b(?:pescado|peces|pesca|pescar|olas|viento|marea|seguro|barco|clima|donde|hay|tiempo|el\s+puerto)\b'
    ]
    FRENCH_PATTERNS = [
        r'\b(?:poisson|poissons|peche|pêche|vagues|vent|maree|marée|navire|bateau|securite|sécurité|meteo|météo|le\s+port|du\s+port)\b'
    ]
    PORTUGUESE_PATTERNS = [
        r'\b(?:peixe|peixes|pesca|pescar|ondas|vento|mare|maré|navio|barco|seguranca|segurança|clima|o\s+porto)\b'
    ]
    DUTCH_PATTERNS = [
        r'\b(?:vis|vissen|golven|getij|getijden|veilig|schip|boot|weer|waar|de\s+haven)\b'
    ]
    GERMAN_PATTERNS = [
        r'\b(?:fisch|fische|fischen|wellen|gezeiten|sicher|schiff|boot|wetter|wo|der\s+hafen)\b'
    ]
    NORWEGIAN_PATTERNS = [
        r'\b(?:fisk|fiske|bølger|bolger|tidevann|trygg|båt|bat|skip|vaer|vær|hvor)\b'
    ]
    INDONESIAN_PATTERNS = [
        r'\b(?:ikan|memancing|pelabuhan|ombak|angin|pasang|surut|aman|kapal|perahu|cuaca|laut|dimana)\b'
    ]
    ARABIC_PATTERNS = [
        r'\b(?:samak|sayd|bahr|amwaj|riyah|taqs|safina)\b'
    ]

    @classmethod
    def detect_language(cls, text: str) -> Tuple[str, str]:
        """
        Detects language and notation across all 50 global port regions.
        Returns tuple of (language_code, script_type):
        - language_code: 'en', 'ja', 'zh', 'ko', 'es', 'fr', 'pt', 'nl', 'de', 'no', 'ar', 'id', 'hi', 'mr', 'ta', 'ml', 'te', 'bn', 'gu', 'kn'
        - script_type: 'latin', 'japanese', 'chinese', 'korean', 'arabic', 'cyrillic', 'devanagari', 'tamil', 'malayalam', 'telugu', 'bengali', 'gujarati', 'latin_romanized'
        """
        raw = text.strip()
        lower = raw.lower()

        # 1. Native script detection
        has_kana = bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF]', raw))
        has_cjk = bool(re.search(r'[\u4E00-\u9FFF]', raw))

        if has_kana:
            return ("ja", "japanese")

        if has_cjk:
            if any(w in raw for w in [
                "上海", "广州", "深圳", "宁波", "青岛", "高雄", "洋山", "香港", "天津", "大连", "厦门",
                "天气", "气象", "风浪", "鱼类", "捕鱼", "渔场", "潮汐", "海况", "出海", "哪里", "什么", "怎么样", "带鱼", "鲈鱼"
            ]):
                return ("zh", "chinese")
            if any(w in raw for w in [
                "東京", "東京湾", "横浜", "大阪", "神戸", "名古屋", "真鱈", "秋刀魚", "鱸", "鰤", "鰹", "すか"
            ]):
                return ("ja", "japanese")
            return ("zh", "chinese")

        # Korean: Hangul
        if re.search(r'[\uAC00-\uD7AF\u1100-\u11FF]', raw):
            return ("ko", "korean")

        # Arabic script
        if re.search(r'[\u0600-\u06FF]', raw):
            return ("ar", "arabic")

        # Cyrillic script
        if re.search(r'[\u0400-\u04FF]', raw):
            return ("ru", "cyrillic")

        # Greek script
        if re.search(r'[\u0370-\u03FF]', raw):
            return ("el", "greek")

        # Indic scripts
        if re.search(r'[\u0900-\u097F]', raw):
            if any(w in lower for w in ["आहे", "कसा", "कसे", "दर्या", "वारा", "नाही", "जायचे", "सांगा", "मासे", "बोंबील", "कोळंबी"]):
                return ("mr", "devanagari")
            return ("hi", "devanagari")
        elif re.search(r'[\u0B80-\u0BFF]', raw):
            return ("ta", "tamil")
        elif re.search(r'[\u0D00-\u0D7F]', raw):
            return ("ml", "malayalam")
        elif re.search(r'[\u0C00-\u0C7F]', raw):
            return ("te", "telugu")
        elif re.search(r'[\u0980-\u09FF]', raw):
            return ("bn", "bengali")
        elif re.search(r'[\u0A80-\u0AFF]', raw):
            return ("gu", "gujarati")
        elif re.search(r'[\u0C80-\u0CFF]', raw):
            return ("kn", "kannada")

        # 2. Global Port Language Keyword Detection (Latin / Romanized)
        en_hits = sum(1 for p in cls.ENGLISH_PATTERNS if re.search(p, lower))
        ja_hits = sum(1 for p in cls.JAPANESE_ROMANIZED_PATTERNS if re.search(p, lower))
        zh_hits = sum(1 for p in cls.CHINESE_PINYIN_PATTERNS if re.search(p, lower))
        es_hits = sum(1 for p in cls.SPANISH_PATTERNS if re.search(p, lower))
        fr_hits = sum(1 for p in cls.FRENCH_PATTERNS if re.search(p, lower))
        pt_hits = sum(1 for p in cls.PORTUGUESE_PATTERNS if re.search(p, lower))
        nl_hits = sum(1 for p in cls.DUTCH_PATTERNS if re.search(p, lower))
        de_hits = sum(1 for p in cls.GERMAN_PATTERNS if re.search(p, lower))
        no_hits = sum(1 for p in cls.NORWEGIAN_PATTERNS if re.search(p, lower))
        id_hits = sum(1 for p in cls.INDONESIAN_PATTERNS if re.search(p, lower))
        ar_hits = sum(1 for p in cls.ARABIC_PATTERNS if re.search(p, lower))

        # Indic Romanized
        hinglish_hits = sum(1 for p in cls.HINGLISH_PATTERNS if re.search(p, lower))
        marathlish_hits = sum(1 for p in cls.MARATHLISH_PATTERNS if re.search(p, lower))
        tanglish_hits = sum(1 for p in cls.TANGLISH_PATTERNS if re.search(p, lower))
        mal_eng_hits = sum(1 for p in cls.MALAYALAM_ENG_PATTERNS if re.search(p, lower))
        benglish_hits = sum(1 for p in cls.BENGLISH_PATTERNS if re.search(p, lower))
        gujlish_hits = sum(1 for p in cls.GUJLISH_PATTERNS if re.search(p, lower))

        global_scores = [
            ("ja", ja_hits),
            ("zh", zh_hits),
            ("es", es_hits),
            ("fr", fr_hits),
            ("pt", pt_hits),
            ("nl", nl_hits),
            ("de", de_hits),
            ("no", no_hits),
            ("id", id_hits),
            ("ar", ar_hits),
            ("mr", marathlish_hits),
            ("ta", tanglish_hits),
            ("ml", mal_eng_hits),
            ("bn", benglish_hits),
            ("gu", gujlish_hits),
            ("hi", hinglish_hits),
        ]
        best_lang, best_score = max(global_scores, key=lambda x: x[1])

        if en_hits >= 2 and en_hits >= best_score:
            return ("en", "latin")

        if best_score >= 1:
            return (best_lang, "latin_romanized" if best_lang in ["hi", "mr", "ta", "ml", "bn", "gu", "ja", "zh"] else "latin")

        # Default
        return ("en", "latin")

    @classmethod
    def get_localized_fish_name(cls, english_name: str, lang: str = "hi") -> str:
        """
        Resolves local coastal vernacular name and scientific binomial for a fish species.
        e.g. 'Indian Mackerel' -> 'Indian Mackerel (Rastrelliger kanagurta) — Bangda (बांगडा)'.
        """
        lookup = english_name.strip().lower()
        if lookup in VERNACULAR_FISH_DIRECTORY:
            entry = VERNACULAR_FISH_DIRECTORY[lookup]
            local = entry.get(lang, entry.get("hi", entry.get("en", english_name)))
            sci = entry.get("scientific")
            sci_str = f" (*{sci}*)" if sci else ""
            return f"{entry['en']}{sci_str} — {local}"
        
        # Check partial
        for key, entry in VERNACULAR_FISH_DIRECTORY.items():
            if key in lookup or lookup in key:
                local = entry.get(lang, entry.get("hi", entry.get("en", english_name)))
                sci = entry.get("scientific")
                sci_str = f" (*{sci}*)" if sci else ""
                return f"{entry['en']}{sci_str} — {local}"

        return english_name

    @classmethod
    def format_localized_out_of_domain_reply(
        cls,
        raw_msg: str,
        lang: str,
        script: str
    ) -> Tuple[str, List[str]]:
        """
        Formats a polite, helpful rejection and redirection in the user's exact regional language and script.
        """
        clean_msg = raw_msg[:60] + ("..." if len(raw_msg) > 60 else "")

        # 1. HINDI DEVANAGARI
        if script == "devanagari" and lang == "hi":
            reply = (
                f"**[समुद्री कार्यक्षेत्र सूचना / Marine Intelligence Notice]**\n\n"
                f"आपकी क्वेरी (\"*{clean_msg}*\") समुद्री संचालन, मत्स्य पालन, अथवा तटीय नेविगेशन से संबंधित नहीं है।\n\n"
                f"**प्रोजेक्ट ओर्का (Project ORCA) के तहत आप निम्न जानकारी प्राप्त कर सकते हैं:**\n"
                f"- **तटीय बंदरगाह:** उदा. मुंबई ससून डॉक्स, कोच्चि, विशाखापत्तनम, वेरावल, पारादीप\n"
                f"- **संभाव्य मत्स्य क्षेत्र (PFZ):** बांगडा (Bangda), सुरमई (Surmai), पापलेट (Paplet) हॉटस्पॉट\n"
                f"- **समुद्री मौसम व सुरक्षा:** लहरों की ऊंचाई, हवा की गति, और नौका निकासी (Vessel Clearance)"
            )
            suggested = ["मुंबई बंदरगाह (Mumbai Port)", "कोच्चि हार्बर (Kochi)", "बांगडा हॉटस्पॉट (Bangda PFZ)", "24h मौसम (Weather)"]
            return reply, suggested

        # 2. MARATHI DEVANAGARI
        elif script == "devanagari" and lang == "mr":
            reply = (
                f"**[सागरी कार्यक्षेत्र सूचना / Marine Domain Notice]**\n\n"
                f"आपला प्रश्न (\"*{clean_msg}*\") सागरी नौकानयन, मासेमारी, किंवा हवामानाशी संबंधित नाही.\n\n"
                f"**प्रोजेक्ट ओर्का (Project ORCA) सागरी सहाय्यक खालील बाबींमध्ये मदत करू शकतो:**\n"
                f"- **किनारी बंदरे:** उदा. मुंबई ससून डॉक्स, रत्नागिरी, दापोली हर्णे, मालवण, गोवा\n"
                f"- **संभाव्य मासेमारी क्षेत्र (PFZ):** बांगडा (Bangda), सुरमई (Surmai), पापलेट (Paplet), बोंबील (Bombil)\n"
                f"- **सागरी हवामान व सुरक्षा:** लाटांची उंची, वाऱ्याचा वेग, आणि बोट योग्यता प्रमाणपत्र"
            )
            suggested = ["मुंबई ससून डॉक्स (Mumbai)", "दापोली हर्णे (Dapoli)", "बांगडा मासेमारी (Bangda PFZ)", "हवामान तपशील (Weather)"]
            return reply, suggested

        # 3. HINGLISH (Romanized Hindi)
        elif script == "latin_romanized" and lang == "hi":
            reply = (
                f"**[Samundari Domain Notice]**\n\n"
                f"Aapki query (\"*{clean_msg}*\") samundari kshetra, machhimari, ya coastal navigation se judi nahi hai.\n\n"
                f"**Project ORCA marine assistant se aap yeh pooch sakte hain:**\n"
                f"- **Coastal Ports & Harbors:** jaise Mumbai Sassoon Docks, Kochi, Chennai Kasimedu, Dapoli, Veraval\n"
                f"- **Machli Pakadne ke Kshetr (PFZ):** Bangda (Mackerel), Surmai (Kingfish), Paplet (Pomfret) hotspots\n"
                f"- **Mausam & Suraksha:** Laharon ki unchai (wave height), hawa ki raftaar, aur boat seaworthiness clearance"
            )
            suggested = ["Mumbai Port Status", "Dapoli Harnai Sector", "Bangda Fishing Hotspot", "Check Wave & Wind Forecast"]
            return reply, suggested

        # 4. MARATHLISH (Romanized Marathi)
        elif script == "latin_romanized" and lang == "mr":
            reply = (
                f"**[Daryavardi Kshetr Suchana]**\n\n"
                f"Tumcha prashna (\"*{clean_msg}*\") daryavardi vatavaran, machhimari kinva bot chalavnyashi sambandhit nahi.\n\n"
                f"**Project ORCA daryavardi sahayyak ya goshtit madat karu shakto:**\n"
                f"- **Kinari Bandare:** e.g., Mumbai Sassoon Docks, Ratnagiri, Dapoli Harnai, Malvan, Goa\n"
                f"- **Machhimari Kshetr (PFZ):** Bangda, Surmai, Bombil, Paplet che taaje zones\n"
                f"- **Vatavaran & Suraksha:** Lataan chi unchi (wave height), waryacha veg, ani bot seaworthiness suchana"
            )
            suggested = ["Mumbai Sassoon Docks", "Dapoli Harnai Ahwal", "Bangda Machhimari Kshetr", "Latanche Vatavaran"]
            return reply, suggested

        # 5. TAMIL NATIVE
        elif script == "tamil":
            reply = (
                f"**[கடல்சார் கள அறிவிப்பு / Marine Domain Notice]**\n\n"
                f"உங்கள் கேள்வி (\"*{clean_msg}*\") கடல்சார் செயல்பாடுகள், மீன்பிடி மண்டலங்கள் அல்லது வானிலையுடன் தொடர்புடையது அல்ல.\n\n"
                f"**Project ORCA கடல்சார் நுண்ணறிவு அமைப்பு பின்வருவனவற்றிற்கு வழிகாட்டும்:**\n"
                f"- **துறைமுகங்கள்:** சென்னை காசிமேடு, தூத்துக்குடி, ராமேஸ்வரம், கொச்சி\n"
                f"- **சாத்தியமான மீன்பிடி மண்டலங்கள் (PFZ):** வஞ்சிரம் (Vanjaram), குமலா (Kumla), சூரை (Tuna), கணவா பகுதிகள்\n"
                f"- **கடல் நிலை & பாதுகாப்பு:** அலைகளின் உயரம், காற்றின் வேகம், மற்றும் படகு பாதுகாப்பு அனுமதி"
            )
            suggested = ["சென்னை காசிமேடு (Chennai)", "ராமேஸ்வரம் தளம் (Rameswaram)", "வஞ்சிரம் மீன்பிடி (Vanjaram PFZ)", "வானிலை அறிக்கை (Weather)"]
            return reply, suggested

        # 6. TANGLISH (Romanized Tamil)
        elif script == "latin_romanized" and lang == "ta":
            reply = (
                f"**[Kadal Domain Notice]**\n\n"
                f"Unga kelvi (\"*{clean_msg}*\") kadal saarntha vishayam, meenpidi, or boat navigation patriya vishayam illai.\n\n"
                f"**Project ORCA marine copilot-la neenga idhula ketkalam:**\n"
                f"- **Coastal Ports:** e.g., Chennai Kasimedu, Thoothukudi, Rameswaram Base, Kochi Harbor\n"
                f"- **Meenpidi Valayam (PFZ):** Vanjaram (Seer fish), Kumla (Mackerel), Soorai (Tuna) hotspots\n"
                f"- **Kadal Vanilai & Safety:** Alaiyin uyarum (wave height), kaatrin vegam, and boat clearance"
            )
            suggested = ["Chennai Kasimedu", "Rameswaram Base", "Vanjaram Fishing Zone", "Wave & Wind Report"]
            return reply, suggested

        # 7. MALAYALAM NATIVE OR ROMANIZED
        elif script == "malayalam" or (script == "latin_romanized" and lang == "ml"):
            reply = (
                f"**[സമുദ്ര വിവര അറിയിപ്പ് / Marine Domain Notice]**\n\n"
                f"നിങ്ങളുടെ ചോദ്യം (\"*{clean_msg}*\") സമുദ്ര നാവിഗേഷൻ, മത്സ്യബന്ധനം അല്ലെങ്കിൽ സമുദ്ര കാലാവസ്ഥയുമായി ബന്ധപ്പെട്ടതല്ല.\n\n"
                f"**പ്രോജക്റ്റ് ഓർക്ക (Project ORCA) മറൈൻ ഇന്റലിജൻസ് പ്ലാറ്റ്‌ഫോം വഴി നിങ്ങൾക്ക് ഇവ ചോദിക്കാം:**\n"
                f"- **തീരദേശ തുറമുഖങ്ങൾ:** കൊച്ചി, വിഴിഞം, ബേപ്പൂർ, രാമേശ്വരം\n"
                f"- **സാധ്യതാ മത്സ്യബന്ധന മേഖലകൾ (PFZ):** അയല (Ayala), മത്തി (Mathi), നെയ്മീൻ (Neymeen), ചൂര മേഖലകൾ\n"
                f"- **കാലാവസ്ഥയും സുരക്ഷയും:** തിരമാലയുടെ ഉയരം, കാറ്റിന്റെ വേഗത, ബോട്ട് സുരക്ഷ"
            )
            suggested = ["കൊച്ചി തുറമുഖം (Kochi)", "വിഴിഞം (Vizhinjam)", "അയല മത്തി മേഖല (PFZ)", "കാലാവസ്ഥ (Weather)"]
            return reply, suggested

        # 8. BENGALI
        elif script == "bengali" or (script == "latin_romanized" and lang == "bn"):
            reply = (
                f"**[সামুদ্রিক ডোমেন নোটিশ / Marine Domain Notice]**\n\n"
                f"আপনার প্রশ্নটি (\"*{clean_msg}*\") সামুদ্রিক নৌচলাচল, মৎস্য শিকার বা উপকূলীয় আবহাওয়া সম্পর্কিত নয়।\n\n"
                f"**Project ORCA সামুদ্রিক গোয়েন্দা ব্যবস্থা থেকে আপনি যা জানতে পারেন:**\n"
                f"- **উপকূলীয় বন্দর:** কলকাতা, পারাদীপ, হলদিয়া, দিঘা, চেন্নাই\n"
                f"- **সম্ভাব্য মৎস্য অঞ্চল (PFZ):** ইলিশ (Ilish), রূপচাঁদা (Pomfret), ভেটকি (Bhetki) জোন\n"
                f"- **সমুদ্রের আবহাওয়া ও নিরাপত্তা:** ঢেউয়ের উচ্চতা, বাতাসের গতি, এবং নৌযান অনুমোদন"
            )
            suggested = ["কলকাতা বন্দর (Kolkata)", "পারাদীপ (Paradip)", "ইলিশ মৎস্য জোন (Ilish PFZ)", "সমুদ্রের আবহাওয়া (Weather)"]
            return reply, suggested

        # 9. JAPANESE
        elif lang == "ja" or script == "japanese":
            reply = (
                f"**[海洋業務ドメイン通知 / Marine Intelligence Notice]**\n\n"
                f"ご入力いただいた内容（\"*{clean_msg}*\"）は、海洋気象、漁場、船舶航行、または沿岸港湾に関する問い合わせとして認識されませんでした。\n\n"
                f"**Project ORCA 海洋インテリジェンス・コパイロットで確認可能な情報:**\n"
                f"- **主要港湾・拠点:** 東京湾 (Tokyo Bay)、横浜港、大阪港、シンガポール、ロッテルダム\n"
                f"- **有望漁場 (PFZ):** マグロ (Tuna)、サバ (Mackerel)、アジ、スズキの好漁場・水温フロント\n"
                f"- **気象・航行安全:** 有義波高、風速、海面水温 (SST)、船舶出港可否判定 (Seaworthiness)"
            )
            suggested = ["東京湾 (Tokyo Bay)", "横浜港 (Yokohama)", "有望漁場 (PFZ Hotspot)", "波高・風速予測 (Weather)"]
            return reply, suggested

        # 10. CHINESE
        elif lang == "zh" or script == "chinese":
            reply = (
                f"**[海洋专业领域提示 / Marine Domain Notice]**\n\n"
                f"您的查询（\"*{clean_msg}*\"）未包含海洋气象、渔业捕捞、船舶适航或沿岸港口相关航海要素。\n\n"
                f"**Project ORCA 海洋智能助理可为您提供以下服务:**\n"
                f"- **全球重要港口:** 上海港 (Shanghai)、洋山深水港、宁波舟山、高雄港、新加坡港\n"
                f"- **潜在渔场 (PFZ):** 金枪鱼、鲭鱼、带鱼热点水温锋面与叶绿素羽流\n"
                f"- **海况与安全:** 有效波高、海面风速、海表温度 (SST) 及船舶出海适航矩阵"
            )
            suggested = ["上海港 (Shanghai)", "宁波舟山 (Ningbo)", "潜在渔场 (PFZ Hotspot)", "海况与风浪 (Marine Weather)"]
            return reply, suggested

        # 11. KOREAN
        elif lang == "ko" or script == "korean":
            reply = (
                f"**[해양 도메인 안내 / Marine Domain Notice]**\n\n"
                f"입력하신 쿼리(\"*{clean_msg}*\")는 해양 기상, 어장 탐색, 항해 또는 연안 항만 관련 질의로 확인되지 않았습니다.\n\n"
                f"**Project ORCA 해양 관측 시스템 안내:**\n"
                f"- **주요 항만:** 부산항 (Busan), 인천항, 도쿄만, 싱가포르항\n"
                f"- **유망 어장 (PFZ):** 고등어, 참치, 오징어 수온 전선대 및 플랑크톤 분포\n"
                f"- **해양 기상 및 안전:** 파고, 풍속, 해수면 온도(SST), 선박 출항 허가 기준"
            )
            suggested = ["부산항 (Busan Port)", "유망 어장 (PFZ Hotspot)", "해양 날씨 (Weather)", "선박 안전 (Safety)"]
            return reply, suggested

        # 12. SPANISH
        elif lang == "es":
            reply = (
                f"**[Aviso de Dominio Marítimo / Marine Domain Notice]**\n\n"
                f"Su consulta (\"*{clean_msg}*\") no contiene referencias a operaciones marítimas, meteorología oceánica, zonas de pesca o navegación costera.\n\n"
                f"**Project ORCA puede asistirle con:**\n"
                f"- **Puertos Estratégicos:** Barcelona, Valencia, Algeciras, Santos, Callao\n"
                f"- **Zonas Potenciales de Pesca (ZPP):** Atún, caballa, sardina y gradientes térmicos Sentinel-3\n"
                f"- **Estado del Mar y Seguridad:** Altura de olas, viento, temperatura superficial y despacho marítimo"
            )
            suggested = ["Puerto de Barcelona", "Zona de Pesca (PFZ)", "Previsión de Olas", "Seguridad del Barco"]
            return reply, suggested

        # 13. FRENCH
        elif lang == "fr":
            reply = (
                f"**[Notice Maritime / Marine Domain Notice]**\n\n"
                f"Votre requête (\"*{clean_msg}*\") ne mentionne pas d'opérations maritimes, d'océanographie, de zones de pêche ou de navigation côtière.\n\n"
                f"**Project ORCA peut vous fournir:**\n"
                f"- **Grands Ports:** Port de Marseille, Le Havre, Rotterdam, Singapour\n"
                f"- **Zones Potentielles de Pêche (PFZ):** Thon, maquereau, fronts thermiques et panaches de chlorophylle\n"
                f"- **Météo et Sécurité:** Hauteur des vagues, vitesse du vent, SST et navigabilité du navire"
            )
            suggested = ["Port de Marseille", "Front Halieutique (PFZ)", "Météo et Vagues", "Sécurité Navire"]
            return reply, suggested

        # 14. DUTCH
        elif lang == "nl":
            reply = (
                f"**[Maritieme Kennisgeving / Marine Domain Notice]**\n\n"
                f"Uw vraag (\"*{clean_msg}*\") bevat geen verwijzing naar maritieme operaties, zeegang, visgronden of kustnavigatie.\n\n"
                f"**Project ORCA kan u helpen met:**\n"
                f"- **Wereldhavens:** Haven van Rotterdam, Maasvlakte, Vlaardingen, Antwerpen\n"
                f"- **Potentiële Viszones (PFZ):** Makreel, kabeljauw, thermische gradiënten en chlorofylpluimen\n"
                f"- **Zeegang & Veiligheid:** Golfhoogte, windsnelheid, watertemperatuur (SST) en zeewaardigheid"
            )
            suggested = ["Haven van Rotterdam", "Maasvlakte Terminal", "Viszone (PFZ)", "Golf- en Windverwachting"]
            return reply, suggested

        # 15. GERMAN
        elif lang == "de":
            reply = (
                f"**[Maritimer Hinweis / Marine Domain Notice]**\n\n"
                f"Ihre Anfrage (\"*{clean_msg}*\") enthält keine Bezüge zu Seefahrt, Ozeanographie, Fischereizonen oder Küstennavigation.\n\n"
                f"**Project ORCA unterstützt Sie bei:**\n"
                f"- **Häfen:** Hamburger Hafen, Bremerhaven, Rotterdam, Singapur\n"
                f"- **Potenzielle Fischereizonen (PFZ):** Makrele, Hering, Kabeljau und Temperaturfronten\n"
                f"- **Seegang & Sicherheit:** Wellenhöhe, Windgeschwindigkeit, Wassertemperatur (SST) und Auslaufstatus"
            )
            suggested = ["Hamburger Hafen", "Fischereizone (PFZ)", "Wellen- & Windbericht", "Schiffssicherheit"]
            return reply, suggested

        # 16. NORWEGIAN
        elif lang == "no":
            reply = (
                f"**[Maritimt Varsel / Marine Domain Notice]**\n\n"
                f"Forespørselen din (\"*{clean_msg}*\") har ingen referanser til maritime operasjoner, havforhold, fiskesoner eller navigasjon.\n\n"
                f"**Project ORCA kan bistå med:**\n"
                f"- **Kysthavner:** Bergen havn, Oslo, Rotterdam, Nordsjøen\n"
                f"- **Potensielle Fiskesoner (PFZ):** Torsk, makrell, sild og oseaniske temperaturfronter\n"
                f"- **Havtilstand & Sikkerhet:** Bølgehøyde, vindstyrke, overflatetemperatur (SST) og sjødyktighet"
            )
            suggested = ["Bergen Havn", "Fiskesone (PFZ)", "Bølge- og Vindvarsel", "Sjødyktighet"]
            return reply, suggested

        # 17. ARABIC
        elif lang == "ar" or script == "arabic":
            reply = (
                f"**[إشعار النطاق البحري / Marine Domain Notice]**\n\n"
                f"استفسارك (\"*{clean_msg}*\") لا يتضمن إشارة إلى العمليات البحرية، مصائد الأسماك، أحوال الطقس الملاحي أو الموانئ الساحلية.\n\n"
                f"**مشروع أوركا (Project ORCA) يوفر لك البيانات التالية:**\n"
                f"- **الموانئ الاستراتيجية:** ميناء راشد (دبي)، جبل علي، الدوحة، الإسكندرية\n"
                f"- **مناطق الصيد الواعدة (PFZ):** نقاط تجمع التونة، الهامور، الشعري والجبهات الحرارية\n"
                f"- **أحوال البحر والسلامة:** ارتفاع الموج، سرعة الرياح، حرارة سطح البحر وصلاحية الإبحار"
            )
            suggested = ["ميناء دبي (Dubai Port)", "ميناء جبل علي", "منطقة الصيد (PFZ)", "حالة البحر والطقس"]
            return reply, suggested

        # 18. INDONESIAN
        elif lang == "id":
            reply = (
                f"**[Pemberitahuan Domain Maritim / Marine Domain Notice]**\n\n"
                f"Pertanyaan Anda (\"*{clean_msg}*\") tidak memuat referensi tentang operasi maritim, perikanan, cuaca laut, atau navigasi pelabuhan.\n\n"
                f"**Project ORCA dapat membantu Anda dengan:**\n"
                f"- **Pelabuhan Utama:** Tanjung Priok Jakarta, Pelabuhan Singapura, Surabaya\n"
                f"- **Zona Potensial Penangkapan Ikan (ZPPI):** Daerah kaya klorofil & suhu permukaan laut untuk tongkol, cakalang, dan kembung\n"
                f"- **Kondisi Laut & Keselamatan:** Tinggi gelombang, kecepatan angin, suhu laut (SPL), dan kelaikan berlayar kapal"
            )
            suggested = ["Tanjung Priok Jakarta", "Pelabuhan Singapura", "Zona Penangkapan Ikan (ZPPI)", "Prakiraan Gelombang & Angin"]
            return reply, suggested

        # 19. DEFAULT ENGLISH
        else:
            reply = (
                f"**[No Marine Reference Detected]**\n\n"
                f"Your query (\"*{clean_msg}*\") contains no reference to maritime operations, oceanography, fishing zones, coastal navigation, or valid geographic coordinates.\n\n"
                f"**How I can assist you:**\n"
                f"- **Global & Satellite Ports:** e.g., *'Port of Tokyo (Tokyo Bay)'*, *'Port of Singapore'*, *'Port of Shanghai'*, *'Port of Rotterdam'*, *'Mumbai Sassoon Docks'*\n"
                f"- **Potential Fishing Zones (PFZ):** e.g., *'Where can I catch fish in Tokyo Bay?'*, *'Where can I catch Bangda near Ratnagiri?'*\n"
                f"- **Sea Basin Conditions:** e.g., *'Bay of Bengal details'*, *'Northwest Pacific status'*\n"
                f"- **Vessel Navigation & Safety:** e.g., *'Is it safe for a Motorized Skiff to sail from Rameswaram today?'*"
            )
            suggested = ["Port of Tokyo (Tokyo Bay)", "Port of Singapore", "Check 17.8°N, 84.2°E", "Bay of Bengal Details"]
            return reply, suggested

    @classmethod
    def localize_species_list(cls, species_list: List[str], lang: str = "hi") -> List[str]:
        """
        Returns species list enriched with regional vernacular coastal names.
        """
        result = []
        for s in species_list:
            result.append(cls.get_localized_fish_name(s, lang))
        return result

    @classmethod
    def format_regional_reply(
        cls,
        lang: str,
        script: str,
        location_label: Optional[str] = "Coastal Sector",
        wave: float = 0.0,
        wind: float = 0.0,
        sst: float = 0.0,
        species_list: Optional[List[str]] = None,
        risk_badge: str = "[CLEAR]",
        risk_summary: str = "",
        bearing_info: Optional[str] = None,
        include_vessel_matrix: bool = False
    ) -> str:
        """
        Generates a culturally attuned regional marine advisory in the user's notation.
        """
        loc_str = location_label or "Coastal Sector"
        enriched_species = cls.localize_species_list(species_list or [], lang)
        species_str = ", ".join(enriched_species)

        # 1. HINGLISH (Romanized Hindi)
        if lang == "hi" and script == "latin_romanized":
            bearing_block = f"\n- **Disha & Antar (Nav Bearing):** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**Jahaz Suraksha Nirdesh (Vessel Seaworthiness):**\n"
                f"- **Clearance Status:** **{risk_badge}**\n"
                f"- **Salla (Advisory):** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**Samundari Suraksha & Mausam Advisory ({loc_str}):**\n\n"
                f"- **Lahar ki Unchai (Wave Height):** **{wave} m**\n"
                f"- **Hawa ki Gati (Wind Speed):** **{wind} km/h**\n"
                f"- **Samundar Ka Tapman (SST):** **{sst} °C**\n"
                f"- **Machli Pakadne ke Kshetr (Target Fish Hotspot):** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 2. MARATHLISH (Romanized Marathi)
        elif lang == "mr" and script == "latin_romanized":
            bearing_block = f"\n- **Disha ani Antar (Nav Bearing):** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**Bot Seaworthiness Matrix (Vessel Safety):**\n"
                f"- **Clearance Status:** **{risk_badge}**\n"
                f"- **Suchana:** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**Daryavardi Suraksha & Vatavaran Ahwal ({loc_str}):**\n\n"
                f"- **Lataan Chi Unchi (Wave Height):** **{wave} m**\n"
                f"- **Waryacha Veg (Wind Speed):** **{wind} km/h**\n"
                f"- **Samudra Tapman (SST):** **{sst} °C**\n"
                f"- **Machhimari Kshetr (PFZ Hotspot):** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 3. TANGLISH (Romanized Tamil)
        elif lang == "ta" and script == "latin_romanized":
            bearing_block = f"\n- **Thisai & Thooram (Nav Bearing):** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**Padagu Paathukappu Nilai (Vessel Seaworthiness):**\n"
                f"- **Clearance Status:** **{risk_badge}**\n"
                f"- **Arivuraikal:** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**Kadal Paathukappu & Vanilai Arikkai ({loc_str}):**\n\n"
                f"- **Alaiyin Uyarum (Wave Height):** **{wave} m**\n"
                f"- **Katrin Vegam (Wind Speed):** **{wind} km/h**\n"
                f"- **Kadal Veppanilai (SST):** **{sst} °C**\n"
                f"- **Meenpidi Valayam (PFZ Hotspot):** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 4. NATIVE DEVANAGARI (Hindi / Marathi)
        elif script == "devanagari":
            if lang == "mr":
                vessel_block = (
                    f"\n\n**नौका सुरक्षा व योग्यता (Vessel Matrix):**\n"
                    f"- **स्थिती (Status):** **{risk_badge}**\n"
                    f"- **सूचना (Advisory):** {risk_summary}"
                ) if include_vessel_matrix else ""
                return (
                    f"**सागरी हवामान व मासेमारी सुरक्षा अहवाल ({loc_str}):**\n\n"
                    f"- **लाटांची उंची (Wave Height):** **{wave} m**\n"
                    f"- **वाऱ्याचा वेग (Wind Speed):** **{wind} km/h**\n"
                    f"- **समुद्राचे तापमान (SST):** **{sst} °C**\n"
                    f"- **संभाव्य मासेमारी क्षेत्र (PFZ Hotspot):** {species_str}"
                    f"{vessel_block}"
                )
            else:
                vessel_block = (
                    f"\n\n**पोत सुरक्षा एवं सागरीय निकासी (Vessel Matrix):**\n"
                    f"- **स्थिति (Status):** **{risk_badge}**\n"
                    f"- **परामर्श (Advisory):** {risk_summary}"
                ) if include_vessel_matrix else ""
                return (
                    f"**समुद्री सुरक्षा एवं मौसम परामर्श ({loc_str}):**\n\n"
                    f"- **लहरों की ऊंचाई (Wave Height):** **{wave} m**\n"
                    f"- **हवा की गति (Wind Speed):** **{wind} km/h**\n"
                    f"- **समुद्र का तापमान (SST):** **{sst} °C**\n"
                    f"- **मत्स्य क्षेत्र (Target Species):** {species_str}"
                    f"{vessel_block}"
                )

        # 5. NATIVE TAMIL
        elif script == "tamil":
            vessel_block = (
                f"\n\n**படகு பாதுகாப்பு அறிக்கை (Vessel Matrix):**\n"
                f"- **நிலை (Status):** **{risk_badge}**\n"
                f"- **வழிகாட்டுதல் (Advisory):** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**கடல் பாதுகாப்பு மற்றும் வானிலை அறிக்கை ({loc_str}):**\n\n"
                f"- **அலைகளின் உயரம் (Wave Height):** **{wave} m**\n"
                f"- **காற்றின் வேகம் (Wind Speed):** **{wind} km/h**\n"
                f"- **கடல் மேற்பரப்பு வெப்பநிலை (SST):** **{sst} °C**\n"
                f"- **இலக்கு மீன் வளங்கள் (Target Species):** {species_str}"
                f"{vessel_block}"
            )

        # 6. JAPANESE (Tokyo Bay, Yokohama, Osaka, Kobe, Nagoya)
        elif lang == "ja" or script == "japanese":
            bearing_block = f"\n- **航行針路と距離 (Nav Bearing):** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**船舶航行安全性および出港基準 (Vessel Seaworthiness Matrix):**\n"
                f"- **出港可否判定 (Status):** **{risk_badge}**\n"
                f"- **航行安全勧告 (Advisory Directive):** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**海洋気象および漁業安全情報 ({loc_str}):**\n\n"
                f"- **有義波高 (Significant Wave Height):** **{wave} m**\n"
                f"- **表面風速 (Wind Speed):** **{wind} km/h**\n"
                f"- **海面水温 (SST):** **{sst} °C**\n"
                f"- **有望漁場・対象魚種 (Target Pelagic Species / PFZ):** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 7. CHINESE (Shanghai, Ningbo, Shenzhen, Guangzhou, Qingdao, Kaohsiung)
        elif lang == "zh" or script == "chinese":
            bearing_block = f"\n- **航向与距离 (Nav Bearing):** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**船舶适航与出海安全评估 (Vessel Matrix):**\n"
                f"- **放行状态 (Clearance Status):** **{risk_badge}**\n"
                f"- **海事指引 (Advisory Directive):** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**海洋气象与渔业安全通报 ({loc_str}):**\n\n"
                f"- **有效波高 (Significant Wave Height):** **{wave} m**\n"
                f"- **海面风速 (Wind Speed):** **{wind} km/h**\n"
                f"- **海表温度 (SST):** **{sst} °C**\n"
                f"- **潜在渔场重点鱼种 (Target Pelagic Species / PFZ):** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 8. KOREAN (Busan, Incheon, Ulsan)
        elif lang == "ko" or script == "korean":
            bearing_block = f"\n- **항로 방위 및 거리 (Nav Bearing):** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**선박 안전 운항 및 출항 기준 (Vessel Seaworthiness Matrix):**\n"
                f"- **출항 허가 상태 (Status):** **{risk_badge}**\n"
                f"- **안전 권고 사항 (Advisory):** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**해양 기상 및 어로 안전 정보 ({loc_str}):**\n\n"
                f"- **유의 파고 (Wave Height):** **{wave} m**\n"
                f"- **해상 풍속 (Wind Speed):** **{wind} km/h**\n"
                f"- **해수면 온도 (SST):** **{sst} °C**\n"
                f"- **유망 어장 및 주요 어종 (Target Species / PFZ):** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 9. SPANISH (Barcelona, Valencia, Algeciras, Santos, Callao, Buenos Aires)
        elif lang == "es":
            bearing_block = f"\n- **Rumbo y Distancia de Navegación:** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**Matriz de Seguridad y Navegabilidad del Barco:**\n"
                f"- **Estado de Despacho:** **{risk_badge}**\n"
                f"- **Aviso Operacional:** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**Aviso Meteorológico y de Pesca Marítima ({loc_str}):**\n\n"
                f"- **Altura Significativa de Ola:** **{wave} m**\n"
                f"- **Velocidad del Viento:** **{wind} km/h**\n"
                f"- **Temperatura Superficial del Mar (TSM):** **{sst} °C**\n"
                f"- **Especies Objetivo en Zona de Pesca (ZPP):** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 10. FRENCH (Marseille, Le Havre, Dunkirk)
        elif lang == "fr":
            bearing_block = f"\n- **Cap et Distance de Navigation:** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**Matrice de Sécurité Maritime et Navigabilité:**\n"
                f"- **Statut d'Autorisation:** **{risk_badge}**\n"
                f"- **Consigne Opérationnelle:** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**Bulletin Météorologique et Halieutique Maritime ({loc_str}):**\n\n"
                f"- **Hauteur Significative des Vagues:** **{wave} m**\n"
                f"- **Vitesse du Vent:** **{wind} km/h**\n"
                f"- **Température de Surface de la Mer (TSM):** **{sst} °C**\n"
                f"- **Zone Potentielle de Pêche & Espèces Cibles:** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 11. PORTUGUESE (Santos, Rio de Janeiro, Lisbon)
        elif lang == "pt":
            bearing_block = f"\n- **Rumo e Distância de Navegação:** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**Matriz de Segurança e Navegabilidade da Embarcação:**\n"
                f"- **Status de Liberação:** **{risk_badge}**\n"
                f"- **Diretiva de Segurança:** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**Boletim Meteorológico e de Pesca Marítima ({loc_str}):**\n\n"
                f"- **Altura das Ondas:** **{wave} m**\n"
                f"- **Velocidade do Vento:** **{wind} km/h**\n"
                f"- **Temperatura da Superfície do Mar (TSM):** **{sst} °C**\n"
                f"- **Espécies Alvo na Zona de Pesca (ZPP):** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 12. DUTCH (Rotterdam, Maasvlakte, Vlaardingen, Antwerp)
        elif lang == "nl":
            bearing_block = f"\n- **Navigatiekoers en Afstand:** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**Zeewaardigheid en Veiligheidsmatrix:**\n"
                f"- **Vertrekstatus:** **{risk_badge}**\n"
                f"- **Veiligheidsadvies:** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**Maritiem Weer- en Visserijbericht ({loc_str}):**\n\n"
                f"- **Significante Golfhoogte:** **{wave} m**\n"
                f"- **Windsnelheid:** **{wind} km/h**\n"
                f"- **Zeewatertemperatuur (SST):** **{sst} °C**\n"
                f"- **Potentiële Viszone en Doelsoorten:** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 13. GERMAN (Hamburg, Bremerhaven, Wilhelmshaven)
        elif lang == "de":
            bearing_block = f"\n- **Navigationskurs und Distanz:** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**Schiffssicherheits- und Seetauglichkeitsmatrix:**\n"
                f"- **Freigabestatus:** **{risk_badge}**\n"
                f"- **Sicherheitshinweis:** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**Maritimer Wetter- und Fischereibericht ({loc_str}):**\n\n"
                f"- **Signifikante Wellenhöhe:** **{wave} m**\n"
                f"- **Windgeschwindigkeit:** **{wind} km/h**\n"
                f"- **Meeresoberflächentemperatur (SST):** **{sst} °C**\n"
                f"- **Potenzielle Fischereizone & Zielarten:** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 14. NORWEGIAN (Bergen, Oslo, Tromsø)
        elif lang == "no":
            bearing_block = f"\n- **Navigasjonskurs og Avstand:** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**Fartøyssikkerhet og Sjødyktighetsmatrise:**\n"
                f"- **Avgangsstatus:** **{risk_badge}**\n"
                f"- **Sikkerhetsråd:** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**Maritimt Vær- og Fiskerivarsel ({loc_str}):**\n\n"
                f"- **Signifikant Bølgehøyde:** **{wave} m**\n"
                f"- **Vindstyrke:** **{wind} km/h**\n"
                f"- **Havoverflatetemperatur (SST):** **{sst} °C**\n"
                f"- **Potensiell Fiskesone og Målarter:** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 15. ARABIC (Dubai Port Rashid, Jebel Ali, Doha, Alexandria)
        elif lang == "ar" or script == "arabic":
            bearing_block = f"\n- **الاتجاه الملاحي والمسافة:** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**مصفوفة سلامة السفينة وصلاحية الإبحار:**\n"
                f"- **حالة التصريح:** **{risk_badge}**\n"
                f"- **التوجيه الأمني:** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**النشرة البحرية للسلامة والطقس ومصائد الأسماك ({loc_str}):**\n\n"
                f"- **ارتفاع الموج الهام:** **{wave} م**\n"
                f"- **سرعة الرياح:** **{wind} كم/س**\n"
                f"- **درجة حرارة سطح البحر (SST):** **{sst} °م**\n"
                f"- **الأسماك المستهدفة في منطقة الصيد الواعدة (PFZ):** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 16. INDONESIAN (Tanjung Priok, Singapore Strait, Surabaya)
        elif lang == "id":
            bearing_block = f"\n- **Arah Navigasi & Jarak:** {bearing_info}" if bearing_info else ""
            vessel_block = (
                f"\n\n**Matriks Kelayakan Laut & Keselamatan Kapal:**\n"
                f"- **Status Izin Berlayar:** **{risk_badge}**\n"
                f"- **Petunjuk Keselamatan:** {risk_summary}"
            ) if include_vessel_matrix else ""
            return (
                f"**Laporan Cuaca Maritim & Daerah Penangkapan Ikan ({loc_str}):**\n\n"
                f"- **Tinggi Gelombang Signifikan:** **{wave} m**\n"
                f"- **Kecepatan Angin:** **{wind} km/j**\n"
                f"- **Suhu Permukaan Laut (SPL):** **{sst} °C**\n"
                f"- **Zona Potensial Penangkapan Ikan (ZPPI):** {species_str}"
                f"{bearing_block}"
                f"{vessel_block}"
            )

        # 17. DEFAULT ENGLISH (With Localized Vernacular Fish Names)
        return ""
