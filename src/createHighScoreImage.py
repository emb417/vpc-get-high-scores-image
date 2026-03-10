import warnings

# Suppress RequestsDependencyWarning without importing requests first
warnings.filterwarnings("ignore", message=".*character detection dependency.*")

try:
    import charset_normalizer
except ImportError:
    pass

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
highScoresUri = apiBaseUri + "/vpc/api/v1/generateHighScoresLeaderboard"
weeklyUri = apiBaseUri + "/vpc/api/v1/generateWeeklyLeaderboard"

headers = {
    "Content-Type": "application/json",
}


def log_setup():
    logName = "vpc-get-high-scores-image.log"
    log_handler = RotatingFileHandler(logName, maxBytes=10000000, backupCount=3)
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s : %(message)s", "%b %d %H:%M:%S"
    )
    formatter.converter = time.gmtime
    log_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)


def createHighScoresLeaderboard(
    vpsId, numRows, mediaPath, gameName, fileNameSuffix, layout="landscape"
):
    payload = json.dumps({"vpsId": vpsId, "numRows": numRows, "layout": layout})
    res = make_session().request("POST", highScoresUri, headers=headers, data=payload)
    fullPath = mediaPath + "\\" + gameName + fileNameSuffix + ".png"
    with open(fullPath, "wb") as fh:
        fh.write(res.content)
    logging.info(f"High scores leaderboard image saved to {fullPath}")


def createWeeklyLeaderboard(
    mediaPath, fileName="pl_TOTW", fileNameSuffix="", numRows=20, layout="landscape"
):
    payload = json.dumps({"layout": layout, "numRows": numRows})
    res = make_session().request("POST", weeklyUri, headers=headers, data=payload)
    fullPath = mediaPath + "\\" + fileName + fileNameSuffix + ".png"
    with open(fullPath, "wb") as fh:
        fh.write(res.content)
    logging.info(f"Weekly leaderboard image saved to {fullPath}")


def fetchHighScoreLeaderboard(
    vpsId, fieldNames, numRows, mediaPath, layout="landscape"
):
    logging.info(f"\n--------------- fetchHighScoreLeaderboard Start")
    logging.info(
        f"vpsId: {vpsId}, numRows: {numRows}, mediaPath: {mediaPath}, layout: {layout}"
    )

    table = getTableFromPopperDB(vpsId, dbPath)
    gameName = table[fieldNames.index("GameName")]

    createHighScoresLeaderboard(
        vpsId, numRows, mediaPath, gameName, fileNameSuffix, layout
    )

    logging.info(f"\n--------------- fetchHighScoreLeaderboard End")


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

    if len(sys.argv) > 1 and sys.argv[1].lower() == "weekly":
        weeklyMediaPath = sys.argv[2] if len(sys.argv) > 2 else "c:\\temp"
        weeklyFileName = sys.argv[3] if len(sys.argv) > 3 else "pl_TOTW"
        weeklyFileNameSuffix = sys.argv[4] if len(sys.argv) > 4 else ""
        weeklyNumRows = int(sys.argv[5]) if len(sys.argv) > 5 else 20
        weeklyLayout = sys.argv[6] if len(sys.argv) > 6 else "landscape"
        logging.info(f"Starting weekly leaderboard fetch")
        createWeeklyLeaderboard(
            weeklyMediaPath,
            weeklyFileName,
            weeklyFileNameSuffix,
            weeklyNumRows,
            weeklyLayout,
        )
    elif len(sys.argv) > 1:
        exeName = sys.argv[0]
        updateAll = strtobool(sys.argv[1])
        vpsId = sys.argv[2]
        vpsIdField = sys.argv[3]
        dbPath = sys.argv[4]
        mediaPath = sys.argv[5]
        numRows = int(sys.argv[6])
        fileNameSuffix = sys.argv[7]
        layout = sys.argv[8] if len(sys.argv) > 8 else "landscape"
        logging.info(
            f"exeName: {exeName}, updateAll: {updateAll}, vpsId: {vpsId}, vpsIdField: {vpsIdField}, dbPath: {dbPath}, mediaPath: {mediaPath}, numRows: {numRows}, fileNameSuffix: {fileNameSuffix}, layout: {layout}"
        )

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
                    fetchHighScoreLeaderboard(
                        vpsId, fieldNames, numRows, mediaPath, layout
                    )
                else:
                    logging.info(f"Skipping {gameName} — no vpsId")
            logging.info(f"Finished updating all tables")
        else:
            logging.info(f"Starting to update 1 table: " + vpsId)
            fetchHighScoreLeaderboard(vpsId, fieldNames, numRows, mediaPath, layout)
    else:
        logging.info("Found 0 arguments. Using default arguments for debugging")
        updateAll = False
        vpsId = "NTissEZP"
        vpsIdField = "CUSTOM3"
        dbPath = "c:\\temp"
        mediaPath = "c:\\temp"
        numRows = 5
        fileNameSuffix = ""
        layout = "landscape"

except Exception as err:
    logging.exception(err)

logging.info("--- INSTANCE STOPPED ---\n\n")
