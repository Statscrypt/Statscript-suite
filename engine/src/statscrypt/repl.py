from statscrypt.core.tokenizer import Tokenizer
from statscrypt.core.parser import StatParser
from statscrypt.core.session import StatSession
from statscrypt.commands.stats import run_summarize
from statscrypt.commands.data_mgmt import run_use, run_list, run_gen
from statscrypt.commands.viz import run_graph 
import sys 
import json 
import statscrypt.core.exceptions as exceptions 

COMMAND_MAP = {
    'summarize': run_summarize,
    'use': run_use,
    'list': run_list,
    'gen': run_gen,
    'graph': run_graph, 
}

def _process_command(session: StatSession, tokenizer: Tokenizer, parser: StatParser, user_input: str, send_message_func):
    """Helper function to process a single command and send its output."""
    try:
        tokens = tokenizer.tokenize(user_input)
        if not tokens:
            return
            
        parsed_cmd = parser.parse(tokens)
        
        cmd_func = COMMAND_MAP.get(parsed_cmd['command'])
        
        if cmd_func:
            if parsed_cmd['command'] == 'gen':
                result = cmd_func(session, gen_expression=parsed_cmd['gen_expression'])
                send_message_func("output", result)
                send_message_func("variable_update", session.variables)
            elif parsed_cmd['command'] == 'graph':
                image_base64 = cmd_func(
                    session,
                    variables=parsed_cmd['variables']
                )
                send_message_func("plot_update", image_base64)
            elif parsed_cmd['command'] == 'use':
                result = cmd_func(
                    session,
                    variables=parsed_cmd['variables'],
                    **({'condition': parsed_cmd['condition']} if parsed_cmd['condition'] else {})
                )
                send_message_func("output", result)
                send_message_func("variable_update", session.variables)
            else:
                result = cmd_func(
                    session,
                    variables=parsed_cmd['variables'],
                    **({'condition': parsed_cmd['condition']} if parsed_cmd['condition'] else {})
                )
                send_message_func("output", result)
        else:
            send_message_func("output", f"Unknown command: {parsed_cmd['command']}")
            
    except exceptions.StatscryptError as e:
        send_message_func("error", e.stata_message)
    except Exception as e:
        send_message_func("error", f"An unexpected error occurred: {e}")
def start_repl_interactive():
    """Starts the interactive Read-Eval-Print Loop for statscrypt (CLI mode)."""
    session = StatSession()
    tokenizer = Tokenizer()
    parser = StatParser()
    
    print("statscrypt v0.1.0 (Open Source Stata Alternative)")
    print("Type 'exit' or press Ctrl+C to quit.")
    
    while True:
        try:
            user_input = input(">>> ").strip()
            if user_input.lower() == 'exit':
                break
            
            _process_command(session, tokenizer, parser, user_input, lambda t, p: print(p))
                
        except (KeyboardInterrupt, EOFError):
            print("\nExiting statscrypt.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def start_repl_json(send_json_message_func):
    """Starts the JSON-based Read-Eval-Print Loop for statscrypt (IPC mode)."""
    session = StatSession()
    tokenizer = Tokenizer()
    parser = StatParser()

    send_json_message_func("ready", "statscrypt engine ready for JSON commands.")

    while True:
        try:
            line = sys.stdin.readline()
            if not line: 
                break
            
            try:
                command_obj = json.loads(line)
                task = command_obj.get("task")
                payload = command_obj.get("payload")

                if task == "EXECUTE" and payload:
                    _process_command(session, tokenizer, parser, payload, send_json_message_func)
                elif task == "EXIT":
                    break
                else:
                    send_json_message_func("error", "Invalid JSON command format.")
            except json.JSONDecodeError:
                send_json_message_func("error", "Invalid JSON received.")

        except Exception as e:
            send_json_message_func("error", f"An unexpected error occurred in JSON REPL: {e}")
            
def main():
    """The main entry point for the REPL application."""
    start_repl_interactive()

if __name__ == '__main__':
    main()
