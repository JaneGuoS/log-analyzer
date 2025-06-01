from jsonschema import ValidationError
from analyzer import retriever
from llama_index.core.llms import ChatMessage,MessageRole

history = [ ChatMessage(role=MessageRole.USER,content="") ]

def get_stream_response(query_string, model):
    # If query_string is a list (e.g., [ChatMessage]), extract the content string
    if isinstance(query_string, list) and len(query_string) > 0 and hasattr(query_string[0], 'content'):
        query_str = query_string[0].content
    else:
        query_str = query_string

    print(f"[DEBUG] before getting the chat engine")
    chat_engine = retriever.get_chat_engine('logs_collection','default',model)
    print(f"[DEBUG] after getting the chat engine")

    try:
        result = chat_engine.chat(query_string, chat_history=history)   
        if history.__len__() > 20:
            history.clear()
        history.append(ChatMessage(role=MessageRole.USER, content=result.response))
        return result.response
    except ValidationError as e:
        print(f"[DEBUG] Validation Error: {e}")
        return f"Validation Error: {e}"
    except ValueError as e:
        print(f"[DEBUG] Value Error: {e}")
        return f"Value Error: {e}"
    except Exception as e:
        print(f"[DEBUG] Unexpected Exception: {e}")
        return f"Unexpected Exception: {e}"
    
def chat_with_llm(message, history, model):
    print(f"[DEBUG] chat_with_llm called with message={message}, history={history}, model={model}")
    i = len(message)
    query = message[: i+1]
    response_str = ''
    stream_response = get_stream_response(query, model)

    if isinstance(stream_response, str):
        # It's an error message, just yield it
        print(f"[DEBUG] stream_response is str: {stream_response}")
        yield stream_response
        return
    else:
        print(f"[DEBUG] Stream Response: {stream_response}")
        # Check if the stream_response has a 'response_gen' attribute
        result = getattr(stream_response, 'response_gen', None)
        print(f"[DEBUG] response_gen:")
        if result is None:
            print("[DEBUG] No response generated.")
            yield "Error: No response generated."
            return
        for r in result:
            print(f"[DEBUG] response_gen item: {r}")
            if isinstance(r, str):
                print(f"[DEBUG] r is str: {r}")
                response_str += r
            elif hasattr(r, 'delta'):
                print(f"[DEBUG] r has delta: {r.delta}")
                response_str += r.delta
            else:
                print(f"[DEBUG] r is not str and has no delta: {r}")
            response_str += r
        yield response_str
        return