import mido


class Track(mido.MidiTrack):
    def __init__(self,name,inst,bpm,key):
        self.name = name
        self.inst = inst
        self.bpm = bpm
        self.key = key

        # 上一个音符结束位置
        self.lastNoteEndPos = 0
        self.initialize_metadata()

    def initialize_metadata(self):
        tempo = mido.bpm2tempo(self.bpm)
        super().append(mido.MetaMessage('set_tempo',tempo = tempo, time = 0))
        super().append(mido.MetaMessage('key_signature',key = self.key))
        super().append(mido.Message('program_change',channel = self.inst[0],program = self.inst[1],time = 0))

    def __add_note(self,pitch,velocity,startTime,length,channel):
        intervalFromLast = startTime - self.lastNoteEndPos
        super().append(mido.Message('note_on',note = pitch,velocity=velocity,time = intervalFromLast,channel = channel))
        super().append(mido.Message('note_off',note = pitch,velocity=velocity,time = length,channel = channel))
        self.lastNoteEndPos = startTime + length



    def add_note(self,pitch,startTime,length):
        self.__add_note(pitch=pitch,velocity=100,startTime=startTime,length=length,channel=self.inst[0])

    def add_drum(self,startTime,length):
        self.__add_note(pitch=self.inst[1],velocity=100,startTime=startTime,length=length,channel=self.inst[0])






