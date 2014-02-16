from flask import Flask, request
from crossdomain import crossdomain
import db
import config
import json
import logging
from daemonizer import Daemon
import time

conf = config.getConfig()
database = False
app = Flask(__name__)
secret=conf["karmaServer"]["secret"]

karmaWaiting = {}
karmaGivers = {}
karmaTickets = {}

sysMsg = "you got the sysMsg, prepare to be delta'd"

@app.route('/')
@crossdomain(origin='*')
def hello_world():
    logging.debug("someone called hello world")
    return 'Hello World!'

@app.route('/requestKarma/<uuid>/<name>/<platform>/<version>/<stoken>')
@crossdomain(origin='*')
def requestKarma(uuid, platform, version, name, stoken):
    """request karma from the server"""
    if stoken == secret:
        logging.debug("attempting to request karma for {0}".format(name))
        database.userRequest(uuid, name, platform, version)
        karmaWaiting[uuid]=name
        karmaTickets[uuid]=name
        logging.info("Karma requested for {0}".format(name))
        return json.dumps({'success': True})
    else:
        logging.warn("User {0} tried to get karma".format(name))
        return json.dumps({'success': False})

@app.route('/fillKarma/<filluuid>/<uuid>/<name>/<platform>/<version>/<stoken>')
@crossdomain(origin='*')
def fillKarma(filluuid, uuid, name, platform, version, stoken):
    """complete a karma request row in the database and remove the karma from the active queue"""
    if stoken == secret:
        logging.debug("{0} is trying to fill {1}'s door karma".format(uuid, filluuid))
        if uuid in karmaTickets:
            del karmaTickets[uuid]
        else:
            return json.dumps({'success': False})
        database.userFilled(filluuid, uuid, name, platform, version)
        return json.dumps({'success': True})
    else:
        logging.warn("User {0} tried to get karma".format(name))
        return json.dumps({'success': False})

@app.route('/readyKarma/<uuid>/<name>/<stoken>')
@crossdomain(origin='*')
def readyKarma(uuid, name, stoken):
    if stoken == secret:
        karmaGivers[uuid]=name
        logging.info("{0} is ready to give karma".format(name))
        return json.dumps({'success': True})
    else:
        logging.warn("User {0} tried to get karma".format(name))
        return json.dumps({'success': False})

@app.route('/unreadyKarma/<uuid>/<name>/<stoken>')
@crossdomain(origin='*')
def unreadyKarma(uuid, name, stoken):
    if stoken == secret:
        del karmaGivers[uuid]
        logging.info("{0} is no longer ready to give karma".format(name))
        return json.dumps({'success': True})
    else:
        logging.warn("User {0} tried to get karma".format(name))
        return json.dumps({'success': False})

@app.route('/userListKarma/<stoken>')
@crossdomain(origin='*')
def karmaTicketList(stoken):
    """the people who provide karma need to know who wants it"""
    if stoken == secret:
        return json.dumps({'success': True, 'tickets': karmaTickets, 'ready': karmaGivers})
    else:
        logging.warn("User tried to get karma")
        return json.dumps({'success': False})

@app.route('/waitingPollKarma/<uuid>/<stoken>')
@crossdomain(origin='*')
def pollWaitingKarma(uuid, stoken):
    """these are the people who want karma, they need to know who is coming"""
    if stoken == secret:
        return json.dumps({'success': True, 'onTheWay': karmaWaiting[uuid] and not (uuid in karmaTickets)})
    else:
        logging.warn("User {0} tried to get karma".format(uuid))
        return json.dumps({'success': False})

@app.route('/readyPollKarma/<stoken>')
@crossdomain(origin='*')
def readyPoll(stoken):
    """these are the people that are ready to give karma, they get the list of people who want it"""
    if stoken == secret:
        logging.info("Karma giver wanted an update on possible recipients")
        return json.dumps({'success': True, 'tickets': karmaTickets})
    else:
        logging.warn("A user tried to get an update on who wanted karma")
        return json.dumps({'success': False})
        
@app.route('/messagePollKarma/<stoken>')
@crossdomain(origin='*')
def systemMessage(stoken):
    """this function is for sending system messages"""
    logging.info("The system message was sent")
    return json.dumps({'lastUpdate': time.time(), 'message': sysMsg})

@app.route('/killKarma/<uuid>/<name>/<stoken>')
@crossdomain(origin='*')
def killKarma(uuid, name, stoken):
    """pull the record out of the RAM table"""
    if stoken==secret:
        logging.info("Removing {0} from the karma request list".format(name))
        del karmaWaiting[uuid]
        if uuid in karmaTickets:
            del karmaTickets[uuid]
        return json.dumps({'success': True})
    else:
        logging.warn("User {0} tried to get karma".format(name))
        return json.dumps({'success': False})

class DoorKarmaDaemon(Daemon):
    def run(self):
        global database
        database = db.DoorKarmaDatabase(conf["db"]["host"], conf["db"]["user"], conf["db"]["pass"], conf["db"]["db"], conf["db"]["table"])
        app.run(host=conf["karmaServer"]["bindaddr"])
        
if __name__ == '__main__':
    app.run(host='0.0.0.0')
