CREATE KEYSPACE shop WITH REPLICATION = { 'class' : 'SimpleShop', 'replication_factor' : 1 };
USE shop;

CREATE TABLE shopping_list (
  user_id text,
  created_at timeuuid,
  item text,
  quantity float,
  PRIMARY KEY(user_id)
);
