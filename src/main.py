import json
from steam_data.combined_data import CombinedSteamDataSource

lang = 'english'
app_id = 1174180
ds = CombinedSteamDataSource()
data = ds.get_data(app_id, lang=lang)

if data:
    # save data to json
    with open(f'data_{app_id}_{lang}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
else:
    print("No data found")