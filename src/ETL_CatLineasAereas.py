import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions



class TransformCatLineasAereas(beam.DoFn):
    def process(self, element):
        yield {
            '__$start_lsn': element['__$start_lsn'],
            '__$end_lsn': element.get('__$end_lsn', None),
            '__$seqval': element['__$seqval'],
            '__$operation': element['__$operation'],
            '__$update_mask': element['__$update_mask'],
            'Code': element['Code'],
            'Linea_Aerea': element['Linea_Aerea']
        }

def run():
    options = PipelineOptions(streaming=True)
    connection_central = 'jdbc:sqlserver://localhost:1433;databaseName=Central'

    with beam.Pipeline(options=options) as pipeline:
        (pipeline
         | 'ReadFromSQLServer' >> beam.io.ReadFromJdbc(
                table_name='cdc.dbo_CatLineasAereas_CT',
                jdbc_url=connection_central,
                driver_class_name='com.microsoft.sqlserver.jdbc.SQLServerDriver',
                username='sa',
                password='mypass192837465!'
          )
         | 'TransformData' >> beam.ParDo(TransformCatLineasAereas())
         | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
                table='replicacion_cdc.CatLineasAereas',
                create_disposition='CREATE_IF_NEEDED',
                write_disposition='WRITE_APPEND'))

if __name__ == '__main__':
    run()