bq mk replicacion_cdc

bq mk --table replicacion_cdc.CatLineasAereas \
__$start_lsn:BYTES,__$end_lsn:BYTES,__$seqval:BYTES,__$operation:INTEGER,__$update_mask:BYTES, \
Code:STRING, Linea_Aerea:STRING

bq mk --table replicacion_cdc.Pasajeros \
__$start_lsn:BYTES,__$end_lsn:BYTES,__$seqval:BYTES,__$operation:INTEGER,__$update_mask:BYTES, \
ID_Pasajero:INTEGER, Pasajero:STRING, Edad:INTEGER


bq mk --table replicacion_cdc.Vuelos \
__$start_lsn:BYTES,__$end_lsn:BYTES,__$seqval:BYTES,__$operation:INTEGER,__$update_mask:BYTES, \
Sucursal:INTEGER, Cve_LA:STRING, Viaje:DATE, Clase:STRING, Precio:INTEGER, Ruta:STRING, Cve_Cliente:INTEGER
