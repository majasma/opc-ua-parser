
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
BDV_array = [random.uniform(6, 8) for _ in range(300)]
temp1_array = [random.uniform(23, 26) for _ in range(300)]
temp2_array = [random.uniform(22, 25) for _ in range(300)]
temp_vol_array = [random.uniform(1, 2) for _ in range(300)]

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

    prv_var = await node_2.add_variable(idx_2, "PRV", prv)
    drain_var = await node_2.add_variable(idx_2, "Drain Valve", drain)
    ts_liquid_var = await node_2.add_variable(idx_2, "Temperature liquids", ts_liquid)
    ts_gas_var = await node_2.add_variable(idx_2, "Temperature gas", ts_gas)
    f = open("../log_files/BDV_scenario_Level0_2.csv", "a")

    i = 0

    async with server_2:
        while i < 2.5 * 60:

            if i > 5 and i < 25:
                bdv = 1
                ts_gas -= temp_vol_array[i]

            if i >= 25:
                bdv = 0

                if ts_gas < 23:
                    ts_gas += temp_vol_array[i]
                else:
                    ts_gas = temp1_array[i]

            lt += bdv * BDV_array[i]

            if i < 5:
                ts_gas = temp1_array[i]

            

            if (lt >= 10): 
                ls = 1
                drain = 1
            else:
                ls = 0

            if (drain == 1):
                lt -= 8

            ts_liquid = temp2_array[i]

            
            
            if lt <= 0:
                drain = 0
                lt = 0
            
            # end scenario when prv closed and tank is empty
            if (bdv == 0 and lt <= 0 and i >= 50):
                lt = 0
                drain = 0
                print(i, "\t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)

                await prv_var.write_value(round(float(prv),2))
                await ts_liquid_var.write_value(float(ts_liquid))
                await ts_gas_var.write_value(float(ts_gas))
                await drain_var.write_value(float(drain))

                
                f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 
                break
            
            
            await prv_var.write_value(round(float(prv),2))
            await ts_liquid_var.write_value(float(ts_liquid))
            await ts_gas_var.write_value(float(ts_gas))
            await drain_var.write_value(float(drain))

            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "bdv: ", bdv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 

            await asyncio.sleep(2)
            i += 1

    print("BD relief Level 0 scenario complete")  
    await server_2.stop()
    f.close()
    return

if __name__ == '__main__':
    asyncio.run(main())