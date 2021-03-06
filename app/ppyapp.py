# -*- coding: utf-8 -*-
import os
import yaml
import json
import logging
from flask import Flask
from flask import request
from commLib import appTools
from ppyappLib import ppyHandler

with open('./app/ppyapp.yaml', encoding='utf8') as f:
    config = yaml.load(f)


app = Flask(__name__)

@app.route('/bp', methods=['POST'])
@appTools.deco()
def bpApi(**kw):
    uid = kw.get('osuid')
    mode = kw.get('mode', 0)
    limit = kw.get('limit', 10)
    pyh = ppyHandler.ppyHandler()
    ret = pyh.getOsuUserBp(uid, mode, limit)
    return json.dumps(ret)
    

@app.route('/osuerinfo', methods=['POST'])
@appTools.deco()
def getOsuUserInfo(**kw):
    uid = kw.get('osuid')
    pyh = ppyHandler.ppyHandler()
    ret = pyh.getOsuUserInfo(uid)
    return json.dumps(ret)

@app.route('/recent', methods=['POST'])
@appTools.deco()
def recent(**kw):
    uid = kw.get('osuid')
    mode = kw.get('mode', 0)
    limit = kw.get('limit', 10)
    pyh = ppyHandler.ppyHandler()
    ret = pyh.getRecent(uid, mode, limit)
    return json.dumps(ret)

@app.route('/oppai', methods=['POST'])
@appTools.deco()
def oppai(**kw):
    bid = kw['bid'] if not kw.get('iargs') else kw['iargs'][0]
    extend = kw.get('extend', '')
    # ret = os.popen('curl https://osu.ppy.sh/osu/%s | /root/oppai/./oppai - %s -ojson' % (bid, extend))
    ret = os.popen('curl https://osu.ppy.sh/osu/%s | oppai - %s -ojson' % (bid, extend))
    return json.dumps(ret.read())

@app.route('/osufile', methods=['POST'])
@appTools.deco()
def osufile(**kw):
    bid = kw['bid']
    ret = os.popen('curl https://osu.ppy.sh/osu/%s' % bid)
    return json.dumps(ret)

@app.route('/beatmap', methods=['POST'])
@appTools.deco()
def beatmap(**kw):
    bid = kw.get('bid')
    pyh = ppyHandler.ppyHandler()
    ret = pyh.getOsuBeatMapInfo(bid)
    return json.dumps(ret)

@app.route('/osuskill', methods=['POST'])
@appTools.deco()
def osuskill(**kw):
    osuname = kw.get('osuname')
    pyh = ppyHandler.ppyHandler()
    ret = pyh.getSkillInfo(osuname)
    return ret

@app.route('/osuskillvs', methods=['POST'])
@appTools.deco()
def osuskillvs(**kw):
    osuname = kw.get('osuname')
    vsosuname = kw.get('vsosuname')
    pyh = ppyHandler.ppyHandler()
    ret = pyh.skillVsInfo(osuname, vsosuname)
    return ret

if __name__ == '__main__':
    app.run(threaded=True)
    
