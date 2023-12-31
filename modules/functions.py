from modules.globals import *

from requests import get;
from urllib.parse import *;
from urllib import *;
import base64, random, os, json, re;
from zipfile import ZipFile;
import json;

import threading, time;

# TOOLBOX
def UniqueList(l):
    return list(dict.fromkeys(l));

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def getKeyValueFromUrl(url, key):
    query = parse_qs(urlparse(url).query)
    return query.get(key);

def get_as_base64(url):
    return base64.b64encode(get(url).content)

def getCharFromURIHex(match):
    match = match.group();
    return chr(int(match[1:], 16));

def getJSONFile(filename, default = {}):
    if os.path.isfile(filename):
        with open(filename, encoding="utf8") as file:
            content = file.read();
        
        if len(content) == 0:
            return default;
        else:
            return json.loads(content);
    else:
        return default;

def writeJSONFile(filename, data):
    with open(filename, "w") as file:
        file.write(json.dumps(data, indent=2));


def setInterval(func, interval):
    def wrapped():
        while True:
            func();
            time.sleep(interval);
    thread = threading.Thread(target=wrapped);
    thread.daemon = True;  # Permet au thread de se terminer lorsque le programme principal se termine
    thread.start();


def setTimeout(func, delay):
    def wrapped():
        time.sleep(delay)
        func()
    thread = threading.Thread(target=wrapped)
    thread.daemon = True
    thread.start()

def getPackMcMeta(path):
    archive = ZipFile(path, 'r')
    content = archive.read('pack.mcmeta')

    return json.loads(content.decode('utf8'));

def getPackVersion(path):
    mcmeta = getPackMcMeta(path)

    if ('version' in mcmeta['pack']):
        return mcmeta['pack']['version']
    else:
        return None

def getPackVersionFromName(packname):
    m = re.search("v(\.*[0-9])*", packname);
    p = re.search("(p|preview)\s*([0-9]+)", packname);
    
    if not p is None:
        p = int( p.group(2) )
    else:
        p = 0

    if p == 0:
        return m.group(0)[1:]
    else:
        return m.group(0)[1:] + '_' + str(p)

def findPackVersion(category, packname):
    version = getPackVersion(os.path.join(LOCATION.RESSOURCEPACKS, category, packname));
    if version is None:
        version = getPackVersionFromName(packname)
    
    return version