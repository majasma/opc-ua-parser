
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
temp1_array = [random.uniform(14, 16) for _ in range(300)]
temp2_array = [random.uniform(14, 16) for _ in range(300)]

async def main(): 

    server_2 = Server()
    await server_2.init()
    url = "opc.tcp://localhost:4841/"
    server_2.set_endpoint(url)
    server_2.set_server_name("Flare OPC UA Tester 2")
    idx_2 = await server_2.register_namespace("flare_system_2")
    node_2 = await server_2.nodes.objects.add_object(idx_2, "Sensor-group-2")

    lt = 0.0
    rp = 0.0
    ls = 0.0
    bdv = 0.0
    prv = 0.0
    ts_liquid = 14.0
    ts_gas = 0.0
    drain = 0.0

    lt_var = await node_2.add_variable(idx_2, "Level Transmitter", lt)
    rp_var = await node_2.add_variable(idx_2, "Return Pumps", rp)
    ls_var = await node_2.add_variable(idx_2, "Level Switch", ls)
    bdv_var = await node_2.add_variable(idx_2, "BDV", bdv)

    print("Started server 2 - Containing sensors LT, RP, LS and BDV")
    f = open("../log_files/attack_scenario_Level0_2.csv", "a")
    bdv = 1
    i = 0
   
    async with server_2:
        print("Attack Level 0 scenario started..")
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

            ts_gas = temp1_array[i]
            ts_liquid = temp2_array[i]
            
            await lt_var.write_value(round(float(lt),2))
            await rp_var.write_value(float(0))
            await ls_var.write_value(float(ls))
            await bdv_var.write_value(float(0))


            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv)  +'\n') 

            await asyncio.sleep(2) 
            i += 1

    print("Attack Level 0 scenario complete")    
    await server_2.stop()

if __name__ == "__main__":
    asyncio.run(main())