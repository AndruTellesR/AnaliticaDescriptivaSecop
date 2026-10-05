"""Cliente Gemini con function calling para invocar al modelo predictivo."""

from __future__ import annotations
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import google.generativeai as genai

from prompts import SYSTEM_PROMPT, REPRESENTAR_TOOL
from predictor import Predictor


# Cargar .env del proyecto raíz
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent.parent
load_dotenv(RAIZ_PROYECTO / '.env')

API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY no encontrada. Configurar en .env del proyecto raíz."
    )

MODELO_GEMINI = os.getenv('MODELO_GEMINI_CHATBOT', 'gemini-2.5-flash')


class ChatBot:
    """Conversación stateful con Gemini + function calling al modelo predictivo."""

    def __init__(self, modelo: str = MODELO_GEMINI):
        genai.configure(api_key=API_KEY)
        self.predictor = Predictor()
        # Declarar la tool en formato Gemini
        self.tool = genai.protos.Tool(
            function_declarations=[
                genai.protos.FunctionDeclaration(
                    name=REPRESENTAR_TOOL['name'],
                    description=REPRESENTAR_TOOL['description'],
                    parameters=self._schema_to_proto(REPRESENTAR_TOOL['parameters']),
                )
            ]
        )
        self.model = genai.GenerativeModel(
            model_name=modelo,
            system_instruction=SYSTEM_PROMPT,
            tools=[self.tool],
        )
        self.chat = self.model.start_chat()

    def _schema_to_proto(self, schema: dict):
        """Convierte JSON schema dict a proto Schema de Gemini."""
        type_map = {
            'string': genai.protos.Type.STRING,
            'number': genai.protos.Type.NUMBER,
            'integer': genai.protos.Type.INTEGER,
            'boolean': genai.protos.Type.BOOLEAN,
            'object': genai.protos.Type.OBJECT,
            'array': genai.protos.Type.ARRAY,
        }
        if schema.get('type') == 'object':
            props = {
                k: self._schema_to_proto(v)
                for k, v in schema.get('properties', {}).items()
            }
            return genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties=props,
                required=schema.get('required', []),
            )
        return genai.protos.Schema(
            type=type_map.get(schema.get('type'), genai.protos.Type.STRING),
            description=schema.get('description', ''),
        )

    # ------------------------------------------------------------------ #
    # Bucle conversacional                                                #
    # ------------------------------------------------------------------ #

    def send(self, user_message: str) -> str:
        """Envía mensaje del usuario, resuelve tool calls si las hay,
        devuelve respuesta textual final."""
        response = self.chat.send_message(user_message)
        return self._process_response(response)

    def _process_response(self, response, depth: int = 0) -> str:
        if depth > 3:
            return "[Demasiadas llamadas tool encadenadas; abortando]"

        # Buscar function call en la respuesta
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call') and part.function_call.name:
                fname = part.function_call.name
                fargs = dict(part.function_call.args)
                print(f"\n[Llamando función {fname} con args:]")
                for k, v in fargs.items():
                    print(f"   {k} = {v}")

                if fname == 'predecir_riesgo':
                    pred = self.predictor.predict(fargs)
                    resultado = pred.to_dict()
                    print(f"[Resultado: atraso={resultado['proba_atraso']*100:.1f}% | "
                          f"sobrecosto={resultado['proba_sobrecosto']*100:.1f}%]\n")

                    # Devolver resultado a Gemini para que humanize
                    follow = self.chat.send_message(
                        genai.protos.Content(
                            parts=[
                                genai.protos.Part(
                                    function_response=genai.protos.FunctionResponse(
                                        name=fname,
                                        response={'resultado': resultado},
                                    )
                                )
                            ]
                        )
                    )
                    return self._process_response(follow, depth + 1)

        # No hay function call → respuesta textual directa
        return response.text


if __name__ == '__main__':
    print("ChatBot inicializando...")
    bot = ChatBot()
    print("Listo. Escribe 'salir' para terminar.\n")
    while True:
        try:
            user = input("Tú: ").strip()
            if user.lower() in {'salir', 'exit', 'quit'}:
                break
            if not user:
                continue
            resp = bot.send(user)
            print(f"\nBot: {resp}\n")
        except KeyboardInterrupt:
            print("\n[Interrumpido]")
            break
        except Exception as e:
            print(f"[Error: {e}]")
