import streamlit as st

def load_feature_section():
    # --- Custom CSS aligned with the Classic Corporate (Blue & Neutrals) palette ---
    st.markdown("""
        <style>
        :root {
            --primary-color: #003366;      /* Navy Blue */
            --secondary-bg: #CCCCCC;       /* Light Gray */
            --accent-color: #FF6600;       /* Bright Orange */
            --background-color: #FFFFFF;   /* White */
            --text-color: #1C1C1C;         /* Charcoal Text */
        }

        /* ==== Global Section Styling ==== */
        .section-header {
            color: var(--primary-color);
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .section-subtext {
            color: var(--text-color);
            text-align: center;
            font-size: 1rem;
            margin-bottom: 2rem;
        }

        /* ==== Feature Cards ==== */
        .feature-card {
            background-color: var(--secondary-bg);
            border-radius: 18px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-top: 4px solid var(--primary-color);
        }
        .feature-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            border-top: 4px solid var(--accent-color);
        }
        .feature-card h4 {
            color: var(--primary-color);
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }
        .feature-card p {
            color: var(--text-color);
            font-size: 0.95rem;
        }

        /* ==== Testimonials ==== */
        .testimonial-box {
            background-color: #F2F6F6; /* Off-white */
            border-left: 5px solid var(--primary-color);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        .testimonial-box:hover {
            border-left: 5px solid var(--accent-color);
        }
        .testimonial-box p {
            color: var(--text-color);
            font-size: 0.95rem;
        }
        .testimonial-box b {
            color: var(--primary-color);
        }

        /* ==== Footer ==== */
        .footer {
            text-align: center;
            color: var(--text-color);
            font-size: 14px;
            padding: 30px 0 15px 0;
            border-top: 1px solid var(--secondary-bg);
            background-color: var(--background-color);
        }
        .footer a {
            color: var(--accent-color);
            text-decoration: none;
        }
        .footer a:hover {
            color: #e55b00;
        }

        /* ==== Responsive ==== */
        @media (max-width: 768px) {
            .feature-card { padding: 15px; }
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Features Section ---
    st.markdown("<h2 class='section-header'>🌟 Why Choose SmartBricks?</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtext'>Our AI-powered platform ensures smarter, faster and more reliable property valuations.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown("<div class='feature-card'>"
                    "<img src='https://cdn-icons-png.flaticon.com/512/1077/1077012.png' width='60'>"
                    "<h4>AI Price Prediction</h4>"
                    "<p>Get accurate property valuation instantly using advanced ML models.</p>"
                    "</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-card'>"
                    "<img src='https://cdn-icons-png.flaticon.com/512/3176/3176366.png' width='60'>"
                    "<h4>Smart Insights</h4>"
                    "<p>Understand real-time market trends and make informed investment decisions.</p>"
                    "</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='feature-card'>"
                    "<img src='https://cdn-icons-png.flaticon.com/512/2769/2769339.png' width='60'>"
                    "<h4>Compare Properties</h4>"
                    "<p>Evaluate listings side by side based on area, pricing, and demand data.</p>"
                    "</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Testimonials Section ---
    st.markdown("<h2 class='section-header'>💬 What Our Users Say</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtext'>Real experiences from our happy clients and users.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<div class='testimonial-box'>"
                    "<p>“SmartBricks made our property evaluation 3x faster and more reliable. Love the interface!”</p>"
                    "<b>– Riya Sharma, Realtor</b>"
                    "</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='testimonial-box'>"
                    "<p>“Highly accurate predictions. It’s like having a real estate expert in your pocket.”</p>"
                    "<b>– Arjun Verma, Home Buyer</b>"
                    "</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
        <div class='footer'>
            © 2025 <b>SmartBricks</b> | All Rights Reserved <br>
            Built with ❤️ using <a href='https://streamlit.io/' target='_blank'>Streamlit</a> and AI
        </div>
    """, unsafe_allow_html=True)
