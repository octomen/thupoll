import datetime
import json

from thupoll.models import _BaseModel
from thupoll.utils import CustomJSONEncoder


def marshall(obj: _BaseModel):
    return json.loads(json.dumps(obj.marshall(), cls=CustomJSONEncoder))


def get_future_datetime(delta=30):
    return datetime.datetime.now() + datetime.timedelta(days=delta)


def get_past_datetime(delta=30):
    return datetime.datetime.now() - datetime.timedelta(days=delta)
