# boot.py - Starts Simon Says automatically
import time

print("Simon Says - Starting in 2 seconds...")
time.sleep(2)

try:
    import main
    main.main()
except Exception as e:
    print(f"Error: {e}")
