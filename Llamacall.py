from langchain.llms import LlamaCpp
from huggingface_hub import hf_hub_download
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


# temporary checking for LlamaCPP
model_name_or_path = "TheBloke/Llama-2-13B-GGUF"
model_basename = "llama-2-13b.Q4_K_S.gguf"
model_path = hf_hub_download(
    repo_id=model_name_or_path, filename=model_basename)
n_gpu_layers = 30
n_batch = 256
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# loading model,

llm = LlamaCpp(
    model_path=model_path,
    max_tokens=256,
    n_gpu_layers=n_gpu_layers,
    main_gpu=1,
    n_batch=n_batch,
    callback_manager=callback_manager,
    n_ctx=2048,
    verbose=True,
)
