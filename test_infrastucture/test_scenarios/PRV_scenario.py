## some logical considerations
# if the level of the knock-out drum increases, the level switch should go high at the point of threshold.
# if the PRV or BDSV is open, the tank level should increase.
# the flare should be activated at all times.
# if the level in the tank is increasing the return pumps and drain system valves should be activated. 

from opcua import ua, Server
from datetime import datetime
import time
import random 

def main():
    #--------------------------------------INIT--------------------------------------------
    # create server
    server = Server()
    url = "opc.tcp://localhost:4840/"
    server.set_endpoint(url)

    # create address space - name
    uri = "http://example.org/UA/"
    idx = server.register_namespace(uri)

    # create node for temperature
    node = server.nodes.objects.add_object(idx, "Parameters")

    # create variables
    lt_var = node.add_variable(idx, "Level Transmitter", 0.0,  varianttype=ua.VariantType.Float)
    rp_var = node.add_variable(idx, "Return Pumps", 0.0,  varianttype=ua.VariantType.Float)
    ls_var = node.add_variable(idx, "Level Switch", 0, varianttype=ua.VariantType.Boolean)
    bdv_var = node.add_variable(idx, "BDV", 0,  varianttype=ua.VariantType.Boolean)
    prv_var = node.add_variable(idx, "PRV", 0, varianttype=ua.VariantType.Float)
    drain_var = node.add_variable(idx, "Drain Valve", 0, varianttype=ua.VariantType.Boolean)
    ts_liquid_var = node.add_variable(idx, "Temperature liquids", 14, varianttype=ua.VariantType.Float)
    ts_gas_var = node.add_variable(idx, "Temperature gas", 14, varianttype=ua.VariantType.Float)


    lt = 0.0
    rp = 0.0
    ls = 0
    bdv = 0
    prv = 0.0
    ts_liquid = 14
    ts_gas = 0
    drain = 0

    # make variables writable
    lt_var.set_writable()
    rp_var.set_writable()
    ls_var.set_writable()
    bdv_var.set_writable()
    prv_var.set_writable()
    ts_liquid_var.set_writable()
    ts_gas_var.set_writable()
    drain_var.set_writable()

    server.start()
    print("Server started at {}".format(url))
    

#--------------------------------------------SCENARIO START------------------------------------

    # Large relief
    # TODO include temperature consideration

    print("Large relief scenario started")
    f = open("PRV_scenario.csv", "a")
    prv = 70
    i = 0

    while i < 5* 60:
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
        else: 
            prv = random.randint(65, 75)


        # end scenario when prv closed and tank is empty
        if (prv == 0 and lt <= 0):
            lt = 0
            rp = 0

            lt_var.set_value(lt)
            rp_var.set_value(rp)
            ls_var.set_value(ls)
            bdv_var.set_value(bdv)
            prv_var.set_value(prv)
            ts_liquid_var.set_value(ts_liquid)
            ts_gas_var.set_value(ts_gas)
            drain_var.set_value(drain)

            print(i, "\t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(i) + "\t, " + repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 
            break

        # set server values
        lt_var.set_value(round(lt,2))
        rp_var.set_value(rp)
        ls_var.set_value(ls)
        bdv_var.set_value(bdv)
        prv_var.set_value(prv)
        ts_liquid_var.set_value(ts_liquid)
        ts_gas_var.set_value(ts_gas)
        drain_var.set_value(drain)

        print(i, "\t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
        f.write(repr(i) + "\t, " + repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 

        time.sleep(1) 
        i += 1

    print("Large relief scenario complete")    

    # small relief

    print("\n")
    print("Small relief scenario started")
    prv = 30
    i = 0

    while i < 5 * 60:
        lt += 0.1 * prv

        # close valgves after x seconds
        if i >= 3:
            prv = 0
        else: 
            prv = random.randint(27, 36)

        # TODO ask about this
        if lt >= 10:
            if temp < 150:
                temp += 7
        
        # decrease level in tank when the temperature is high enough
        if temp > 150:
            lt -= 0.02*temp

        # operators remove heating when there is no liquid, temp change have high delay
        if lt <= 0:
            temp -= 11
            lt = 0


        #exit scenario when prv closed, tank empty and temp returned to low
        if prv == 0 and temp <= 14 and lt <= 0:
            lt = 0

            lt_var.set_value(round(lt,2))
            rp_var.set_value(rp)
            ls_var.set_value(ls)
            bdv_var.set_value(bdv)
            prv_var.set_value(prv)
            ts_liquid_var.set_value(ts_liquid)
            ts_gas_var.set_value(ts_gas)
            drain_var.set_value(drain)

            print(i, "\t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(i) + "\t, " + repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 
            
            break

                # set server values
        lt_var.set_value(round(lt,2))
        rp_var.set_value(rp)
        ls_var.set_value(ls)
        bdv_var.set_value(bdv)
        prv_var.set_value(prv)
        ts_liquid_var.set_value(ts_liquid)
        ts_gas_var.set_value(ts_gas)
        drain_var.set_value(drain)

        print(i, "\t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
        f.write(repr(i) + "\t, " + repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 

        time.sleep(1) 
        i += 1

    print("Small relief scenario complete")
    f.close()

    return

if __name__ == "__main__":
    main()