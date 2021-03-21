def on_server_loaded(server_context):
    print("server loaded")
    # If present, this function executes when the server starts.
    pass

def on_server_unloaded(server_context):
    # If present, this function executes when the server shuts down.
    print("server unloading")
    pass

def on_session_created(session_context):
    # If present, this function executes when the server creates a session.
    print("new session created")
    pass

def on_session_destroyed(session_context):
    # If present, this function executes when the server closes a session.
    print("session destroyed")
    pass