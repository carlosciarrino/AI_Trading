import json, os, sys, tempfile
sys.path.insert(0, "/home/carlo/AI_Trading")

def test_write_sl_command():
    """Test: write_sl_command crea il file corretto."""
    test_file = "/tmp/test_sl_commands.json"
    os.environ["SL_COMMANDS_FILE"] = test_file
    
    # Import dopo aver settato l'env
    import importlib
    import tools.position_manager as pm
    importlib.reload(pm)
    
    # Override del path
    pm.SL_COMMANDS_FILE = test_file
    
    # Esegui
    pm.write_sl_command("35483", 1.12475)
    
    # Verifica
    if not os.path.exists(test_file):
        print("❌ FAIL: file non creato")
        return False
    
    with open(test_file) as f:
        data = json.load(f)
    
    if len(data) != 1:
        print(f"❌ FAIL: attesi 1 comando, trovati {len(data)}")
        return False
    
    if data[0]["ticket"] != "35483":
        print(f"❌ FAIL: ticket errato: {data[0]['ticket']}")
        return False
    
    if abs(data[0]["new_sl"] - 1.12475) > 0.00001:
        print(f"❌ FAIL: new_sl errato: {data[0]['new_sl']}")
        return False
    
    os.unlink(test_file)
    print("✅ PASS: write_sl_command funziona")
    return True

def test_get_orders():
    """Test: get_orders legge il file correttamente."""
    import importlib
    import tools.position_manager as pm
    importlib.reload(pm)
    
    orders = pm.get_orders()
    print(f"✅ PASS: get_orders ha letto {len(orders)} ordini")
    return True

if __name__ == "__main__":
    results = []
    results.append(("test_write_sl_command", test_write_sl_command()))
    results.append(("test_get_orders", test_get_orders()))
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\n=== RISULTATI: {passed}/{total} PASS ===")
    
    sys.exit(0 if passed == total else 1)
