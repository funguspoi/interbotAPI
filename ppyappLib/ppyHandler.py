# -*- coding: utf-8 -*-
import logging
import traceback
import re
from ppyappLib import ppyAPI
from baseappLib import baseHandler

class ppyHandler():


    def __init__(self):
        pass
    
    def getRecent(self, uid, mode=0, limit=10):
        kw = {
            'uid': uid,
            'mode': mode,
            'limit': limit
        }
        logging.info(kw)
        return ppyAPI.apiRoute('recent', **kw)
    
    def getOsuUserInfo(self, uid):
        kw = {'uid': uid}
        logging.info(kw)
        return ppyAPI.apiRoute('userinfo', **kw)
    
    def getOsuUserBp(self, uid, mode=0, limit=10):
        kw = {
            'uid': uid,
            'mode': mode,
            'limit': limit
        }
        logging.info(kw)
        return ppyAPI.apiRoute('bp', **kw)
    
    def getOsuBeatMapInfo(self, bid):
        kw = {'bid': bid}
        logging.info(kw)
        return ppyAPI.apiRoute('beatmap', **kw)

    def getSkillInfo(self, osuname):
        """Skill抓取
        """
        try:
            kw = {'osuname': osuname}
            res = ppyAPI.crawlPageByGet('skill', **kw)
            if not res:
                return '网络异常!!'
            s_msg = osuname+"'s skill\n"
            value = re.compile(r'<output class="skillValue">(.*?)</output>')
            values = value.findall(res)
            if not values:
                return '抓取不到相关信息!!'
            skills = ['Stamina', 'Tenacity', 'Agility', 'Accuracy', 'Precision', 'Reaction', 'Memory', 'Reading']
            #skills_list = list(map(lambda x,y:x+y ,skills,values))
            for i,s in enumerate(skills):
                val = int(values[i])
                if  1000 > val >= 100:
                    snum = int(values[i][0:1])
                elif val >= 1000:
                    snum = int(values[i][0:2])
                else:
                    snum = 0
                star = '*' * snum
                skillkey = '%s:' % s
                valueskey = '%s ' % values[i]
                s_msg = s_msg+skillkey+valueskey+star+'\n'
            return s_msg[0:-1]
        except:
            logging.error(traceback.format_exc())
            return '那个破网站连不上!!'

    def skillVsInfo(self, uid, uid2):
        try:
            kw = {'osuname': uid, 'vsosuname': uid2}
            res = ppyAPI.crawlPageByGet('skillvs', **kw)
            if not res:
                return '网络异常!!'
            value = re.compile(r'<output class="skillValue">(.*?)</output>')
            values = value.findall(res)
            if not values:
                return '那个破网站连不上,你们还是去床上解决吧!!'
            skills = ['Stamina', 'Tenacity', 'Agility', 'Accuracy', 'Precision', 'Reaction', 'Memory', 'Reading']
            s_msg = '%s vs %s\n'%(uid, uid2)
            for i,s in enumerate(skills):
                v1 = int(values[i])
                v2 = int(values[i+8])
                vv = str(abs(v1-v2))
                fuhao = ' -- '
                if v1 > v2:
                    s_msg = s_msg + s + ' : ' + values[i]+'(+'+vv+')' + fuhao + values[i+8] +'\n'
                elif v1 < v2:
                    s_msg = s_msg + s + ' : ' + values[i] + fuhao + values[i+8] +'(+'+vv+')'+'\n'
                else:
                    s_msg = s_msg + s + ' : ' + values[i] + fuhao + values[i+8] +'\n'
            return s_msg[0:-1]
        except:
            logging.error(traceback.format_exc())
            return '那个破网站连不上,你们还是去床上解决吧!!'

    def getFriends(self, qq, groupid):
        uinfo = baseHandler.baseHandler().getUserBindInfo({"qq": qq, "groupid": groupid})
        token = uinfo[0]["acesstoken"]
        refreshtoken = uinfo[0]["refreshtoken"]
        osuname = uinfo[0]["osuname"]
        if not token:
            return '请使用oauth进行认证绑定!'
        res = ppyAPI.apiv2Req("friends", token, refreshtoken, qq=qq, groupid=groupid)
        if res == -1:
            return '网络异常!'
        elif res == -2:
            return 'token失效!请使用oauth进行认证绑定!' 
        else:
            friendsNum = len(res)
            rs = "%s's friends(%s)\n" % (osuname, friendsNum)
            for i, r in enumerate(res[:10]):
                rs += '%s.%s\n' % (i+1, r["username"])
        return rs[:-1]
