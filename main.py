from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests
import threading

class ChatApp(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # SUA API DO LM STUDIO
        self.api_url = "http://26.17.59.232:1234/v1/chat/completions"
        
        # Interface igual ChatGPT
        titulo = Label(text="💬 Qwen Chat", size_hint_y=None, height=50, font_size=20)
        
        self.chat = Label(
            text="Olá! Sou o Qwen. Como posso ajudar?\n\n",
            text_size=(None, None),
            halign="left",
            valign="top"
        )
        
        scroll = ScrollView()
        scroll.add_widget(self.chat)
        
        self.entrada = TextInput(
            hint_text="Digite sua mensagem...",
            multiline=False,
            size_hint_y=None,
            height=50
        )
        
        botao = Button(text="Enviar", size_hint_y=None, height=50)
        botao.bind(on_press=self.enviar)
        self.entrada.bind(on_text_validate=self.enviar)
        
        self.add_widget(titulo)
        self.add_widget(scroll)
        self.add_widget(self.entrada)
        self.add_widget(botao)
    
    def enviar(self, instance):
        msg = self.entrada.text.strip()
        if not msg:
            return
            
        self.entrada.text = ""
        self.chat.text += f"Você: {msg}\n"
        
        threading.Thread(target=self.processar, args=(msg,), daemon=True).start()
    
    def processar(self, mensagem):
        try:
            dados = {
                "model": "qwen/qwen3-4b",
                "messages": [{"role": "user", "content": mensagem}],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            resp = requests.post(self.api_url, json=dados, timeout=30)
            
            if resp.status_code == 200:
                texto = resp.json()["choices"][0]["message"]["content"]
                self.chat.text += f"🤖 Qwen: {texto}\n\n"
            else:
                self.chat.text += f"❌ Erro: {resp.status_code}\n\n"
                
        except Exception as e:
            self.chat.text += f"❌ Erro: {str(e)}\n\n"

class QwenApp(App):
    def build(self):
        return ChatApp()

QwenApp().run()