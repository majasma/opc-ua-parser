#Simple Python OPC-UA Client
#code repository at https://github.com/techbeast-org/opc-ua
#LGPL-3.0 License

import asyncio
import logging
from asyncua import Client, Node, ua
logger = logging.getLogger('asyncua')
logging.disable(logging.WARNING)

#sjekk opp om rekkefølgen er irrelevant

data_variables_2 = ["PRV", "Drain Valve", "Temperature liquids", "Temperature gas" ]
data_variables_1 = ["Level Transmitter","Return Pumps","Level Switch", "BDV"]


async def dict_format(keys, values):
  return dict(zip(keys, values))

async def main():
    while True:
        url = "opc.tcp://localhost:4840/"
        async with Client(url=url) as client:
            data_list = []
            namespace = "flare_system_1"
            idx = await client.get_namespace_index(namespace)
            for i in range(len(data_variables_1)):
                myvar = await client.nodes.root.get_child(["0:Objects", "{}:Sensor-group-1".format(idx), "{}:{}".format(idx,data_variables_1[i])])
                val = await myvar.get_value()
                data_list.append(val)
            # _list = data_list
            print(await dict_format(data_variables_1,data_list))
    
        
        url2 ="opc.tcp://localhost:4841/"
        async with Client(url=url2) as client:
            data_list = []
            namespace = "flare_system_2"
            idx = await client.get_namespace_index(namespace)
            for i in range(len(data_variables_2)):
                myvar = await client.nodes.root.get_child(["0:Objects", "{}:Sensor-group-2".format(idx), "{}:{}".format(idx,data_variables_2[i])])
                val = await myvar.get_value()
                data_list.append(val)
            # _list = data_list
            print(await dict_format(data_variables_2,data_list))
            
            await asyncio.sleep(2)

if __name__ == '__main__':
    asyncio.run(main())