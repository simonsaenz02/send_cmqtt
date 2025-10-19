import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# ======================
# Configuración inicial
# ======================
st.set_page_config(
    page_title="MQTT Control",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ======================
# CSS personalizado
# ======================
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #232526, #414345);
            color: white;
        }

        h1 {
            text-align: center;
            font-size: 2.5em;
            color: #00FA9A;
            text-shadow: 1px 1px 4px black;
        }

        .stSlider label {
            font-weight: bold;
            color: #FFD700;
        }

        .stButton > button {
            background-color: #1E90FF;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 0.6em 1.2em;
            font-size: 1em;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #104E8B;
            transform: scale(1.05);
        }

        .box-result {
            background-color: #2e2e3e;
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
            border-left: 5px solid #1E90FF;
            font-size: 1.1em;
        }
    </style>
""", unsafe_allow_html=True)

# ======================
# Muestra versión de Python
# ======================
st.write("🐍 Versión de Python:", platform.python_version())

# ======================
# Variables globales
# ======================
values = 0.0
act1 = "OFF"

# ======================
# Funciones de callback
# ======================
def on_publish(client, userdata, result):
    print("✅ El dato ha sido publicado\n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(1)
    message_received = str(message.payload.decode("utf-8"))
    st.markdown(f"<div class='box-result'>📩 Mensaje recibido: {message_received}</div>", unsafe_allow_html=True)

# ======================
# Configuración del cliente MQTT
# ======================
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("SimonS")
client1.on_message = on_message

# ======================
# Interfaz
# ======================
st.title("🔌 Control MQTT con Streamlit")

st.write("Este panel permite **encender, apagar y enviar valores analógicos** "
         "a través del broker MQTT. Usa los botones y el control deslizante para interactuar.")

# Botón ON
if st.button('⚡ Encender (ON)'):
    act1 = "ON"
    client1 = paho.Client("SimonS")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    client1.publish("cmqtt_sSaenz", message)
    st.success("✅ Dispositivo encendido")

# Botón OFF
if st.button('💤 Apagar (OFF)'):
    act1 = "OFF"
    client1 = paho.Client("SimonS")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    client1.publish("cmqtt_sSaenz", message)
    st.error("⛔ Dispositivo apagado")

# Control analógico
values = st.slider('🎚️ Selecciona el rango de valores', 0.0, 100.0)
st.write(f'📊 Valor actual: **{values}**')

if st.button('📡 Enviar valor analógico'):
    client1 = paho.Client("SimonS")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_aSimon", message)
    st.success(f"📤 Valor analógico {values} enviado")


