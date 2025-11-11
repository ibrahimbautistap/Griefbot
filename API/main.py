from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os
from fastapi.responses import Response
import logging
import random

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("La clave API de Gemini no está configurada en el archivo .env")

# Inicializar el cliente de Gemini
try:
    client = genai.Client(api_key=API_KEY)
    logger.info("Cliente de Gemini inicializado correctamente")
except Exception as e:
    logger.error(f"Error al inicializar el cliente de Gemini: {e}")
    raise

app = FastAPI(title="GriefBot con Gemini API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos
class MensajeUsuario(BaseModel):
    user_id: str
    message: str

# Sistema robusto de respuestas empáticas predefinidas
def generar_respuesta_empatia(mensaje: str) -> str:
    
    mensaje_lower = mensaje.lower().strip()
    
    # Respuestas para saludos
    if any(palabra in mensaje_lower for palabra in ['hola', 'hi', 'hey', 'buenas', 'saludos']):
        saludos = [
            "Hola, soy tu GriefBot. Estoy aquí para ofrecerte apoyo emocional. ¿Cómo te sientes hoy?",
            "Hola, me da gusto que estés aquí. Estoy listo para escucharte y apoyarte. ¿Qué te trae por aquí hoy?",
            "Hola, es un honor poder acompañarte en este momento. ¿Cómo estás sintiéndote?"
        ]
        return random.choice(saludos)
    
    # Respuestas para bienestar positivo
    elif any(palabra in mensaje_lower for palabra in ['bien', 'ok', 'genial', 'contento', 'feliz', 'mejor']):
        respuestas_positivas = [
            "Me alegra saber que te sientes bien. Celebrar los momentos de calma es importante en el proceso de duelo.",
            "Es reconfortante escuchar que tienes un momento de bienestar. ¿Quieres compartir qué te está ayudando a sentirte así?",
            "Me da gusto que estés teniendo un momento positivo. Recuerda que es normal tener altibajos, y cada emoción es válida."
        ]
        return random.choice(respuestas_positivas)
    
    # Respuestas para tristeza
    elif any(palabra in mensaje_lower for palabra in ['triste', 'deprimido', 'llorar', 'dolor', 'tristeza', 'mal']):
        respuestas_tristeza = [
            "Lamento que te sientas así. El dolor y la tristeza son emociones naturales en el proceso de duelo. Estoy aquí para escucharte.",
            "Es completamente válido sentirse triste. El duelo tiene sus propios tiempos. ¿Quieres hablar más sobre lo que te está causando este sentimiento?",
            "Acompañarte en tu tristeza es un honor. Recuerda que no estás solo/a en esto. ¿Hay algo específico que te gustaría compartir?"
        ]
        return random.choice(respuestas_tristeza)
    
    # Respuestas para enojo
    elif any(palabra in mensaje_lower for palabra in ['enojo', 'enfadado', 'rabia', 'furia', 'molesto', 'irritado']):
        respuestas_enojo = [
            "El enojo es una respuesta natural al dolor y la pérdida. Está bien sentirse así. ¿Qué es lo que más te molesta en este momento?",
            "Entiendo tu enojo. A veces la rabia es la forma en que nuestro corazón expresa el dolor tan grande que sentimos.",
            "El enojo puede ser abrumador. Está bien sentirlo. ¿Quieres contarme más sobre lo que despierta esta emoción en ti?"
        ]
        return random.choice(respuestas_enojo)
    
    # Respuestas para soledad
    elif any(palabra in mensaje_lower for palabra in ['solo', 'soledad', 'aislado', 'abandonado', 'vacío']):
        respuestas_soledad = [
            "La sensación de soledad puede ser muy intensa durante el duelo. Quiero que sepas que estoy aquí contigo en este momento.",
            "El sentimiento de soledad es común cuando hemos perdido a alguien importante. Estoy aquí para acompañarte en este sentimiento.",
            "Aunque te sientas solo/a, quiero recordarte que estoy aquí para ti. ¿Hay alguien más con quien te gustaría conectar?"
        ]
        return random.choice(respuestas_soledad)
    
    # Respuestas para miedo/ansiedad
    elif any(palabra in mensaje_lower for palabra in ['miedo', 'asustado', 'ansiedad', 'preocupado', 'nervioso', 'angustia']):
        respuestas_miedo = [
            "Entiendo que puedas sentir miedo o ansiedad. Son emociones normales cuando estamos procesando una pérdida. ¿Qué es lo que más te preocupa?",
            "El miedo puede ser abrumador. Tomemos un respiro juntos. Estoy aquí para apoyarte mientras navegas estos sentimientos.",
            "La ansiedad en el duelo es común. ¿Quieres contarme más sobre lo que te genera esta preocupación?"
        ]
        return random.choice(respuestas_miedo)
    
    # Respuestas para agradecimiento
    elif any(palabra in mensaje_lower for palabra in ['gracias', 'agradecido', 'thanks', 'agradezco']):
        respuestas_gracias = [
            "Gracias a ti por confiar en mí. Estar aquí para apoyarte es un honor. ¿Hay algo más en lo que pueda ayudarte?",
            "Agradezco tu apertura. Es un privilegio poder acompañarte en este proceso. Estoy aquí para lo que necesites.",
            "Tu agradecimiento me conmueve. Sigamos caminando juntos este proceso. ¿Cómo te sientes en este momento?"
        ]
        return random.choice(respuestas_gracias)
    
    # Respuestas para despedidas
    elif any(palabra in mensaje_lower for palabra in ['adiós', 'chao', 'bye', 'nos vemos', 'hasta luego']):
        respuestas_despedida = [
            "Hasta luego. Recuerda que estoy aquí cuando me necesites. Cuídate mucho.",
            "Fue un honor acompañarte. Vuelve cuando quieras hablar. No estás solo/a.",
            "Hasta pronto. Tómate un momento para respirar y cuidar de ti. Estaré aquí cuando regreses."
        ]
        return random.choice(respuestas_despedida)

def intentar_gemini_gratuito(mensaje: str) -> str:

    try:
        # modelo gratuito
        modelos_gratuitos = ["gemini-2.5-flash"]
        
        for modelo in modelos_gratuitos:
            try:
                logger.info(f"Intentando con modelo gratuito: {modelo}")
                
                response = client.models.generate_content(
                    model=modelo,
                    contents=mensaje,
                    config={
                        "system_instruction": "Eres un asistente de apoyo emocional de duelo. Responde con máxima empatía o si sientes que sea el caso recomendar ayuda humana profecional.",
                        "max_output_tokens": 100000000,
                        "temperature": 0.8,
                    }
                )
                
                # Extraer texto de manera segura
                if hasattr(response, 'text') and response.text and response.text.strip():
                    respuesta = response.text.strip()
                    logger.info(f"Gemini respondió: {respuesta}")
                    return respuesta
                    
            except Exception as e:
                logger.warning(f"Modelo {modelo} falló: {e}")
                continue
        
        # Si todos los modelos fallan
        return None
        
    except Exception as e:
        logger.error(f"Error general en Gemini: {e}")
        return None

# Endpoints
@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    return Response(status_code=204)

@app.get("/")
async def bienvenida():
    return {
        "mensaje": "Bienvenido al GriefBot. Usa /chat para comenzar a conversar.", 
        "docs": "Visita /docs para ver la documentación interactiva."
    }

@app.post("/chat")
async def conversar(datos: MensajeUsuario):
    
    try:
        # Validar mensaje
        if not datos.message or not datos.message.strip():
            return {
                "reply": "Hola, estoy aquí para escucharte. ¿Podrías contarme más sobre lo que estás sintiendo?"
            }
        
        logger.info(f"Usuario {datos.user_id} dijo: {datos.message}")
        
        # Primero intenta con Gemini
        respuesta_gemini = intentar_gemini_gratuito(datos.message)
        
        if respuesta_gemini:
            logger.info("Usando respuesta de Gemini")
            return {"reply": respuesta_gemini}
        else:
            # si Gemini falla, usa el sistema robusto de respuestas
            respuesta_empatia = generar_respuesta_empatia(datos.message)
            logger.info(f"Usando respuesta empática predefinida: {respuesta_empatia}")
            return {"reply": respuesta_empatia}
        
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        # Fallback absoluto
        return {
            "reply": "Estoy aquí para ti en este momento. ¿Quieres compartir cómo te sientes?"
        }

@app.get("/status")
async def status():
    return {
        "status": "activo", 
        "servicio": "GriefBot API",
        "version": "2.0",
        "caracteristica": "Sistema híbrido (Gemini + Respuestas Empáticas Predefinidas)"
    }

# Ejecutar al inicio
@app.on_event("startup")
async def startup_event():
    logger.info("=== GRIEFBOT INICIADO ===")
    logger.info("Sistema: Respuestas empáticas predefinidas + Gemini gratuito de respaldo")
    logger.info("Modelos gratuitos disponibles: gemini-2.5-flash, gemini-pro")