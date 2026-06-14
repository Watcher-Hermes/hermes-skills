# Producer
def emit(stream: str, event: dict):
    r.xadd(stream, event, maxlen=10000)  # Cap stream length