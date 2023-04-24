
from asyncua import ua, Server
from asyncua.common.methods import uamethod
import asyncio
import logging
import time

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

    #,  varianttype=ua.VariantType.Float

    # create variables
    lt_var = await node.add_variable(idx, "Level Transmitter", 0.0)
    rp_var = await node.add_variable(idx, "Return Pumps", 0)
    ls_var = await node.add_variable(idx, "Level Switch", 0)
    bdv_var = await node.add_variable(idx, "BDV", 0)
    prv_var = await node.add_variable(idx, "PRV", 0.0)
    drain_var = await node.add_variable(idx, "Drain Valve", 0)
    ts_liquid_var = await node.add_variable(idx, "Temperature liquids", 14.0)
    ts_gas_var = await node.add_variable(idx, "Temperature gas", 14.0)

    # TODO change sequence of initialization of variables and setpoints
    lt = 0.0
    rp = 0.0
    ls = 0
    bdv = 0
    prv = 0.0
    ts_liquid = 14.0
    ts_gas = 0.0
    drain = 0

    print("Server started at {}".format(url))
    _logger.info("starting server...")
    

#--------------------------------------------SCENARIO START------------------------------------

    print("BD relief scenario started")
    f = open("BDV_scenario.csv", "a")
    bdv = 1
    i = 0

    #open bdv
    #increase lt quickly
    #close bdv
    #turn on ls
    #turn on drain
    #descrease level
    # TODO should esd status be added, and drain add to other scenarios
    async with server:
        while i < 3 * 60:
            lt += 10 * bdv

            if (lt >= 50): 
                ls = 1
                drain = 1
            else:
                ls = 0

            if (drain == 1):
                lt -= 7

            if i >= 8:
                bdv = 0
            

            # end scenario when prv closed and tank is efmpty
            if (bdv == 0 and lt <= 0):
                lt = 0
                drain = 0

                await lt_var.write_value(round(lt,1))
                await rp_var.write_value(rp)
                await ls_var.write_value(ls)
                await bdv_var.write_value(bdv)
                await prv_var.write_value(round(prv,1))
                await ts_liquid_var.write_value(round(ts_liquid,1))
                await ts_gas_var.write_value(round(ts_gas,1))
                await drain_var.write_value(drain)

                print(i, "\t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
                f.write(repr(i) + "\t, " + repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 
                break

            # set server values
            await lt_var.write_value(round(lt,2))
            await rp_var.write_value(rp)
            await ls_var.write_value(ls)
            await bdv_var.write_value(bdv)
            await prv_var.write_value(prv)
            await ts_liquid_var.write_value(ts_liquid)
            await ts_gas_var.write_value(ts_gas)
            await drain_var.write_value(drain)

            print(i, "\t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(i) + "\t, " + repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 

            await asyncio.sleep(5)
            i += 1

    print("BD relief scenario complete")  
    f.close()
    server.stop()

if __name__ == "__main__":
    asyncio.run(main())