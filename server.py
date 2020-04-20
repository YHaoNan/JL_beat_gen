#!/usr/bin/env python
# coding=utf-8
import gen
import tones
from flask import Flask,Response

app = Flask("BeatGEN")
@app.route('/gen/<int:bpm>/<tune>/<int:loop>/<kick>/<snare>/<bass>')
def genBeat(bpm=170,tune="C",loop=16,kick=tones.KICK["bass1"],snare=tones.SNARE['acoustic_snare'],bass=tones.BASS['synth_bass_1']):
    if paramsChecked(bpm,tune,loop,kick,snare,bass):
        buf = gen.genBeat(bpm,loop,tune,kick,snare,bass)
        return Response(buf,mimetype='audio/midi')
    else :
        return "Wrong params"

def safeGet(_map,key):
    try:
        return _map[key]
    except:
        return None


def paramsChecked(bpm,tune,loop,kick,snare,bass):
    if bpm < 160 and bpm > 240:
        return False
    if tune not in ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]:
        return False
    if loop <8 and loop > 32:
        return False
    if safeGet(tones.KICK,kick) == None:
        return False
    if safeGet(tones.SNARE,snare) == None:
        return False
    if safeGet(tones.BASS,bass) == None:
        return False
    return True


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

