"""
pip install pysnmp
"""
from pysnmp import hlapi
from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi import ContextData, UsmUserData, CommunityData

target_host = "127.0.0.1"
community = "fcut"


def construct_object_types( list_of_oids ):
  object_types = []
  for oid in list_of_oids:
    object_types.append( hlapi.ObjectType( hlapi.ObjectIdentity( oid ) ) )
  return object_types


def cast( value ):
  try:
    return int( value )
  except (ValueError, TypeError):
    try:
      return float( value )
    except (ValueError, TypeError):
      try:
        return str( value )
      except (ValueError, TypeError):
        pass
  return value


def fetch( handler, count ):
  result = []
  for _ in range( count ):
    try:
      error_indication, error_status, error_index, var_binds = next( handler )
      if not error_indication and not error_status:
        items = {}
        for var_bind in var_binds:
          items[str( var_bind[0] )] = cast( var_bind[1] )
        result.append( items )
      else:
        raise RuntimeError( 'Got SNMP error: {0}'.format( error_indication ) )
    except StopIteration:
      break
  return result


def get( target: str, oids: list, credentials: CommunityData | UsmUserData, port: int = 161, engine: SnmpEngine = SnmpEngine(), context: ContextData = ContextData() ):
  handler = hlapi.getCmd(
    engine,
    credentials,
    hlapi.UdpTransportTarget( (target, port) ),
    context,
    *construct_object_types( oids )
  )
  return fetch( handler, 1 )[0]


if __name__ == '__main__':
  print( get( target_host, ['1.3.6.1.2.1.1.5.0'], hlapi.CommunityData( community ) ) )
