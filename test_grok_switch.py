import os
import sys
import database
import ai
import app_utils

# Ensure we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_grok_integration():
    print("----------------------------------------------------------------")
    print("Testing Grok AI Integration...")
    
    # Check Health
    health = ai.ai_health_check()
    print(f"Health Check Result: {health}")
    
    if health.get("status") == "online":
        print("✅ Grok AI is ONLINE.")
    else:
        print(f"❌ Grok AI is OFFLINE: {health.get('message')}")
        
    # Check Analysis (Mock if we don't want to spend credits, but user asked to test code)
    # We will skip deep analysis call unless health is online
    if health.get("status") == "online":
        print("   Testing Analysis Connection...")
        res = ai.ai_analyze("This is a test cube.")
        print(f"   Analysis Result Summary: {res.get('summary')}")

def test_db_robustness():
    print("\n----------------------------------------------------------------")
    print("Testing Database Robustness...")
    
    if database.check_connection():
        print("✅ Database Connection: ONLINE")
    else:
        print("❌ Database Connection: OFFLINE")

if __name__ == "__main__":
    print("🚀 STARTING GROK SWITCH TEST")
    test_db_robustness()
    test_grok_integration()
    print("\n✅ TEST SEQUENCE COMPLETE")
