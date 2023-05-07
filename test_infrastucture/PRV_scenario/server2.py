
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
PRV1_array = [random.uniform(50, 65) for _ in range(300)]
PRV2_array = [random.uniform(5, 7) for _ in range(300)]

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
    f = open("../log_files/PRV_scenario_level0_2.csv", "a")

    bdv = 1
    i = 0

    await asyncio.sleep(2)

    async with server_2:
        print("PRV Level 0 scenario started")
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
                prv = PRV1_array[i]
                ts_gas -= 3
            
            if lt <= 0:
                lt = 0
            
            # end scenario when prv closed and tank is empty
            if (prv == 0 and lt <= 0):
                lt = 0
                drain = 0
                print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)

                await lt_var.write_value(round(float(lt),2))
                await rp_var.write_value(float(rp))
                await ls_var.write_value(float(ls))
                await bdv_var.write_value(float(bdv))

                
                f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv)+'\n') 
                break
            
            ts_gas = random.randint(14,16)
            ts_liquid = random.randint(14,16)
            
            # set server values
            await lt_var.write_value(round(float(lt),2))
            await rp_var.write_value(float(rp))
            await ls_var.write_value(float(ls))
            await bdv_var.write_value(float(bdv))


            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv)+'\n')  

            await asyncio.sleep(2)
            i += 1
        
        prv = 30
        i = 0

        while i < 1.5 * 60:
            lt += 0.1 * prv

            if i >= 37:
                prv = 0
            else: 
                prv = PRV2_array[i]

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

                print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "ts_liquid liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
                f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv)+'\n')  
                
                break
            

            # set server values
            await lt_var.write_value(float(round(lt,2)))
            await rp_var.write_value(float(rp))
            await ls_var.write_value(float(ls))
            await bdv_var.write_value(float(bdv))

            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv)+'\n') 

            await asyncio.sleep(2)
            i += 1
        
    print("PRV Level 0 scenario finished")
    await server_2.stop()
    f.close()
    return

if __name__ == "__main__":
    asyncio.run(main())