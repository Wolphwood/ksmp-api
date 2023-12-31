from modules.functions import *;
from modules.globals import *;

import requests, json;

MODRINTH_API = "https://api.modrinth.com/v2";

headers = {
    "Authorization": MODRINTH_TOKEN_API,
    "User-Agent": "KSMP-API (vps.wolphwood.ovh/ksmp-api) (wolphwood.ovh)"
};

def getModVersion(version_id):
    url = f'/version/{version_id}';

    result = requests.get(MODRINTH_API + url, headers=headers);
    if not result.status_code == 200:
        return {
            "error": result.status_code,
            "message": result.text
        }
    
    content = result.content.decode('utf-8');
    data = json.loads( content );

    return data;


def getMod(mod_id, force_update = False):
    mods = getJSONFile(LOCATION.MODSFILE, []);

    if force_update:
        # Find index
        index = next((index for (index, mod) in enumerate(mods) if mod['id'] == mod_id or mod['slug'] == mod_id), -1);

        fetchedMod = fetchMod(mod_id);
    
        if index == -1:
            mods.append(fetchedMod);
        else:
            mods[index] = fetchedMod;

        writeJSONFile(LOCATION.MODSFILE, mods);

        return fetchedMod;

    else:
        # Search in mods
        for mod in mods:
            if mod['id'] == mod_id or mod['slug'] == mod_id:
                return mod;
        
        # Fetch if not found
        fetchedMod = fetchMod(mod_id);
        
        if not 'error' in fetchedMod:
            mods.append(fetchedMod);
            writeJSONFile(LOCATION.MODSFILE, mods);
            
            return fetchedMod;

    # Return Error
    return None

def fetchMod(mod_id):
    url = f'/project/{mod_id}';

    print(COLOR_PURPLE, f"fetching '{url}'...", RESET_FORMAT);

    result = requests.get(MODRINTH_API + url, headers=headers);
    if not result.status_code == 200:
        return {
            "error": result.status_code,
            "message": result.text
        }
    
    content = result.content.decode('utf-8');
    data = json.loads( content );

    mod_data = {
        "plateform": "modrinth",
        "id": data['id'],
        "icon": data['icon_url'],
        "loaders": data['loaders'],
        "game_versions": data['game_versions'],
        "versions": fetchModVersions(mod_id),
        "slug": data['slug'],
        "name": data['title'],
        "team": fetchTeamMembers(data['team']),

    }

    return mod_data;


def fetchModVersions(mod_id):
    url = f'/project/{mod_id}/version';

    result = requests.get(MODRINTH_API + url, headers=headers);
    if not result.status_code == 200:
        return {
            "error": result.status_code,
            "message": result.text
        }
    
    content = result.content.decode('utf-8');

    versions = [];
    for data in  json.loads(content):
        versions.append({
            "id": data['id'],
            "name": data['name'],
            "dependencies": [{
                "optional": dependency['dependency_type'] == 'optional',
                "filename": dependency['file_name'],
                "project": dependency['project_id'],
                "version": dependency['version_id'],
            } for dependency in data['dependencies']],
            "game_versions": data['game_versions'],
            "loaders": data['loaders'],
            "type": data['version_type'],
            "version": data['version_number'],
            "files": [{
                "filename": file['filename'],
                "hashes": file['hashes'],
                "url": file['url'],
            } for file in data['files']],
        });
    

    return versions;

def fetchTeamMembers(team_id):
    url = f"/team/{team_id}/members";

    result = requests.get(MODRINTH_API + url, headers=headers);
    if not result.status_code == 200:
        return {
            "error": result.status_code,
            "message": result.text
        }
    
    content = result.content.decode('utf-8');

    team = [];
    for data in  json.loads(content):
        team.append({
            "id": data['user']['id'],
            "username": data['user']['username'],
            "name": data['user']['name'],
            "avatar": data['user']['avatar_url'],
            "role": str.lower(data['role']),
        });

    return team;