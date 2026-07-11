
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IDENT//SCAN — Face Dossier Terminal</title>
<style>
  :root{
    --bg: #0B0E11;
    --panel: #12161B;
    --line: #232A32;
    --text: #E8E6DF;
    --text-dim: #8A9099;
    --amber: #F2B85C;
    --cyan: #5CC8F2;
    --danger: #F2705C;
    --mono: 'Space Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }

  @media (prefers-reduced-motion: reduce){
    *{ animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
  }

  *{ box-sizing: border-box; margin:0; padding:0; }

  html,body{
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    min-height: 100vh;
  }

  body{
    background-image:
      linear-gradient(var(--line) 1px, transparent 1px),
      linear-gradient(90deg, var(--line) 1px, transparent 1px);
    background-size: 42px 42px;
    background-position: -1px -1px;
  }

  a{ color: inherit; }

  /* ---------- Top bar ---------- */
  .topbar{
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding: 20px clamp(20px, 5vw, 64px);
    border-bottom: 1px solid var(--line);
    background: rgba(11,14,17,0.85);
    backdrop-filter: blur(6px);
    position: sticky;
    top:0;
    z-index: 20;
  }

  .brand{
    display:flex;
    align-items:center;
    gap:10px;
    font-family: var(--mono);
    letter-spacing: 0.08em;
    font-size: 15px;
    text-transform: uppercase;
  }

  .brand .dot{
    width:8px; height:8px; border-radius:50%;
    background: var(--amber);
    box-shadow: 0 0 8px var(--amber);
  }

  .topbar nav{
    display:flex;
    gap: clamp(14px, 3vw, 32px);
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: 0.06em;
    color: var(--text-dim);
    text-transform: uppercase;
  }

  .topbar nav span.n{ color: var(--cyan); margin-right: 6px; }

  /* ---------- Hero ---------- */
  .hero{
    padding: clamp(28px, 5vw, 56px) clamp(20px, 5vw, 64px) 20px;
    max-width: 1280px;
    margin: 0 auto;
  }

  .eyebrow{
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--amber);
    display:flex;
    align-items:center;
    gap: 10px;
    margin-bottom: 18px;
  }

  .eyebrow::before{
    content:"";
    width: 26px; height: 1px;
    background: var(--amber);
  }

  h1{
    font-family: var(--mono);
    font-weight: 700;
    font-size: clamp(28px, 5vw, 46px);
    line-height: 1.15;
    letter-spacing: -0.01em;
    max-width: 18ch;
  }

  h1 em{
    font-style: normal;
    color: var(--cyan);
  }

  .lede{
    margin-top: 16px;
    max-width: 56ch;
    color: var(--text-dim);
    font-size: 15px;
    line-height: 1.6;
  }

  /* ---------- Layout: scanner + dossier ---------- */
  .stage{
    display:grid;
    grid-template-columns: minmax(0, 1.1fr) minmax(280px, 0.9fr);
    gap: 24px;
    max-width: 1280px;
    margin: 32px auto 0;
    padding: 0 clamp(20px, 5vw, 64px);
    align-items: start;
  }

  @media (max-width: 880px){
    .stage{ grid-template-columns: 1fr; }
  }

  /* ---------- Camera viewport ---------- */
  .viewport{
    position: relative;
    background: #05070A;
    border: 1px solid var(--line);
    border-radius: 4px;
    aspect-ratio: 4/3;
    overflow: hidden;
  }

  .viewport video{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display:block;
    transform: scaleX(-1);
    filter: saturate(0.85) contrast(1.05);
  }

  .viewport .placeholder{
    position:absolute;
    inset:0;
    display:flex;
    flex-direction: column;
    align-items:center;
    justify-content:center;
    gap: 18px;
    color: var(--text-dim);
    font-family: var(--mono);
    text-align:center;
    padding: 20px;
  }

  .placeholder .glyph{
    width: 56px; height: 56px;
    border: 1px solid var(--line);
    border-radius: 50%;
    display:flex; align-items:center; justify-content:center;
    color: var(--cyan);
    font-size: 22px;
  }

  #enableCam{
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    background: transparent;
    color: var(--amber);
    border: 1px solid var(--amber);
    padding: 10px 20px;
    border-radius: 2px;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
  }

  #enableCam:hover{ background: var(--amber); color: #0B0E11; }
  #enableCam:focus-visible, a:focus-visible, button:focus-visible{
    outline: 2px solid var(--cyan);
    outline-offset: 3px;
  }

  /* corner brackets */
  .corner{
    position:absolute;
    width: 26px; height: 26px;
    border: 2px solid var(--cyan);
    opacity: 0.85;
  }
  .corner.tl{ top:14px; left:14px; border-right:none; border-bottom:none; }
  .corner.tr{ top:14px; right:14px; border-left:none; border-bottom:none; }
  .corner.bl{ bottom:14px; left:14px; border-right:none; border-top:none; }
  .corner.br{ bottom:14px; right:14px; border-left:none; border-top:none; }

  /* scan line sweep */
  .scanline{
    position:absolute;
    left:0; right:0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    box-shadow: 0 0 12px 2px var(--cyan);
    top:0;
    animation: sweep 3.4s ease-in-out infinite;
    opacity: 0;
  }

  .viewport.active .scanline{ opacity: 0.9; }

  @keyframes sweep{
    0%{ top: 6%; }
    50%{ top: 92%; }
    100%{ top: 6%; }
  }

  .statusbar{
    position:absolute;
    left:0; right:0; bottom:0;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding: 10px 14px;
    background: linear-gradient(0deg, rgba(0,0,0,0.75), transparent);
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-dim);
  }

  .statusbar .led{
    display:inline-block;
    width:7px; height:7px;
    border-radius:50%;
    background: var(--text-dim);
    margin-right: 6px;
  }

  .viewport.active .statusbar .led{
    background: var(--cyan);
    box-shadow: 0 0 6px var(--cyan);
  }

  /* ---------- Dossier panels ---------- */
  .dossier{
    display:flex;
    flex-direction: column;
    gap: 20px;
  }

  .panel{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 4px;
    overflow: hidden;
  }

  .panel-head{
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding: 14px 18px;
    border-bottom: 1px solid var(--line);
  }

  .panel-head h2{
    font-family: var(--mono);
    font-size: 13px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text);
  }

  .panel-head .tag{
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 0.08em;
    color: var(--amber);
    border: 1px solid var(--amber);
    border-radius: 2px;
    padding: 2px 8px;
    text-transform: uppercase;
  }

  .panel-head.cyan .tag{ color: var(--cyan); border-color: var(--cyan); }

  .rows{ padding: 6px 18px 14px; }

  .row{
    display:flex;
    align-items:baseline;
    justify-content:space-between;
    gap: 12px;
    padding: 11px 0;
    border-bottom: 1px dashed var(--line);
  }

  .row:last-child{ border-bottom: none; }

  .row .k{
    font-family: var(--mono);
    font-size: 12px;
    color: var(--text-dim);
    letter-spacing: 0.04em;
  }

  .row .v{
    font-family: var(--mono);
    font-size: 13px;
    color: var(--text);
    text-align: right;
  }

  .row .v.pending{
    color: var(--text-dim);
  }

  .row .v.pending::after{
    content: "";
    display:inline-block;
    width: 6px; height: 6px;
    margin-left: 8px;
    border-radius: 50%;
    background: var(--text-dim);
  }

  .confidence-bar{
    height: 4px;
    background: var(--line);
    border-radius: 2px;
    overflow: hidden;
    margin: 4px 0 2px;
  }

  .confidence-bar span{
    display:block;
    height: 100%;
    width: 0%;
    background: var(--cyan);
  }

  /* ---------- footer note ---------- */
  .footnote{
    max-width: 1280px;
    margin: 28px auto 60px;
    padding: 14px clamp(20px, 5vw, 64px);
  }

  .footnote p{
    font-family: var(--mono);
    font-size: 11.5px;
    color: var(--text-dim);
    letter-spacing: 0.03em;
    border-left: 2px solid var(--line);
    padding-left: 14px;
    line-height: 1.6;
  }

  .footnote strong{ color: var(--amber); font-weight: 400; }
</style>
</head>
<body>

  <header class="topbar">
    <div class="brand"><span class="dot"></span> IDENT // SCAN</div>
    <nav>
      <span><span class="n">01</span>Viewport</span>
      <span><span class="n">02</span>Identity</span>
      <span><span class="n">03</span>Attributes</span>
    </nav>
  </header>

  <section class="hero">
    <div class="eyebrow">Local face dossier terminal</div>
    <h1>Point the camera at yourself. <em>Read the file it builds.</em></h1>
    <p class="lede">
      A live viewport on the left, a two-part dossier on the right — one panel for
      how you show up online, one for what a face alone can estimate. The layout
      is wired up; the detection engine plugs in later.
    </p>
  </section>

  <div class="stage">
    <!-- Camera viewport -->
    <div class="viewport" id="viewport">
      <video id="video" autoplay playsinline muted></video>

      <div class="placeholder" id="placeholder">
        <div class="glyph">◎</div>
        <div>
          <div style="color:var(--text); font-size:13px; margin-bottom:10px;">CAMERA STANDBY</div>
          <button id="enableCam" type="button">Enable Camera</button>
        </div>
      </div>

      <div class="corner tl"></div>
      <div class="corner tr"></div>
      <div class="corner bl"></div>
      <div class="corner br"></div>
      <div class="scanline"></div>

      <div class="statusbar">
        <span><span class="led"></span><span id="statusText">Standby</span></span>
        <span id="clock">00:00:00</span>
      </div>
    </div>

    <!-- Dossier -->
    <div class="dossier">

      <div class="panel">
        <div class="panel-head">
          <h2>Digital Identity</h2>
          <span class="tag">Awaiting model</span>
        </div>
        <div class="rows">
          <div class="row"><span class="k">Matched name</span><span class="v pending">—</span></div>
          <div class="row"><span class="k">Known aliases</span><span class="v pending">—</span></div>
          <div class="row"><span class="k">Linked platforms</span><span class="v pending">—</span></div>
          <div class="row"><span class="k">Public mentions</span><span class="v pending">—</span></div>
          <div class="row">
            <span class="k">Match confidence</span>
            <span class="v pending">0%</span>
          </div>
        </div>
        <div style="padding: 0 18px 16px;">
          <div class="confidence-bar"><span id="idConfidence"></span></div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-head cyan">
          <h2>Estimated Attributes</h2>
          <span class="tag">Awaiting model</span>
        </div>
        <div class="rows">
          <div class="row"><span class="k">Estimated age</span><span class="v pending">—</span></div>
          <div class="row"><span class="k">Perceived gender</span><span class="v pending">—</span></div>
          <div class="row"><span class="k">Dominant emotion</span><span class="v pending">—</span></div>
          <div class="row"><span class="k">Head pose</span><span class="v pending">—</span></div>
          <div class="row">
            <span class="k">Estimate confidence</span>
            <span class="v pending">0%</span>
          </div>
        </div>
        <div style="padding: 0 18px 16px;">
          <div class="confidence-bar"><span id="attrConfidence"></span></div>
        </div>
      </div>

    </div>
  </div>

  <div class="footnote">
    <p>
      <strong>Note —</strong> this page only requests camera access and displays the
      feed. No face detection, recognition, or age-estimation model is wired in yet —
      every value above is a placeholder waiting on that logic.
    </p>
  </div>

<script>
  // Minimal JS: needed only to request the webcam feed and drive the
  // standby/active UI state. No detection logic lives here — plug that
  // in later against #video (and swap the placeholders in the dossier).

  const video = document.getElementById('video');
  const viewport = document.getElementById('viewport');
  const placeholder = document.getElementById('placeholder');
  const enableBtn = document.getElementById('enableCam');
  const statusText = document.getElementById('statusText');
  const clockEl = document.getElementById('clock');

  function tick(){
    const now = new Date();
    const pad = n => String(n).padStart(2, '0');
    clockEl.textContent = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
  }
  setInterval(tick, 1000);
  tick();

  enableBtn.addEventListener('click', async () => {
    statusText.textContent = 'Requesting…';
    try{
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      video.srcObject = stream;
      placeholder.style.display = 'none';
      viewport.classList.add('active');
      statusText.textContent = 'Live';
    }catch(err){
      statusText.textContent = 'Access denied';
      placeholder.querySelector('div div').textContent = 'CAMERA UNAVAILABLE';
      console.error('Camera error:', err);
    }
  });
</script>

</body>
</html>
