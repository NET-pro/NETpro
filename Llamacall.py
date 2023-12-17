from langchain.llms import LlamaCpp
from huggingface_hub import hf_hub_download
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


#temporary checking for LlamaCPP
model_name_or_path = "TheBloke/Llama-2-13B-chat-GGUF"
model_basename = "llama-2-13b-chat.Q4_K_S.gguf"
model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)
n_gpu_layers = 20
n_batch = 128
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

#loading model,

llm = LlamaCpp(
        model_path=model_path,
        max_tokens=256,
        n_gpu_layers=n_gpu_layers,
        n_batch = n_batch,
        callback_manager=callback_manager,
        n_ctx=1024,
        verbose=True,
    )