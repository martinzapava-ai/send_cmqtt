import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# ---- HEADER ----
st.set_page_config(page_title="MQTT Control", layout="centered")
st.title("🎛️ Panel de Control MQTT")
st.caption(f"Python {platform.python_version()}")

# ---- VARIABLES ----
values = 0.0
act1 = "OFF"

# ---- CALLBACKS ----
def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.success(f"📩 Mensaje recibido: {message_received}")

# ---- CONFIG MQTT ----
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("Martin")
client1.on_message = on_message

# ---- CONTROL DIGITAL ----
st.subheader("🔘 Control Digital")

col1, col2 = st.columns(2)

with col1:
    if st.button('🟢 Encender'):
        act1 = "ON"
        client1 = paho.Client("Martin")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("Boton", message)
        st.success("Dispositivo ENCENDIDO")

with col2:
    if st.button('🔴 Apagar'):
        act1 = "OFF"
        client1 = paho.Client("Martin")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("Boton", message)
        st.warning("Dispositivo APAGADO")

# ---- CONTROL ANALÓGICO ----
st.subheader("🎚️ Control Analógico")

values = st.slider(
    'Selecciona el valor',
    0.0, 100.0,
    value=0.0,
    step=0.1
)

st.metric(label="Valor actual", value=values)

if st.button('📤 Enviar valor'):
    client1 = paho.Client("Martin")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("Luz", message)
    st.success("Valor enviado correctamente")

