
from opcua import ua, Server
import time
import random 
import numpy as np

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

    print("Masked attack scenario started")
    f = open("attack_scenario_mask.csv", "a")
    bdv = 1
    i = 0

    # Generate a array of values following a sine curve
    x = np.linspace(0, 300, 299)
    y = 2 * np.sin(1 * np.pi * 2 * x / 300)
    sine_arr = (y + 2) * 4 / 4

    while i <= 2*60:
        
        if i > 60 and i < 124:
            prv = random.randint(2,7)
            lt = sine_arr[i]

        temp = random.randint(13,16)
        # set server values
        lt_var.set_value(0)
        rp_var.set_value(0)
        ls_var.set_value(0)
        bdv_var.set_value(0)
        prv_var.set_value(random.randint(0,10))
        ts_liquid_var.set_value(random.randint(13,16))
        ts_gas_var.set_value(random.randint(13,16))
        drain_var.set_value(0)

        print(i," \t", "lt: ", lt, "prv: ", prv, "ls: ", ls, "rp: ", rp, "temp: ", temp, "drain valve: ", drain)
        f.write(repr(i) + "\t , " + repr(round(lt,2)) + ", " + repr(rp) + ", " + repr(ls) + ", " + repr(bdv) + ", " + repr(prv) + ", " + repr(round(temp, 2)) + ", " + repr(drain) +'\n')

        time.sleep(1) 
        i += 1

    print("Masked attack scenario complete") 
    f.close() 
    server.stop()

if __name__ == "__main__":
    main()