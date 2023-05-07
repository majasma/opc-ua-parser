
from asyncua import ua, Server
from asyncua.common.methods import uamethod
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

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
    f = open("../log_files/BDV_scenario_Level0_2.csv", "a")

    bdv = 1
    i = 0

    async with server_2:
        while i < 2.5 * 60:
            lt += 4 * bdv
            ts_gas -= 5 * bdv

            if (lt >= 50): 
                ls = 1
                drain = 1
            else:
                ls = 0

            if (drain == 1):
                lt -= 7

            ts_gas = random.randint(14,16)
            ts_liquid = random.randint(14,16)

            if i >= 20:
                bdv = 0

                if ts_gas < 14:
                    ts_gas += 3
            

            
            # end scenario when prv closed and tank is empty
            if (bdv == 0 and lt <= 0):
                lt = 0
                drain = 0
                print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)

                await lt_var.write_value(float(lt))
                await rp_var.write_value(float(rp))
                await ls_var.write_value(float(ls))
                await bdv_var.write_value(float(bdv))

                
                f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv)  +'\n') 
                break
            
            
            # set server values
            await lt_var.write_value(round(float(lt),2))
            await rp_var.write_value(float(rp))
            await ls_var.write_value(float(ls))
            await bdv_var.write_value(float(bdv))


            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv)  +'\n') 

            await asyncio.sleep(2)
            i += 1

    print("BD relief Level 0 scenario complete")  
    await server_2.stop()
    f.close()

if __name__ == "__main__":
    asyncio.run(main())