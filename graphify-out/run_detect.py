import json
from pathlib import Path
from graphify.detect import detect

result = detect(Path('.'))
print(json.dumps(result, ensure_ascii=False))
