import os, requests, streamlit as st

API = os.getenv("API_URL", "http://127.0.0.1:8080/api")
st.set_page_config(page_title="WebConnect Dashboard", layout="centered")
st.title("🌐 WebConnect — Cloud Tester")

st.write("API base URL:")
api_url = st.text_input("API_URL", value=API)

st.subheader("Health")
if st.button("Ping /health"):
    try:
        r = requests.get(f"{api_url}/health", timeout=8)
        st.code(r.text, language="json")
    except Exception as e:
        st.error(f"Health error: {e}")

st.subheader("Auth")
c1, c2 = st.columns(2)

with c1:
    st.write("**Register**")
    e1 = st.text_input("Reg Email", value="owner@webconnect.com")
    p1 = st.text_input("Reg Password", value="Admin@123", type="password")
    if st.button("Register"):
        try:
            r = requests.post(f"{api_url}/auth/register", json={"email": e1, "password": p1}, timeout=10)
            st.code(r.text, language="json")
        except Exception as e:
            st.error(e)

with c2:
    st.write("**Login**")
    e2 = st.text_input("Login Email", value="owner@webconnect.com", key="lg_e")
    p2 = st.text_input("Login Password", value="Admin@123", type="password", key="lg_p")
    if "token" not in st.session_state: st.session_state.token = None
    if st.button("Login"):
        try:
            r = requests.post(f"{api_url}/auth/login", json={"email": e2, "password": p2}, timeout=10)
            j = r.json() if r.headers.get("content-type","").startswith("application/json") else {}
            tok = j.get("token")
            if r.ok and tok:
                st.session_state.token = tok
                st.success("Logged in ✅")
                st.code(tok[:60]+"...", language="text")
            else:
                st.error(r.text)
        except Exception as e:
            st.error(e)

st.subheader("Content: Home Hero")
c3, c4 = st.columns(2)

with c3:
    if st.button("GET /content/page/home-hero"):
        try:
            r = requests.get(f"{api_url}/content/page/home-hero", timeout=10)
            st.code(r.text, language="json")
        except Exception as e:
            st.error(e)

with c4:
    title = st.text_input("Title", value="Empower Your Business Digitally")
    subtitle = st.text_input("Subtitle", value="We build world-class web & mobile solutions.")
    if st.button("PUT /content/page/home-hero"):
        tok = st.session_state.get("token")
        if not tok:
            st.error("Login first to get a token.")
        else:
            try:
                r = requests.put(
                    f"{api_url}/content/page/home-hero",
                    json={"title": title, "content": {"subtitle": subtitle}, "published": True},
                    headers={"Authorization": f"Bearer {tok}"},
                    timeout=12
                )
                st.code(r.text, language="json")
            except Exception as e:
                st.error(e)

st.caption("Tip: On Streamlit Cloud, set API_URL in app secrets. Locally, it defaults to http://127.0.0.1:8080/api")
