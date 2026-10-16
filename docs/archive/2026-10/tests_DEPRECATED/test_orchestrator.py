import sys, os
sys.path.insert(0, "/home/carlo/AI_Trading")

def test_import_orchestrator():
    try:
        import orchestrator
        assert hasattr(orchestrator, 'main'), "manca funzione main()"
        assert hasattr(orchestrator, 'load_config'), "manca load_config()"
        assert hasattr(orchestrator, 'is_trading_hours'), "manca is_trading_hours()"
        print("✅ PASS: import orchestrator OK")
        return True
    except Exception as e:
        print(f"❌ FAIL: import orchestrator: {e}")
        return False

def test_import_prompts():
    try:
        from prompts import prompt_bull, prompt_bear, prompt_judge
        assert isinstance(prompt_bull, str)
        assert isinstance(prompt_bear, str)
        assert isinstance(prompt_judge, str)
        print("✅ PASS: import prompts OK")
        return True
    except Exception as e:
        print(f"❌ FAIL: import prompts: {e}")
        return False

def test_import_tools():
    try:
        from tools.risk_manager import RiskManager
        from tools.portfolio_manager import PortfolioManager
        from tools.support_resistance import find_sr
        from tools.news_fetcher import get_forex_live_news
        from tools.volume_analyst import get_session, analyze_volume
        from tools.trend_scout import get_trend
        print("✅ PASS: import tools OK")
        return True
    except Exception as e:
        print(f"❌ FAIL: import tools: {e}")
        return False

def test_data_fetch():
    try:
        import yfinance as yf
        df = yf.download("EURUSD=X", period="5d", interval="1d", multi_level_index=False)
        assert not df.empty, "DataFrame vuoto"
        assert "Close" in df.columns
        print(f"✅ PASS: yfinance OK ({len(df)} righe)")
        return True
    except Exception as e:
        print(f"❌ FAIL: yfinance: {e}")
        return False

if __name__ == "__main__":
    results = [
        ("test_import_orchestrator", test_import_orchestrator()),
        ("test_import_prompts", test_import_prompts()),
        ("test_import_tools", test_import_tools()),
        ("test_data_fetch", test_data_fetch()),
    ]
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\n=== RISULTATI: {passed}/{total} PASS ===")
    sys.exit(0 if passed == total else 1)
