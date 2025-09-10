from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi import getCmd, CommunityData, UdpTransportTarget, ContextData
from pysnmp.smi.rfc1902 import ObjectType, ObjectIdentity

iterator = getCmd(
  SnmpEngine(),
  CommunityData( "public" ),
  UdpTransportTarget( ("demo.snmplabs.com", 161), timeout = 10, retries = 1 ),
  ContextData(),
  ObjectType( ObjectIdentity( "SNMPv2-MIB", "sysDescr", 0 ) ) )

errorIndication, errorStatus, errorIndex, varBinds = next( iterator )

if errorIndication:  # SNMP engine errors
  print( errorIndication )
else:
  if errorStatus:  # SNMP agent errors
    print( "%s at %s" % (errorStatus.prettyPrint(), varBinds[int( errorIndex ) - 1] if errorIndex else '?') )
  else:
    for varBind in varBinds:  # SNMP response contents
      print( " = ".join( [x.prettyPrint() for x in varBind] ) )
