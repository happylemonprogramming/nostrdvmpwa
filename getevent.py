from pynostr.relay import Relay
from pynostr.filters import FiltersList, Filters
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool
from pynostr.event import EventKind
import tornado.ioloop
from tornado import gen
import uuid
import json

def getevent(ids=None, kinds=None, authors=None, since=None, until=None, event_refs=None, pubkey_refs=None, limit=None):
    message_pool = MessagePool(first_response_only=False)
    policy = RelayPolicy()
    io_loop = tornado.ioloop.IOLoop.current()
    r = Relay(
        "wss://relay.damus.io",
        message_pool,
        io_loop,
        policy,
        timeout=2
    )

    event_list = []
    filter = FiltersList([Filters(ids=ids, kinds=kinds, authors=authors, since=since, until=until, event_refs=event_refs, pubkey_refs=pubkey_refs, limit=limit)])

    subscription_id = uuid.uuid1().hex
    r.add_subscription(subscription_id, filter)

    try:
        io_loop.run_sync(r.connect)
    except gen.Return:
        pass
    # io_loop.stop()

    while message_pool.has_notices():
        notice_msg = message_pool.get_notice()
        print(notice_msg.content)
    while message_pool.has_events():
        event_msg = message_pool.get_event()
        event = json.loads(str(event_msg.event))
        event_list.append(event)

    return event_list

if __name__ == "__main__":
    from pynostr.key import PublicKey
    # # note = "note1gn882ya9mc5c6f8xyndzvznsg3sxsp06ht6rj5lqfktdgefnaxjq2pm8w2"
    # note = 'note1mhd4jhd7gskczleapg8fxmmv8fvt69yukw93znjeqflwhx4c5qlss3gkwh'
    # note = 'npub1hee433872q2gen90cqh2ypwcq9z7y5ugn23etrd2l2rrwpruss8qwmrsv6'
    # notehex = PublicKey.from_npub(note).hex()
    # # notehex = '4ef5f373012e7ada9838fcce0282d93cd14b49c95c5fc62a41365ea6874d03fd'
    # # bech32 = PublicKey.from_hex(notehex).bech32()
    # # print(bech32)
    # # notehex = PublicKey.from_npub(bech32).hex()
    # print(notehex,type(notehex))
    # event = getevent(authors=[notehex])
    # print(event)
    # video = event[0][1]['tags'][1][1]
    # print(video)
    # note = 'note1jcat6pztsjyslcg8mrhzjfgeks9y64lc75y74qhdwqqfcs2f0ptqd0yn98'
    # from pynostr.key import PublicKey
    # notehex = PublicKey.from_npub(note).hex()
    # event = getevent(ids=[notehex])
    # print(event)
    # Loop
    # import time
    # since = round(time.time())
    # while True:
    #     pubkey = 'npub1hee433872q2gen90cqh2ypwcq9z7y5ugn23etrd2l2rrwpruss8qwmrsv6'
    #     pubhex = PublicKey.from_npub(pubkey).hex()
    #     event = getevent(kinds=[1],pubkey_refs=[pubhex])
    #     print(event[0], len(event))
    #     time.sleep(1)
    #     print('nothing...')
    #     if len(event) > 6:
    #         print('yay')
    #         break
    import json
    # pubkey = 'npub1nxa4tywfz9nqp7z9zp7nr7d4nchhclsf58lcqt5y782rmf2hefjquaa6q8'
    # pubhex = PublicKey.from_npub(pubkey).hex()
    events = getevent(kinds=[6100])
    i = 0
    for event in events:
        i+=1
        # Get prompt
        for tag in event[1]['tags']:
            if tag[0] == 'i':
                prompt = tag[1]
        if 'http' in event[1]['content']:
            print(f'PROMPT #{i}:', prompt)
            print(f'IMAGE LINK #{i}:', event[1]['content'])
        

'''
if someone @'s npub with language selection, then offer invoice
[detect reference to npub with pubkey_ref, then have bot ]
if invoice is paid then offer translated content
'''