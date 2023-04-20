
from opcua import ua, Server
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
    ts_liquid_var = node.add_variable(idx, "Temperature", 14, varianttype=ua.VariantType.Float)
    ts_gas_var = node.add_variable(idx, "Temperature", 14, varianttype=ua.VariantType.Float)

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

    print("Attack scenario started")
    f = open("attack_scenario.csv", "a")
    bdv = 1
    i = 0

    #open bdv
    #increase lt quicker than bdv


    while i < 5 * 60:

        if i > 30:
            lt += 11 * bdv

        if (lt >= 50): 
            ls = 1
        else:
            ls = 0

        # end scenario when prv closed and tank is empty
        if (bdv == 0 and lt <= 0):
            lt = 0
            drain = 0

            lt_var.set_value(lt)
            rp_var.set_value(0)
            ls_var.set_value(0)
            bdv_var.set_value(0)
            prv_var.set_value(random.randint(0,10))
            ts_liquid_var.set_value(random.randint(13,16))
            ts_gas_var.set_value(random.randint(13,16))
            drain_var.set_value(drain)

            print(i, "\t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
            f.write(repr(i) + "\t, " + repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 
            break
        
        prv = random.randint()
        ts_liquid = random.randint(13,16)
        # set server values
        lt_var.set_value(random.randint(0,1))
        rp_var.set_value(0)
        ls_var.set_value(0)
        bdv_var.set_value(0)
        prv_var.set_value(random.randint(0,10))
        ts_liquid_var.set_value(random.randint(13,16))
        ts_gas_var.set_value(random.randint(13,16))
        drain_var.set_value(0)

        print(i, "\t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp liquids: ", ts_liquid, "temp gas: ", ts_gas , "drain valve: ", drain)
        f.write(repr(i) + "\t, " + repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(ts_liquid, 2)) + ", " + repr(round(ts_gas, 2)) + ", "+ repr(drain) +'\n') 

        time.sleep(1) 
        i += 1

    print("BD relief scenario complete") 
    f.close() 
    server.stop()

if __name__ == "__main__":
    main()