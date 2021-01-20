import config as cfg

def validateApiKey(key):
    if key  != cfg.apiKey:
        raise Exception('Invalid API Key')