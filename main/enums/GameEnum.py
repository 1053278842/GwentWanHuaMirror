from enum import Enum


class EGameStatus(Enum):
    UNINIT = 0
    RUNNING = 1 # 已经运行的依据
    ENDING = 2
    ENDED = 3   # 结束依据

class EGameEndReason(Enum):
	Normal = 0
	PlayerForfeit = 1
	PlayerDisconnected = 2
	PlayerCompromisedClientState = 3
	PlayerCompromisedClientLocked = 4
	PlayerCompromisedUnauthorizedAction = 5
	PlayerOverQuota = 6
	ServerError = 7
	EndGameTimeout = 8
	ReplayInconsistent = 9
	ReplayNotProgressing = 10
	PlayerNotPlaying = 11

class EGameMode(Enum):
    SinglePlayer = 0    # p vs ai   
    Client = 1          # p vs p
    Server = 2
    Replay = 3
    Spectator = 4

class EBattleType(Enum):
    Unknown = 0
    Quick = 1       # 训练模式-娛樂【pvp】
    Ranked = 2      # 天梯【非职天】
    Tournament = 3  # 錦標賽
    Friend = 4      # 友谊赛
    ProLadder = 5   # 职业天梯
    Challenges = 6  # 挑战
    HolidayEvent = 7    # 假日活动
    Arena = 8       # 竞技场
    OnlineTournament = 9    # 在线锦标赛
    ArenaV2 = 10    # 竞技场v2
    Seasonal = 11   # 季节性？赛季？？