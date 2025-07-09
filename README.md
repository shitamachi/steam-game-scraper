# Steam Game Scraper

This project provides a Python tool to scrape comprehensive game information from Steam store pages.

## Project Structure

```
steam/
├── src/
│   └── steam_scraper/
│       ├── __init__.py
│       ├── scraper.py        # Core scraping and parsing logic
│       ├── utils.py          # Utility functions (e.g., URL validation)
│       └── constants.py      # Supported languages and other constants
├── html_cache/             # Cached HTML files for faster processing
├── tests/                  # Unit tests for the scraper
├── cli.py                  # Command-line interface entry point
└── README.md               # Project documentation
```

## How it Works

The `cli.py` script serves as the command-line interface. It utilizes the `steam_scraper` package to:
1. Validate the provided Steam store URL.
2. Fetch the HTML content of the game page. It first checks the `html_cache/` directory for a cached version (named `game_name-appid-lang.html`). If not found, it downloads the page from Steam, respecting the specified language, and then caches it.
3. Parse the HTML using `BeautifulSoup` to extract various game details.
4. Output the extracted data as a JSON object to the console or a specified file.

## Usage

To scrape game data, run the `cli.py` script with the Steam store URL and optional arguments:

```bash
uv run cli.py <steam_game_url> [--output <output_file.json>] [--lang <language_code>]
```

**Arguments:**
*   `<steam_game_url>`: The full URL of the Steam store page (e.g., `https://store.steampowered.com/app/1091500/Cyberpunk_2077/`).
*   `--output <output_file.json>`: (Optional) Path to save the extracted JSON data. If omitted, data is printed to the console.
*   `--lang <language_code>`: (Optional) The language for the store page. Defaults to `english`. Supported language codes are defined in `src/steam_scraper/constants.py`.

**Example:**

```bash
uv run cli.py https://store.steampowered.com/app/1091500/Cyberpunk_2077/ --lang schinese --output cyberpunk_2077_schinese.json
```

## Data Schema

The script returns a JSON object with the following fields:

| Key                   | Type        | Description                                                                 |
|-----------------------|-------------|-----------------------------------------------------------------------------|
| `title`               | `String`    | The official name of the game.                                              |
| `header_image`        | `String`    | URL of the main header image for the game.                                  |
| `short_description`   | `String`    | A brief summary or snippet of the game's description.                       |
| `full_description`    | `String`    | The complete description of the game.                                       |
| `developer`           | `Object`    | Developer information (`name`: String, `link`: String).                     |
| `publisher`           | `Object`    | Publisher information (`name`: String, `link`: String).                     |
| `release_date`        | `String`    | The date when the game was released on Steam.                               |
| `media`               | `Object`    | Contains lists of `videos` and `screenshots`.                               |
| `media.videos`        | `[Object]`  | List of video objects (`title`, `thumbnail`, `webm_source`, `mp4_source`).  |
| `media.screenshots`   | `[String]`  | List of URLs for game screenshots.                                          |
| `price`               | `String/Object` | The current price. Can be a string (e.g., "Free to Play") or an object (`discount_price`, `original_price`). |
| `tags`                | `[String]`  | A list of user-defined tags associated with the game.                       |
| `reviews`             | `Object`    | Review summaries for `recent` and `all` reviews (`summary`, `tooltip`).     |
| `system_requirements` | `Object`    | System requirements for different OS (e.g., `win`, `mac`, `linux`). Each OS contains key-value pairs like `os`, `processor`, `memory`, etc. |
| `language_support`    | `[Object]`  | List of supported languages (`language`, `interface`, `full_audio`, `subtitles`). |
| `metacritic`          | `Object`    | Metacritic score and URL (`score`: Integer, `url`: String).                 |
| `dlcs`                | `[Object]`  | List of downloadable content (`name`: String, `price`: String).             |
| `features`            | `[String]`  | List of game features (e.g., "Single-player", "Steam Achievements").      |
| `content_descriptors` | `[String]`  | Content warning descriptors (e.g., "Violence", "Sexual scenes").          |

## JSON Example

Here is an example of the output for "Cyberpunk 2077" (Simplified Chinese):

```json
{
  "title": "赛博朋克 2077",
  "header_image": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/4e88035f3a75e69e0ef2005fc611a7fafcb227e1/header_schinese.jpg?t=1749198613",
  "short_description": "《赛博朋克 2077》是一款开放世界动作冒险 RPG 游戏。故事发生在暗黑未来的夜之城，一座五光十色、危机四伏的超级大都会，权力更迭和无尽的身体改造是这里不变的主题。",
  "full_description": "关于此游戏《赛博朋克 2077》的舞台位于大都会夜之城，是一款在开放世界动作冒险角色扮演游戏。您扮演一位赛博朋克雇佣兵, 身陷绝地求生、不成功便成仁的险境。经过改进的同时更有全新免费额外内容加入。接受任务、累积声望、解锁升级，自定义您的人物和玩法。玩家经营的人际关系和做出的选择将会改变剧情的走向和身边的世界。这里是传奇诞生的地方。您的传奇又在哪里？版本更新 2.2，自定义你的赛博朋克！免费版本更新 2.2 让你表现自我！通过新的时装义体、纹身和妆容打造角色。凭借雷菲尔德独家专属的晶彩车衣技术，更换豪车和超跑的喷漆，让爱车焕然一新。此外还可以沉浸在加强后的照片模式里，通过令人惊叹的细节捕捉每一个瞬间。创造属于你的赛博朋克装备赛博增强科技，化身城市法外之徒，在夜之城的街头谱写属于你的传奇。探索未来都市夜之城充斥着丰富的活动，看不完的风景，以及各式各样的人。去哪里，什么时候去，怎么去，全都取决于你自己。打造您的传奇展开大胆的冒险，和令人难忘的角色起建立亲密关系。您作出的选择决定了他们最终的命运。推出改良内容体验《赛博朋克 2077》在游戏性、经济系统、城市、地图使用等方面的大量改良内容。",
  "developer": {
    "name": "CD PROJEKT RED",
    "link": "https://store.steampowered.com/developer/CDPR?snr=1_5_9__2000"
  },
  "publisher": {
    "name": "CD PROJEKT RED",
    "link": "https://store.steampowered.com/publisher/CDPR?snr=1_5_9__2000"
  },
  "release_date": "2020 年 12 月 9 日",
  "media": {
    "videos": [
      {
        "title": "《赛博朋克 2077: 终极版》 梦想之城",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/257082814/9698fdf58d051fb4d2967ed29612dcb0edc3dd2c/movie_232x130.jpg?t=1734434708",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/257082814/movie480_vp9.webm?t=1734434708",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/257082814/movie480.mp4?t=1734434708"
      },
      {
        "title": "",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/256987142/movie.184x123.jpg?t=1701872721",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/256987142/movie480_vp9.webm?t=1701872721",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/256987142/movie480.mp4?t=1701872721"
      },
      {
        "title": "",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/256984155/movie.184x123.jpg?t=1700653141",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/256984155/movie480_vp9.webm?t=1700653141",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/256984155/movie480.mp4?t=1700653141"
      },
      {
        "title": "",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/256977948/movie.184x123.jpg?t=1698157602",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/256977948/movie480_vp9.webm?t=1698157602",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/256977948/movie480.mp4?t=1698157602"
      },
      {
        "title": "",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/256979907/movie.184x123.jpg?t=1699262639",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/256979907/movie480_vp9.webm?t=1699262639",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/256979907/movie480.mp4?t=1699262639"
      },
      {
        "title": "",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/256975600/movie.184x123.jpg?t=1697117065",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/256975600/movie480_vp9.webm?t=1697117065",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/256975600/movie480.mp4?t=1697117065"
      },
      {
        "title": "",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/256975568/movie.184x123.jpg?t=1697117153",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/256975568/movie480_vp9.webm?t=1697117153",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/256975568/movie480.mp4?t=1697117153"
      },
      {
        "title": "",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/256975526/movie.184x123.jpg?t=1697117241",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/256975526/movie480_vp9.webm?t=1697117241",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/256975526/movie480.mp4?t=1697117241"
      },
      {
        "title": "",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/256904576/movie.184x123.jpg?t=1662480328",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/256904576/movie480_vp9.webm?t=1662480328",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/256904576/movie480.mp4?t=1662480328"
      },
      {
        "title": "",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/256876053/movie.184x123.jpg?t=1697117313",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/256876053/movie480_vp9.webm?t=1697117313",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/256876053/movie480.mp4?t=1697117313"
      },
      {
        "title": "",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/256810254/movie.184x123.jpg?t=1611326528",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/256810254/movie480_vp9.webm?t=1611326528",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/256810254/movie480.mp4?t=1611326528"
      },
      {
        "title": "",
        "thumbnail": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/256812969/movie.184x123.jpg?t=1611328088",
        "webm_source": "https://video.fastly.steamstatic.com/store_trailers/256812969/movie480_vp9.webm?t=1611328088",
        "mp4_source": "https://video.fastly.steamstatic.com/store_trailers/256812969/movie480.mp4?t=1611328088"
      }
    ],
    "screenshots": [
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_2f649b68d579bf87011487d29bc4ccbfdd97d34f.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_0e64170751e1ae20ff8fdb7001a8892fd48260e7.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_af2804aa4bf35d4251043744412ce3b359a125ef.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_7924f64b6e5d586a80418c9896a1c92881a7905b.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_4eb068b1cf52c91b57157b84bed18a186ed7714b.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_b529b0abc43f55fc23fe8058eddb6e37c9629a6a.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_8640d9db74f7cad714f6ecfb0e1aceaa3f887e58.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_9284d1c5b248726760233a933dbb83757d7d5d95.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_4bda6f67580d94832ed2d5814e41ebe018ba1d9e.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_e5a94665dbfa5a30931cff2f45cdc0ebea9fcebb.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_429db1d013a0366417d650d84f1eff02d1a18c2d.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_872822c5e50dc71f345416098d29fc3ae5cd26c1.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_ae4465fa8a44dd330dbeb7992ba196c2f32cabb1.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_f79fda81e6f3a37e0978054102102d71840f8b57.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_bb1a60b8e5061caef7208369f42c5c9d574c9ac4.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_a0c4e4015b5cf766d19bf97eee8b086183510e04.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_b20689e73e3ac19bcc5fad2c18d0353c769de144.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_ff3d920e254d18aa2a25d3765ac2ebe845efd208.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_0002f18563d313bdd1d82c725d411408ebf762b0.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_526123764d1c628caa1eb62c596f1b732f416c8c.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_284ba40590de8f604ae693631c751a0aefdc452e.1920x1080.jpg?t=1749198613",
      "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_9beef14102f164fa1163536d0fb3a51d0a2e4a3f.1920x1080.jpg?t=1749198613"
    ]
  },
  "price": {
    "discount_price": "S$24.49",
    "original_price": "S$69.90"
  },
  "tags": [
    "赛博朋克",
    "开放世界",
    "裸露",
    "角色扮演",
    "单人",
    "科幻",
    "第一人称射击",
    "剧情丰富",
    "成人",
    "未来",
    "第一人称",
    "氛围",
    "探索",
    "动作",
    "暴力",
    "好评原声音轨",
    "动作角色扮演",
    "冒险",
    "角色自定义",
    "沉浸式模拟"
  ],
  "reviews": {
    "recent": {
      "summary": "好评如潮",
      "tooltip": "过去 30 天内的 9,329 篇用户评测中有 95% 为好评。<br><br>此产品在一个或多个时间段内出现跑题评测活动。这些时间段内的评测已按您的偏好设置不计入此产品的评测分数。"
    },
    "all": {
      "summary": "特别好评",
      "tooltip": "此游戏的 758,464 篇用户评测中有 85% 为好评。<br><br>此产品在一个或多个时间段内出现跑题评测活动。这些时间段内的评测已按您的偏好设置不计入此产品的评测分数。"
    }
  },
  "system_requirements": {
    "win": {
      "操作系统": "64-bit Windows 10",
      "处理器": "Core i7-12700 or Ryzen 7 7800X3D",
      "内存": "16 GB RAM",
      "显卡": "GeForce RTX 2060 SUPER or Radeon RX 5700 XT or Arc A770",
      "directx 版本": "12",
      "存储空间": "需要 70 GB 可用空间",
      "附注事项": "SSD required."
    }
  },
  "language_support": [
    {
      "language": "简体中文",
      "interface": true,
      "full_audio": true,
      "subtitles": true
    },
    {
      "language": "英语",
      "interface": true,
      "full_audio": true,
      "subtitles": true
    },
    {
      "language": "法语",
      "interface": true,
      "full_audio": true,
      "subtitles": true
    },
    {
      "language": "意大利语",
      "interface": true,
      "full_audio": true,
      "subtitles": true
    },
    {
      "language": "德语",
      "interface": true,
      "full_audio": true,
      "subtitles": true
    },
    {
      "language": "西班牙语 - 西班牙",
      "interface": true,
      "full_audio": true,
      "subtitles": true
    },
    {
      "language": "阿拉伯语",
      "interface": true,
      "full_audio": false,
      "subtitles": true
    },
    {
      "language": "捷克语",
      "interface": true,
      "full_audio": false,
      "subtitles": true
    },
    {
      "language": "匈牙利语",
      "interface": true,
      "full_audio": false,
      "subtitles": true
    },
    {
      "language": "日语",
      "interface": true,
      "full_audio": true,
      "subtitles": true
    },
    {
      "language": "韩语",
      "interface": true,
      "full_audio": true,
      "subtitles": true
    },
    {
      "language": "波兰语",
      "interface": true,
      "full_audio": true,
      "subtitles": true
    },
    {
      "language": "葡萄牙语 - 巴西",
      "interface": true,
      "full_audio": true,
      "subtitles": true
    },
    {
      "language": "俄语",
      "interface": true,
      "full_audio": true,
      "subtitles": true
    },
    {
      "language": "西班牙语 - 拉丁美洲",
      "interface": true,
      "full_audio": false,
      "subtitles": true
    },
    {
      "language": "泰语",
      "interface": true,
      "full_audio": false,
      "subtitles": true
    },
    {
      "language": "繁体中文",
      "interface": true,
      "full_audio": false,
      "subtitles": true
    },
    {
      "language": "土耳其语",
      "interface": true,
      "full_audio": false,
      "subtitles": true
    },
    {
      "language": "乌克兰语",
      "interface": true,
      "full_audio": false,
      "subtitles": true
    }
  ],
  "metacritic": {
    "score": 86,
    "url": "https://www.metacritic.com/game/pc/cyberpunk-2077?ftag=MCD-06-10aaa1f"
  },
  "dlcs": [
    {
      "name": "赛博朋克 2077：终极版",
      "price": "S$24.49"
    },
    {
      "name": "赛博朋克 2077：往日之影",
      "price": "S$39.90"
    },
    {
      "name": "赛博朋克 2077 资料片通行证",
      "price": "S$39.90"
    }
  ],
  "features": [
    "单人",
    "Steam 成就",
    "Steam 集换式卡牌",
    "Steam 云",
    "家庭共享"
  ],
  "content_descriptors": [
    "Violence",
    "Sexual scenes",
    "Coarse language"
  ]
}
```