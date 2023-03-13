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
temp_var = node.add_variable(idx, "Temp", 0.0)


# make variables writable
temp_var.set_writable()

# --------------------------------------- WHAT IS THIS --------------------------


# create a new object type for the temperature sensor
sensor_type = server.nodes.base_object_type.add_object_type(idx, "TemperatureSensorType")

# create method for the temperature sensor to update its value
sensor_type.add_method(idx, "UpdateTemperature", uv.update_temperature, [], [])

# create a new instance of the temperature sensor object
sensor_node = server.nodes.objects.add_object(idx, "TemperatureSensor", sensor_type)

# -------------------------------------- START SERVER ------------------------------------------
server.start()

while True:
    # update temperature every second
    temp = uv.update_temperature()
    temp_var.set_value(temp)

    time_var = datetime.datetime.now()

    print(temp, time_var)
    time.sleep(1)


