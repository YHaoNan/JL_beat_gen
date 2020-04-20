import mido
import os
import uuid
import tones
from Track import Track

SONG_ROOT_PITCH = 30

def genBeat(SONG_BPM,SONG_LOOP_NUM,SONG_TUNE,kick,snare,bass):

    mid = mido.MidiFile()
    kick = Track(name="kick",inst=tones.KICK['bass1'],bpm=SONG_BPM,key=SONG_TUNE)
    snare = Track(name="snare",inst=tones.SNARE['acoustic_snare'],bpm=SONG_BPM,key=SONG_TUNE)
    bass = Track(name='bass',inst=tones.BASS['synth_bass_1'],bpm=SONG_BPM,key=SONG_TUNE)
    mid.tracks.append(kick)
    mid.tracks.append(snare)
    mid.tracks.append(bass)

    bass_lead = [4,4,4,4,0,0,0,0,7,7,7,7,2,2,2,2]
    bass_i = 0


    snare_n_kick_sym = 0

    loop_start_time = 0
    for j in range(SONG_LOOP_NUM):
        for i in range(loop_start_time,loop_start_time+7680):
            if i % 480 == 0 and snare_n_kick_sym == 0:
                kick.add_drum(startTime=i,length=30)
                snare_n_kick_sym = 1
            elif i % 480 == 0 and snare_n_kick_sym == 1:
                snare.add_drum(startTime=i,length=30)
                snare_n_kick_sym = 0
            elif i % 240 == 0:
                bass.add_note(pitch=SONG_ROOT_PITCH+bass_lead[bass_i],startTime=i,length=240)
                bass_i = bass_i + 1
                if bass_i == 16:
                    bass_i = 0
        loop_start_time = loop_start_time + 7680

    fileName = str(uuid.uuid4())+".mid"
    mid.save(fileName)
    buf = bytearray(os.path.getsize(fileName))
    with open(fileName,'rb') as f:
        f.readinto(buf)
    f.close()
    os.remove(fileName)
    return buf


