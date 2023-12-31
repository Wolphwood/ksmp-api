from requests import get;
from datetime import date, datetime;
import os, time, re;

from modules.functions import *;
from modules.globals import *;

import updater;

from flask import redirect, request, send_file;
from main import app;


_last_update = 0;
@app.route(API_PREFIX + '/mods/update')
def update_mods():
    global _last_update;

    if (time.time() - _last_update) > (60*60*12):
        updater.Update();
        _last_update = time.time();

    return redirect(request.url_root + "ksmp-api/mods/list");

@app.route(API_PREFIX + '/mods/list')
def get_packs():
    MODS = getJSONFile("mods.json", {"forge":{}, "fabric": {}});

    modlist = {
        "mods": MODS,
        "packs": {
            'optifabric': {},
            'fabric': {},
            'sodium': {},
            'forge': {},
        }
    }

    for modname in OPTIFABRIC_PACK:
        modlist["packs"]["optifabric"][modname] = ( MODS["fabric"][modname][0] if len(MODS["fabric"][modname]) > 0 else None ) if modname in MODS["fabric"] else None;

    for modname in FABRIC_PACK:
        modlist["packs"]["fabric"][modname] = ( MODS["fabric"][modname][0] if len(MODS["fabric"][modname]) > 0 else None ) if modname in MODS["fabric"] else None;
        
    for modname in SODIUM_PACK:
        modlist["packs"]["sodium"][modname] = ( MODS["fabric"][modname][0] if len(MODS["fabric"][modname]) > 0 else None ) if modname in MODS["fabric"] else None;

    for modname in FORGE_PACK:
        modlist["packs"]["forge"][modname] = ( MODS["forge"][modname][0] if len(MODS["forge"][modname]) > 0 else None ) if modname in MODS["forge"] else None;


    return modlist;

@app.route(API_PREFIX + '/mods/<pack>')
def get_fabric_pack(pack):
    MODS = getJSONFile("mods.json", {"forge":{}, "fabric": {}});
    modlist = {};

    PACK = None;
    if pack == 'sodium': PACK = SODIUM_PACK;
    if pack == 'fabric': PACK = FABRIC_PACK;
    if pack == 'optifabric': PACK = OPTIFABRIC_PACK;
    if pack == 'forge': PACK = FORGE_PACK;

    loader = 'fabric';
    if pack == 'forge': loader = 'forge';

    if PACK == None:
        return {
            "error": 404,
            "message": "Invalid Packname."
        };

    for modname in PACK:
        modlist[modname] = MODS[loader][modname] = ( MODS[loader][modname][0] if len(MODS[loader][modname]) > 0 else None ) if modname in MODS[loader] else None;

    return modlist;







def compare_versions(item):
    return list(map(int, item["version"].split('.')));



@app.route(API_PREFIX + '/ressourcepack/list')
def get_ressourcepacks():
    packs = {};

    for category in os.listdir(os.getcwd() + "/assets/ressourcepacks"):
        cat = []
        for packname in os.listdir(os.getcwd() + "/assets/ressourcepacks/"+ category):
            m = re.search("v(\.*[0-9])*", packname);

            cat.append({
                "version": m.group(0)[1:],
                "filename": packname
            });
        
        packs[category] = sorted(cat, key=compare_versions, reverse=True);

    return packs;

@app.route(API_PREFIX + '/ressourcepack/get/<category>/latest')
def get_last_ressourcepack(category):
    packs = [];
    for packname in os.listdir(os.getcwd() + "/assets/ressourcepacks/"+ category):
        m = re.search("v(\.*[0-9])*", packname);

        packs.append({
            "version": m.group(0)[1:],
            "filename": packname
        });
    
    sortedPacks = sorted(packs, key=compare_versions, reverse=True);

    filename = sortedPacks[0]['filename'];
    return send_file(os.getcwd() + f"/assets/ressourcepacks/{category}/{filename}", as_attachment=True);

@app.route(API_PREFIX + '/ressourcepack/get/<category>/<version>')
def get_specific_ressourcepack(category, version):
    for packname in os.listdir(os.getcwd() + "/assets/ressourcepacks/"+ category):
        m = re.search("v(\.*[0-9])*", packname);

        if version == m.group(0)[1:]:
            return send_file(os.getcwd() + f"/assets/ressourcepacks/{category}/{packname}", as_attachment=True);

    return {
        "error": 404,
        "message": "No pack found for this version."
    };

@app.route(API_PREFIX + '/ressourcepack/<category>/list')
def list_specific_ressourcepack(category):
    if not os.path.exists(os.getcwd() + f"/assets/ressourcepacks/{category}"):
        return {
            "error": 404,
            "message": "Unknow category."
        };

    packs = os.listdir(os.getcwd() + f"/assets/ressourcepacks/{category}");

    # return packs
    def _compare_versions(item):
        m = re.search("v(\.*[0-9])*", item);
        return list(map(int, m.group(0)[1:].split('.')));

    return sorted(packs, key=_compare_versions);


@app.route(API_PREFIX + '/others/config/emojitype')
def get_config_emojitype():
    return getJSONFile("./assets/config/emojitype.json", []);


@app.route(API_PREFIX + '/app/list')
def get_app_versions():
    apps = {
        "release": {},
        "beta": {},
        "alpha": {},
    };

    for folder in os.listdir(os.getcwd() + "/assets/app"):
        category = 'release';
        if 'beta' in folder:
            category = 'beta';
        if 'alpha' in folder:
            category = 'alpha';

        apps[category][folder] = os.listdir(os.getcwd() + "/assets/app/"+ folder);

    return apps;

@app.route(API_PREFIX + '/app/version/<version>')
@app.route(API_PREFIX + '/app/version/<version>/<targetFile>')
def get_app_get_version(version, targetFile=None):
    if not os.path.exists(os.getcwd() + f"/assets/app/{version}"):
        return {
            "error": 404,
            "message": f"No version found for {version}."
        }

    files = os.listdir(os.getcwd() + f"/assets/app/{version}");
    if len(files) == 0:
        return {
            "error": 404,
            "message": f"Missing file for '{version}' version."
        }
    else:
        if targetFile == None:
            return files;
        else:
            file = (os.getcwd() + f"/assets/app/{version}/{targetFile}").replace('\\','/');

            if not os.path.exists(file):
                print(COLOR_RED + STYLE_REVERSE, f"MISSING FILE '{targetFile}' FOR v{version}", RESET_FORMAT);
                return {
                    "error": 404,
                    "messsage": f"Missing file '{targetFile}' for version {version}"
                }
            return send_file(file, as_attachment=True);

@app.route(API_PREFIX + '/app/version/list')
def get_app_get_versions():
    folders = os.listdir(os.getcwd() + f"/assets/app");
    
    versions = [];
    for version in sorted(list(dict.fromkeys([v.replace('-beta','').replace('-alpha','') for v in folders]))):
        for prefix in ['','-beta', '-alpha']:
            if version + prefix in folders:
                versions.append(version + prefix);

    return versions;

@app.route(API_PREFIX + '/app/version/last')
@app.route(API_PREFIX + '/app/version/last/<targetFile>')
def get_app_get_last_version(targetFile = None):
    folders = os.listdir(os.getcwd() + f"/assets/app");
    
    versions = [];
    for version in sorted(list(dict.fromkeys([v.replace('-beta','').replace('-alpha','') for v in folders]))):
        for prefix in ['','-beta', '-alpha']:
            if version + prefix in folders:
                versions.append(version + prefix);

    version = versions[-1];

    files = os.listdir(os.getcwd() + f"/assets/app/{version}");
    if len(files) == 0:
        return {
            "error": 404,
            "message": f"Missing file for '{version}' version."
        }
    else:
        if targetFile == None:
            return files;
        else:
            file = (os.getcwd() + f"/assets/app/{version}/{targetFile}").replace('\\','/');

            if not os.path.exists(file):
                print(COLOR_RED + STYLE_REVERSE, f"MISSING FILE '{targetFile}' FOR v{version}", RESET_FORMAT);
                return {
                    "error": 404,
                    "messsage": f"Missing file '{targetFile}' for version {version}"
                }
            return send_file(file, as_attachment=True);





@app.route(API_PREFIX + '/app/<category>/list')
def get_app_category_versions(category):
    filters = {
        "alpha": lambda e: 'alpha' in e,
        "beta": lambda e: 'beta' in e,
        "release": lambda e: not 'alpha' in e and not 'beta' in e,
    }

    return [version.replace(f"-{category}", '') for version in sorted(list(filter(filters[category], os.listdir(os.getcwd() + f"/assets/app/"))))];


@app.route(API_PREFIX + '/app/<category>/last/')
@app.route(API_PREFIX + '/app/<category>/last/<targetFile>')
def get_app_last_version(category, targetFile=None):
    filters = {
        "alpha": lambda e: 'alpha' in e,
        "beta": lambda e: 'beta' in e,
        "release": lambda e: not 'alpha' in e and not 'beta' in e,
    }

    folders = os.listdir(os.getcwd() + f"/assets/app/");
    sortedFolders = sorted(list(filter(filters[category], folders)));
    if len(sortedFolders) == 0:
        return {
            "error": 404,
            "message": f"No version found for {category}."
        }
    folder = sortedFolders[-1];
    
    
    files = os.listdir(os.getcwd() + "/assets/app/"+ folder);
    if len(files) == 0:
        return {
            "error": 404,
            "message": f"Missing file for '{folder}' version."
        }
    else:
        if targetFile == None:
            return files;
        else:
            file = (os.getcwd() + f"/assets/app/{folder}/{targetFile}").replace('\\','/');

            if not os.path.exists(file):
                print(COLOR_RED + STYLE_REVERSE, f"MISSING FILE '{targetFile}' FOR v{folder}", RESET_FORMAT);
                return {
                    "error": 404,
                    "messsage": f"Missing file '{targetFile}' for version {folder}"
                }
            return send_file(file, as_attachment=True);



@app.route(API_PREFIX + '/app/<category>/<version>')
@app.route(API_PREFIX + '/app/<category>/<version>/<targetFile>')
def get_app_version(category, version, targetFile=None):
    filters = {
        "alpha": lambda e: 'alpha' in e,
        "beta": lambda e: 'beta' in e,
        "release": lambda e: not 'alpha' in e and not 'beta' in e,
    }

    

    folders = [v.replace(f"-{category}", '') for v in list(filter(filters[category], os.listdir(os.getcwd() + f"/assets/app/")))];

    if not version in folders:
        return {
            "error": 404,
            "message": "No version found."
        }

    files = os.listdir(os.getcwd() + f"/assets/app/{version}-{category}/");
    if len(files) == 0:
        return {
            "error": 404,
            "message": f"Missing file for '{version}' version."
        }
    else:
        if targetFile == None:
            return files;
        else:
            file = (os.getcwd() + f"/assets/app/{version}-{category}/{targetFile}").replace('\\','/');

            if not os.path.exists(file):
                print(COLOR_RED + STYLE_REVERSE, f"MISSING FILE '{targetFile}' FOR v{version}-{category}", RESET_FORMAT);
                return {
                    "error": 404,
                    "messsage": f"Missing file '{targetFile}' for version {version}-{category}"
                }
            return send_file(file, as_attachment=True);