import json
import os
import psycopg2
import boto3
import pandas as pd
#import s3fs

def lambda_handler(event, context):
   
   client = boto3.client('secretsmanager')
   cjamsdb = client.get_secret_value(SecretId= os.environ.get('db_cred'))
   # s3_path = client.get_secret_value(SecretId='cjams_s3_path')

   dn_cred = json.loads(cjamsdb['SecretString'])
   # s3_loc = json.loads(s3_path['SecretString'])

#establishing the connection
   conn = psycopg2.connect(
          database=dn_cred['dbname'],
          user=dn_cred['username_cjams'],
          password=dn_cred['password_cjams'],
          host=dn_cred['host'],
          port=dn_cred['port']
         )
         

   #sql_query = """select user,usename,query,calls,avgtime_seconds,state from (select  user,usename,query,calls,avgtime_seconds,state,RANK () OVER (ORDER BY avgtime_seconds desc) as rank_time from(SELECT  user,  usename,  query,  state,  count(query) as calls,  avg(state_change - query_start) as avgtime_seconds FROM pg_stat_activity where query !='' and datname ='mdtcjamsdbs' and state in ('idle','active') and (query_start > (now() - interval '30 minutes')) group by user,usename,query,state order by avgtime_seconds desc) as pg_stat) as final where final.rank_time <= 20"""
   sql_query_lr = """select usename,query,state,calls,avgtime_seconds from (select  user,usename,query,state,calls,avgtime_seconds,RANK () OVER (ORDER BY avgtime_seconds desc) as rank_time from(   SELECT  datname,user,  usename,  query,  state,  count(query) as calls, avg(EXTRACT(EPOCH FROM (current_timestamp - query_start))) as avgtime_seconds FROM pg_stat_activity where query !=''  and state in ('active') and datname='mdtcjamsdbs' and (query not like 'SET%' and query not like 'SHOW%' and query not like '%pg_%' and query not like 'START_REPLICATION%') group by datname,user,usename,query,state order by avgtime_seconds desc) as pg_stat) as final where final.usename not like 'rds%' and final.avgtime_seconds>=5 order by avgtime_seconds desc"""

   sql_query_conn = """with t1 as (select count(*) as total_count from pg_stat_activity where state in ('idle','active') and usename not like '%rds%') select usename,state,client_addr,count(*) as count,t1.total_count FROM pg_stat_activity a,t1 where 1=1 and state in ('idle','active') and usename not like '%rds%' group by usename,state,t1.total_count,client_addr  order by count desc"""
        
#Creating a cursor object using the cursor() method
   cursor = conn.cursor()

#Executing an sql function using the execute() method
   cursor.execute(sql_query_lr)

# Fetch a single row using fetchone() method.
   data = cursor.fetchall()
   
   row_count = len(data)

# Writing it to data frame and saving it in s3 bucket
   df = pd.DataFrame(data,columns=['usename','query','state','calls','avgtime_seconds'])
   #df.to_csv(s3_loc['cjams_s3_path'], index=False, header=True)
   #table = df.to_html(buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None, index_names=True, justify=None, max_rows=None, max_cols=None, show_dimensions=False, decimal='.', bold_rows=True, classes=None, escape=True, notebook=False, border=None, table_id=None, render_links=False, encoding=None)
#Creating a cursor object using the cursor() method
   cursor = conn.cursor()   
   
#Executing an sql function using the execute() method
   cursor.execute(sql_query_conn)   
   
   data1 = cursor.fetchall()
   
   df1 = pd.DataFrame(data1,columns=['usename','state','client_addr','count','total_count'])
   
   table = df.to_html(header="true", table_id="table").replace('<th>', '<th align="left">')
   
   table1 = df1.to_html(header="true", table_id="table").replace('<th>', '<th align="left">')
   
   #html = '<html> <body> <h2>CJAMS Top 20 Long Running Queries</h2> <table>' + table + '</table> </body> </html>' + '<html> <body> <h2>CJAMS Prod Connections</h2> <table>' + table1 + '</table> </body> </html>'
   html = '<html> <body> <h2>CJAMS Top 20 Long Running Queries (>5 Secs)</h2>' + table + '<h2>CJAMS Prod Connections</h2>' + table1 + '</body> </html>'
   
   print (html)
   
   return {'result': html,'result1': row_count}
   
