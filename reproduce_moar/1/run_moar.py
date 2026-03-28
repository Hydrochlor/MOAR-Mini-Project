import os
import sys
import litellm
import yaml

original_completion = litellm.completion
def intercepted_completion(**kwargs):
    kwargs["azure"] = False
    
    kwargs["api_key"] = os.environ.get("OPENAI_API_KEY")
    kwargs["api_base"] = os.environ.get("OPENAI_API_BASE")

    # kwargs["api_key"] = os.environ.get("OPENROUTER_API_KEY")
    # kwargs["api_base"] = "https://openrouter.ai/api/v1"
    
    kwargs.pop("api_version", None)
    
    return original_completion(**kwargs)

litellm.completion = intercepted_completion

from docetl.cli import app
if __name__ == "__main__":
    sys.argv = ["docetl", "build", "pipeline.yaml", "--optimizer", "moar"]
    try:
        app()
    except Exception as e:
        print(f"\nError : {e}")