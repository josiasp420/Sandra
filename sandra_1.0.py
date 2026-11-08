from customtkinter import *
from ia_gemini import *
from ia_gemini import LIST_PROMPTS

class Program(CTk):
	def __init__(self,title,width,height):
		super().__init__()
		self.title(title)
		self.geometry(str(width)+"x"+str(height))
		self.width = width
		self.height = height

		self.bottom()
		self.top()
		self.load_all_promts()

		# self.user_message("So tentando uma coisa")
		# self.ia_message("So respondendo uma coisa a mais")


	def bottom(self):
		self.base_frame = CTkFrame(self,width=1,height=70)
		self.entry = CTkTextbox(self.base_frame,height=50,font=("Arial",15))
		self.btn = CTkButton(self.base_frame,text="San.",width=40,fg_color="green",command=self.create_prompt,font=("Arial",15));

		self.base_frame.pack(side=BOTTOM,fill=X,padx=20)
		self.entry.pack(side=LEFT,expand=True,fill=X)
		self.btn.pack(side=RIGHT,padx=10)

	def top(self):
		self.body_frame = CTkScrollableFrame(self,width=1,height=1,fg_color="gray",corner_radius=0)
		#base = CTkScrollbar(self.body_frame,height=200)
		self.body_frame.pack(side=TOP,fill=BOTH,expand=True,padx=20,pady=5)

	def load_all_promts(self):
		for sender,msg in LIST_PROMPTS:
			if (sender == "user"):
				self.user_message(msg)
			else:
				self.ia_message(msg)

	def create_prompt(self):
		msg = self.entry.get("0.0",END)
		print("Voce: '"+msg+"'")
		if (msg == ""):
			return None

		self.user_message(msg)
		self.ia_action(msg);

	def user_message(self,msg: str):
		wid = CTkLabel(self.body_frame,text=msg,fg_color="gray4",wraplength=500,justify="left",corner_radius=7,font=("Arial",15))
		wid.pack(anchor=E, padx=10,pady=10, ipadx=20)

	def ia_message(self,msg: str):
		self.wid = CTkTextbox(self.body_frame,height=600,font=("JetBrainsMono",15))
		#wid = CTkLabel(self.body_frame,text=msg,fg_color="gray4",wraplength=500,justify="left",corner_radius=7,font=("Arial",15))
		self.wid.insert("0.0",msg)
		self.wid.pack(anchor=W, padx=10,pady=10, ipadx=20,fill=X,expand=True)

	def ia_action(self,msg:str):
		thing = chat(msg)
		if (thing):
			self.ia_message(thing)


prog = Program("Sandra",800,800)
prog.mainloop()

'''

Ah, agora entendi! Você quer um comportamento de **Auto-ajuste de Altura (Content-based height)**. Ou seja, se o texto for curto, o `textbox` é pequeno; se o texto for um textão, o `textbox` cresce para caber tudo, sem precisar de scroll interno.

O `CTkTextbox` padrão do `CustomTkinter` não faz isso nativamente porque ele é baseado no `Text` do Tkinter, que é feito para ter um tamanho fixo com scroll.

Para resolver isso, você tem dois caminhos:

### 1. O "Pulo do Gato": Usar `CTkLabel` (A melhor solução visual)
Se o objetivo é exibir o histórico da conversa (a mensagem da IA ou do usuário), o **`CTkLabel`** é muito superior ao `CTkTextbox` para isso.
*   **Vantagem:** O `CTkLabel` se ajusta automaticamente ao tamanho do texto (basta configurar `wraplength`).
*   **Estética:** Ele não tem "hover", não tem borda, e você pode configurar o `justify="left"`.

**Exemplo:**
```python
self.msg_label = CTkLabel(
    self.body_frame, 
    text="Aqui vai a sua mensagem gigante que vai ajustar o tamanho do frame automaticamente...",
    wraplength=400, # Define a largura máxima antes de quebrar a linha
    justify="left",
    anchor="w"
)
self.msg_label.pack(fill="x", pady=5)
```

---

### 2. Se você REALMENTE precisa ser um `Textbox` (para permitir seleção de texto)
Se você precisa que o usuário consiga copiar o texto da IA, você terá que calcular o tamanho com base no número de linhas e "forçar" a altura.

Como não existe um `height=auto`, você deve fazer uma função que atualiza o `height` com base na contagem de quebras de linha (`\n`):

```python
def ajustar_altura(textbox):
    # Pega o texto atual
    conteudo = textbox.get("1.0", "end-1c")
    # Conta quantas linhas existem
    num_linhas = len(conteudo.split('\n'))
    # Define uma altura base (ex: 20 pixels por linha)
    nova_altura = num_linhas * 25 
    textbox.configure(height=nova_altura)

# No seu código, toda vez que adicionar texto:
self.wid.insert("end", "Nova mensagem da IA...")
ajustar_altura(self.wid)
```

---

### Por que o `CTkLabel` é melhor para o seu caso?
No desenvolvimento de aplicações de Chat (como o ChatGPT desktop), quase ninguém usa `Textbox` para exibir mensagens passadas. Eles usam **Labels** ou **Widgets personalizados** criados dentro de um `ScrollableFrame`.

**Minha recomendação técnica para o seu projeto:**
1. Crie um `CTkScrollableFrame` no centro da sua tela.
2. Cada mensagem que chegar (ou for enviada) você cria um `CTkLabel` novo dentro desse `ScrollableFrame`.
3. O `CTkLabel` vai "empurrar" os outros para baixo automaticamente conforme cresce.

**Isso elimina o problema do `hover`, o problema da altura fixa e ainda deixa o design igual ao do ChatGPT original.**

O que acha dessa abordagem de usar o `ScrollableFrame` com `Labels`? Quer que eu te monte um exemplo básico de como seria essa estrutura de "bolhas de chat"?
'''



# __init__(self
#  master: <built-in function any>
#  width: int = 200
#  height: int = 200
#  corner_radius: Optional[int] = None
#  border_width: Optional[int] = None
#  border_spacing: int = 3
#  bg_color: Union[str , Tuple[str, str]] = 'transparent'
#  fg_color: Union[str, Tuple[str, str] ,NoneType] = None
#  border_color: Union[str, Tuple[str, str] = None
#  text_color: Optional[str] = None
#  scrollbar_button_color: Union[str
#  Tuple[str, str], NoneType] = None
#  scrollbar_button_hover_color: Union[str, Tuple[str, str], NoneType] = None
#  font: Union[tuple, customtkinter.windows.widgets.font.ctk_font.CTkFont, NoneType] = None
#  activate_scrollbars: bool = True


























