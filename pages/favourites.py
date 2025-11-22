import streamlit as st
import pandas as pd
import json
from datetime import datetime
from uuid import uuid4


def init_favourites_state():
    """Ensure favourites list exists in session_state."""
    if "favourites" not in st.session_state:
        st.session_state.favourites = []


def render_favourites_page():
    init_favourites_state()

    st.title("⭐ Favourites")
    st.caption("View, manage, and export your saved properties and predictions.")

    favourites = st.session_state.favourites

    # ---------- Empty state ----------
    if not favourites:
        st.info(
            "You don't have any favourites yet. "
            "Go to the prediction page and save some properties to see them here."
        )
        return

    # ---------- Controls: search, sort, export ----------
    st.markdown("### Manage Favourites")

    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:
        search_term = st.text_input(
            "Search favourites",
            placeholder="Search by city, state, title or notes...",
            key="fav_search_term",
        )

    with c2:
        sort_by = st.selectbox(
            "Sort by",
            options=[
                "Date Saved (Newest First)",
                "Date Saved (Oldest First)",
                "Price (High → Low)",
                "Price (Low → High)",
                "City (A → Z)",
            ],
            key="fav_sort_by",
        )

    with c3:
        # Export all favourites as CSV
        df_all = pd.DataFrame(favourites)
        csv_all = df_all.to_csv(index=False)
        st.download_button(
            label="📥 Download All as CSV",
            data=csv_all,
            file_name=f"favourites_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ---------- Filter favourites ----------
    filtered = favourites

    if search_term:
        search_lower = search_term.lower()
        filtered = [
            fav
            for fav in favourites
            if search_lower in json.dumps(fav, default=str).lower()
        ]

    # ---------- Sort favourites ----------
    def get_price(f):
        return f.get("predicted_price") or f.get("price") or 0

    def get_timestamp(f):
        # supports 'timestamp' as string; if not available, keep None
        ts = f.get("timestamp")
        if not ts:
            return None
        try:
            return datetime.fromisoformat(ts)
        except Exception:
            return ts  # could be any string

    if sort_by == "Date Saved (Newest First)":
        filtered = sorted(filtered, key=get_timestamp, reverse=True)
    elif sort_by == "Date Saved (Oldest First)":
        filtered = sorted(filtered, key=get_timestamp)
    elif sort_by == "Price (High → Low)":
        filtered = sorted(filtered, key=get_price, reverse=True)
    elif sort_by == "Price (Low → High)":
        filtered = sorted(filtered, key=get_price)
    elif sort_by == "City (A → Z)":
        filtered = sorted(filtered, key=lambda f: (f.get("city") or "").lower())

    st.markdown("### Saved Properties")

    # ---------- Render each favourite ----------
    for idx, fav in enumerate(filtered):
        # Graceful fallbacks
        title = fav.get("title") or f"{fav.get('bhk', 'N/A')}BHK Property"
        city = fav.get("city", "Unknown City")
        state = fav.get("state", "Unknown State")
        bhk = fav.get("bhk", "N/A")
        size_sqft = fav.get("size_sqft", fav.get("size", "N/A"))
        year_built = fav.get("year_built", "N/A")
        price = get_price(fav)
        timestamp = fav.get("timestamp", "N/A")

        st.markdown(
            """
            <div style="
                border-radius: 1rem;
                padding: 1.25rem;
                margin-bottom: 1rem;
                border: 1px solid rgba(148, 163, 184, 0.5);
                background: rgba(15, 23, 42, 0.02);
            ">
            """,
            unsafe_allow_html=True,
        )

        c_main, c_actions = st.columns([3, 1])

        with c_main:
            st.markdown(
                f"""
                <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem;">
                    {title}
                </div>
                <div style="font-size: 0.9rem; opacity: 0.7; margin-bottom: 0.5rem;">
                    📍 {city}, {state}
                </div>
                <div style="display: flex; gap: 1.5rem; font-size: 0.9rem; margin-bottom: 0.5rem;">
                    <span><strong>BHK:</strong> {bhk}</span>
                    <span><strong>Size:</strong> {size_sqft} sq.ft.</span>
                    <span><strong>Year:</strong> {year_built}</span>
                </div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #2563EB;">
                    ₹{price:,.2f} Lakhs
                </div>
                <div style="font-size: 0.8rem; opacity: 0.6; margin-top: 0.25rem;">
                    Saved on: {timestamp}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Note editor
            current_note = fav.get("note", "")
            new_note = st.text_area(
                "Personal note",
                value=current_note,
                key=f"fav_note_{idx}",
                label_visibility="collapsed",
                placeholder="Add a short note about this property (location pros/cons, seller info, etc.)",
                height=70,
            )

            if new_note != current_note:
                fav["note"] = new_note

        with c_actions:
            st.write("")  # spacing
            st.write("")

            # Remove button
            if st.button("🗑️ Remove", key=f"fav_remove_{idx}", use_container_width=True):
                # Remove from the original list in session_state
                try:
                    st.session_state.favourites.remove(fav)
                except ValueError:
                    pass
                st.success("Removed from favourites.")
                st.experimental_rerun()

            # View details in expander
            with st.expander("📄 View Details"):
                st.json(fav)

            # Export single favourite as JSON
            json_data = json.dumps(fav, indent=2, default=str)
            st.download_button(
                label="📥 Export JSON",
                data=json_data,
                file_name=f"favourite_{fav.get('id', idx)}.json",
                mime="application/json",
                key=f"fav_export_{idx}",
                use_container_width=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


# If this is in pages, just call render_favourites_page() at the bottom.
# Example:
if __name__ == "__main__":
    render_favourites_page()
