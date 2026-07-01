import json, zipfile, os, struct, math
from io import BytesIO

def make_beep_wav(freq=440, duration=0.3):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    buf = BytesIO()
    buf.write(b'RIFF')
    buf.write(struct.pack('<I', 36 + num_samples * 2))
    buf.write(b'WAVE')
    buf.write(b'fmt ')
    buf.write(struct.pack('<I', 16))
    buf.write(struct.pack('<H', 1))
    buf.write(struct.pack('<H', 1))
    buf.write(struct.pack('<I', sample_rate))
    buf.write(struct.pack('<I', sample_rate * 2))
    buf.write(struct.pack('<H', 2))
    buf.write(struct.pack('<H', 16))
    buf.write(b'data')
    buf.write(struct.pack('<I', num_samples * 2))
    samples = b''
    for i in range(num_samples):
        t = i / sample_rate
        fade = min(1.0, min(t * 20, (duration - t) * 20))
        val = int(16000 * fade * math.sin(2 * math.pi * freq * t))
        samples += struct.pack('<h', val)
    return buf.getvalue() + samples

hero_svg = '''<svg width="34" height="34" viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="17" cy="22" rx="9" ry="10" fill="#4A90D9" stroke="#2C5F8A" stroke-width="1.5"/>
  <circle cx="17" cy="10" r="8" fill="#FDDBB4" stroke="#C8956C" stroke-width="1.5"/>
  <circle cx="14" cy="9" r="1.8" fill="#333"/>
  <circle cx="20" cy="9" r="1.8" fill="#333"/>
  <path d="M13 14 Q17 17 21 14" stroke="#C8956C" stroke-width="1.5" fill="none" stroke-linecap="round"/>
  <ellipse cx="7"  cy="21" rx="3.5" ry="2.5" fill="#4A90D9" stroke="#2C5F8A" stroke-width="1"/>
  <ellipse cx="27" cy="21" rx="3.5" ry="2.5" fill="#4A90D9" stroke="#2C5F8A" stroke-width="1"/>
  <ellipse cx="13" cy="31" rx="3.5" ry="2.5" fill="#2C5F8A"/>
  <ellipse cx="21" cy="31" rx="3.5" ry="2.5" fill="#2C5F8A"/>
</svg>'''

hero_svg2 = '''<svg width="34" height="34" viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="17" cy="22" rx="9" ry="10" fill="#4A90D9" stroke="#2C5F8A" stroke-width="1.5"/>
  <circle cx="17" cy="10" r="8" fill="#FDDBB4" stroke="#C8956C" stroke-width="1.5"/>
  <circle cx="14" cy="9" r="1.8" fill="#333"/>
  <circle cx="20" cy="9" r="1.8" fill="#333"/>
  <path d="M13 14 Q17 17 21 14" stroke="#C8956C" stroke-width="1.5" fill="none" stroke-linecap="round"/>
  <ellipse cx="7"  cy="23" rx="3.5" ry="2.5" fill="#4A90D9" stroke="#2C5F8A" stroke-width="1"/>
  <ellipse cx="27" cy="19" rx="3.5" ry="2.5" fill="#4A90D9" stroke="#2C5F8A" stroke-width="1"/>
  <ellipse cx="10" cy="31" rx="3.5" ry="2.5" fill="#2C5F8A"/>
  <ellipse cx="24" cy="31" rx="3.5" ry="2.5" fill="#2C5F8A"/>
</svg>'''

monster_svg = '''<svg width="34" height="34" viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg">
  <circle cx="17" cy="19" r="14" fill="#E74C3C" stroke="#922B21" stroke-width="2"/>
  <circle cx="11" cy="15" r="3.5" fill="white"/>
  <circle cx="12" cy="15" r="1.8" fill="#333"/>
  <circle cx="23" cy="15" r="3.5" fill="white"/>
  <circle cx="24" cy="15" r="1.8" fill="#333"/>
  <line x1="7" y1="9" x2="15" y2="12" stroke="#922B21" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="19" y1="12" x2="27" y2="9"  stroke="#922B21" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M9 25 Q17 31 25 25" stroke="#922B21" stroke-width="1.5" fill="#922B21"/>
  <line x1="13" y1="25" x2="13" y2="29" stroke="white" stroke-width="2"/>
  <line x1="17" y1="25" x2="17" y2="30" stroke="white" stroke-width="2"/>
  <line x1="21" y1="25" x2="21" y2="29" stroke="white" stroke-width="2"/>
  <polygon points="9,7 6,0 13,4" fill="#E74C3C" stroke="#922B21" stroke-width="1"/>
  <polygon points="25,7 28,0 21,4" fill="#E74C3C" stroke="#922B21" stroke-width="1"/>
</svg>'''

star_svg = '''<svg width="36" height="36" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
  <circle cx="18" cy="18" r="17" fill="#FFF9C4" opacity="0.4"/>
  <polygon points="18,2 22.4,13.2 34.6,14 25.2,22.2 28.2,34.2 18,27.4 7.8,34.2 10.8,22.2 1.4,14 13.6,13.2"
           fill="#F1C40F" stroke="#E67E22" stroke-width="1.5" stroke-linejoin="round"/>
</svg>'''

wall_svg = '''<svg width="480" height="360" viewBox="0 0 480 360" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="480" height="12" fill="#0F3460"/>
  <rect x="0" y="348" width="480" height="12"  fill="#0F3460"/>
  <rect x="0" y="0" width="12" height="360" fill="#0F3460"/>
  <rect x="468" y="0" width="12" height="360" fill="#0F3460"/>
  <rect x="60" y="60" width="130" height="18" fill="#0F3460"/>
  <rect x="60" y="60" width="18" height="110" fill="#0F3460"/>
  <rect x="12" y="150" width="120" height="18" fill="#0F3460"/>
  <rect x="220" y="90" width="18" height="120" fill="#0F3460"/>
  <rect x="130" y="200" width="160" height="18" fill="#0F3460"/>
  <rect x="80" y="270" width="180" height="18" fill="#0F3460"/>
  <rect x="310" y="60" width="18" height="120" fill="#0F3460"/>
  <rect x="310" y="60" width="158" height="18" fill="#0F3460"/>
  <rect x="370" y="200" width="18" height="100" fill="#0F3460"/>
  <rect x="280" y="300" width="188" height="18" fill="#0F3460"/>
</svg>'''

backdrop_svg = '''<svg width="480" height="360" viewBox="0 0 480 360" xmlns="http://www.w3.org/2000/svg">
  <rect width="480" height="360" fill="#1A1A2E"/>
  <line x1="0" y1="180" x2="480" y2="180" stroke="#16213E" stroke-width="1" opacity="0.5"/>
  <line x1="240" y1="0" x2="240" y2="360" stroke="#16213E" stroke-width="1" opacity="0.5"/>
  <text x="22"  y="44" font-family="Arial" font-size="13" fill="#4ECCA3" font-weight="bold">START</text>
  <text x="380" y="342" font-family="Arial" font-size="13" fill="#FFD700" font-weight="bold">FINISH</text>
  <text x="240" y="30" font-family="Arial" font-size="17" fill="#E94560" font-weight="bold" text-anchor="middle">MAZE ADVENTURE</text>
</svg>'''

BACKDROP_ID = "cd21514d0531fdffb22204e0ec5ed84a"
WALL_ID = "aa11bb22cc33dd44ee55ff66aa11bb22"
HERO1_ID = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"
HERO2_ID = "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5"
MONSTER_ID = "c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6"
STAR_ID = "d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1"
OOPS_ID = "e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
WIN_ID = "f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3"

WALL_COLOR = "#0F3460"
VAR_SCORE = "score_var_id_001"
VAR_TIMER = "timer_var_id_001"

project = {
  "targets": [
    {
      "isStage": True, "name": "Stage",
      "variables": {
        VAR_SCORE: ["Skor", 0],
        VAR_TIMER: ["Timer", 0],
      },
      "lists": {}, "broadcasts": {}, "comments": {},
      "blocks": {
        "stflag": {"opcode":"event_whenflagclicked","next":"streset","parent":None,"inputs":{},"fields":{},"shadow":False,"topLevel":True,"x":20,"y":20},
        "streset": {"opcode":"data_setvariableto","next":"stscore0","parent":"stflag","inputs":{"VALUE":[1,[4,"0"]]},"fields":{"VARIABLE":["Timer",VAR_TIMER]},"shadow":False,"topLevel":False},
        "stscore0": {"opcode":"data_setvariableto","next":"stforever","parent":"streset","inputs":{"VALUE":[1,[4,"0"]]},"fields":{"VARIABLE":["Skor",VAR_SCORE]},"shadow":False,"topLevel":False},
        "stforever":{"opcode":"control_forever","next":None,"parent":"stscore0","inputs":{"SUBSTACK":[2,"stwait"]},"fields":{},"shadow":False,"topLevel":False},
        "stwait": {"opcode":"control_wait","next":"sttime","parent":"stforever","inputs":{"DURATION":[1,[5,"1"]]},"fields":{},"shadow":False,"topLevel":False},
        "sttime": {"opcode":"data_changevariableby","next":"stscore","parent":"stwait","inputs":{"VALUE":[1,[4,"1"]]},"fields":{"VARIABLE":["Timer",VAR_TIMER]},"shadow":False,"topLevel":False},
        "stscore": {"opcode":"data_changevariableby","next":None,"parent":"sttime","inputs":{"VALUE":[1,[4,"10"]]},"fields":{"VARIABLE":["Skor",VAR_SCORE]},"shadow":False,"topLevel":False},
      },
      "currentCostume": 0,
      "costumes": [{"name":"backdrop1","assetId":BACKDROP_ID,"md5ext":BACKDROP_ID+".svg","dataFormat":"svg","rotationCenterX":240,"rotationCenterY":180}],
      "sounds": [], "volume": 100, "layerOrder": 0,
      "tempo": 60, "videoTransparency": 50, "videoState": "on", "textToSpeechLanguage": None
    },

    {
      "isStage": False, "name": "Tembok",
      "variables": {}, "lists": {}, "broadcasts": {}, "comments": {},
      "blocks": {
        "wf1": {"opcode":"event_whenflagclicked","next":"wg1","parent":None,"inputs":{},"fields":{},"shadow":False,"topLevel":True,"x":20,"y":20},
        "wg1": {"opcode":"motion_gotoxy","next":None,"parent":"wf1","inputs":{"X":[1,[4,"0"]],"Y":[1,[4,"0"]]},"fields":{},"shadow":False,"topLevel":False},
      },
      "currentCostume": 0,
      "costumes": [{"name":"wall","assetId":WALL_ID,"md5ext":WALL_ID+".svg","dataFormat":"svg","rotationCenterX":240,"rotationCenterY":180}],
      "sounds": [], "volume": 100, "layerOrder": 1, "visible": True,
      "x": 0, "y": 0, "size": 100, "direction": 90,
      "draggable": False, "rotationStyle": "don't rotate"
    },

    {
      "isStage": False, "name": "Hero",
      "variables": {}, "lists": {}, "broadcasts": {}, "comments": {},
      "blocks": {
        "flag1": {"opcode":"event_whenflagclicked","next":"go1","parent":None,"inputs":{},"fields":{},"shadow":False,"topLevel":True,"x":20,"y":20},
        "go1": {"opcode":"motion_gotoxy","next":"sz1","parent":"flag1","inputs":{"X":[1,[4,"-195"]],"Y":[1,[4,"145"]]},"fields":{},"shadow":False,"topLevel":False},
        "sz1": {"opcode":"looks_setsizeto","next":"cs1","parent":"go1","inputs":{"SIZE":[1,[4,"55"]]},"fields":{},"shadow":False,"topLevel":False},
        "cs1": {"opcode":"looks_switchcostumeto","next":"for1","parent":"sz1","inputs":{"COSTUME":[1,"cs1m"]},"fields":{},"shadow":False,"topLevel":False},
        "cs1m": {"opcode":"looks_costume","next":None,"parent":"cs1","inputs":{},"fields":{"COSTUME":["hero1",None]},"shadow":True,"topLevel":False},
        "for1": {"opcode":"control_forever","next":None,"parent":"cs1","inputs":{"SUBSTACK":[2,"ifR"]},"fields":{},"shadow":False,"topLevel":False},

        "ifR": {"opcode":"control_if","next":"ifL","parent":"for1","inputs":{"CONDITION":[2,"kpR"],"SUBSTACK":[2,"mvR"]},"fields":{},"shadow":False,"topLevel":False},
        "kpR": {"opcode":"sensing_keypressed","next":None,"parent":"ifR","inputs":{"KEY_OPTION":[1,"koR"]},"fields":{},"shadow":False,"topLevel":False},
        "koR": {"opcode":"sensing_keyoptions","next":None,"parent":"kpR","inputs":{},"fields":{"KEY_OPTION":["right arrow",None]},"shadow":True,"topLevel":False},
        "mvR": {"opcode":"motion_changexby","next":"wchkR","parent":"ifR","inputs":{"DX":[1,[4,"5"]]},"fields":{},"shadow":False,"topLevel":False},
        "wchkR": {"opcode":"control_if","next":"ncR","parent":"mvR","inputs":{"CONDITION":[2,"tcR"],"SUBSTACK":[2,"undoR"]},"fields":{},"shadow":False,"topLevel":False},
        "tcR": {"opcode":"sensing_touchingcolor","next":None,"parent":"wchkR","inputs":{"COLOR":[1,[9,WALL_COLOR]]},"fields":{},"shadow":False,"topLevel":False},
        "undoR": {"opcode":"motion_changexby","next":None,"parent":"wchkR","inputs":{"DX":[1,[4,"-5"]]},"fields":{},"shadow":False,"topLevel":False},
        "ncR": {"opcode":"looks_nextcostume","next":None,"parent":"wchkR","inputs":{},"fields":{},"shadow":False,"topLevel":False},

        "ifL": {"opcode":"control_if","next":"ifU","parent":"ifR","inputs":{"CONDITION":[2,"kpL"],"SUBSTACK":[2,"mvL"]},"fields":{},"shadow":False,"topLevel":False},
        "kpL": {"opcode":"sensing_keypressed","next":None,"parent":"ifL","inputs":{"KEY_OPTION":[1,"koL"]},"fields":{},"shadow":False,"topLevel":False},
        "koL": {"opcode":"sensing_keyoptions","next":None,"parent":"kpL","inputs":{},"fields":{"KEY_OPTION":["left arrow",None]},"shadow":True,"topLevel":False},
        "mvL": {"opcode":"motion_changexby","next":"wchkL","parent":"ifL","inputs":{"DX":[1,[4,"-5"]]},"fields":{},"shadow":False,"topLevel":False},
        "wchkL": {"opcode":"control_if","next":"ncL","parent":"mvL","inputs":{"CONDITION":[2,"tcL"],"SUBSTACK":[2,"undoL"]},"fields":{},"shadow":False,"topLevel":False},
        "tcL": {"opcode":"sensing_touchingcolor","next":None,"parent":"wchkL","inputs":{"COLOR":[1,[9,WALL_COLOR]]},"fields":{},"shadow":False,"topLevel":False},
        "undoL": {"opcode":"motion_changexby","next":None,"parent":"wchkL","inputs":{"DX":[1,[4,"5"]]},"fields":{},"shadow":False,"topLevel":False},
        "ncL": {"opcode":"looks_nextcostume","next":None,"parent":"wchkL","inputs":{},"fields":{},"shadow":False,"topLevel":False},

        "ifU": {"opcode":"control_if","next":"ifD","parent":"ifL","inputs":{"CONDITION":[2,"kpU"],"SUBSTACK":[2,"mvU"]},"fields":{},"shadow":False,"topLevel":False},
        "kpU": {"opcode":"sensing_keypressed","next":None,"parent":"ifU","inputs":{"KEY_OPTION":[1,"koU"]},"fields":{},"shadow":False,"topLevel":False},
        "koU": {"opcode":"sensing_keyoptions","next":None,"parent":"kpU","inputs":{},"fields":{"KEY_OPTION":["up arrow",None]},"shadow":True,"topLevel":False},
        "mvU": {"opcode":"motion_changeyby","next":"wchkU","parent":"ifU","inputs":{"DY":[1,[4,"5"]]},"fields":{},"shadow":False,"topLevel":False},
        "wchkU": {"opcode":"control_if","next":None,"parent":"mvU","inputs":{"CONDITION":[2,"tcU"],"SUBSTACK":[2,"undoU"]},"fields":{},"shadow":False,"topLevel":False},
        "tcU": {"opcode":"sensing_touchingcolor","next":None,"parent":"wchkU","inputs":{"COLOR":[1,[9,WALL_COLOR]]},"fields":{},"shadow":False,"topLevel":False},
        "undoU": {"opcode":"motion_changeyby","next":None,"parent":"wchkU","inputs":{"DY":[1,[4,"-5"]]},"fields":{},"shadow":False,"topLevel":False},

        "ifD": {"opcode":"control_if","next":"ifM","parent":"ifU","inputs":{"CONDITION":[2,"kpD"],"SUBSTACK":[2,"mvD"]},"fields":{},"shadow":False,"topLevel":False},
        "kpD": {"opcode":"sensing_keypressed","next":None,"parent":"ifD","inputs":{"KEY_OPTION":[1,"koD"]},"fields":{},"shadow":False,"topLevel":False},
        "koD": {"opcode":"sensing_keyoptions","next":None,"parent":"kpD","inputs":{},"fields":{"KEY_OPTION":["down arrow",None]},"shadow":True,"topLevel":False},
        "mvD": {"opcode":"motion_changeyby","next":"wchkD","parent":"ifD","inputs":{"DY":[1,[4,"-5"]]},"fields":{},"shadow":False,"topLevel":False},
        "wchkD": {"opcode":"control_if","next":None,"parent":"mvD","inputs":{"CONDITION":[2,"tcD"],"SUBSTACK":[2,"undoD"]},"fields":{},"shadow":False,"topLevel":False},
        "tcD": {"opcode":"sensing_touchingcolor","next":None,"parent":"wchkD","inputs":{"COLOR":[1,[9,WALL_COLOR]]},"fields":{},"shadow":False,"topLevel":False},
        "undoD": {"opcode":"motion_changeyby","next":None,"parent":"wchkD","inputs":{"DY":[1,[4,"5"]]},"fields":{},"shadow":False,"topLevel":False},

        "ifM": {"opcode":"control_if","next":"ifS","parent":"ifD","inputs":{"CONDITION":[2,"tmM"],"SUBSTACK":[2,"sfM"]},"fields":{},"shadow":False,"topLevel":False},
        "tmM": {"opcode":"sensing_touchingobject","next":None,"parent":"ifM","inputs":{"TOUCHINGOBJECTMENU":[1,"tmMm"]},"fields":{},"shadow":False,"topLevel":False},
        "tmMm": {"opcode":"sensing_touchingobjectmenu","next":None,"parent":"tmM","inputs":{},"fields":{"TOUCHINGOBJECTMENU":["Monster",None]},"shadow":True,"topLevel":False},
        "sfM": {"opcode":"sound_playuntildone","next":"syM","parent":"ifM","inputs":{"SOUND_MENU":[1,"sfMm"]},"fields":{},"shadow":False,"topLevel":False},
        "sfMm": {"opcode":"sound_sounds_menu","next":None,"parent":"sfM","inputs":{},"fields":{"SOUND_MENU":["Oops",None]},"shadow":True,"topLevel":False},
        "syM": {"opcode":"looks_sayforsecs","next":"rsM","parent":"sfM","inputs":{"MESSAGE":[1,[10,"Game Over!"]],"SECS":[1,[4,"1"]]},"fields":{},"shadow":False,"topLevel":False},
        "rsM": {"opcode":"data_setvariableto","next":"rs2M","parent":"syM","inputs":{"VALUE":[1,[4,"0"]]},"fields":{"VARIABLE":["Skor",VAR_SCORE]},"shadow":False,"topLevel":False},
        "rs2M": {"opcode":"data_setvariableto","next":"gtM","parent":"rsM","inputs":{"VALUE":[1,[4,"0"]]},"fields":{"VARIABLE":["Timer",VAR_TIMER]},"shadow":False,"topLevel":False},
        "gtM": {"opcode":"motion_gotoxy","next":None,"parent":"rs2M","inputs":{"X":[1,[4,"-195"]],"Y":[1,[4,"145"]]},"fields":{},"shadow":False,"topLevel":False},

        "ifS": {"opcode":"control_if","next":None,"parent":"ifM","inputs":{"CONDITION":[2,"tmS"],"SUBSTACK":[2,"sfS"]},"fields":{},"shadow":False,"topLevel":False},
        "tmS": {"opcode":"sensing_touchingobject","next":None,"parent":"ifS","inputs":{"TOUCHINGOBJECTMENU":[1,"tmSm"]},"fields":{},"shadow":False,"topLevel":False},
        "tmSm": {"opcode":"sensing_touchingobjectmenu","next":None,"parent":"tmS","inputs":{},"fields":{"TOUCHINGOBJECTMENU":["Bintang",None]},"shadow":True,"topLevel":False},
        "sfS": {"opcode":"sound_playuntildone","next":"syS","parent":"ifS","inputs":{"SOUND_MENU":[1,"sfSm"]},"fields":{},"shadow":False,"topLevel":False},
        "sfSm": {"opcode":"sound_sounds_menu","next":None,"parent":"sfS","inputs":{},"fields":{"SOUND_MENU":["Win",None]},"shadow":True,"topLevel":False},
        "syS": {"opcode":"looks_sayforsecs","next":"stS","parent":"sfS","inputs":{"MESSAGE":[1,[10,"Selamat! Kamu Menang!"]],"SECS":[1,[4,"3"]]},"fields":{},"shadow":False,"topLevel":False},
        "stS": {"opcode":"control_stop","next":None,"parent":"syS","inputs":{},"fields":{"STOP_OPTION":["all",None]},"shadow":False,"topLevel":False},
      },
      "currentCostume": 0,
      "costumes": [
        {"name":"hero1","assetId":HERO1_ID,"md5ext":HERO1_ID+".svg","dataFormat":"svg","rotationCenterX":17,"rotationCenterY":17},
        {"name":"hero2","assetId":HERO2_ID,"md5ext":HERO2_ID+".svg","dataFormat":"svg","rotationCenterX":17,"rotationCenterY":17},
      ],
      "sounds": [
        {"name":"Oops","assetId":OOPS_ID,"md5ext":OOPS_ID+".wav","dataFormat":"wav","rate":44100,"sampleCount":22050},
        {"name":"Win", "assetId":WIN_ID, "md5ext":WIN_ID +".wav","dataFormat":"wav","rate":44100,"sampleCount":26460},
      ],
      "volume": 100, "layerOrder": 3, "visible": True,
      "x": -195, "y": 145, "size": 55, "direction": 90,
      "draggable": False, "rotationStyle": "left-right"
    },

    {
      "isStage": False, "name": "Monster",
      "variables": {}, "lists": {}, "broadcasts": {}, "comments": {},
      "blocks": {
        "mf1": {"opcode":"event_whenflagclicked","next":"mg1","parent":None,"inputs":{},"fields":{},"shadow":False,"topLevel":True,"x":20,"y":20},
        "mg1": {"opcode":"motion_gotoxy","next":"ms1","parent":"mf1","inputs":{"X":[1,[4,"20"]],"Y":[1,[4,"40"]]},"fields":{},"shadow":False,"topLevel":False},
        "ms1": {"opcode":"looks_setsizeto","next":"md1","parent":"mg1","inputs":{"SIZE":[1,[4,"60"]]},"fields":{},"shadow":False,"topLevel":False},
        "md1": {"opcode":"motion_pointindirection","next":"mfl","parent":"ms1","inputs":{"DIRECTION":[1,[4,"90"]]},"fields":{},"shadow":False,"topLevel":False},
        "mfl": {"opcode":"control_forever","next":None,"parent":"md1","inputs":{"SUBSTACK":[2,"mm1"]},"fields":{},"shadow":False,"topLevel":False},
        "mm1": {"opcode":"motion_movesteps","next":"mb1","parent":"mfl","inputs":{"STEPS":[1,[4,"2"]]},"fields":{},"shadow":False,"topLevel":False},
        "mb1": {"opcode":"motion_ifonedgebounce","next":"mwc","parent":"mm1","inputs":{},"fields":{},"shadow":False,"topLevel":False},
        "mwc": {"opcode":"control_if","next":"mw1","parent":"mb1","inputs":{"CONDITION":[2,"mtc"],"SUBSTACK":[2,"mun"]},"fields":{},"shadow":False,"topLevel":False},
        "mtc": {"opcode":"sensing_touchingcolor","next":None,"parent":"mwc","inputs":{"COLOR":[1,[9,WALL_COLOR]]},"fields":{},"shadow":False,"topLevel":False},
        "mun": {"opcode":"motion_turnright","next":None,"parent":"mwc","inputs":{"DEGREES":[1,[4,"90"]]},"fields":{},"shadow":False,"topLevel":False},
        "mw1": {"opcode":"control_wait","next":None,"parent":"mwc","inputs":{"DURATION":[1,[5,"0.02"]]},"fields":{},"shadow":False,"topLevel":False},
      },
      "currentCostume": 0,
      "costumes": [{"name":"monster1","assetId":MONSTER_ID,"md5ext":MONSTER_ID+".svg","dataFormat":"svg","rotationCenterX":17,"rotationCenterY":17}],
      "sounds": [], "volume": 100, "layerOrder": 2, "visible": True,
      "x": 20, "y": 40, "size": 60, "direction": 90,
      "draggable": False, "rotationStyle": "left-right"
    },

    {
      "isStage": False, "name": "Bintang",
      "variables": {}, "lists": {}, "broadcasts": {}, "comments": {},
      "blocks": {
        "sf1": {"opcode":"event_whenflagclicked","next":"sg1","parent":None,"inputs":{},"fields":{},"shadow":False,"topLevel":True,"x":20,"y":20},
        "sg1": {"opcode":"motion_gotoxy","next":"ss1","parent":"sf1","inputs":{"X":[1,[4,"195"]],"Y":[1,[4,"-145"]]},"fields":{},"shadow":False,"topLevel":False},
        "ss1": {"opcode":"looks_setsizeto","next":"sfl","parent":"sg1","inputs":{"SIZE":[1,[4,"75"]]},"fields":{},"shadow":False,"topLevel":False},
        "sfl": {"opcode":"control_forever","next":None,"parent":"ss1","inputs":{"SUBSTACK":[2,"st1"]},"fields":{},"shadow":False,"topLevel":False},
        "st1": {"opcode":"motion_turnright","next":"sw1","parent":"sfl","inputs":{"DEGREES":[1,[4,"2"]]},"fields":{},"shadow":False,"topLevel":False},
        "sw1": {"opcode":"control_wait","next":None,"parent":"st1","inputs":{"DURATION":[1,[5,"0.05"]]},"fields":{},"shadow":False,"topLevel":False},
      },
      "currentCostume": 0,
      "costumes": [{"name":"star1","assetId":STAR_ID,"md5ext":STAR_ID+".svg","dataFormat":"svg","rotationCenterX":18,"rotationCenterY":18}],
      "sounds": [], "volume": 100, "layerOrder": 4, "visible": True,
      "x": 195, "y": -145, "size": 75, "direction": 90,
      "draggable": False, "rotationStyle": "all around"
    }
  ],
  "monitors": [
    {"id":VAR_SCORE,"mode":"default","opcode":"data_variable","params":{"VARIABLE":"Skor"},
     "spriteName":None,"value":0,"width":0,"height":0,"x":5,"y":5,"visible":True,
     "sliderMin":0,"sliderMax":100,"isDiscrete":True},
    {"id":VAR_TIMER,"mode":"default","opcode":"data_variable","params":{"VARIABLE":"Timer"},
     "spriteName":None,"value":0,"width":0,"height":0,"x":5,"y":30,"visible":True,
     "sliderMin":0,"sliderMax":100,"isDiscrete":True}
  ],
  "extensions": [],
  "meta": {"semver":"3.0.0","vm":"0.2.0-prerelease.20230901","agent":""}
}

output = 'maze_adventure_v2.sb3'

with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED) as zf:
    zf.writestr('project.json', json.dumps(project))
    zf.writestr(BACKDROP_ID + '.svg', backdrop_svg)
    zf.writestr(WALL_ID + '.svg', wall_svg)
    zf.writestr(HERO1_ID + '.svg', hero_svg)
    zf.writestr(HERO2_ID + '.svg', hero_svg2)
    zf.writestr(MONSTER_ID + '.svg', monster_svg)
    zf.writestr(STAR_ID + '.svg', star_svg)
    zf.writestr(OOPS_ID + '.wav', make_beep_wav(200, 0.5))
    zf.writestr(WIN_ID + '.wav', make_beep_wav(880, 0.6))

print(f'"{output}" berhasil dibuat! ({os.path.getsize(output):,} bytes)')
print()
print('CARA UPLOAD KE SCRATCH:')
print('1. Buka https://scratch.mit.edu dan login')
print('2. Klik Buat / Create')
print('3. File > Load from your computer')
print('4. Pilih maze_adventure_v2.sb3')
print('5. Klik ▶️ dan mainkan!')
print()
print('KONTROL: Arrow keys ⬆️⬇️⬅️➡️')
print('Sentuh Bintang  = MENANG!')
print('Kena Monster = Game Over + Reset skor')
print('Tembok = Tidak bisa ditembus')
print('Skor & Timer = Tampil di pojok kiri atas')