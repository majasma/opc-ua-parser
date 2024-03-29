
from asyncua import ua, Server
from asyncua.common.methods import uamethod
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

# Set the seed for the random number generator
random.seed(42)
# Generate an array of 300 values ranging between 50 and 65
temp1_array = [random.uniform(23, 26) for _ in range(300)]
temp2_array = [random.uniform(22, 25) for _ in range(300)]
bdv_arr = [random.uniform(6, 8) for _ in range(300)]
temp_vol_array = [random.uniform(1, 2) for _ in range(300)]

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
    f = open("test_infrastucture/log_files/attack_real_scenario_Level1.csv", "a")
    i = 0
   
    async with server:
        while i < 80:

            if i < 30:
                ts_gas = temp1_array[i]

            if i > 30:
                bdv = 1
                lt += bdv_arr[i]
                ts_gas =- temp_vol_array[i]

            if lt > 100:
                lt = 100

            if (lt >= 10): 
                ls = 1
            else:
                ls = 0

            if ts_gas <= -25:
                ts_gas = -temp1_array[i]

            ts_liquid = temp2_array[i]
            

            await lt_var.write_value(round(float(lt),2))
            await rp_var.write_value(float(0))
            await ls_var.write_value(float(ls))
            await bdv_var.write_value(float(0))
            await prv_var.write_value(float(0))
            await ts_liquid_var.write_value(float(ts_liquid))
            await ts_gas_var.write_value(float(ts_gas))
            await drain_var.write_value(float(0))


            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "bdv: ", bdv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 

            #await asyncio.sleep(2) 
            i += 1

        print("Unmasked attack scenario complete") 
        f.close() 
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())