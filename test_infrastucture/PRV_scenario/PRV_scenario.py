from asyncua import ua, Server
from asyncua.common.methods import uamethod
import asyncio
import logging
import time
import random

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

# Set the seed for the random number generator
random.seed(42)
# Generate an array of 300 values ranging between 50 and 65
PRV1_array = [random.uniform(40, 55) for _ in range(300)]
PRV2_array = [random.uniform(3, 5) for _ in range(300)]
temp1_array = [random.uniform(23, 26) for _ in range(300)]
temp2_array = [random.uniform(22, 25) for _ in range(300)]

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
    ts_liquid = 23.0
    ts_gas = 23.0
    drain = 0.0

    # create variables
    lt_var = await node.add_variable(idx, "Level Transmitter", 0.0)
    rp_var = await node.add_variable(idx, "Return Pumps", 0.0)
    ls_var = await node.add_variable(idx, "Level Switch", 0.0)
    bdv_var = await node.add_variable(idx, "BDV", 0.0)
    prv_var = await node.add_variable(idx, "PRV", 0.0)
    drain_var = await node.add_variable(idx, "Drain Valve", 0.0)
    ts_liquid_var = await node.add_variable(idx, "Temperature liquids", 23.0)
    ts_gas_var = await node.add_variable(idx, "Temperature gas", 23.0)


    print("Server started at {}".format(url))
    _logger.info("starting server...")
    

#--------------------------------------------LARGE RELIEF SCENARIO------------------------------------

    print("PR relief scenario started")
    f = open("./test_infrastucture/log_files/PRV_scenario_Level1.csv", "a")
    prv = 70
    i = 0

    async with server:
        while i < 1.5 * 60:
            
            if (rp == 1):
                lt -= 2
            
            lt += 0.1 * prv

            if (lt >= 10): 
                ls = 1
                rp = 1
            else:
                ls = 0

            if i >= 10:
                prv = 0
                ts_gas += 3
            else: 
                prv = PRV1_array[i]
                ts_gas -= 3

            if ts_gas >= 23:
                ts_gas = temp2_array[i]

            if lt <= 0:
                lt = 0
                rp = 0


            # end scenario when prv closed and tank is empty
            if (prv == 0 and lt <= 0 and i > 30):
                lt = 0
                rp = 0

                await lt_var.write_value(float(lt))
                await rp_var.write_value(float(rp))
                await ls_var.write_value(float(ls))
                await bdv_var.write_value(float(bdv))
                await prv_var.write_value(round(float(prv),2))
                await ts_liquid_var.write_value(round(float(temp1_array[i]),2))
                await ts_gas_var.write_value(float(ts_gas))
                await drain_var.write_value(float(drain))

                print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
                f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(float(temp1_array[i]),2)) + ", " + repr(round(float(temp2_array[i]),2)) + ", "+ repr(drain) +'\n') 
                break

            # set server values
            await lt_var.write_value(round(float(lt),2))
            await rp_var.write_value(float(rp))
            await ls_var.write_value(float(ls))
            await bdv_var.write_value(float(bdv))
            await prv_var.write_value(round(float(prv),2))
            await ts_liquid_var.write_value(round(float(temp1_array[i]),2))
            await ts_gas_var.write_value(float(ts_gas))
            await drain_var.write_value(float(drain))

            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(float(temp1_array[i]),2)) + ", " + repr(round(float(temp2_array[i]),2)) + ", "+ repr(drain) +'\n') 

            #await asyncio.sleep(2)
            i += 1

        print("Large relief scenario complete")    

    #----------------------------------------------------SMALL RELIEF SCENARIO-----------------------------------------------------------------------------

        print("\n")
        print("Small relief scenario started")
        prv = 30
        i = 0

        while i < 1.5 * 60:
            
            if (rp == 1):
                lt -= 2
            
            lt += 0.1 * prv

            if i >= 26:
                prv = 0
            else: 
                prv = PRV2_array[i]

            if lt >= 10:
                ls = 1
                rp = 1
            else:
                ls = 0

            if lt <= 0:
                lt = 0
                if prv == 0:
                    rp = 0

            #exit scenario when prv closed, tank empty and temp returned to low
            if prv == 0 and lt <= 0 and i > 30:
                lt = 0

                await lt_var.write_value(float(lt))
                await rp_var.write_value(float(rp))
                await ls_var.write_value(float(ls))
                await bdv_var.write_value(float(bdv))
                await prv_var.write_value(float(prv))
                await ts_liquid_var.write_value(float(ts_liquid))
                await ts_gas_var.write_value(float(ts_gas))
                await drain_var.write_value(float(drain))

                print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "ts_liquid liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
                f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(float(temp1_array[i]),2)) + ", " + repr(round(float(temp2_array[i]),2)) + ", "+ repr(drain) +'\n') 
                
                break
            

            # set server values
            await lt_var.write_value(round(float(lt),2))
            await rp_var.write_value(float(rp))
            await ls_var.write_value(float(ls))
            await bdv_var.write_value(float(bdv))
            await prv_var.write_value(round(float(prv),2))
            await ts_liquid_var.write_value(round(float(temp1_array[i]),2))
            await ts_gas_var.write_value(round(float(temp2_array[i]),2))
            await drain_var.write_value(float(drain))

            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(float(temp1_array[i]),2)) + ", " + repr(round(float(temp2_array[i]),2)) + ", "+ repr(drain) +'\n') 

            #await asyncio.sleep(2)
            i += 1

        print("Small relief scenario complete")
        f.close()
    

    return

if __name__ == "__main__":
    asyncio.run(main())