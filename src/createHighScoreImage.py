import warnings
from requests.packages.urllib3.exceptions import RequestsDependencyWarning
warnings.filterwarnings("ignore", category=RequestsDependencyWarning)

import requests
import json
import sys
import sqlite3
import logging
from logging.handlers import RotatingFileHandler
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

apiBaseUri = "https://virtualpinballchat.com"
convertUri = apiBaseUri + "/vpc/api/v1/convert"
headers = {
    "Content-Type": "application/json",
}


def log_setup():
    logName = "vpc-get-high-scores-image.log"
    log_handler = RotatingFileHandler(logName, maxBytes=10000000, backupCount=3)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s : %(message)s", "%b %d %H:%M:%S"
    )
    formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)


def createImage(vpsId, numRows, mediaPath, gameName, fileNameSuffix):
    payload = json.dumps({"vpsId": vpsId, "numRows": numRows})
    res = make_session().request("POST", convertUri, headers=headers, data=payload)
    fullPath = mediaPath + "\\" + gameName + fileNameSuffix + ".png"
    with open(fullPath, "wb") as fh:
        fh.write(res.content)


def fetchHighScoreImage(vpsId, fieldNames, numRows, mediaPath):
    logging.info(f"\n\n----- fetchHighScoreImage Start")
    logging.info(f"vpsId: {vpsId}, numRows: {numRows}, mediaPath: {mediaPath}")

    table = getTableFromPopperDB(vpsId, dbPath)
    gameName = table[fieldNames.index("GameName")]

    createImage(vpsId, numRows, mediaPath, gameName, fileNameSuffix)

    logging.info(f"----- fetchHighScoreImage End")


def getTableFromPopperDB(vpsId, dbPath):
    conn = sqlite3.connect(dbPath + "\\" + "PUPDatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM 'Games' WHERE " + vpsIdField + " = '" + vpsId + "'")
    table = cur.fetchone()
    conn.close()
    return table


def strtobool(val):
    return val.lower() in ("yes", "true", "t", "1")


def make_session():
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=Retry(connect=3, backoff_factor=1))
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


log_setup()
logging.info("--- INSTANCE STARTED ---")

updateAll = False
numRows = 5
fieldNames = []

try:
    logging.info(f"args: {sys.argv[1:]}")

    if len(sys.argv) > 1:
        logging.info("Found more than 0 arguments")
        exeName = sys.argv[0]
        updateAll = strtobool(sys.argv[1])
        vpsId = sys.argv[2]
        vpsIdField = sys.argv[3]
        dbPath = sys.argv[4]
        mediaPath = sys.argv[5]
        numRows = int(sys.argv[6])
        fileNameSuffix = sys.argv[7]
        logging.info(
            f"exeName: {exeName}, updateAll: {updateAll}, vpsId: {vpsId}, vpsIdField: {vpsIdField}, dbPath: {dbPath}, mediaPath: {mediaPath}, numRows: {numRows}, fileNameSuffix: ${fileNameSuffix}"
        )
    else:
        logging.info("Found 0 arguments. Using default arguments for debugging")
        updateAll = False
        vpsId = "NTissEZP"
        vpsIdField = "CUSTOM3"
        dbPath = "c:\\temp"
        mediaPath = "c:\\temp"
        numRows = 5
        fileNameSuffix = ""

    ## fetching all tables
    conn = sqlite3.connect(dbPath + "\\" + "PUPDatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM 'Games' WHERE EMUID = 1 ORDER BY GameDisplay")
    fieldNames = [description[0] for description in cur.description]
    rows = cur.fetchall()
    conn.close()

    if updateAll:
        logging.info(f"Starting to update all tables")
        logging.info(f"Found {str(len(rows))} tables")
        for row in rows:
            gameName = row[fieldNames.index("GameName")]
            vpsId = row[fieldNames.index(vpsIdField)]
            if vpsId:
                fetchHighScoreImage(vpsId, fieldNames, numRows, mediaPath)
            else:
                logging.info(f"Skipping {gameName} — no vpsId")
        logging.info(f"Finished updating all tables")
    else:
        logging.info(f"Starting to update 1 table: " + vpsId)
        fetchHighScoreImage(vpsId, fieldNames, numRows, mediaPath)
except Exception as err:
    logging.exception(err)

logging.info("--- INSTANCE STOPPED ---\n\n")
