import json
import pandas as pd


def create_csv(file, header):
    with open(file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    df = pd.DataFrame(data, columns=header)
    file_name = file[:len(file) - 4] + "csv"
    df.to_csv(file_name, sep='\t', encoding='utf-8')


if __name__ == '__main__':
    create_csv("sources/result_hb.json", ["item_name", "item_url", "item_phones_list", "item_address", "item_site"])
    create_csv("sources/result_vl.json", ["item_name", "item_url", "item_phones_list", "item_address", "item_site"])
    create_csv("sources_dvhub/result_hb.json",
               ["item_name", "item_url", "item_email", "item_phone", "item_address", "item_site"])
    create_csv("sources_dvhub/result_vl.json",
               ["item_name", "item_url", "item_email", "item_phone", "item_address", "item_site"])
