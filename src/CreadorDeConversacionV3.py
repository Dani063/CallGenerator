import os
import boto3
from pydub import AudioSegment

# Configurar cliente de AWS Polly
session = boto3.Session(profile_name='recordia')
polly_client = session.client('polly', region_name='eu-west-1')

# Función para generar el audio con Amazon Polly
def generar_audio(texto, voice_name, output_filename):
    print(f"Generando audio para: '{texto}' con la voz: {voice_name}")
    try:
        response = polly_client.synthesize_speech(
            Text=texto,
            VoiceId=voice_name,
            OutputFormat='mp3',
            Engine='neural'
        )
        with open(output_filename, 'wb') as file:
            file.write(response['AudioStream'].read())
        print(f"Audio generado y guardado: {output_filename}")
    except Exception as e:
        print(f"Error al generar audio: {e}")

# Función para procesar la transcripción y dividirla en fragmentos
def cargar_dialogos_desde_texto(texto, config_voz):
    combinaciones = {
        "HH": ("Sergio", "Sergio"),  # Hombre-Hombre
        "HM": ("Sergio", "Lucia"),   # Hombre-Mujer
        "MH": ("Lucia", "Sergio"),  # Mujer-Hombre
        "MM": ("Lucia", "Lucia")     # Mujer-Mujer
    }
    voz_agente, voz_cliente = combinaciones.get(config_voz, ("Sergio", "Lucia"))
    dialogos = []
    roles = {"Agente": voz_agente, "Cliente": voz_cliente}
    rol_actual = None
    for linea in texto.split("\n"):
        linea = linea.strip()
        if not linea:  # Saltar líneas vacías
            continue
        if linea.endswith(":"):  # Identificar roles
            rol_actual = linea[:-1]
        elif rol_actual:
            voz = roles.get(rol_actual, "Lucia")
            dialogos.append((linea, voz, rol_actual))
    return dialogos

# Generar los audios para cada fragmento de diálogo
def generar_frases(dialogos):
    archivos = []
    for i, (texto, voz, _) in enumerate(dialogos, start=1): 
        filename = f"dialogo_{i:02}.mp3"
        generar_audio(texto, voz, filename)
        archivos.append(filename)
    print("Todos los audios han sido generados.")
    return archivos

# Unir los audios separando cliente y agente por canales
def unir_audios_por_canales(archivos, roles, output_file):
    canal_izquierdo = AudioSegment.silent(duration=0)  # Comienza con silencio
    canal_derecho = AudioSegment.silent(duration=0)     # Comienza con silencio

    # Procesar cada archivo de acuerdo con su rol
    for archivo, rol in zip(archivos, roles):
        if not os.path.exists(archivo):
            print(f"Archivo no encontrado: {archivo}")
            continue
        try:
            audio = AudioSegment.from_mp3(archivo)

            if rol == "Agente":
                canal_izquierdo += audio
                canal_derecho += AudioSegment.silent(duration=len(audio))  # Silencio para el canal derecho
            elif rol == "Cliente":
                canal_derecho += audio
                canal_izquierdo += AudioSegment.silent(duration=len(audio))  # Silencio para el canal izquierdo
            
            os.remove(archivo)  # Eliminar archivo temporal
            print(f"Archivo temporal eliminado: {archivo}")
        except Exception as e:
            print(f"Error al procesar el archivo {archivo}: {e}")

    # Obtener el número total de muestras por cada canal
    samples_izquierdo = len(canal_izquierdo.get_array_of_samples())
    samples_derecho = len(canal_derecho.get_array_of_samples())

    print(f"Total muestras canal izquierdo: {samples_izquierdo}")
    print(f"Total muestras canal derecho: {samples_derecho}")

    # Ajustar ambos canales para que tengan la misma cantidad de muestras
    while samples_izquierdo != samples_derecho:
        # Si el canal izquierdo tiene más muestras, recortar
        if samples_izquierdo > samples_derecho:
            canal_izquierdo = canal_izquierdo[:-1]
        # Si el canal derecho tiene más muestras, recortar
        elif samples_derecho > samples_izquierdo:
            canal_derecho = canal_derecho[:-1]

        # Actualizar las muestras después del recorte
        samples_izquierdo = len(canal_izquierdo.get_array_of_samples())
        samples_derecho = len(canal_derecho.get_array_of_samples())

        # Verificar que ambos canales tienen la misma longitud
        print(f"Total final muestras canal izquierdo: {samples_izquierdo}")
        print(f"Total final muestras canal derecho: {samples_derecho}")

    # Combinar los dos canales (izquierdo y derecho) en un audio estéreo
    audio_final = AudioSegment.from_mono_audiosegments(canal_izquierdo, canal_derecho)

    # Exportar el archivo combinado
    audio_final.export(output_file, format="mp3", bitrate="192k")
    print(f"Audio combinado guardado como: {output_file}")

# Procesar un archivo de transcripción
def procesar_transcripcion(file_path, output_dir, config_voz):
    try:
        with open(file_path, 'r', encoding='utf-8') as archivo:
            transcripcion = archivo.read()
        dialogos = cargar_dialogos_desde_texto(transcripcion, config_voz)
        archivos = generar_frases(dialogos)  # Pasar la lista completa de diálogos
        roles = [rol for _, _, rol in dialogos]
        output_filename = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}_output.mp3")
        unir_audios_por_canales(archivos, roles, output_filename)
    except Exception as e:
        print(f"Error al procesar la transcripción {file_path}: {e}")

# Procesar todos los archivos de texto en un directorio
def procesar_archivos_txt(input_dir, output_dir, config_voz):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            print(f"Procesando archivo: {file_path}")
            procesar_transcripcion(file_path, output_dir, config_voz)
