"""
╔══════════════════════════════════════════════════════════════════════════════╗
║       DEPLOYMENT READINESS TEST SUITE                                       ║
║       Real-Time AI Recommendation Engine                                    ║
║                                                                              ║
║  Run:  python test_deployment_ready.py [--api-url http://your-api-url]      ║
║                                                                              ║
║  Tests every layer:                                                          ║
║   1.  Source code structure & imports                                        ║
║   2.  Dockerfile validity                                                    ║
║   3.  Environment variable handling                                          ║
║   4.  Live API endpoints (health, users, items, recs, events)               ║
║   5.  MongoDB connectivity & data presence                                   ║
║   6.  Redis connectivity & read/write                                        ║
║   7.  Kafka producer connectivity                                            ║
║   8.  Recommendation engine model logic                                      ║
║   9.  Dashboard configuration                                                ║
║   10. Frontend build artifact presence                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import argparse
import importlib
import subprocess
from pathlib import Path

# ── Colour helpers ────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ok(msg):    print(f"  {GREEN}✅  PASS{RESET}  {msg}")
def fail(msg):  print(f"  {RED}❌  FAIL{RESET}  {msg}")
def warn(msg):  print(f"  {YELLOW}⚠️   WARN{RESET}  {msg}")
def info(msg):  print(f"  {BLUE}ℹ️   INFO{RESET}  {msg}")
def header(msg): print(f"\n{BOLD}{BLUE}{'─'*72}\n  {msg}\n{'─'*72}{RESET}")

# ── Counters ──────────────────────────────────────────────────────────────────
results = {"pass": 0, "fail": 0, "warn": 0}

def record(kind: str, msg: str):
    if kind == "pass":   ok(msg);   results["pass"] += 1
    elif kind == "fail": fail(msg); results["fail"] += 1
    elif kind == "warn": warn(msg); results["warn"] += 1

def assert_true(condition: bool, pass_msg: str, fail_msg: str):
    record("pass" if condition else "fail", pass_msg if condition else fail_msg)
    return condition

# ── Locate project root ───────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1 — Source File Structure
# ══════════════════════════════════════════════════════════════════════════════
def test_file_structure():
    header("TEST 1 — Required File Structure")

    required = [
        "api/main.py",
        "api/requirements.txt",
        "api/Dockerfile",
        "database/mongo_client.py",
        "database/redis_client.py",
        "database/data_generator.py",
        "database/Dockerfile",
        "database/requirements.txt",
        "kafka_stream/producer.py",
        "kafka_stream/consumer.py",
        "recommendation_engine/model.py",
        "recommendation_engine/worker.py",
        "recommendation_engine/requirements.txt",
        "recommendation_engine/Dockerfile",
        "dashboard/app.py",
        "dashboard/requirements.txt",
        "dashboard/Dockerfile",
        "frontend/src/App.jsx",
        "frontend/src/context/AppContext.jsx",
        "frontend/package.json",
        "frontend/vite.config.js",
        "frontend/Dockerfile",
        "frontend/nginx.conf",
    ]

    for rel_path in required:
        p = PROJECT_ROOT / rel_path
        assert_true(p.exists(), f"EXISTS  {rel_path}", f"MISSING {rel_path}")

    # Ensure shadow directory is gone
    shadow = PROJECT_ROOT / "api" / "database"
    assert_true(
        not shadow.exists(),
        "api/database/ shadow directory is absent (import conflict resolved)",
        "api/database/ shadow directory STILL EXISTS — will cause ImportError"
    )


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2 — Python Imports
# ══════════════════════════════════════════════════════════════════════════════
def test_imports():
    header("TEST 2 — Python Package Imports")

    modules = [
        ("database.mongo_client",        "MongoDBClient",     "db_client"),
        ("database.redis_client",        "RedisClient",       "redis_client"),
        ("kafka_stream.producer",        "ActivityProducer",  "activity_producer"),
        ("kafka_stream.consumer",        "ActivityConsumer",  None),
        ("recommendation_engine.model",  "HybridRecommender", None),
        ("recommendation_engine.worker", None,                None),
    ]

    for mod_name, class_name, instance_name in modules:
        try:
            mod = importlib.import_module(mod_name)
            if class_name:
                assert_true(hasattr(mod, class_name),
                    f"Import OK — {mod_name}.{class_name}",
                    f"Class missing — {mod_name}.{class_name}")
            if instance_name:
                assert_true(hasattr(mod, instance_name),
                    f"Singleton OK — {mod_name}.{instance_name}",
                    f"Singleton missing — {mod_name}.{instance_name}")
            else:
                record("pass", f"Import OK — {mod_name}")
        except ImportError as e:
            record("fail", f"ImportError in {mod_name}: {e}")
        except Exception as e:
            record("warn", f"Import loaded but runtime warning in {mod_name}: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3 — Dockerfile Validation
# ══════════════════════════════════════════════════════════════════════════════
def test_dockerfiles():
    header("TEST 3 — Dockerfile Content Validation")

    checks = [
        ("api/Dockerfile",
         ["python:3.10-slim", "PYTHONPATH=/app", "uvicorn", "0.0.0.0", "8000"]),
        ("recommendation_engine/Dockerfile",
         ["python:3.10-slim", "PYTHONPATH=/app", "worker.py"]),
        ("dashboard/Dockerfile",
         ["python:3.10-slim", "8501", "streamlit", "0.0.0.0"]),
        ("frontend/Dockerfile",
         ["node:20-alpine", "nginx:alpine", "npm run build", "VITE_API_URL", "nginx.conf"]),
        ("database/Dockerfile",
         ["python:3.10-slim", "data_generator.py"]),
    ]

    for rel_path, keywords in checks:
        p = PROJECT_ROOT / rel_path
        if not p.exists():
            record("fail", f"MISSING {rel_path}")
            continue
        content = p.read_text()
        for kw in keywords:
            assert_true(kw in content,
                f"{rel_path} contains '{kw}'",
                f"{rel_path} MISSING keyword '{kw}'")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4 — Critical Code Patterns
# ══════════════════════════════════════════════════════════════════════════════
def test_code_patterns():
    header("TEST 4 — Critical Source Code Patterns")

    # api/main.py: must have /health endpoint
    api_main = (PROJECT_ROOT / "api/main.py").read_text()
    assert_true('/health' in api_main,
        "api/main.py has /health endpoint",
        "api/main.py MISSING /health endpoint — Azure health probe will fail")
    assert_true('localhost' not in api_main,
        "api/main.py has no localhost references",
        "api/main.py still references localhost")

    # dashboard/app.py: must NOT have localhost fallback
    dashboard = (PROJECT_ROOT / "dashboard/app.py").read_text()
    assert_true('localhost' not in dashboard,
        "dashboard/app.py has no localhost fallback",
        "dashboard/app.py still has localhost fallback — will break in Azure")
    assert_true('@st.cache_data' not in dashboard,
        "dashboard/app.py has no @st.cache_data (removed correctly)",
        "dashboard/app.py still has @st.cache_data — errors will be hidden")
    assert_true('st.stop()' in dashboard,
        "dashboard/app.py calls st.stop() when API_URL is missing",
        "dashboard/app.py missing st.stop() guard for missing API_URL")

    # data_generator.py: must use absolute import
    gen = (PROJECT_ROOT / "database/data_generator.py").read_text()
    assert_true('from database.mongo_client import db_client' in gen,
        "data_generator.py uses absolute import (Docker-safe)",
        "data_generator.py uses relative import — will break inside Docker")
    assert_true('from mongo_client import db_client' not in gen,
        "data_generator.py has no old relative import",
        "data_generator.py still has old relative import")

    # redis_client.py: must have SSL support
    redis_src = (PROJECT_ROOT / "database/redis_client.py").read_text()
    assert_true('ssl' in redis_src.lower(),
        "redis_client.py has SSL support (required for Azure Redis)",
        "redis_client.py missing SSL support — Azure Cache for Redis requires SSL")

    # kafka producer: must have SASL support
    producer_src = (PROJECT_ROOT / "kafka_stream/producer.py").read_text()
    assert_true('SASL_SSL' in producer_src,
        "kafka_stream/producer.py has SASL_SSL support (required for Confluent Cloud)",
        "kafka_stream/producer.py missing SASL_SSL — Confluent Cloud will reject connections")
    assert_true('KAFKA_API_KEY' in producer_src,
        "kafka_stream/producer.py reads KAFKA_API_KEY env var",
        "kafka_stream/producer.py missing KAFKA_API_KEY env var handling")

    # kafka consumer: must have SASL support
    consumer_src = (PROJECT_ROOT / "kafka_stream/consumer.py").read_text()
    assert_true('SASL_SSL' in consumer_src,
        "kafka_stream/consumer.py has SASL_SSL support",
        "kafka_stream/consumer.py missing SASL_SSL")

    # worker.py: must have retry logic, not just sleep
    worker_src = (PROJECT_ROOT / "recommendation_engine/worker.py").read_text()
    assert_true('for attempt in range' in worker_src,
        "worker.py has Kafka retry loop (not just sleep)",
        "worker.py missing retry loop — will crash if Kafka isn't ready immediately")

    # frontend Dockerfile: must be multi-stage with nginx
    frontend_docker = (PROJECT_ROOT / "frontend/Dockerfile").read_text()
    assert_true('nginx' in frontend_docker,
        "frontend/Dockerfile uses nginx (production serving)",
        "frontend/Dockerfile still uses Vite dev server — not production-safe")
    assert_true('npm run build' in frontend_docker,
        "frontend/Dockerfile runs npm run build",
        "frontend/Dockerfile missing npm run build")

    # nginx.conf: must support React Router fallback
    nginx_conf = (PROJECT_ROOT / "frontend/nginx.conf").read_text()
    assert_true('try_files' in nginx_conf,
        "frontend/nginx.conf supports React Router (try_files fallback)",
        "frontend/nginx.conf missing try_files — React Router will 404 on refresh")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 5 — Environment Variables
# ══════════════════════════════════════════════════════════════════════════════
def test_env_vars():
    header("TEST 5 — Environment Variable Configuration")

    required_for_api = ["MONGO_URI", "REDIS_HOST", "KAFKA_BROKER", "KAFKA_TOPIC"]
    required_for_dashboard = ["API_URL"]
    optional_cloud = ["REDIS_PASSWORD", "KAFKA_API_KEY", "KAFKA_API_SECRET", "REDIS_SSL"]

    info("Checking which Azure-required env vars are set in the current shell:")
    all_critical_set = True
    for var in required_for_api:
        val = os.getenv(var)
        if val:
            ok(f"{var} = {val[:40]}{'...' if len(val) > 40 else ''}")
        else:
            warn(f"{var} is NOT set (required for api & worker services)")
            all_critical_set = False

    for var in required_for_dashboard:
        val = os.getenv(var)
        if val:
            ok(f"{var} = {val[:60]}")
        else:
            warn(f"{var} is NOT set (required for dashboard service)")

    info("Optional cloud-auth env vars:")
    for var in optional_cloud:
        val = os.getenv(var)
        if val:
            ok(f"{var} is set")
        else:
            warn(f"{var} not set (only needed for Confluent Cloud / Azure Redis)")

    if all_critical_set:
        record("pass", "All critical environment variables are configured")
    else:
        record("warn", "Some env vars are missing — OK for local run, required before Azure deploy")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 6 — Live API Tests (optional, requires API_URL)
# ══════════════════════════════════════════════════════════════════════════════
def test_live_api(api_url: str):
    header(f"TEST 6 — Live API Endpoint Tests ({api_url})")

    try:
        import requests
    except ImportError:
        record("warn", "requests library not installed — skipping live API tests")
        return

    # 6.1 Health Check
    try:
        res = requests.get(f"{api_url}/health", timeout=10)
        data = res.json()
        assert_true(
            res.status_code == 200 and data.get("status") in ["ok", "healthy"],
            f"GET /health → 200 {data}",
            f"GET /health → {res.status_code} {res.text[:100]}"
        )
    except Exception as e:
        record("fail", f"GET /health failed: {e}")
        return  # Cannot test further if health fails

    # 6.2 Users
    try:
        res = requests.get(f"{api_url}/users", timeout=10)
        users = res.json().get("users", [])
        assert_true(
            res.status_code == 200 and len(users) > 0,
            f"GET /users → {len(users)} users found",
            f"GET /users → {res.status_code}, {len(users)} users (need data seeded)"
        )
    except Exception as e:
        record("fail", f"GET /users failed: {e}")
        users = []

    # 6.3 Items
    try:
        res = requests.get(f"{api_url}/items", timeout=10)
        items = res.json().get("items", [])
        assert_true(
            res.status_code == 200 and len(items) > 0,
            f"GET /items → {len(items)} items found",
            f"GET /items → {res.status_code}, {len(items)} items (need data seeded)"
        )
    except Exception as e:
        record("fail", f"GET /items failed: {e}")
        items = []

    # 6.4 Recommendations (use first user if available)
    if users:
        uid = users[0].get("user_id", "test_user")
        try:
            res = requests.get(f"{api_url}/recommendations/{uid}", timeout=10)
            recs = res.json().get("recommendations", [])
            assert_true(
                res.status_code == 200,
                f"GET /recommendations/{uid} → 200 ({len(recs)} recs)",
                f"GET /recommendations/{uid} → {res.status_code}"
            )
        except Exception as e:
            record("fail", f"GET /recommendations failed: {e}")

    # 6.5 User History
    if users:
        uid = users[0].get("user_id", "test_user")
        try:
            res = requests.get(f"{api_url}/users/{uid}/history", timeout=10)
            assert_true(
                res.status_code == 200,
                f"GET /users/{uid}/history → 200",
                f"GET /users/{uid}/history → {res.status_code}"
            )
        except Exception as e:
            record("fail", f"GET /users/history failed: {e}")

    # 6.6 Fire Event (POST /event)
    if users and items:
        uid = users[0].get("user_id")
        iid = items[0].get("item_id")
        try:
            res = requests.post(
                f"{api_url}/event",
                json={"user_id": uid, "item_id": iid, "action_type": "view"},
                timeout=10
            )
            assert_true(
                res.status_code == 200,
                f"POST /event (view) → 200",
                f"POST /event → {res.status_code} {res.text[:100]}"
            )
        except Exception as e:
            record("fail", f"POST /event failed: {e}")

    # 6.7 Auth Signup
    import uuid as _uuid
    test_email = f"test_{_uuid.uuid4().hex[:6]}@deploy-test.com"
    try:
        res = requests.post(
            f"{api_url}/auth/signup",
            json={"name": "Deploy Bot", "email": test_email, "password": "test1234"},
            timeout=10
        )
        data = res.json()
        assert_true(
            res.status_code == 200 and "user_id" in data,
            f"POST /auth/signup → 200, user_id={data.get('user_id')}",
            f"POST /auth/signup → {res.status_code} {res.text[:100]}"
        )

        # 6.8 Auth Login with the same user
        res2 = requests.post(
            f"{api_url}/auth/login",
            json={"email": test_email, "password": "test1234"},
            timeout=10
        )
        assert_true(
            res2.status_code == 200,
            f"POST /auth/login → 200",
            f"POST /auth/login → {res2.status_code} {res2.text[:100]}"
        )
    except Exception as e:
        record("fail", f"Auth tests failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 7 — MongoDB Connectivity
# ══════════════════════════════════════════════════════════════════════════════
def test_mongodb():
    header("TEST 7 — MongoDB Connectivity & Data")

    try:
        from database.mongo_client import db_client
        # Ping
        db_client.client.admin.command("ping")
        record("pass", "MongoDB connection successful")

        users = db_client.get_all_users()
        items = db_client.get_all_items()
        assert_true(len(users) > 0, f"MongoDB has {len(users)} users seeded", "MongoDB has 0 users — run db-seeder job")
        assert_true(len(items) > 0, f"MongoDB has {len(items)} items seeded", "MongoDB has 0 items — run db-seeder job")
    except Exception as e:
        record("fail", f"MongoDB test failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 8 — Redis Connectivity
# ══════════════════════════════════════════════════════════════════════════════
def test_redis():
    header("TEST 8 — Redis Connectivity & Read/Write")

    try:
        from database.redis_client import redis_client
        if redis_client.r is None:
            record("warn", "Redis client is None — not connected (may be OK if Redis not needed locally)")
            return

        # Write test
        redis_client.set_recommendations("deploy_test_user", [{"item_id": "test_item"}])
        recs = redis_client.get_recommendations("deploy_test_user")
        assert_true(
            len(recs) == 1 and recs[0]["item_id"] == "test_item",
            "Redis write+read roundtrip successful",
            "Redis read/write failed"
        )
        # Cleanup
        redis_client.r.delete("recs:deploy_test_user")
        record("pass", "Redis test key cleaned up")
    except Exception as e:
        record("fail", f"Redis test failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 9 — Kafka Producer
# ══════════════════════════════════════════════════════════════════════════════
def test_kafka():
    header("TEST 9 — Kafka Producer")

    try:
        from kafka_stream.producer import activity_producer
        if activity_producer.producer is None:
            record("warn", "Kafka producer not connected (OK if Kafka is a managed cloud service not accessible locally)")
            return
        # Send a test event
        activity_producer.send_event({
            "user_id": "deploy_test",
            "item_id": "test_item",
            "action_type": "view",
            "timestamp": time.time()
        })
        record("pass", "Kafka producer send_event() completed without error")
    except Exception as e:
        record("fail", f"Kafka producer test failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 10 — Recommendation Engine Model Logic
# ══════════════════════════════════════════════════════════════════════════════
def test_model():
    header("TEST 10 — Recommendation Engine Model Logic")

    try:
        from recommendation_engine.model import HybridRecommender
        record("pass", "HybridRecommender class imported successfully")

        rec = HybridRecommender()
        # If MongoDB has no data, items_df will be empty — that's ok here
        info(f"Model initialized. items_df shape: {rec.items_df.shape}")

        if not rec.items_df.empty:
            record("pass", f"Model loaded {len(rec.items_df)} items from MongoDB")

            # Simulate an event for a fake user
            test_uid = "model_test_user"
            test_iid = rec.items_df.index[0]
            rec.process_new_event({
                "user_id": test_uid,
                "item_id": test_iid,
                "action_type": "purchase",
                "timestamp": time.time()
            })
            record("pass", f"process_new_event() completed for user={test_uid}, item={test_iid}")
        else:
            record("warn", "items_df is empty — seeder has not run yet (model logic not fully tested)")
    except Exception as e:
        record("fail", f"Model test failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 11 — Dashboard Configuration
# ══════════════════════════════════════════════════════════════════════════════
def test_dashboard_config():
    header("TEST 11 — Dashboard Configuration")

    src = (PROJECT_ROOT / "dashboard/app.py").read_text()

    checks = [
        ('os.getenv("API_URL")',       "Reads API_URL from environment"),
        ('st.stop()',                   "Stops app when API_URL is missing"),
        ('res.raise_for_status()',      "Uses raise_for_status() for error visibility"),
        ('fetch_users',                 "fetch_users() function defined"),
        ('fetch_items',                 "fetch_items() function defined"),
        ('fetch_recs',                  "fetch_recs() function defined"),
        ('fetch_history',               "fetch_history() function defined"),
        ('fire_event',                  "fire_event() function defined"),
        ('plotly',                      "Plotly analytics charts present"),
    ]
    for keyword, description in checks:
        assert_true(keyword in src, f"dashboard: {description}", f"dashboard: MISSING — {description}")

    reqs = (PROJECT_ROOT / "dashboard/requirements.txt").read_text()
    for pkg in ["streamlit", "requests", "pandas", "plotly"]:
        assert_true(pkg in reqs, f"dashboard/requirements.txt includes '{pkg}'",
                    f"dashboard/requirements.txt missing '{pkg}'")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 12 — Frontend Build
# ══════════════════════════════════════════════════════════════════════════════
def test_frontend():
    header("TEST 12 — Frontend Source & Build Config")

    # Check key source files
    for rel_path in [
        "frontend/src/App.jsx",
        "frontend/src/main.jsx",
        "frontend/src/context/AppContext.jsx",
        "frontend/src/pages/Home.jsx",
        "frontend/src/pages/Login.jsx",
        "frontend/src/pages/Signup.jsx",
        "frontend/src/pages/Cart.jsx",
        "frontend/src/pages/OrderHistory.jsx",
        "frontend/src/pages/ProductDetail.jsx",
        "frontend/src/components/ProductCard.jsx",
    ]:
        p = PROJECT_ROOT / rel_path
        assert_true(p.exists(), f"EXISTS {rel_path}", f"MISSING {rel_path}")

    # AppContext: must reference VITE_API_URL
    ctx = (PROJECT_ROOT / "frontend/src/context/AppContext.jsx").read_text()
    assert_true("VITE_API_URL" in ctx,
        "AppContext reads VITE_API_URL (build-time injection)",
        "AppContext missing VITE_API_URL — API URL won't be injected at build time")

    # package.json: must have build script
    pkg = json.loads((PROJECT_ROOT / "frontend/package.json").read_text())
    assert_true("build" in pkg.get("scripts", {}),
        "package.json has 'build' script",
        "package.json missing 'build' script")

    # Check dist/ build artifact (only if already built)
    dist = PROJECT_ROOT / "frontend/dist"
    if dist.exists() and (dist / "index.html").exists():
        record("pass", "frontend/dist/index.html exists (pre-built bundle found)")
    else:
        record("warn", "frontend/dist/ not found — run 'cd frontend && npm run build' to pre-verify")


# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
def print_summary():
    total = results["pass"] + results["fail"] + results["warn"]
    header("DEPLOYMENT READINESS SUMMARY")
    print(f"  {GREEN}Passed : {results['pass']}{RESET}")
    print(f"  {RED}Failed : {results['fail']}{RESET}")
    print(f"  {YELLOW}Warnings: {results['warn']}{RESET}")
    print(f"  Total  : {total}\n")

    if results["fail"] == 0:
        print(f"  {BOLD}{GREEN}🚀 PROJECT IS READY FOR AZURE DEPLOYMENT!{RESET}\n")
    else:
        print(f"  {BOLD}{RED}❌ {results['fail']} issue(s) must be fixed before deploying.{RESET}\n")

    return results["fail"] == 0


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deployment Readiness Test Suite")
    parser.add_argument("--api-url", default=os.getenv("API_URL", ""),
                        help="API base URL to run live endpoint tests against")
    parser.add_argument("--skip-live",  action="store_true", help="Skip live API tests")
    parser.add_argument("--skip-mongo", action="store_true", help="Skip MongoDB tests")
    parser.add_argument("--skip-redis", action="store_true", help="Skip Redis tests")
    parser.add_argument("--skip-kafka", action="store_true", help="Skip Kafka tests")
    parser.add_argument("--skip-model", action="store_true", help="Skip model logic tests")
    args = parser.parse_args()

    print(f"\n{BOLD}{BLUE}{'═'*72}")
    print("  🔍  DEPLOYMENT READINESS TEST SUITE")
    print(f"      Project: Real-Time AI Recommendation Engine")
    print(f"      Root:    {PROJECT_ROOT}")
    print(f"{'═'*72}{RESET}")

    test_file_structure()
    test_imports()
    test_dockerfiles()
    test_code_patterns()
    test_env_vars()

    if args.api_url and not args.skip_live:
        test_live_api(args.api_url)
    else:
        header("TEST 6 — Live API Tests (SKIPPED)")
        info(f"Pass --api-url <url> to run live tests against a deployed or local API.")
        info(f"Example: python test_deployment_ready.py --api-url http://localhost:8001")

    if not args.skip_mongo:
        test_mongodb()
    if not args.skip_redis:
        test_redis()
    if not args.skip_kafka:
        test_kafka()
    if not args.skip_model:
        test_model()

    test_dashboard_config()
    test_frontend()

    success = print_summary()
    sys.exit(0 if success else 1)
