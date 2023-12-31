from modules.functions import *;
from modules.globals import *;

import requests, json;

API = "https://api.modrinth.com/v2";

MODRINTH_API = "https://api.modrinth.com/v2";

CURSEFORGE_API = 'https://api.curseforge.com/v1';
































def ___getModVersions(mod):
    versions = None;

    if DEBUG:
        print(COLOR_DARKGRAY + STYLE_REVERSE, f'{mod["modname"]}, {mod["modloader"]}, {MOD_VERSION}', RESET_FORMAT);

    if (mod["site"] == "modrinth"):
        versions = getModVersionsFromModrinth(mod["modname"], [mod["modloader"]], [MOD_VERSION]);
    
    if (mod["site"] == "curseforge"):
        print(COLOR_RED + f"'curseforge' scrapper is disabled due to an 403 error." + RESET_FORMAT);
        # versions = getModVersionsFromCurseForge(mod["modname"], MOD_VERSION, 'release', mod["modloader"]);
    
    if (mod["site"] == "local"):
        print(COLOR_LIGHTRED + f"'local' website work in progress." + RESET_FORMAT);
        # versions = getModVersionsFromCurseForge(mod["modname"], MOD_VERSION, 'release', mod["modloader"]);
    

    if DEBUG and versions != None:
        print(COLOR_LIGHTCYAN + STYLE_REVERSE, versions, RESET_FORMAT);
    

    return versions;


def ___getModVersionsFromModrinth(slug, loaders=None, versions=None):
    headers = {
        "Authorization": MODRINTH_TOKEN_API,
        "User-Agent": "KSMP-API (vps.wolphwood.ovh/ksmp-api)"
    };

    url = f'/project/{slug}/version';
    args = [];

    if loaders != None: args.append(f'loaders={loaders}');
    if versions != None: args.append(f'game_versions={versions}');

    if len(args) > 0:
        url += '?'+ '&'.join(args);
    
    url = url.replace("'", "\"");

    result = requests.get(API + url, headers=headers);
    content = result.content.decode('utf-8');
    
    return json.loads( content );



def Update():
    MODS = getJSONFile("mods.json", {"forge":{}, "fabric": {}});
    for mod in LIST_MODS:
        MODS[mod["modloader"]][mod["modname"]] = ___getModVersions(mod);

    with open('./mods.json', 'w') as file:
        file.write( json.dumps( MODS, indent=2 ) );


if __name__ == '__main__':
    Update();