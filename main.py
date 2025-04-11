import whisper
import os
import subprocess
import tkinter as tk
from pytubefix import YouTube
from moviepy import VideoFileClip
from transformers import BartTokenizer, BartForConditionalGeneration



    
def get_url():
    url = entry.get()
    entry.delete(0, tk.END)#limpar a caixa de input quando o input for recebido
    return url


def generate_answer_window(resumo, event=None):
    
    text = tk.Text(root, height=8, width=40, wrap="word", font=("Arial", 14))
    text.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    text.insert("1.0", resumo)
    #label.update_idletasks()  # Ensures accurate size measurement
    #label.config(width=label.winfo_reqwidth(), height=label.winfo_reqheight())
    #janela.mainloop()
    
 
    

def download_video(url):
    
    
    try: #Pesquisar sobre o comando try
        yt = YouTube(url)
    
    except: 
        print("Erro de conexão")
    
    mp4_streams = yt.streams.filter(file_extension='mp4') #Pegar todas as streams
    
    for i in range(len(mp4_streams)):
        print(i, mp4_streams[i])
        
    vnum = 0 #Get the first stream
    video1 = mp4_streams[vnum]
    
    try: 
        out_file = video1.download(output_path=CURRENT_DIRECTORY) #Foi preciso mudar a variavel client para ANDROID na file __main__ de pytubefix
        #Acima usando out_file para guardar o endereço  do video baixado
        print("Video baixado com sucesso")
        print(yt.title)
    except:
        print("Erro no download")
        
    return out_file
        
def converter_em_mp3(input_video, output_audio): 
    video = VideoFileClip(input_video)
    video.audio.write_audiofile(output_audio)
    
    
def transcrever(output_audio): #Vai ter que passar a variável do end do audio como parâmetro
    model = whisper.load_model("small")#Escolha do modelo whisper
    result = model.transcribe(output_audio)#Indicando file que o modelo vai transcrever
    transcrito = result["text"]
    print(result["text"])
    
    return transcrito

def resumir(transcrito):
   tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
   model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
   inputs = tokenizer.encode("summarize: " + transcrito, return_tensors="pt", max_length=1024, truncation=True)
   summary_ids = model.generate(inputs, max_length=1000, min_length=100, length_penalty= 1.0, num_beams=4, early_stopping=True)
   summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
   
   return summary

def summarize(event=None):
    CURRENT_DIRECTORY = os.path.dirname(__file__) #Gets the directory where python app is
    AUDIO_SAVE_PATH = os.path.join(CURRENT_DIRECTORY, "audio.mp3") #Creates the file path including the working directory
    url = get_url()
    input_video = download_video(url)
    converter_em_mp3(input_video, AUDIO_SAVE_PATH)
    transcrito = transcrever(AUDIO_SAVE_PATH)
    resumo = resumir(transcrito)
    
    #Delete downloaded files
    if os.path.exists(AUDIO_SAVE_PATH):  # Check if the file exists before deleting
        os.remove(AUDIO_SAVE_PATH)
        print("Audio file deleted successfully.")
    else:
        print("Audio file not found.")
    if os.path.exists(input_video):  # Check if the file exists before deleting
        os.remove(input_video)
        print("Video file deleted successfully.")
    else:
        print("Video file not found.")
    
    print(resumo)
    generate_answer_window(resumo)
    
    
    


CURRENT_DIRECTORY = os.path.dirname(__file__) #Gets the directory where python app is
AUDIO_SAVE_PATH = os.path.join(CURRENT_DIRECTORY, "audio.mp3") #Creates the file path including the working directory


#Initialize GUI:
root = tk.Tk() #Creates main window
root.title("transcribe Video APP")
    
root.columnconfigure(0, weight=5)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
    
frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")
frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
    
    
entry = tk.Entry(frame)
entry.grid(row=0, column=0, sticky="ew")
entry.bind("<Return>", get_url)
    
entry_btn = tk.Button(frame, text="Summarize", command=summarize)
entry_btn.grid(row=0, column=1)
    
    
    
root.mainloop()


    