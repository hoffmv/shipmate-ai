# shipmate_ai/command_loop_test.py

from core.shipmate_command_router import ShipmateCommandRouter

def main():
    router = ShipmateCommandRouter()
    print("🛳️ Shipmate Command Loop Active. Type commands. 'exit' to quit.\n")
    
    while True:
        user_command = input(">> ")
        if user_command.lower() in ["exit", "quit"]:
            break
        response = router.route_command(user_command)
        print(response)

if __name__ == "__main__":
    main()
