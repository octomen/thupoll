import json

from thupoll.models import _BaseModel
from thupoll.utils import CustomJSONEncoder


def marshall(obj: _BaseModel):
    return json.loads(json.dumps(obj.marshall(), cls=CustomJSONEncoder))
