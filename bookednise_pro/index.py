import pusher

pusher_client = pusher.Pusher(
  app_id='1796310',
  key='8eb96ce903a8e1cf541f',
  secret='7ddc1ad769cbaa539d19',
  cluster='mt1',
  ssl=True
)



pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})