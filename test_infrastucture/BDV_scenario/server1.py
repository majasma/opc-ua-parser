
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
temp1_array = [random.uniform(14, 16) for _ in range(300)]
temp2_array = [random.uniform(14, 16) for _ in range(300)]

async def main():
    
    server_1 = Server()
    await server_1.init()
    url = "opc.tcp://localhost:4840/"
    server_1.set_endpoint(url)
    server_1.set_server_name("Flare OPC UA Tester 1")
    idx_1 = await server_1.register_namespace("flare_system_1")
    node_1 = await server_1.nodes.objects.add_object(idx_1, "Sensor-group-1")

    lt = 0.0
    rp = 0.0
    ls = 0.0
    bdv = 0.0
    prv = 0.0
    ts_liquid = 14.0
    ts_gas = 0.0
    drain = 0.0

    prv_var = await node_1.add_variable(idx_1, "PRV", prv)
    drain_var = await node_1.add_variable(idx_1, "Drain Valve", drain)
    ts_liquid_var = await node_1.add_variable(idx_1, "Temperature liquids", ts_liquid)
    ts_gas_var = await node_1.add_variable(idx_1, "Temperature gas", ts_gas)

    print("Started server 1 - containing sensors PRV, Drain, Temp Gas and Temp Liquid")
    f = open("../log_files/BDV_scenario_Level0_1.csv", "a")

    bdv = 1
    i = 0

    async with server_1:
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

            ts_gas = temp1_array[i]
            ts_liquid = temp2_array[i]

            if i >= 20:
                bdv = 0

                if ts_gas < 14:
                    ts_gas += 3
            

            
            # end scenario when prv closed and tank is empty
            if (bdv == 0 and lt <= 0 and i > 30):
                lt = 0
                drain = 0
                print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)

                await prv_var.write_value(round(float(prv),2))
                await ts_liquid_var.write_value(float(ts_liquid))
                await ts_gas_var.write_value(float(ts_gas))
                await drain_var.write_value(float(drain))

                
                f.write( repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 
                break
            
            
            # set server values
            await prv_var.write_value(round(float(prv),2))
            await ts_liquid_var.write_value(float(ts_liquid))
            await ts_gas_var.write_value(float(ts_gas))
            await drain_var.write_value(float(drain))


            print(i, "\t", "lt: ", round(lt,2), "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 

            await asyncio.sleep(2)
            i += 1

    print("BD relief Level 0 scenario complete")  
    await server_1.stop()
    f.close()
    return

if __name__ == '__main__':
    asyncio.run(main())