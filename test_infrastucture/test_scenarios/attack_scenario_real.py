
from asyncua import ua, Server
from asyncua.common.methods import uamethod
import asyncio
import logging
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

    lt = 0.0
    rp = 0.0
    ls = 0
    bdv = 0
    prv = 0.0
    ts_liquid = 14.0
    ts_gas = 0.0
    drain = 0

    # create variables
    lt_var = await node.add_variable(idx, "Level Transmitter", 0.0)
    rp_var = await node.add_variable(idx, "Return Pumps", 0.0)
    ls_var = await node.add_variable(idx, "Level Switch", 0.0)
    bdv_var = await node.add_variable(idx, "BDV", 0.0)
    prv_var = await node.add_variable(idx, "PRV", 0.0)
    drain_var = await node.add_variable(idx, "Drain Valve", 0.0)
    ts_liquid_var = await node.add_variable(idx, "Temperature liquids", 14.0)
    ts_gas_var = await node.add_variable(idx, "Temperature gas", 14.0)


    print("Server started at {}".format(url))
    _logger.info("starting server...")
    

#--------------------------------------------SCENARIO START------------------------------------
    print("Unmasked attack scenario started")
    f = open("test_scenarios/log_files/attack_real_scenario.csv", "a")
    bdv = 1
    i = 0
   
    async with server:
        while i < 2.5 * 60:

            if i > 30:
                lt += 4 * bdv

            if i > 40 and i < 120:
                ts_gas =- 5
            
            if lt > 100:
                lt = 100

            if (lt >= 50): 
                ls = 1
            else:
                ls = 0

            ts_gas = random.randint(14,16)
            ts_liquid = random.randint(14,16)
            

            await lt_var.write_value(float(lt))
            await rp_var.write_value(float(0))
            await ls_var.write_value(float(ls))
            await bdv_var.write_value(float(0))
            await prv_var.write_value(float(0))
            await ts_liquid_var.write_value(float(ts_liquid))
            await ts_gas_var.write_value(float(ts_gas))
            await drain_var.write_value(float(0))


            print(i, "\t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 

            await asyncio.sleep(2) 
            i += 1

        print("Unmasked attack scenario complete") 
        f.close() 
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())