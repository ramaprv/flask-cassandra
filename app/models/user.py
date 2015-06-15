import uuid
import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class User(Model):
  id = columns.UUID(primary_key=True, default=uuid.uuid4)
  handle = columns.Text(index=True)
  password = columns.Text(required=True)
  email = columns.Text(required=False)
  phone = columns.Integer(required=False)
  created_at = columns.DateTime(default=datetime.datetime.now)

  def __repr__(self):
    return '%s %s %d' % (self.handle, self.email, self.phone)
