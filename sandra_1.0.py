from customtkinter import *
from ia_gemini import *
#from ia_gemini import LIST_PROMPTS

class Program(CTk):
	def __init__(self,title,width,height):
		super().__init__()
		self.title(title)
		self.configure(fg_color="#171A21")
		self.geometry(str(width)+"x"+str(height))
		self.width = width
		self.height = height
		self.chat_id = 0
		self.chatObj = chatIa(self.chat_id)

		self.frame = CTkFrame(self,width=1,height=1,fg_color="#171A21")
		self.frame.pack(side=RIGHT,fill=BOTH,expand=True,ipadx=20)
		self.bottom()
		self.top()
		self.left_menu()

	def bottom(self):
		self.base_frame = CTkFrame(self.frame,width=1,height=70,fg_color="#171A21")
		self.entry = CTkTextbox(self.base_frame,height=50,font=("Arial",15),fg_color="#202631",text_color="#E2E5EC",border_color="#353D4B",scrollbar_button_color="#414B5C",scrollbar_button_hover_color="#596780")
		self.btn = CTkButton(self.base_frame,text="San.",width=40,fg_color="#7889D8",hover_color="#8C9BE5",text_color="#FFFFFF",command=self.create_prompt,font=("Arial",15));

		self.base_frame.pack(side=BOTTOM,fill=X,padx=20)
		self.entry.pack(side=LEFT,expand=True,fill=X)
		self.btn.pack(side=RIGHT,padx=10)

	def top(self):
		self.body_frame = CTkScrollableFrame(self.frame,width=1,height=1,fg_color="#171A21",corner_radius=0,scrollbar_button_color="#414B5C",scrollbar_button_hover_color="#596780")
		self.body_frame.pack(side=TOP,fill=BOTH,expand=True,padx=10,pady=5)
		self.body_frame._scrollbar.grid_forget()
		for sender,msg in self.chatObj.getListPrompts():
			if (sender == "user"):
				self.user_message(msg)
			else:
				self.ia_message(msg)
		self.body_frame._parent_canvas.yview_moveto(1.0)
		
	def left_menu(self):
		self.leftm = CTkScrollableFrame(self,width=150,fg_color="#1D222B",corner_radius=5,scrollbar_button_color="#414B5C",scrollbar_button_hover_color="#596780")
		self.leftm.pack(side=LEFT,fill=Y,pady=10)
		self.leftm._scrollbar.grid_forget()

		self.butAddChat = CTkButton(self.leftm,text="Novo Chat",width=100,fg_color="#7889D8",hover_color="#8C9BE5",text_color="#FFFFFF",command=self.new_chat,font=("Arial",15))
		self.butAddChat.pack()

	def create_prompt(self):
		msg = self.entry.get("0.0",END)
		print("Voce: '"+msg+"'")
		if (msg == ""):
			return None

		self.entry.delete("0.0", END)
		self.user_message(msg)
		self.ia_action(msg)

	def user_message(self,msg: str):
		wid = CTkLabel(self.body_frame,text=msg,fg_color="#30395A",text_color="#EEF0F6",wraplength=500,justify="left",corner_radius=7,font=("Arial",15))
		wid.pack(anchor=E, padx=10,pady=10, ipadx=20)

	def ia_message(self,msg: str):
		self.wid = CTkTextbox(self.body_frame,height=600,font=("JetBrainsMono",15),fg_color="#202631",text_color="#E2E5EC",border_color="#353D4B",scrollbar_button_color="#414B5C",scrollbar_button_hover_color="#596780")
		#wid = CTkLabel(self.body_frame,text=msg,fg_color="gray4",wraplength=500,justify="left",corner_radius=7,font=("Arial",15))
		self.wid.insert("0.0",msg)
		self.wid.pack(anchor=W, padx=10,pady=10, ipadx=20,fill=X,expand=True)

	def ia_action(self,msg:str):
		thing = self.chatObj.chat(msg)
		if (thing):
			self.ia_message(thing)

	def new_chat(self):
		self.chat_id += 1
		self.chatObj = chatIa(self.chat_id)
		if hasattr(self, 'frame'):
			self.frame.destroy()
		self.frame = CTkFrame(self,width=1,height=1,fg_color="#171A21")
		self.frame.pack(side=RIGHT,fill=BOTH,expand=True,ipadx=20)
		self.bottom()
		self.top()

prog = Program("Sandra",800,800)
prog.mainloop()


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

'''