import streamlit as st

st.set_page_config(
    page_title="AI Authenticity Engine",
    page_icon="🛡️",
    layout="wide",
)

# ==============================
# GLOBAL STYLING + CYBER EFFECT
# ==============================
st.markdown("""
<style>

/* Remove Streamlit top padding */
.block-container {
    padding-top: 2rem;
}

/* Prevent header clipping */
h1, h2, h3 {
    overflow: visible !important;
}

/* Remove Streamlit anchor link icons */
a[href^="#"] {
    display: none !important;
}

/* Disable text selection (light protection) */
body {
    user-select: none;
}

/* Animated gradient background */
body {
    background: linear-gradient(-45deg, #0E1117, #111827, #0F172A, #000814);
    background-size: 400% 400%;
    animation: gradient 18s ease infinite;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Fade transition */
.main {
    animation: fadeIn 0.6s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Title */
.main-title {
    font-size: 52px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 10px;
    letter-spacing: 1px;
}

.sub-title {
    font-size: 20px;
    text-align: center;
    color: #9FA6B2;
    margin-bottom: 60px;
}

/* Navigation Card */
.nav-card {
    background-color: rgba(22,27,34,0.75);
    padding: 50px 35px;
    border-radius: 22px;
    border: 1px solid #1f2937;
    text-align: center;
    transition: 0.3s ease;
    cursor: pointer;
}

.nav-card:hover {
    border: 1px solid #00E0FF;
    box-shadow: 0 0 35px rgba(0,224,255,0.35);
    transform: translateY(-6px);
}

/* Icon */
.icon {
    font-size: 55px;
    margin-bottom: 15px;
    transition: 0.3s ease;
}

.nav-card:hover .icon {
    text-shadow: 0 0 25px #00E0FF;
}

/* Description */
.card-desc {
    color: #9FA6B2;
    font-size: 16px;
}

/* Hide Streamlit button appearance */
.stButton>button {
    background: transparent;
    border: none;
    height: 0;
    padding: 0;
    margin: 0;
}

/* Particle canvas */
#particle-canvas {
    position: fixed;
    top: 0;
    left: 0;
    z-index: -1;
}
</style>

<canvas id="particle-canvas"></canvas>

<script>
const canvas = document.getElementById("particle-canvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];

class Particle {
    constructor(){
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.radius = Math.random() * 2;
        this.dx = (Math.random() - 0.5) * 0.6;
        this.dy = (Math.random() - 0.5) * 0.6;
    }
    draw(){
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = "#00E0FF";
        ctx.fill();
    }
    update(){
        this.x += this.dx;
        this.y += this.dy;

        if(this.x < 0 || this.x > canvas.width) this.dx *= -1;
        if(this.y < 0 || this.y > canvas.height) this.dy *= -1;

        this.draw();
    }
}

function init(){
    particles = [];
    for(let i = 0; i < 80; i++){
        particles.push(new Particle());
    }
}

function animate(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => p.update());
    requestAnimationFrame(animate);
}

init();
animate();
</script>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown('<div class="main-title">🛡️ Multilevel AI Authenticity Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Advanced Multi-Model Deepfake & Synthetic Media Detection System</div>', unsafe_allow_html=True)

# ==============================
# NAVIGATION
# ==============================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <a href="/Image_Forensics" target="_self" style="text-decoration: none;">
        <div class="nav-card">
            <div class="icon">🖼️</div>
            <h3>Image Forensics</h3>
            <p class="card-desc">
                Analyze a single image using Frequency, Face, and Semantic Experts.
            </p>
        </div>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <a href="/Video_Forensics" target="_self" style="text-decoration: none;">
        <div class="nav-card">
            <div class="icon">🎥</div>
            <h3>Video Forensics</h3>
            <p class="card-desc">
                Extract frames and evaluate AI-generated video probability.
            </p>
        </div>
    </a>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <a href="/Batch_Analysis" target="_self" style="text-decoration: none;">
        <div class="nav-card">
            <div class="icon">📂</div>
            <h3>Batch Analysis</h3>
            <p class="card-desc">
                Upload multiple images and evaluate them simultaneously.
            </p>
        </div>
    </a>
    """, unsafe_allow_html=True)

st.markdown("")
st.caption("Competition-Grade AI Forensics Evaluation System")