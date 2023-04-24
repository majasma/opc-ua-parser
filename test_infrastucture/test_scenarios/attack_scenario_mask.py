from asyncua import ua, Server
from asyncua.common.methods import uamethod
import asyncio
import logging
import time
import numpy as np
import random

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

async def main():
    #--------------------------------------INIT--------------------------------------------
    # create server
    server = Server()
    await server.init()
    url = "opc.tcp://localhost:4840/"
    server.set_endpoint(url)
    server.set_server_name("Flare OPC UA Tester")
    idx = await server.register_namespace("flare_system")

    # create node for temperature
    node = await server.nodes.objects.add_object(idx, "PLC")

    #,  varianttype=ua.VariantType.Float

    lt = 0.0
    rp = 0.0
    ls = 0.0
    bdv = 0.0
    prv = 0.0
    ts_liquid = 14.0
    ts_gas = 14.0
    drain = 0.0

    # create variables
    lt_var = await node.add_variable(idx, "Level Transmitter", lt)
    rp_var = await node.add_variable(idx, "Return Pumps", rp)
    ls_var = await node.add_variable(idx, "Level Switch", ls)
    bdv_var = await node.add_variable(idx, "BDV", bdv)
    prv_var = await node.add_variable(idx, "PRV", prv)
    drain_var = await node.add_variable(idx, "Drain Valve", drain)
    ts_liquid_var = await node.add_variable(idx, "Temperature liquids", ts_liquid)
    ts_gas_var = await node.add_variable(idx, "Temperature gas", ts_gas)


    print("Server started at {}".format(url))
    _logger.info("starting server...")
    

#--------------------------------------------SCENARIO START------------------------------------

    print("Masked attack scenario started")
    f = open("./test_infrastructure/log_files/attack_masked_scenario.csv", "a")
    bdv = 1
    i = 0

    # Generate a array of values following a sine curve
    x = np.linspace(0, 300, 299)
    y = 2 * np.sin(1 * np.pi * 2 * x / 300)
    sine_arr = (y + 2) * 4 / 4

    async with server:
        while i <= 2.5*60:
            rp = 0
            
            if i > 60 and i < 124:
                prv = random.randint(2,3)
                lt = sine_arr[i]

            
            if i > 70 and lt != 0:
                rp = 1
                lt -= 1

            await lt_var.write_value(float(lt))
            await rp_var.write_value(float(rp))
            await ls_var.write_value(float(ls))
            await bdv_var.write_value(float(bdv))
            await prv_var.write_value(float(prv))
            await ts_liquid_var.write_value(float(random.randint(14,16)))
            await ts_gas_var.write_value(float(random.randint(14,16)))
            await drain_var.write_value(float(drain))

            print(i, "\t", "lt: ", float(lt), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 

            await asyncio.sleep(3) 
            i += 1

        print("Masked attack scenario complete") 
        f.close() 
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())