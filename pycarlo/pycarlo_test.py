
from pycarlo.core import Client, Query, Mutation, Session

mcdId="<key>"
mcdToken="<secret_key>"

client=Client(session=Session(mcd_id=mcdId,mcd_token=mcdToken))

#initialize query object
query = Query()

#query get user function
query.get_user.__fields__('email')
print(client(query).get_user.email)


#initialize arguments for create_or_update_domain function 
namevar="pycarlo_test" #Name for the domain
mcon_list=["<MCON_ID>"] #List of mcon values associated with tables to include in the Domain
tag_dict={"name": " ", "value": " " } #Dict of tag name/value pairs to include in the Domain
existing_domain_uuid= "" #Include if updating an existing domain

#initialize mutation object
mutation=Mutation()

#apply mutation operation and call the create_or_update_domain function to create a domain
mutation.create_or_update_domain(name=namevar,assignments=mcon_list).domain.__fields__("name","uuid")
print(client(mutation).create_or_update_domain)

# the query object is already initialzed, so we can call functions using the same query object
query.get_table(dw_id="<dwId>", full_table_id="<full_table_id>").__fields__("mcon", "full_table_id", "discovered_time", "description")
print(client(query).get_table)

# If necessary, you can always generate (e.g. print) the raw query that would be executed.
print(query) #output below
# query {
#   getTable(dwId: "<>", fullTableId: <>") {
#     mcon
#     fullTableId
#     discoveredTime
#     description
#  }


# initialize arguments to create rule/monitor
warehouse="<dw_id>"
comp = {
    "comparisons": [
        {
            "comparison_type": "THRESHOLD",
            "operator": "GT",
            "threshold": 0
        }
    ]
}
s_config = {
    "interval_minutes": 120,
    "start_time": "2023-05-25T18:57:27+00:00",
    "schedule_type": "FIXED"
}
sql = "select distinct user_id from merakidw.fact.ga4_events_dashboard_web where import_date = current_date-1"
name = "pycarlo_check"
time = "UTC"

#call create_or_update_custom_metric_rule function 
mutation.create_or_update_custom_metric_rule(
    dw_id=warehouse,
    comparisons=comp["comparisons"],
    custom_sql=sql,
    description=name,
    schedule_config=s_config,
    timezone=time
).custom_rule.__fields__("uuid")

print(client(mutation).create_or_update_custom_metric_rule)



# If you are not a fan of sgqlc operations (Query and Mutation) you can also execute any raw query using the client.
# For instance, if we want the first 10 tables from getTables.
get_table_query = """
query getTables{
  getTables(first: 10) {
    edges {
      node {
        fullTableId
      }
    }
  }
}
"""
response = client(get_table_query)
# This returns a Box object where fields can be accessed using dot notation. 
# Notice how unlike with the API the response uses the more Pythonic snake_case.
for edge in response.get_tables.edges:
  print(edge.node.full_table_id)
# The response can still be processed as a standard dictionary.
print(response['get_tables']['edges'][0]['node']['full_table_id'])
#output
# merakidw:fact.lt_dashboard_pageviews_file_history
# merakidw:fact.lt_network_health_connectivity_events_file_history
# merakidw:fact.store_orders
# merakidw:fact.edi_orders
# merakidw:fact.counter_history_hr
# merakidw:fact.lt_network_health_connectivity_events
# merakidw:fact.lt_route_stats
# merakidw:fact.lt_network_health_client_packet_latency_file_history
# merakidw:fact.lt_performance_score_history_file_history
# merakidw:fact.free_trials
# merakidw:fact.lt_dashboard_pageviews_file_history




# # You can also execute any mutations too. For instance, generateCollectorTemplate (selecting the templateLaunchUrl).
# mutation = Mutation()
# mutation.generate_collector_template().dc.template_launch_url()
# print(client(mutation))

# # Any errors will raise a GqlError with details. For instance, executing above with an invalid region.
# mutation = Mutation()
# mutation.generate_collector_template(region='artemis')
# print(client(mutation))
# # pycarlo.common.errors.GqlError: [{'message': 'Region "\'artemis\'" not currently active.'...]

