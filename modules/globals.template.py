import os;

DEBUG = False;
MOD_VERSION = "1.20.1";

API_PREFIX = '/ksmp-api/'

__paths__ = {};
__paths__['SELF'] = os.getcwd();
__paths__['MODSFILE'] = os.path.join(__paths__['SELF'], 'mods.json');
__paths__['ASSETS'] = os.path.join(__paths__['SELF'], 'assets');
__paths__['RESSOURCEPACKS'] = os.path.join(__paths__['ASSETS'], 'ressourcepacks');
__paths__['SHADERPACKS'] = os.path.join(__paths__['ASSETS'], 'shaderpacks');
__paths__['CONFIG'] = os.path.join(__paths__['ASSETS'], 'config');
__paths__['APP'] = os.path.join(__paths__['ASSETS'], 'app');

LOCATION = type('LOCATION', (), __paths__)();

# LIST FROM 'https://free-proxy-list.net/'
# MAX_PROXIES_TRY = 5;
# PROXIES = open("./modules/proxies.txt", "r").read().strip().split("\n");

MAX_USER_AGENT_TRY = 2;
USER_AGENT = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
];

MODRINTH_TOKEN_API = "API_KEY";
CURSEFORCE_TOKEN_API = "API_KEY";


RESET_FORMAT = "\033[0m"

STYLE_BOLD       = "\033[1m"
STYLE_DIM        = "\033[2m"
STYLE_UNDERLINED = "\033[4m"
STYLE_BLINK      = "\033[5m"
STYLE_REVERSE    = "\033[7m"
STYLE_HIDDEN     = "\033[8m"

RESET_STYLE_BOLD       = "\033[21m"
RESET_STYLE_DIM        = "\033[22m"
RESET_STYLE_UNDERLINED = "\033[24m"
RESET_STYLE_BLINK      = "\033[25m"
RESET_STYLE_REVERSE    = "\033[27m"
RESET_STYLE_HIDDEN     = "\033[28m"

COLOR_DEFAULT      = "\033[39m"
COLOR_BLACK        = "\033[30m"
COLOR_RED          = "\033[31m"
COLOR_GREEN        = "\033[32m"
COLOR_YELLOW       = "\033[33m"
COLOR_BLUE         = "\033[34m"
COLOR_PURPLE       = "\033[35m"
COLOR_CYAN         = "\033[36m"
COLOR_LIGHTGRAY    = "\033[37m"
COLOR_DARKGRAY     = "\033[90m"
COLOR_LIGHTRED     = "\033[91m"
COLOR_LIGHTGREEN   = "\033[92m"
COLOR_LIGHTYELLOW  = "\033[93m"
COLOR_LIGHTBLUE    = "\033[94m"
COLOR_LIGHTMAGENTA = "\033[95m"
COLOR_LIGHTCYAN    = "\033[96m"
COLOR_WHITE        = "\033[97m"

BACKGROUND_COLOR_DEFAULT      = "\033[49m"
BACKGROUND_COLOR_BLACK        = "\033[40m"
BACKGROUND_COLOR_RED          = "\033[41m"
BACKGROUND_COLOR_GREEN        = "\033[42m"
BACKGROUND_COLOR_YELLOW       = "\033[43m"
BACKGROUND_COLOR_BLUE         = "\033[44m"
BACKGROUND_COLOR_PURPLE       = "\033[45m"
BACKGROUND_COLOR_CYAN         = "\033[46m"
BACKGROUND_COLOR_LIGHTGRAY    = "\033[47m"
BACKGROUND_COLOR_DARKGRAY     = "\033[100m"
BACKGROUND_COLOR_LIGHTRED     = "\033[101m"
BACKGROUND_COLOR_LIGHTGREEN   = "\033[102m"
BACKGROUND_COLOR_LIGHTYELLOW  = "\033[103m"
BACKGROUND_COLOR_LIGHTBLUE    = "\033[104m"
BACKGROUND_COLOR_LIGHTMAGENTA = "\033[105m"
BACKGROUND_COLOR_LIGHTCYAN    = "\033[106m"
BACKGROUND_COLOR_WHITE        = "\033[107m"


FORGE_PACK = [ "ears", "emoji-type", "emotecraft", "simple-voice-chat", ];

OPTIFABRIC_PACK = [ "optifabric", "bundle-jumble", "yacl", "ears", "emoji-type", "emotecraft", "fabric-api", "simple-voice-chat", ];

FABRIC_PACK = [ "bundle-jumble", "yacl", "ears", "emoji-type", "emotecraft", "fabric-api", "simple-voice-chat", ];

SODIUM_PACK = [ "animatica", "ash-api", "bundle-jumble", "yacl", "capes", "cit-resewn", "continuity", "ears", "emoji-type", "emotecraft", "entitytexturefeatures", "entityculling", "fabric-api", "indium", "iris", "lambdynamiclights", "lithium", "logical-zoom", "modmenu", "no_fog", "cloth-config", "sodium", "sodium-extra", "reeses-sodium-options", "starlight", "transparent", "simple-voice-chat", "fabric-language-kotlin", ];


MODPACKS = {
    "forge": FORGE_PACK,
    'optifabric': OPTIFABRIC_PACK,
    'fabric': FABRIC_PACK,
    'sodium': SODIUM_PACK,
}

LOADERS = {
    'forge': 'forge',
    'optifabric': 'fabric',
    'fabric': 'fabric',
    'sodium': 'fabric',
}

LIST_MODS = [
    # {"modname": "optifabric",        "modloader": "fabric", "site": "curseforge"},

    {"modname": "animatica",              "modloader": "fabric", "site": "modrinth"},
    {"modname": "ash-api",                "modloader": "fabric", "site": "modrinth"},
    {"modname": "bundle-jumble",          "modloader": "fabric", "site": "modrinth"},
    {"modname": "yacl",          "modloader": "fabric", "site": "modrinth"},
    {"modname": "capes",                  "modloader": "fabric", "site": "modrinth"},
    {"modname": "cit-resewn",             "modloader": "fabric", "site": "modrinth"},
    {"modname": "continuity",             "modloader": "fabric", "site": "modrinth"},
    {"modname": "ears",                   "modloader": "fabric", "site": "modrinth"},
    {"modname": "emoji-type",             "modloader": "fabric", "site": "modrinth"},
    {"modname": "emotecraft",             "modloader": "fabric", "site": "modrinth"},
    {"modname": "entitytexturefeatures",  "modloader": "fabric", "site": "modrinth"},
    {"modname": "entityculling",          "modloader": "fabric", "site": "modrinth"},
    {"modname": "fabric-api",             "modloader": "fabric", "site": "modrinth"},
    {"modname": "indium",                 "modloader": "fabric", "site": "modrinth"},
    {"modname": "iris",                   "modloader": "fabric", "site": "modrinth"},
    {"modname": "lambdynamiclights",      "modloader": "fabric", "site": "modrinth"},
    {"modname": "lithium",                "modloader": "fabric", "site": "modrinth"},
    {"modname": "logical-zoom",           "modloader": "fabric", "site": "modrinth"},
    {"modname": "modmenu",                "modloader": "fabric", "site": "modrinth"},
    {"modname": "no_fog",                 "modloader": "fabric", "site": "modrinth"},
    {"modname": "cloth-config",           "modloader": "fabric", "site": "modrinth"},
    {"modname": "sodium",                 "modloader": "fabric", "site": "modrinth"},
    {"modname": "sodium-extra",           "modloader": "fabric", "site": "modrinth"},
    {"modname": "reeses-sodium-options",  "modloader": "fabric", "site": "modrinth"},
    {"modname": "starlight",              "modloader": "fabric", "site": "modrinth"},
    {"modname": "transparent",            "modloader": "fabric", "site": "modrinth"},
    {"modname": "simple-voice-chat",      "modloader": "fabric", "site": "modrinth"},
    {"modname": "fabric-language-kotlin", "modloader": "fabric", "site": "modrinth"},

    {"modname": "ears",              "modloader": "forge", "site": "modrinth"},
    {"modname": "emoji-type",        "modloader": "forge", "site": "modrinth"},
    {"modname": "emotecraft",        "modloader": "forge", "site": "modrinth"},
    {"modname": "simple-voice-chat", "modloader": "forge", "site": "modrinth"},
];