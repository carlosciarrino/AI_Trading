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

def test_trading_page():
    try:
        r = requests.get(f"{BASE}/trading", timeout=5)
        assert r.status_code == 200
        assert "Trading" in r.text
        print("✅ PASS: /trading risponde")
        return True
    except Exception as e:
        print(f"❌ FAIL: /trading: {e}")
        return False

def test_media_page():
    try:
        r = requests.get(f"{BASE}/media", timeout=5)
        assert r.status_code == 200
        assert "Media" in r.text
        print("✅ PASS: /media risponde")
        return True
    except Exception as e:
        print(f"❌ FAIL: /media: {e}")
        return False

def test_verification_api():
    try:
        r = requests.get(f"{BASE}/api/verification_status", timeout=5)
        assert r.status_code == 200
        data = r.json()
        if data and "file" in data:
            print(f"✅ PASS: /api/verification_status → {data['file']} ({'PASS' if data.get('success') else 'FAIL'})")
        else:
            print("✅ PASS: /api/verification_status → vuoto")
        return True
    except Exception as e:
        print(f"❌ FAIL: /api/verification_status: {e}")
        return False

def test_chart_api():
    try:
        r = requests.post(f"{BASE}/api/chart_data",
                         json={"symbol": "EURUSD=X", "period": "30d", "interval": "1d"},
                         timeout=15)
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✅ PASS: /api/chart_data → {len(data)} candele")
        return True
    except Exception as e:
        print(f"❌ FAIL: /api/chart_data: {e}")
        return False

if __name__ == "__main__":
    results = [
        ("test_dashboard_online", test_dashboard_online()),
        ("test_trading_page", test_trading_page()),
        ("test_media_page", test_media_page()),
        ("test_verification_api", test_verification_api()),
        ("test_chart_api", test_chart_api()),
    ]
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\n=== RISULTATI: {passed}/{total} PASS ===")
    sys.exit(0 if passed == total else 1)
