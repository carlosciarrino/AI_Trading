import sys, os, requests
sys.path.insert(0, "/home/carlo/AI_Trading")

BASE = "http://localhost:5000"

def test_dashboard_online():
    try:
        r = requests.get(BASE, timeout=5)
        assert r.status_code == 200, f"Status {r.status_code}"
        assert "AI_BRIDGE" in r.text
        print("✅ PASS: dashboard risponde 200")
        return True
    except Exception as e:
        print(f"❌ FAIL: dashboard: {e}")
        return False

def test_status_api():
    try:
        r = requests.get(f"{BASE}/status", timeout=5)
        data = r.json()
        assert "status" in data
        print(f"✅ PASS: /status → {data['status']}")
        return True
    except Exception as e:
        print(f"❌ FAIL: /status: {e}")
        return False

def test_verification_api():
    try:
        r = requests.get(f"{BASE}/verification_status", timeout=5)
        assert r.status_code == 200
        data = r.json()
        if data and "file" in data:
            print(f"✅ PASS: /verification_status → {data['file']} ({'PASS' if data.get('success') else 'FAIL'})")
        else:
            print("✅ PASS: /verification_status → vuoto (nessuna verifica recente)")
        return True
    except Exception as e:
        print(f"❌ FAIL: /verification_status: {e}")
        return False

def test_orders_api():
    try:
        r = requests.get(f"{BASE}/orders", timeout=5)
        data = r.json()
        assert "open" in data
        print(f"✅ PASS: /orders → {data['open']} aperti")
        return True
    except Exception as e:
        print(f"❌ FAIL: /orders: {e}")
        return False

def test_chart_api():
    try:
        r = requests.post(f"{BASE}/chart_data",
                         json={"symbol": "EURUSD=X", "period": "30d", "interval": "1d"},
                         timeout=15)
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✅ PASS: /chart_data → {len(data)} candele")
        return True
    except Exception as e:
        print(f"❌ FAIL: /chart_data: {e}")
        return False

if __name__ == "__main__":
    results = [
        ("test_dashboard_online", test_dashboard_online()),
        ("test_status_api", test_status_api()),
        ("test_verification_api", test_verification_api()),
        ("test_orders_api", test_orders_api()),
        ("test_chart_api", test_chart_api()),
    ]
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\n=== RISULTATI: {passed}/{total} PASS ===")
    sys.exit(0 if passed == total else 1)
