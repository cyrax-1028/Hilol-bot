from aiogram.fsm.state import State, StatesGroup

class AddAudioState(StatesGroup):
    choosing_qori = State()
    choosing_surah = State()
    sending_audio = State()

class UserAudioState(StatesGroup):
    choosing_qori = State()
    choosing_sura = State()