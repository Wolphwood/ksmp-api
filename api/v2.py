from requests import get;
from datetime import date, datetime;
import os, time, re;
import json

from modules.functions import *;
from modules.globals import *;

import modules.modrinth as modrinth;

import updater;

from flask import redirect, request, send_file;
from main import app;

API_VERSION = "v2";

PolitePeople = [];

def excludeGitFiles(files):
    return [file for file in files if file != '.gitkeep']

@app.route(API_PREFIX + API_VERSION + '/hello')
@app.route(API_PREFIX + API_VERSION + '/hello/')
def v2_hello():
    if not request.remote_addr in PolitePeople:
        PolitePeople.append(request.remote_addr);
    
    print(COLOR_CYAN, f"{request.remote_addr} says hello !", RESET_FORMAT);
    
    return "Hello :)";

@app.route(API_PREFIX + API_VERSION + '/goodbye')
@app.route(API_PREFIX + API_VERSION + '/goodbye/')
def v2_goodbye():
    if request.remote_addr in PolitePeople:
        PolitePeople.remove(request.remote_addr);
    
    print(COLOR_CYAN, f"{request.remote_addr} says goobye !", RESET_FORMAT);
    
    return "Goodbye 👋";



# region ROUTE : MODS
_last_update = 0;
@app.route(API_PREFIX + API_VERSION + '/mods/update')
def v2_update_mods():
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }

    global _last_update;

    if (time.time() - _last_update) > (60*60*12):
        slugs = list(set(item for sublist in MODPACKS.values() for item in sublist));
        
        mods = [];
        for slug in slugs:
            response = modrinth.fetchMod(slug);

            if ('error' in response):
                print(COLOR_RED);
                print(f"Can't fetch '{slug}'.");
                print(response);
                print(RESET_FORMAT);
            else:
                mods.append(response);

        
        writeJSONFile(LOCATION.MODSFILE, mods);

        _last_update = time.time();

    return redirect(request.url_root + "ksmp-api/v2/mods/list");

# vestige v1
@app.route(API_PREFIX + API_VERSION + '/mods/list')
def v2_get_mods():
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return list(set(item for sublist in MODPACKS.values() for item in sublist));

@app.route(API_PREFIX + API_VERSION + '/mods')
@app.route(API_PREFIX + API_VERSION + '/mods/')
def v2_get_packs():
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return list(MODPACKS.keys());

@app.route(API_PREFIX + API_VERSION + '/mods/<packname>')
def v2_get_modpack(packname):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    if not packname in MODPACKS:
        return {
            "error": 404,
            "message": f"Unknown mod pack '{packname}'."
        }
    
    mods = getJSONFile("mods.json", []);
    
    loader = LOADERS[packname];
    
    modpack = [];
    for mod in mods:
        if mod['id'] in MODPACKS[packname] or mod['slug'] in MODPACKS[packname]:
            if loader in mod['loaders']:
                modpack.append(mod);

    return modpack;

@app.route(API_PREFIX + API_VERSION + '/mods/<packname>/list')
def v2_get_modpack_list(packname):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return MODPACKS[packname]
# endregion

# region ROUTE : MOD
@app.route(API_PREFIX + API_VERSION + '/mod/<modname>')
def v2_get_mod(modname):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    force = bool(request.args.get('force', 0, int));

    data = modrinth.getMod(modname, force);


    if data is None:
        return {
            "error": 404
        }

    return data;

@app.route(API_PREFIX + API_VERSION + '/mod/version/<version>')
def v2_get_version(version):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    data = modrinth.getModVersion(version);

    if data is None:
        return {
            "error": 404
        }

    return data;
# endregion

# region ROUTE : LOADER
@app.route(API_PREFIX + API_VERSION + '/loaders')
@app.route(API_PREFIX + API_VERSION + '/loaders/')
def v2_get_loaders():
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return LOADERS;

@app.route(API_PREFIX + API_VERSION + '/loader')
@app.route(API_PREFIX + API_VERSION + '/loader/')
def v2_get_loader():
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return list(LOADERS.fromkeys(LOADERS.values()));

@app.route(API_PREFIX + API_VERSION + '/loader/<modpack>')
def v2_get_loader_modpack(modpack):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return LOADERS[modpack];
# endregion

# region ROUTE : RESSOURCEPACK
def _sort_by_version(item):
    return list(map(int, item["version"].split('.')));

# vestige v1
@app.route(API_PREFIX + API_VERSION + '/ressourcepack/list')
def v2_get_ressourcepacks_full():
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    packs = {};

    for category in excludeGitFiles(os.listdir(LOCATION.RESSOURCEPACKS)):
        categories = []
        for packname in excludeGitFiles(os.listdir(os.path.join(LOCATION.RESSOURCEPACKS, category))):
            version = findPackVersion(category, packname)

            categories.append({
                "version": version,
                "filename": packname
            });
        packs[category] = sorted(categories, key=_sort_by_version, reverse=True);

    return packs;

@app.route(API_PREFIX + API_VERSION + '/ressourcepack')
@app.route(API_PREFIX + API_VERSION + '/ressourcepack/')
def v2_get_ressourcepacks():
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return excludeGitFiles(os.listdir(LOCATION.RESSOURCEPACKS));

@app.route(API_PREFIX + API_VERSION + '/ressourcepack/<category>')
@app.route(API_PREFIX + API_VERSION + '/ressourcepack/<category>/')
def v2_list_specific_ressourcepack(category):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    if not os.path.exists(os.path.join(LOCATION.RESSOURCEPACKS, category)):
        return {
            "error": 404,
            "message": f"Unknown '{category}' pack group."
        };

    packs = [];
    for packname in excludeGitFiles(os.listdir(os.path.join(LOCATION.RESSOURCEPACKS, category))):
            version = findPackVersion(category, packname)

            packs.append({
                "version": version,
                "filename": packname
            });

    return sorted(packs, key=_sort_by_version, reverse=True);
    # return [ item['version'] for item in sorted(packs, key=_sort_by_version, reverse=True) ];

@app.route(API_PREFIX + API_VERSION + '/ressourcepack/<category>/latest')
def v2_get_last_ressourcepack(category):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    if not os.path.exists(os.path.join(LOCATION.RESSOURCEPACKS, category)):
        return {
            "error": 404,
            "message": f"Unknown '{category}' pack group."
        };

    packs = v2_list_specific_ressourcepack(category);
    latest = packs[0];

    return send_file(os.path.join(LOCATION.RESSOURCEPACKS, category, latest['filename']), as_attachment=True);

@app.route(API_PREFIX + API_VERSION + '/ressourcepack/<category>/<version>')
def v2_get_specific_ressourcepack(category, version):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    if not os.path.exists(os.path.join(LOCATION.RESSOURCEPACKS, category)):
        return {
            "error": 404,
            "message": f"Unknown '{category}' pack group."
        };

    packs = v2_list_specific_ressourcepack(category);

    for pack in packs:
        if pack['version'] == version:
            return send_file(os.path.join(LOCATION.RESSOURCEPACKS, category, pack['filename']), as_attachment=True);

    return {
        "error": 404,
        "message": f"Unknown version 'v{version}' in category '{category}'"
    };
# endregion

# region ROUTE : shaderpack
def _sort_shader_version(item):
        return list(map(int, item.split('.')));

@app.route(API_PREFIX + API_VERSION + '/shaderpack')
@app.route(API_PREFIX + API_VERSION + '/shaderpack/')
def v2_shaderpacks():
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return excludeGitFiles(os.listdir(LOCATION.SHADERPACKS));

@app.route(API_PREFIX + API_VERSION + '/shaderpack/<shader>')
@app.route(API_PREFIX + API_VERSION + '/shaderpack/<shader>/')
def v2_shaderpack_shader(shader):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }

    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader)):
        return {
            "error": 404,
            "message": f"Unknown '{shader}' shader group."
        };
    
    return list(sorted(excludeGitFiles(os.listdir(os.path.join(LOCATION.SHADERPACKS, shader))), key=_sort_shader_version, reverse=True));

@app.route(API_PREFIX + API_VERSION + '/shaderpack/<shader>/latest')
@app.route(API_PREFIX + API_VERSION + '/shaderpack/<shader>/latest/')
def v2_shaderpack_shader_latest(shader):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader)):
        return {
            "error": 404,
            "message": f"Unknown '{shader}' shader group."
        };

    versions = v2_shaderpack_shader(shader);
    
    return send_file(os.path.join(LOCATION.SHADERPACKS, shader, versions[0], 'shader.zip'), as_attachment=True, download_name=f"{shader}_v{versions[0]}.zip");

@app.route(API_PREFIX + API_VERSION + '/shaderpack/<shader>/<version>')
@app.route(API_PREFIX + API_VERSION + '/shaderpack/<shader>/<version>/')
def v2_shaderpack_shader_version(shader, version):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader)):
        return {
            "error": 404,
            "message": f"Unknown '{shader}' shader group."
        };

    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader, version)):
        return {
            "error": 404,
            "message": f"File not found '{shader} v{version}'."
        };
    
    return send_file(os.path.join(LOCATION.SHADERPACKS, shader, version, 'shader.zip'), as_attachment=True, download_name=f"{shader}_v{version}.zip");



# endregion

# region ROUTE : config
@app.route(API_PREFIX + API_VERSION + '/config/emojitype')
def v2_get_config_emojitype():
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return getJSONFile(os.path.join(LOCATION.CONFIG, 'emojitype.json'), []);

# region ROUTE : config > shaderpack
@app.route(API_PREFIX + API_VERSION + '/config/shaderpack')
@app.route(API_PREFIX + API_VERSION + '/config/shaderpack/')
def v2_get_config_shaderpacks():
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return v2_shaderpacks();


@app.route(API_PREFIX + API_VERSION + '/config/shaderpack/<shader>')
@app.route(API_PREFIX + API_VERSION + '/config/shaderpack/<shader>/')
def v2_get_config_shaderpack(shader):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return v2_shaderpack_shader(shader);

@app.route(API_PREFIX + API_VERSION + '/config/shaderpack/<shader>/latest')
@app.route(API_PREFIX + API_VERSION + '/config/shaderpack/<shader>/latest/')
def v2_get_config_shaderpack_latest(shader):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader)):
        return {
            "error": 404,
            "message": f"Unknown '{shader}' shader group."
        };

    versions = v2_shaderpack_shader(shader);
    
    configs = list(filter(lambda file: os.path.splitext(file)[1] == ".txt", excludeGitFiles(os.listdir(os.path.join(LOCATION.SHADERPACKS, shader, versions[0])))));
    return list(map(lambda file: os.path.splitext(file)[0], configs));

@app.route(API_PREFIX + API_VERSION + '/config/shaderpack/<shader>/latest/<config>')
def v2_get_config_shaderpack_latest_config(shader, config):
    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader)):
        return {
            "error": 404,
            "message": f"Unknown '{shader}' shader group."
        };

    versions = v2_shaderpack_shader(shader);

    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader, versions[0], f"{config}.txt")):
        return {
            "error": 404,
            "message": f"File not found '{shader}/{versions[0]}/{config}.txt'."
        };
    
    return send_file(os.path.join(LOCATION.SHADERPACKS, shader, versions[0], f"{config}.txt"), as_attachment=True, download_name=f"{shader}_v{versions[0]}.zip.txt");

@app.route(API_PREFIX + API_VERSION + '/config/shaderpack/<shader>/<version>')
@app.route(API_PREFIX + API_VERSION + '/config/shaderpack/<shader>/<version>/')
def v2_get_config_shaderpack_version(shader, version):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader)):
        return {
            "error": 404,
            "message": f"Unknown '{shader}' shader group."
        };

    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader, version)):
        return {
            "error": 404,
            "message": f"File not found '{shader} v{version}'."
        };
    
    configs = list(filter(lambda file: os.path.splitext(file)[1] == ".txt", excludeGitFiles(os.listdir(os.path.join(LOCATION.SHADERPACKS, shader, version)))));
    return list(map(lambda file: os.path.splitext(file)[0], configs));

@app.route(API_PREFIX + API_VERSION + '/config/shaderpack/<shader>/<version>/<config>')
def v2_get_config_shaderpack_version_config(shader, version, config):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader)):
        return {
            "error": 404,
            "message": f"Unknown '{shader}' shader group."
        };

    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader, version)):
        return {
            "error": 404,
            "message": f"File not found '{shader} v{version}'."
        };

    if not os.path.exists(os.path.join(LOCATION.SHADERPACKS, shader, version, f"{config}.txt")):
        return {
            "error": 404,
            "message": f"File not found '{shader}/{version}/{config}.txt'."
        };
    
    return send_file(os.path.join(LOCATION.SHADERPACKS, shader, version, f"{config}.txt"), as_attachment=True, download_name=f"{shader}_v{version}.zip.txt");
# endregion
# endregion


# region ROUTE : app
def _sort_app_version(item):
        return list(map(int, item.split('.')));

def _find_app_file(type, version, filename):
    versions = v2_get_app_versions(type);
    vindex = next((index for (index, v) in enumerate(versions) if v == version), None);

    for version in versions[vindex:]:
        file = os.path.join(LOCATION.APP, type, version, filename);
        files = [file for file in excludeGitFiles(os.listdir(os.path.join(LOCATION.APP, type, version)))];

        if os.path.exists(file):
            print(COLOR_GREEN, f"Find {filename} in v{version}");
            print(COLOR_GREEN, STYLE_REVERSE, f"File location : '{file}'", RESET_FORMAT);
            return file;
        
        elif filename in [file.replace(' ', '-') for file in files]:
            filename = next((file for file in files if file.replace(' ', '-') == filename), None);
            file = os.path.join(LOCATION.APP, type, version, filename);
            
            print(COLOR_GREEN, f"Find {filename} in v{version}" ,RESET_FORMAT);
            print(COLOR_GREEN, STYLE_REVERSE, f"File location : '{file}'", RESET_FORMAT);
            return file;

    return None;

@app.route(API_PREFIX + API_VERSION + '/app')
@app.route(API_PREFIX + API_VERSION + '/app/')
def v2_get_app_type():
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    return excludeGitFiles(os.listdir(LOCATION.APP));

@app.route(API_PREFIX + API_VERSION + '/app/<type>')
@app.route(API_PREFIX + API_VERSION + '/app/<type>/')
def v2_get_app_versions(type):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    folder = os.path.join(LOCATION.APP, type)

    if not os.path.exists(folder):
        return {
            "error": 404,
            "message": f"No app {type} found."
        }
    
    
    return list(sorted(excludeGitFiles(os.listdir(folder)), key=_sort_app_version, reverse=True));

@app.route(API_PREFIX + API_VERSION + '/app/<type>/latest')
@app.route(API_PREFIX + API_VERSION + '/app/<type>/latest/')
def v2_get_app_latest_files(type):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    versions = v2_get_app_versions(type);

    if not os.path.exists(os.path.join(LOCATION.APP, type)):
        return {
            "error": 404,
            "message": f"No '{type}' app found."
        }

    return excludeGitFiles(os.listdir(os.path.join(LOCATION.APP, type, versions[0])))

@app.route(API_PREFIX + API_VERSION + '/app/<type>/latest/<filename>')
def v2_get_app_latest_file(type, filename):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    versions = v2_get_app_versions(type);

    if not os.path.exists(os.path.join(LOCATION.APP, type)):
        return {
            "error": 404,
            "message": f"No '{type}' app found."
        }

    foundFile = _find_app_file(type, versions[0], filename);

    if foundFile:
        return send_file(foundFile, as_attachment=True);
    
    else:
        return {
            "error": 404,
            "message": f"Unknown file '{filename}' in {type} app v{versions[0]}."
        }


@app.route(API_PREFIX + API_VERSION + '/app/<type>/<version>')
@app.route(API_PREFIX + API_VERSION + '/app/<type>/<version>/')
def v2_get_app_version_files(type, version):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    if not os.path.exists(os.path.join(LOCATION.APP, type)):
        return {
            "error": 404,
            "message": f"No '{type}' app found."
        }
    
    if not os.path.exists(os.path.join(LOCATION.APP, type, version)):
        return {
            "error": 404,
            "message": f"No '{type}' app v{version} found."
        }
    
    return excludeGitFiles(os.listdir(os.path.join(LOCATION.APP, type, version)));

@app.route(API_PREFIX + API_VERSION + '/app/<type>/<version>/<filename>')
def v2_get_app_version_file(type, version, filename):
    if not request.remote_addr in PolitePeople:
        return {
            "error": "RUDE",
            "message": "you didn't say hello and it make me sad :("
        }
    
    
    if not os.path.exists(os.path.join(LOCATION.APP, type)):
        return {
            "error": 404,
            "message": f"No '{type}' app found."
        }
    
    if not os.path.exists(os.path.join(LOCATION.APP, type, version)):
        return {
            "error": 404,
            "message": f"No '{type}' app v{version} found."
        }
    
    foundFile = _find_app_file(type, version, filename);

    if foundFile:
        return send_file(foundFile, as_attachment=True);
    
    else:
        return {
            "error": 404,
            "message": f"Unknown file '{filename}' in {type} app v{version}."
        }
# endregion