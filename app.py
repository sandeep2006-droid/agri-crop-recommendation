# ── DISTRICT SUMMARY ───────────────────────────────────────────────
if not df_d.empty:

    st.markdown(
        '<p class="section-label" style="margin-top:20px">District Summary</p>',
        unsafe_allow_html=True
    )

    avg_rain = df_d["Avg_Rainfall_mm"].iloc[0]
    num_crops = len(df_d)

    best_crop = (
        df_sorted.iloc[0]["Crop"].title()
        if not df_sorted.empty
        else "N/A"
    )

    st.markdown(
        f"""
        <div class="risk-panel">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;text-align:center;">
                
                <div style="background:#f5f2eb;border-radius:10px;padding:14px;">
                    <div style="font-size:1.4rem;font-weight:600;color:#1a3a2a;">
                        {avg_rain:.0f}
                        <span style="font-size:0.75rem;color:#7a8f82;">mm</span>
                    </div>
                    <div style="font-size:0.75rem;color:#7a8f82;margin-top:2px;">
                        Avg Rainfall
                    </div>
                </div>

                <div style="background:#f5f2eb;border-radius:10px;padding:14px;">
                    <div style="font-size:1.4rem;font-weight:600;color:#1a3a2a;">
                        {num_crops}
                    </div>
                    <div style="font-size:0.75rem;color:#7a8f82;margin-top:2px;">
                        Crops Tracked
                    </div>
                </div>

            </div>

            <div style="margin-top:10px;background:#e8f5e0;border-radius:10px;padding:12px;text-align:center;font-size:0.85rem;color:#1a5c35;">
                <span style="font-weight:600;">Top pick this season:</span>
                {best_crop}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
