import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recc-system.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CineRec — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================
# GLOBAL CSS — Dark Cinema Theme
# =============================
st.markdown(
    """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root Variables ── */
:root {
    --bg-deep:       #0a0a0f;
    --bg-surface:    #111118;
    --bg-card:       #181820;
    --bg-card-hover: #20202c;
    --border:        rgba(255,255,255,0.07);
    --border-hover:  rgba(255,160,50,0.5);
    --accent:        #f5a623;
    --accent-dim:    rgba(245,166,35,0.15);
    --accent-glow:   rgba(245,166,35,0.35);
    --text-primary:  #f0ede8;
    --text-muted:    #7a7a8c;
    --text-dim:      #4a4a5a;
    --red:           #e05252;
    --green:         #52e0a0;
    --radius-sm:     8px;
    --radius-md:     14px;
    --radius-lg:     20px;
}

/* ── App Shell ── */
.stApp {
    background: var(--bg-deep) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 10% 0%, rgba(245,166,35,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(80,80,200,0.05) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ── Block container ── */
.block-container {
    padding: 1.5rem 2.5rem 3rem !important;
    max-width: 1440px !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.2rem !important;
}

/* ── Headings ── */
h1, h2, h3, h4 {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

/* ── Main title ── */
.cinrec-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem;
    letter-spacing: 0.08em;
    background: linear-gradient(135deg, #f5a623 0%, #f5d020 60%, #fff8e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0;
}
.cinrec-sub {
    color: var(--text-muted);
    font-size: 0.88rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.2rem 0 !important;
}

/* ── Text input ── */
.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    padding: 0.7rem 1.1rem !important;
    transition: border-color 0.25s, box-shadow 0.25s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-dim) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--text-dim) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-muted) !important;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    letter-spacing: 0.04em;
    font-weight: 500;
    padding: 0.35rem 0.7rem !important;
    transition: all 0.2s ease;
    width: 100% !important;
    cursor: pointer;
}
.stButton > button:hover {
    background: var(--accent-dim) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    box-shadow: 0 0 14px var(--accent-glow);
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Back button override ── */
.back-btn .stButton > button {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-muted) !important;
    font-size: 0.85rem;
    padding: 0.45rem 1.1rem !important;
    width: auto !important;
}
.back-btn .stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── Poster card wrapper ── */
.poster-wrap {
    position: relative;
    border-radius: var(--radius-md);
    overflow: hidden;
    background: var(--bg-card);
    border: 1px solid var(--border);
    transition: transform 0.28s cubic-bezier(.4,0,.2,1),
                box-shadow 0.28s cubic-bezier(.4,0,.2,1),
                border-color 0.28s;
    cursor: pointer;
    animation: fadeUp 0.4s ease both;
}
.poster-wrap:hover {
    transform: translateY(-6px) scale(1.025);
    box-shadow: 0 18px 40px rgba(0,0,0,0.55), 0 0 20px var(--accent-glow);
    border-color: var(--border-hover);
}
.poster-wrap img {
    width: 100%;
    display: block;
    border-radius: var(--radius-md) var(--radius-md) 0 0;
}
.poster-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(10,10,15,0.92) 0%, transparent 55%);
    border-radius: var(--radius-md);
    opacity: 0;
    transition: opacity 0.28s ease;
    display: flex;
    align-items: flex-end;
    padding: 12px;
}
.poster-wrap:hover .poster-overlay {
    opacity: 1;
}
.poster-overlay-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: #fff;
    line-height: 1.2;
}
.poster-title {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-muted);
    line-height: 1.25;
    margin-top: 7px;
    padding: 0 6px 8px;
    max-height: 2.8em;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.poster-no-img {
    width: 100%;
    aspect-ratio: 2/3;
    background: var(--bg-card);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    color: var(--text-dim);
    border-radius: var(--radius-md) var(--radius-md) 0 0;
}

/* ── Detail card ── */
.detail-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2rem;
    animation: fadeIn 0.5s ease;
}
.detail-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 0.05em;
    color: var(--text-primary);
    line-height: 1.05;
    margin-bottom: 0.6rem;
}
.badge {
    display: inline-block;
    background: var(--accent-dim);
    border: 1px solid rgba(245,166,35,0.3);
    color: var(--accent);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border-radius: 30px;
    padding: 3px 10px;
    margin: 2px 3px;
}
.meta-line {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin: 6px 0;
}
.overview-text {
    color: var(--text-primary);
    font-size: 0.96rem;
    line-height: 1.7;
    margin-top: 1rem;
    border-top: 1px solid var(--border);
    padding-top: 1rem;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.7rem;
    letter-spacing: 0.07em;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.5rem 0 0.8rem;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, var(--border), transparent);
}

/* ── Category pill select ── */
.stSelectbox label, .stSlider label, .stTextInput label {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

/* ── Spinner ── */
.stSpinner > div > div {
    border-color: var(--accent) transparent transparent transparent !important;
}

/* ── Info / Warning / Error boxes ── */
.stAlert {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-muted) !important;
}

/* ── Animations ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0);    }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--bg-card); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-dim); }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.css-18e3th9 { padding-top: 0; }
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=60)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": poster_url,
                "release_date": m.get("release_date", ""),
            })
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id": tmdb["tmdb_id"],
                "title": tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
            })
    return cards


# =============================
# POSTER GRID  — animated cards
# =============================
def poster_grid(cards, cols=6, key_prefix="grid"):
    """Render an animated poster grid. Each card is a hover-effect container."""
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    delay_step = 40  # ms

    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")
            delay_ms = (r * cols + c) * delay_step

            with colset[c]:
                # Animated card shell with staggered delay
                st.markdown(
                    f"""
                    <div class="poster-wrap" style="animation-delay:{delay_ms}ms">
                        {"<img src='" + poster + "' />" if poster else "<div class='poster-no-img'>🎬</div>"}
                        <div class="poster-overlay">
                            <div class="poster-overlay-title">{title}</div>
                        </div>
                        <div class="poster-title">{title}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("▶ Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown(
        "<div style='font-family:\"Bebas Neue\",sans-serif;font-size:1.6rem;"
        "letter-spacing:0.1em;color:#f5a623;margin-bottom:0.3rem'>🎬 CineRec</div>"
        "<div style='color:#4a4a5a;font-size:0.72rem;letter-spacing:0.12em;"
        "text-transform:uppercase;margin-bottom:1.2rem'>Movie Recommender</div>",
        unsafe_allow_html=True,
    )

    if st.button("🏠  Home"):
        goto_home()

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        "<div style='color:#7a7a8c;font-size:0.75rem;letter-spacing:0.1em;"
        "text-transform:uppercase;margin-bottom:8px'>Browse Category</div>",
        unsafe_allow_html=True,
    )
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#7a7a8c;font-size:0.75rem;letter-spacing:0.1em;"
        "text-transform:uppercase;margin-bottom:8px'>Grid Columns</div>",
        unsafe_allow_html=True,
    )
    grid_cols = st.slider("Columns", 3, 8, 6, label_visibility="collapsed")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#4a4a5a;font-size:0.72rem;line-height:1.6'>"
        "Powered by TMDB · TF-IDF recommendations · Genre discovery</div>",
        unsafe_allow_html=True,
    )


# =============================
# HEADER
# =============================
col_title, col_spacer = st.columns([3, 1])
with col_title:
    st.markdown(
        "<p class='cinrec-logo'>CineRec</p>"
        "<p class='cinrec-sub'>Discover · Explore · Recommend</p>",
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)


# ======================================================
# VIEW: HOME
# ======================================================
if st.session_state.view == "home":

    search_col, _ = st.columns([2, 1])
    with search_col:
        typed = st.text_input(
            "Search",
            placeholder="🔍  Search a movie — avenger, batman, inception...",
            label_visibility="collapsed",
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── SEARCH MODE ──
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            with st.spinner("Searching..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)

                if suggestions:
                    labels = ["— Select a movie —"] + [s[0] for s in suggestions]
                    sel_col, _ = st.columns([2, 1])
                    with sel_col:
                        selected = st.selectbox(
                            "Suggestions",
                            labels,
                            index=0,
                            label_visibility="collapsed",
                        )
                    if selected != "— Select a movie —":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions. Try another keyword.")

                st.markdown(
                    "<div class='section-header'>🔎 Search Results</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(cards, cols=grid_cols, key_prefix="search")

        st.stop()

    # ── HOME FEED MODE ──
    label_map = {
        "trending": "🔥 Trending Today",
        "popular": "⭐ Popular Now",
        "top_rated": "🏆 Top Rated",
        "now_playing": "🎭 Now Playing",
        "upcoming": "🚀 Upcoming",
    }
    st.markdown(
        f"<div class='section-header'>{label_map.get(home_category, home_category)}</div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Loading movies..."):
        home_cards, err = api_get_json("/home", params={"category": home_category, "limit": 24})

    if err or not home_cards:
        st.error(f"Feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


# ======================================================
# VIEW: DETAILS
# ======================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id

    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # ── Top bar ──
    top_left, top_right = st.columns([5, 1])
    with top_right:
        st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
        if st.button("← Back"):
            goto_home()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Fetch Details ──
    with st.spinner("Loading movie details..."):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # ── Backdrop Banner ──
    if data.get("backdrop_url"):
        st.markdown(
            f"""
            <div style="
                width:100%;
                height:320px;
                border-radius:20px;
                overflow:hidden;
                position:relative;
                margin-bottom:1.5rem;
                animation: fadeIn 0.6s ease;
            ">
                <img src="{data['backdrop_url']}"
                     style="width:100%;height:100%;object-fit:cover;filter:brightness(0.55);" />
                <div style="
                    position:absolute;inset:0;
                    background:linear-gradient(to right,rgba(10,10,15,0.85) 0%,transparent 60%);
                    border-radius:20px;
                "></div>
                <div style="
                    position:absolute;bottom:28px;left:28px;
                    font-family:'Bebas Neue',sans-serif;
                    font-size:3rem;
                    letter-spacing:0.07em;
                    color:#fff;
                    text-shadow:0 4px 20px rgba(0,0,0,0.6);
                ">{data.get('title','')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Poster + Info ──
    left, right = st.columns([1, 2.6], gap="large")

    with left:
        if data.get("poster_url"):
            st.markdown(
                f"""
                <div style="
                    border-radius:16px;
                    overflow:hidden;
                    border:1px solid rgba(255,255,255,0.08);
                    box-shadow:0 20px 60px rgba(0,0,0,0.5);
                    animation:fadeUp 0.5s ease;
                ">
                    <img src="{data['poster_url']}" style="width:100%;display:block;" />
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div style='width:100%;aspect-ratio:2/3;background:var(--bg-card);"
                "border-radius:16px;display:flex;align-items:center;justify-content:center;"
                "font-size:3rem;color:var(--text-dim)'>🎬</div>",
                unsafe_allow_html=True,
            )

    with right:
        st.markdown("<div class='detail-card'>", unsafe_allow_html=True)

        if not data.get("backdrop_url"):
            st.markdown(
                f"<div class='detail-title'>{data.get('title','')}</div>",
                unsafe_allow_html=True,
            )

        # Genres as badges
        genres = data.get("genres", [])
        if genres:
            badges = "".join(f"<span class='badge'>{g['name']}</span>" for g in genres)
            st.markdown(f"<div style='margin:8px 0'>{badges}</div>", unsafe_allow_html=True)

        release = data.get("release_date") or "—"
        st.markdown(
            f"<div class='meta-line'>📅 Released: <strong>{release}</strong></div>",
            unsafe_allow_html=True,
        )

        overview = data.get("overview") or "No overview available."
        st.markdown(
            f"<div class='overview-text'>{overview}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Recommendations ──
    title = (data.get("title") or "").strip()

    if title:
        with st.spinner("Finding recommendations..."):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            tfidf_cards = to_cards_from_tfidf_items(bundle.get("tfidf_recommendations"))
            genre_cards = bundle.get("genre_recommendations", [])

            if tfidf_cards:
                st.markdown(
                    "<div class='section-header'>🔎 Similar Movies (TF-IDF)</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(tfidf_cards, cols=grid_cols, key_prefix="tfidf")

            if genre_cards:
                st.markdown(
                    "<div class='section-header'>🎭 More Like This (Genre)</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(genre_cards, cols=grid_cols, key_prefix="genre")

        else:
            st.info("Showing genre recommendations (fallback).")
            with st.spinner("Loading genre recs..."):
                genre_only, err3 = api_get_json(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )
            if not err3 and genre_only:
                st.markdown(
                    "<div class='section-header'>🎭 Genre Recommendations</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(genre_only, cols=grid_cols, key_prefix="genre_fallback")
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("Title unavailable — cannot compute recommendations.")