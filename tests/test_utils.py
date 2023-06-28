import os
import json



def load_all_conversations(path_to_conversations):
    conversations = []
    files_names = os.listdir(path_to_conversations)
    files_names.sort()
    for f in files_names:
        file_d = open(f"{path_to_conversations}/{f}", 'r')
        text = file_d.read()
        jsn = json.loads(text)
        conversations.append(jsn)
        file_d.close()

    return conversations


def dict_to_json(dct, json_filename):
    r = json.dumps(dct)
    loaded_r = json.loads(r)
    with open(f"tests_results/{json_filename}.json", "w", encoding='utf-8') as file:
        json.dump(loaded_r, file, ensure_ascii=False, indent=4)