# 与服务端的接口

记牌器只跟服务端说三件事：取卡组库、取版本、交战报。

## 上报战报

对局结束（`GameStatus == ENDED`）且不是单人/观战/友谊赛/竞技场时，
`RequestManager.sendBattleInfo()` 会 POST 到 `{url}/battle/api/save`：

```jsonc
{
  "GameStatus": 3, "GameMode": 1, "GameId": 1732..., "BattleType": 2,
  "roundInfos": [{ "index": 0, "left_score": 12, "right_score": 8,
                   "starting_playerId": 1, "winner_playId": 1, "turn_index": 11 }, ...],
  "curr_round_index": 2, "winner_playId": 1, "end_game_reason": 0,
  "players": [
    { "player_name": "...", "service_id": 900000000000000001, "paragon_level": 0,
      "MMR": 9600, "rank": 0, "leader_id": 200087, "stratagem_id": 0, "faction_id": 4,
      "decks": [200087, 0, 202115, 201779, ...],   // leader + stratagem + 牌表
      "deckId": 1234567890123456789 }              // hash(frozenset(decks))
  ]
}
```

字段与 `dao/CardDao.py:getBattleInfo()` 一一对应：

| 字段 | 来源 | 说明 |
| --- | --- | --- |
| `GameStatus` | `gi+0x20,[0xe8]` | 0 未初始化 / 1 进行中 / 2 结束时 / 3 已结束 |
| `GameMode` | `gi+0x38` | 0 单人 / 1 对战 / 4 观战 |
| `BattleType` | `gi+0x28,[0x58]` | 2 天梯 / 4 友谊 / 8 竞技场 … |
| `roundInfos[]` | `roundInfos` 数组 | 三回合的小分、先手、胜者、回合数 |
| `players[].decks` | 牌表实例 | `[leader_id, stratagem_id, ...25 张]` |
| `players[].deckId` | 计算 | `hash(frozenset(decks))`，服务端拿它当卡组主键 |

### 哪些局会被过滤掉

`sendBattleInfo()` 里依次判断：

1. `GameStatus` 是 RUNNING / UNINIT → 不报；
2. `GameMode` 是 SinglePlayer / Spectator → 不报；
3. `BattleType` 是 Friend / Arena / ArenaV2 → 不报；
4. 全局配置 `automaticSubmit = false` → 把 `players[].decks` 清空后仍上报（只统计对局，不采集牌表）。

### 没有游戏怎么验证这条链路

用仓库根目录的 [`scripts/simulate_battle.py`](https://github.com/1053278842/GwentMirrorAllInOne/blob/main/scripts/simulate_battle.py)：

```bash
python3 scripts/simulate_battle.py --base-url http://localhost:8080/gmapi --matches 3 --unique-decks
```

它造的就是上面这份报文，服务端能完整走完「拆四表 → 入库」。
`--unique-decks` 会换掉两张牌，生成新的卡组指纹（对应「玩家自己组的牌」）。

## 同步卡组库

```bash
GET {url}/deck/api/getDecks
```

返回最多 5000 套卡组，客户端写进 `resources/data/decks.json`（UTF-16），
用于「预测卡组 / 差异对比」：根据你打出的牌去 3488 副历史卡组里找最相似的那副。

`RequestManager.updateDecks()` 只在 `checkCanUpdateDecks()` 判定距上次更新超过
`global_config.max_dif_hours`（默认 3 小时）时才真正拉取。

## 同步版本

```bash
POST {url}/version/api/getId
```

返回 `version` 表整行，客户端写进 `resources/config/version.json`：

```jsonc
{ "id": 9, "address": 59309712, "addressGOG": 56389248, "addressGY": 0,
  "name": "Ver 0.4.3-beta", "canAutoUpdate": 1, "orderMode": 0 }
```

* `address` 是 Steam 版的基址偏移，`addressGOG` / `addressGY` 是另两个平台；
* `canAutoUpdate = 0` 时客户端拒绝自动切基址，弹窗要求手动更新；
* 主窗「更新」页就是调这个接口，成功后再 `FT.resetVersionPlatformAddress(平台)`。

## 与服务器的最小约定

| 项 | 值 |
| --- | --- |
| 协议 | 纯 HTTP，无鉴权 |
| 编码 | UTF-8 JSON |
| 超时 | `getDecks` / `getId` 30 秒，`battle save` 默认 |
| 失败处理 | 战报上报失败只打印「发送对局信息失败!」，不重试、不阻塞界面 |