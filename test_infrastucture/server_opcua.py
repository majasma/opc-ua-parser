from opcua import ua, Server
import datetime
import time
import update_variables as uv

# -------------------------------------- SETUP SERVER AND NODE --------------------------------

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
dsv_var = node.add_variable(idx, "Drain System Valve", 0,  varianttype=ua.VariantType.Float)
flare_var = node.add_variable(idx, "Flare Ignition", 0, varianttype=ua.VariantType.Boolean)


# make variables writable
lt_var.set_writable()
rp_var.set_writable()
ls_var.set_writable()
bdv_var.set_writable()
prv_var.set_writable()
dsv_var.set_writable()
flare_var.set_writable()

# --------------------------------------- NOT SURE IF THIS IS NESESSARY --------------------------


# create a new object type for the temperature sensor
sensor_type = server.nodes.base_object_type.add_object_type(idx, "TemperatureSensorType")

# create method for the temperature sensor to update its value
sensor_type.add_method(idx, "UpdateTemperature", uv.update_lt, [], [])

# create a new instance of the temperature sensor object
sensor_node = server.nodes.objects.add_object(idx, "TemperatureSensor", sensor_type)

# -------------------------------------- START SERVER ------------------------------------------
server.start()
print("Server started at {}".format(url))

while True:
    # update temperature every second
    lt = uv.update_lt()
    rp = uv.update_rp()
    ls = uv.update_ls()
    bdv = uv.update_bdv()
    prv = uv.update_prv()
    dsv = uv.update_dsv()
    flare = uv.update_flare()

    var_arr = [lt, rp, ls, bdv, prv, prv, dsv, flare]


    lt_var.set_value(lt)
    rp_var.set_value(rp)
    ls_var.set_value(ls)
    bdv_var.set_value(bdv)
    prv_var.set_value(prv)
    dsv_var.set_value(dsv)
    flare_var.set_value(flare)
    
    
    time_var = datetime.datetime.now()

    print(var_arr, time_var)
    time.sleep(1)


