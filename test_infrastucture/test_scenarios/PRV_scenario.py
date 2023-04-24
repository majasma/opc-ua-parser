from asyncua import ua, Server
from asyncua.common.methods import uamethod
import asyncio
import logging
import time
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
    ts_gas = 14.0
    drain = 0.0

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
    

#--------------------------------------------LARGE RELIEF SCENARIO------------------------------------

    print("PR relief scenario started")
    f = open("test_scenarios/log_files/PRV_scenario.csv", "a")
    prv = 70
    i = 0

    async with server:
        while i < 1.5 * 60:
            lt += 0.1 * prv

            if (lt >= 50): 
                ls = 1
                rp = 1
            else:
                ls = 0

            if (rp == 1):
                lt -= 7

            if i >= 10:
                prv = 0
                ts_gas += 3
            else: 
                prv = random.randint(50, 65)
                ts_gas -= 3


            # end scenario when prv closed and tank is empty
            if (prv == 0 and lt <= 0):
                lt = 0
                rp = 0

                await lt_var.write_value(float(lt))
                await rp_var.write_value(float(rp))
                await ls_var.write_value(float(ls))
                await bdv_var.write_value(float(bdv))
                await prv_var.write_value(float(prv))
                await ts_liquid_var.write_value(float(ts_liquid))
                await ts_gas_var.write_value(float(ts_gas))
                await drain_var.write_value(float(drain))

                print(i, "\t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
                f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 
                break

            # set server values
            await lt_var.write_value(float(round(lt,2)))
            await rp_var.write_value(float(rp))
            await ls_var.write_value(float(ls))
            await bdv_var.write_value(float(bdv))
            await prv_var.write_value(float(prv))
            await ts_liquid_var.write_value(float(ts_liquid))
            await ts_gas_var.write_value(float(ts_gas))
            await drain_var.write_value(float(drain))

            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 

            await asyncio.sleep(2)
            i += 1

        print("Large relief scenario complete")    

    #----------------------------------------------------SMALL RELIEF SCENARIO-----------------------------------------------------------------------------

        print("\n")
        print("Small relief scenario started")
        prv = 30
        i = 0

        while i < 1.5 * 60:
            lt += 0.1 * prv

            if i >= 37:
                prv = 0
            else: 
                prv = random.randint(5, 7)

            if lt >= 10:
                if ts_liquid < 150:
                    ts_liquid += 7
            
            # decrease level in tank when the temperature is high enough
            if ts_liquid > 150:
                lt -= 0.02*ts_liquid

            # operators remove heating when there is no liquid, temp change have high delay
            if lt <= 0:
                ts_liquid -= 11
                lt = 0

            #exit scenario when prv closed, tank empty and temp returned to low
            if prv == 0 and ts_liquid <= 14 and lt <= 0:
                lt = 0

                await lt_var.write_value(float(lt))
                await rp_var.write_value(float(rp))
                await ls_var.write_value(float(ls))
                await bdv_var.write_value(float(bdv))
                await prv_var.write_value(float(prv))
                await ts_liquid_var.write_value(float(ts_liquid))
                await ts_gas_var.write_value(float(random.randint(14,16)))
                await drain_var.write_value(float(drain))

                print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "ts_liquid liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
                f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 
                
                break

            # set server values
            await lt_var.write_value(float(round(lt,2)))
            await rp_var.write_value(float(rp))
            await ls_var.write_value(float(ls))
            await bdv_var.write_value(float(bdv))
            await prv_var.write_value(float(prv))
            await ts_liquid_var.write_value(float(ts_liquid))
            await ts_gas_var.write_value(float(random.randint(14,16)))
            await drain_var.write_value(float(drain))

            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 

            await asyncio.sleep(2)
            i += 1

        print("Small relief scenario complete")
        f.close()
    

    return

if __name__ == "__main__":
    asyncio.run(main())