import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

class TransformPasajeros(beam.DoFn):
    def process(self, element):
        yield {
            '__$start_lsn': element['__$start_lsn'],
            '__$end_lsn': element.get('__$end_lsn', None),
            '__$seqval': element['__$seqval'],
            '__$operation': element['__$operation'],
            '__$update_mask': element['__$update_mask'],
            'ID_Pasajero': element['ID_Pasajero'],
            'Pasajero': element['Pasajero'],
            'Edad': element['Edad']
        }

def read_from_sql_server(pipeline, connection_url, table_name):
    return (pipeline
            | f'ReadFromSQLServer_{table_name}' >> beam.io.ReadFromJdbc(
                    table_name=table_name,
                    jdbc_url=connection_url,
                    driver_class_name='com.microsoft.sqlserver.jdbc.SQLServerDriver',
                    username='sa',
                    password='mypass192837465!'
                    ))

def run():
    options = PipelineOptions(streaming=True)

    connection_sucursal1 = 'jdbc:sqlserver://localhost:1434;databaseName=Sucursal1'
    connection_sucursal2 = 'jdbc:sqlserver://localhost:1435;databaseName=Sucursal2'

    with beam.Pipeline(options=options) as pipeline:
        # Read and merge data from both Sucursal1 and Sucursal2
        sucursal1_data = read_from_sql_server(pipeline, connection_sucursal1, 'cdc.dbo_Pasajeros_CT')
        sucursal2_data = read_from_sql_server(pipeline, connection_sucursal2, 'cdc.dbo_Pasajeros_CT')

        merged_data = ((sucursal1_data, sucursal2_data)
                       | 'MergeSucursales' >> beam.Flatten())

        # Transform and write data to BigQuery
        (merged_data
         | 'TransformData' >> beam.ParDo(TransformPasajeros())
         | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
                table='replicacion_cdc.Pasajeros',
                create_disposition='CREATE_IF_NEEDED',
                write_disposition='WRITE_APPEND'))

if __name__ == '__main__':
    run()