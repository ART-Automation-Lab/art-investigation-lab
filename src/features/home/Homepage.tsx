import { useNavigate } from 'react-router-dom';
import './Homepage.css';

export function Homepage() {
  const navigate = useNavigate();

  return (
    <div className="hp-wrapper">
      <div className="hp-container">
        <div className="hp-hero-main">
          {/* LEFT COLUMN */}
          <div className="hp-hero-left">
            <div className="hp-label">ART INVESTIGATION LAB</div>
            <h1 className="hp-headline">
              Research.<br />
              Verify.<br />
              <span className="text-cyan">Prototype.</span>
            </h1>
            <p className="hp-description">
              Internal tool strictly for capability research,<br />
              logic verification, and rapid workflow prototyping.
            </p>
            <div className="hp-ctas">
              <button className="hp-cta-primary" onClick={() => navigate('/walkthrough')}>
                START WALKTHROUGH
              </button>
              <button className="hp-cta-secondary" onClick={() => navigate('/workflow')}>
                VIEW WORKFLOW
              </button>
            </div>
          </div>

          {/* RIGHT COLUMN */}
          <div className="hp-hero-right">
            <div className="hp-panel hp-protocol-panel">
              <h2 className="hp-panel-heading">INVESTIGATION PROTOCOL</h2>

              <div className="hp-pipeline-5">
                <div className="hp-stage">
                  <div className="hp-stage-num">01</div>
                  <div className="hp-stage-title">RESEARCH</div>
                  <div className="hp-stage-desc">Gather raw data<br />and business context</div>
                </div>
                <div className="hp-arrow">→</div>

                <div className="hp-stage">
                  <div className="hp-stage-num">02</div>
                  <div className="hp-stage-title">INVESTIGATE</div>
                  <div className="hp-stage-desc">Turn questions into<br />clear checkpoints</div>
                </div>
                <div className="hp-arrow">→</div>

                <div className="hp-stage">
                  <div className="hp-stage-num">03</div>
                  <div className="hp-stage-title">ANALYZE</div>
                  <div className="hp-stage-desc">Structure evidence<br />and build hypotheses</div>
                </div>
                <div className="hp-arrow">→</div>

                <div className="hp-stage">
                  <div className="hp-stage-num">04</div>
                  <div className="hp-stage-title">VALIDATE</div>
                  <div className="hp-stage-desc">Test logic and<br />finalize decisions</div>
                </div>
                <div className="hp-arrow">→</div>

                <div className="hp-stage">
                  <div className="hp-stage-num">05</div>
                  <div className="hp-stage-title">DELIVER</div>
                  <div className="hp-stage-desc">Generate structured<br />output file</div>
                </div>
              </div>
            </div>

            {/* SYSTEM ARCHITECTURE */}
            <div className="hp-architecture">
              <h2 className="hp-panel-heading">HOW THE SYSTEM WORKS</h2>
              <div className="hp-arch-surface">

                <div className="hp-arch-group">
                  <div className="hp-arch-title">art-opportunities-intelligence</div>
                  <div className="hp-arch-sub">RESEARCH REPOSITORY</div>
                  <p className="hp-arch-desc">Stores raw markdown notes,<br />evidence, and source files.</p>
                </div>

                <div className="hp-arch-connector">
                  <div className="hp-connector-line"></div>
                  <div className="hp-compiler-badge">
                    <span className="hp-compiler-name">Investigation Compiler</span>
                    <span className="hp-compiler-action">DATA CONVERSION</span>
                  </div>
                  <div className="hp-connector-line"></div>
                  <div className="hp-connector-arrow">▶</div>
                </div>

                <div className="hp-contract-node">
                  InvestigationBrief.json
                </div>

                <div className="hp-arch-connector simple">
                  <div className="hp-connector-line"></div>
                  <div className="hp-connector-arrow">▶</div>
                </div>

                <div className="hp-arch-group">
                  <div className="hp-arch-title">art-investigation-lab</div>
                  <div className="hp-arch-sub">WEB INTERFACE</div>
                  <p className="hp-arch-desc">Renders the JSON data into a<br />visual, interactive workspace.</p>
                </div>

              </div>
            </div>
          </div>
        </div>

        {/* OUTCOME STRIP */}
        <div className="hp-outcome-strip">
          <div className="hp-outcome-left">
            <div className="hp-outcome-label">SYSTEM OVERVIEW</div>
            <div className="hp-outcome-main">A specialized web interface for rendering and validating research data.</div>
          </div>
          <div className="hp-outcome-attrs">
            <span className="hp-attr">Clear Evidence Boundaries</span>
            <span className="hp-attr-dot">·</span>
            <span className="hp-attr">JSON-Powered UI</span>
            <span className="hp-attr-dot">·</span>
            <span className="hp-attr">Built-in Validation</span>
            <span className="hp-attr-dot">·</span>
            <span className="hp-attr">Independent Frontend</span>
          </div>
        </div>
      </div>
    </div>
  );
}
