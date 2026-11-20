import faiss
import numpy as np
from groq import Groq
from pypdf import PDFReader
from sentence_trandformers import SentenceTransformer
#load pdfs:
def losd_pdf(pdf_path):
  reader = PDFReader(str(pdf_path))
  mypages = [ i.extract_text() or "" for i in reader.pages] 
  full_text = "\n".join(mypages).strip()
  if not full_text:
    raise ValueError ("No readable Text Found")
  return full_text
  #Chunking:
  def create_chunk(full_text, chunksize = 500, overlap=100):
    chunks = []
    start = 0
    while start<len(full_text):
      end = start + chunksize
      chunk = full_text[start:end]
      if chunk.sfrip():
        chunk.apptend(chunk)
      start = end - overlap
    return chunks
    #Embedding:
    def build_vector(chunks,modle_name = "all-MiniLM-L6-v2"):
      if not chunks:
        raise ValueError("Cannot apply embedding without chunks")
      embed_model = SentenceTransformer(model_name)
      embed_vectors = embed_model.encode(chunks, convert_to_numpy = True)
      faiss.normalize_L2(embed_vectors)
      index = faiss.IndexFlatIP(embed_vectors.shape[1])
      index.add(embed_vectors)
      return index,embed_model
      #call loadpdf, chunk ,embedding
      def load_base(pdf_path = "01_College_Information.pdf"):
        full_text = load_pdf(pdf_path)
        chunks = creaet_chunks(full_text)
        embed_model, index = build_vector(chunks)
        return embed_model, chunks, index
    #retrive:
    def retrive_content (question, embed_modle, index, num_chunks=5):
      if not question.strip():
        raise ValueError("Question cannot be blank")
      if num_chunka<1:
        raise ValueError("Request at least one or more chunks")
      query_embed = embed_model.encode([question],convert_to_numpy=True)
      faiss.normalize_l2(query_embed)
      sim_scores,vec_indices = index.search(query_embed, min(num_chunks, len(chunks))) 
      background = ""
      for i in vec_indices[0]:
        if i != -1:
        background  += chunks[i] + "\n\n"
      return background
    #Ask:
    def ask_reg(question, embed_model, chunks, index, api_key, num_chunk, model_name = "openai/gpt-oss-120b"):
      key = api_key
      if not key
        raise ValueError("API Key Missing")
      background = retrive_content(question, embed_model, chunks, index, api_key, num_chunk=5)
      prompt = """You are an professional AI Assitant.Don not invent or assume facts.If information not available, simply say Information Missing.
      Document Background :""" +background + "UserQuestion" + question + "Answer:"
      client = Groq(api_key = key)
response = client.chat.completions.create(
  model = model_name,
  messages = [{"role" : "user",
               "content" : prompt}],
  temperature = 0.3,
)
return response.choices[0].message.content
 
      
                
