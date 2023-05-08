
from asyncua import ua, Server
from asyncua.common.methods import uamethod
import asyncio
import logging
import random
import threading

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
    ts_liquid = 23.0
    ts_gas = 23.0
    drain = 0.0

    prv_var = await node_2.add_variable(idx_2, "PRV", prv)
    drain_var = await node_2.add_variable(idx_2, "Drain Valve", drain)
    ts_liquid_var = await node_2.add_variable(idx_2, "Temperature liquids", ts_liquid)
    ts_gas_var = await node_2.add_variable(idx_2, "Temperature gas", ts_gas)
    await asyncio.sleep(2)

    prv = 70
    i = 0

    f = open("../log_files/PRV_scenario_level0_2.csv", "a")

    async with server_2:
    
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
                ls = 0

            if ts_gas >= 23:
                ts_gas = temp2_array[i]

            if lt <= 0:
                lt = 0
                rp = 0


            # end scenario when prv closed and tank is empty
            if (prv == 0 and lt <= 0 and i > 30):
                lt = 0
                rp = 0

                await prv_var.write_value(round(float(prv),2))
                await ts_liquid_var.write_value(round(float(temp1_array[i]),2))
                await ts_gas_var.write_value(float(ts_gas))
                await drain_var.write_value(float(drain))

                print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
                f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(float(temp1_array[i]),2)) + ", " + repr(round(float(temp2_array[i]),2)) + ", "+ repr(drain) +'\n') 
                break

            # set server values
            await prv_var.write_value(round(float(prv),2))
            await ts_liquid_var.write_value(round(float(temp1_array[i]),2))
            await ts_gas_var.write_value(float(ts_gas))
            await drain_var.write_value(float(drain))

            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(float(temp1_array[i]),2)) + ", " + repr(round(float(temp2_array[i]),2)) + ", "+ repr(drain) +'\n') 

            await asyncio.sleep(2)
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

                await ts_liquid_var.write_value(float(ts_liquid))
                await ts_gas_var.write_value(float(ts_gas))
                await drain_var.write_value(float(drain))

                print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "ts_liquid liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
                f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(float(temp1_array[i]),2)) + ", " + repr(round(float(temp2_array[i]),2)) + ", "+ repr(drain) +'\n') 
                
                break
            

            # set server values
            await prv_var.write_value(round(float(prv),2))
            await ts_liquid_var.write_value(round(float(temp1_array[i]),2))
            await ts_gas_var.write_value(round(float(temp2_array[i]),2))
            await drain_var.write_value(float(drain))

            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(float(temp1_array[i]),2)) + ", " + repr(round(float(temp2_array[i]),2)) + ", "+ repr(drain) +'\n') 

            await asyncio.sleep(2)
            i += 1

        print("Small relief scenario complete")
        f.close()
    await server_2.stop()

if __name__ == '__main__':
    asyncio.run(main())