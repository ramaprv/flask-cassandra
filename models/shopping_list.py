import uuid
from cqlengine import columns
from cqlengine.models import Model


class Shopping_List(Model):
  id = columns.UUID(primary_key=True, default=uuid.uuid4)
  user_id = columns.Integer(index=True)
  item = columns.Text()
  quantity = columns.Integer()
#  created_at = columns.DateTime(default=datetime.now())

  def __repr__(self):
    return '%d %s %d' % (self.user_id, self.item, self.quantity)
