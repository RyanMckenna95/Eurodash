from eurostatapiclient import EurostatAPIClient

VERSION = 'v2.1'

FORMAT = 'json'

LANGUAGE = 'en'

client = EurostatAPIClient(VERSION, FORMAT, LANGUAGE)  # tps00001
dataset = client.get_dataset('tps00010')

df = dataset.to_dataframe()


# print(df.head())

def popAgeGroup():
    dataset = client.get_dataset('tps00010')
    popage = dataset.to_dataframe()

    return popage


