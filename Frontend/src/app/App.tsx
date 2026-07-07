import { useState } from "react";

// ── Wireframe primitives ─────────────────────────────────────────────

function Box({ w = 16, h = 16, className = "" }: { w?: number; h?: number; className?: string }) {
  return <div className={`border border-black bg-white shrink-0 ${className}`} style={{ width: w, height: h }} />;
}

function WInput({ label, placeholder }: { label: string; placeholder?: string }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
      <div style={{ fontSize: 11 }}>{label}</div>
      <div style={{
        border: "1px solid #999", height: 30, padding: "0 8px",
        display: "flex", alignItems: "center", fontSize: 11, color: "#aaa"
      }}>{placeholder || ""}</div>
    </div>
  );
}

function WBtn({ children, variant = "dark" }: { children: React.ReactNode; variant?: "dark" | "outline" }) {
  return (
    <div style={{
      border: "1px solid black",
      background: variant === "dark" ? "#222" : "#e0e0e0",
      color: variant === "dark" ? "white" : "black",
      height: 34, display: "flex", alignItems: "center",
      justifyContent: "center", fontSize: 11, fontWeight: 600,
      cursor: "default"
    }}>
      {children}
    </div>
  );
}

function Divider({ label }: { label?: string }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <div style={{ flex: 1, height: 1, background: "#ccc" }} />
      {label && <span style={{ fontSize: 10, color: "#999" }}>{label}</span>}
      {label && <div style={{ flex: 1, height: 1, background: "#ccc" }} />}
    </div>
  );
}

function BottomNav({ active }: { active: "home" | "lessons" | "practice" | "profile" }) {
  const items = ["Home", "Lessons", "Practice", "Profile"];
  const ids = ["home", "lessons", "practice", "profile"];
  return (
    <div style={{ borderTop: "1px solid #ccc", display: "flex" }}>
      {items.map((label, i) => (
        <div key={label} style={{
          flex: 1, display: "flex", flexDirection: "column",
          alignItems: "center", justifyContent: "center",
          padding: "8px 0", gap: 3,
          borderRight: i < items.length - 1 ? "1px solid #e8e8e8" : "none"
        }}>
          <Box w={14} h={14} className={ids[i] === active ? "bg-black" : ""} />
          <span style={{
            fontSize: 9, fontWeight: ids[i] === active ? 700 : 400,
            color: ids[i] === active ? "#000" : "#999"
          }}>{label}</span>
        </div>
      ))}
    </div>
  );
}

// ── Screen 1: Login ──────────────────────────────────────────────────

function LoginScreen() {
  const [showPw, setShowPw] = useState(false);
  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", padding: 20, gap: 14 }}>
      <div style={{ textAlign: "center", paddingTop: 12 }}>
        <Box w={40} h={40} className="mx-auto" />
        <div style={{ marginTop: 10, fontSize: 14, fontWeight: 700 }}>Sign in</div>
        <div style={{ fontSize: 10, color: "#666", marginTop: 4 }}>Log in by entering your email address and password</div>
      </div>
      <WInput label="Email address" placeholder="email@example.com" />
      <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
        <div style={{ fontSize: 11 }}>Password</div>
        <div style={{ border: "1px solid #999", height: 30, padding: "0 8px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <span style={{ fontSize: 11, color: "#aaa" }}>{showPw ? "password" : "••••••••"}</span>
          <button onClick={() => setShowPw(!showPw)} style={{ fontSize: 10, color: "#666", background: "none", border: "none", cursor: "pointer" }}>
            {showPw ? "hide" : "show"}
          </button>
        </div>
      </div>
      <div style={{ textAlign: "right" }}>
        <span style={{ fontSize: 10, color: "#666", textDecoration: "underline" }}>Forgot password?</span>
      </div>
      <WBtn>Log in</WBtn>
      <Divider label="or" />
      <WBtn variant="outline">Continue with Google</WBtn>
      <div style={{ flex: 1 }} />
      <div style={{ textAlign: "center", fontSize: 10, color: "#666" }}>
        {"Don't have an account? "}<span style={{ textDecoration: "underline", color: "#000", fontWeight: 600 }}>Sign up here</span>
      </div>
    </div>
  );
}

// ── Screen 2: Register ───────────────────────────────────────────────

function RegisterScreen() {
  const [checked, setChecked] = useState(false);
  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", padding: 20, gap: 12 }}>
      <div style={{ textAlign: "center", paddingTop: 12 }}>
        <Box w={40} h={40} className="mx-auto" />
        <div style={{ marginTop: 10, fontSize: 14, fontWeight: 700 }}>Create Your Account</div>
        <div style={{ fontSize: 10, color: "#666", marginTop: 4 }}>Start your sign language journey today</div>
      </div>
      <WBtn variant="outline">Continue with Google</WBtn>
      <Divider label="or" />
      <WInput label="Email address" placeholder="email@example.com" />
      <WInput label="Name" placeholder="Your full name" />
      <WInput label="Password" placeholder="••••••••" />
      <div
        onClick={() => setChecked(!checked)}
        style={{ display: "flex", alignItems: "flex-start", gap: 8, cursor: "pointer" }}
      >
        <div style={{ width: 12, height: 12, border: "1px solid #999", background: checked ? "#222" : "white", marginTop: 1, shrink: 0 }} />
        <span style={{ fontSize: 10, color: "#555", lineHeight: 1.4 }}>Receive news, updates and deals</span>
      </div>
      <div style={{ fontSize: 10, color: "#888", lineHeight: 1.4 }}>
        By creating an account you agree to our <span style={{ textDecoration: "underline" }}>Terms of Service</span> and <span style={{ textDecoration: "underline" }}>Privacy Policy</span>.
      </div>
      <WBtn>Create Account</WBtn>
      <div style={{ flex: 1 }} />
      <div style={{ textAlign: "center", fontSize: 10, color: "#666" }}>
        Already have an account? <span style={{ textDecoration: "underline", color: "#000", fontWeight: 600 }}>Log in</span>
      </div>
    </div>
  );
}

// ── Screen 3: Dashboard ──────────────────────────────────────────────

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ border: "1px solid #ccc", padding: "10px 8px", display: "flex", flexDirection: "column", gap: 6 }}>
      <Box w={16} h={16} />
      <div style={{ fontSize: 13, fontWeight: 700 }}>{value}</div>
      <div style={{ fontSize: 9, color: "#888" }}>{label}</div>
    </div>
  );
}

function LineChart() {
  return (
    <div style={{ border: "1px solid #ccc", padding: 10 }}>
      <div style={{ fontSize: 10, fontWeight: 600, marginBottom: 8 }}>Accuracy Over Time</div>
      <svg viewBox="0 0 200 48" style={{ width: "100%", height: 48 }}>
        <line x1="0" y1="48" x2="200" y2="48" stroke="#ccc" strokeWidth="1" />
        <line x1="0" y1="0" x2="0" y2="48" stroke="#ccc" strokeWidth="1" />
        <polyline
          points="0,38 33,28 66,32 100,18 133,22 166,10 200,8"
          fill="none" stroke="#333" strokeWidth="1.5"
        />
      </svg>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 9, color: "#aaa", marginTop: 4 }}>
        {["Mon","Tue","Wed","Thu","Fri","Sat","Sun"].map(d => <span key={d}>{d}</span>)}
      </div>
    </div>
  );
}

function DashboardScreen() {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ padding: "14px 16px", borderBottom: "1px solid #e0e0e0", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <div style={{ fontSize: 10, color: "#999" }}>Good morning,</div>
          <div style={{ fontSize: 13, fontWeight: 700 }}>Alex</div>
        </div>
        <Box w={28} h={28} />
      </div>
      <div style={{ flex: 1, overflowY: "auto", padding: 14, display: "flex", flexDirection: "column", gap: 14 }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
          <StatCard label="Accuracy" value="87%" />
          <StatCard label="Lessons" value="12/24" />
          <StatCard label="Hours" value="8:30" />
          <StatCard label="Progress" value="12%" />
        </div>
        <LineChart />
        <div>
          <div style={{ fontSize: 10, fontWeight: 600, marginBottom: 8, display: "flex", justifyContent: "space-between" }}>
            <span>Recommended</span>
            <span style={{ fontWeight: 400, color: "#888" }}>See all</span>
          </div>
          <div style={{ display: "flex", gap: 8, overflowX: "auto", paddingBottom: 4 }}>
            {["Alphabet A-Z", "Greetings", "Numbers 1-20"].map(t => (
              <div key={t} style={{ border: "1px solid #ccc", padding: 8, minWidth: 110, display: "flex", flexDirection: "column", gap: 6, flexShrink: 0 }}>
                <Box w={32} h={24} />
                <div style={{ fontSize: 10, fontWeight: 600 }}>{t}</div>
                <div style={{ height: 4, background: "#e8e8e8", border: "1px solid #ccc" }}>
                  <div style={{ width: "60%", height: "100%", background: "#555" }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      <BottomNav active="home" />
    </div>
  );
}

// ── Screen 4: Lessons ────────────────────────────────────────────────

const LESSONS = [
  { title: "Alphabet A-Z", level: "Beginner", progress: 75 },
  { title: "Common Greetings", level: "Beginner", progress: 30 },
  { title: "Numbers 1–20", level: "Beginner", progress: 0 },
  { title: "Family & Relations", level: "Intermediate", progress: 10 },
  { title: "Colors & Shapes", level: "Intermediate", progress: 0 },
  { title: "Sentences", level: "Advanced", progress: 0 },
];

function LessonsScreen() {
  const [filter, setFilter] = useState("All");
  const filters = ["All", "Beginner", "Intermediate", "Advanced"];
  const filtered = filter === "All" ? LESSONS : LESSONS.filter(l => l.level === filter);
  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ padding: "14px 16px", borderBottom: "1px solid #e0e0e0", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ fontSize: 13, fontWeight: 700 }}>Lessons</div>
        <Box w={28} h={28} />
      </div>
      <div style={{ padding: "10px 14px 6px", display: "flex", gap: 6, flexWrap: "wrap" }}>
        {filters.map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            style={{
              border: "1px solid #999", padding: "4px 10px",
              fontSize: 10, fontWeight: filter === f ? 700 : 400,
              background: filter === f ? "#222" : "#e8e8e8",
              color: filter === f ? "white" : "black",
              cursor: "pointer"
            }}
          >
            {f}
          </button>
        ))}
      </div>
      <div style={{ flex: 1, overflowY: "auto", padding: "4px 14px 10px", display: "flex", flexDirection: "column", gap: 8 }}>
        {filtered.map(lesson => (
          <div key={lesson.title} style={{ border: "1px solid #ccc", padding: 10, display: "flex", gap: 10, alignItems: "center" }}>
            <Box w={36} h={36} />
            <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 5 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontSize: 11, fontWeight: 600 }}>{lesson.title}</span>
                <span style={{ fontSize: 9, border: "1px solid #ccc", padding: "1px 6px", background: "#f0f0f0" }}>{lesson.level}</span>
              </div>
              <div style={{ height: 4, background: "#e8e8e8", border: "1px solid #ccc" }}>
                <div style={{ width: `${lesson.progress}%`, height: "100%", background: "#333" }} />
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontSize: 9, color: "#888" }}>{lesson.progress}% complete</span>
                <button style={{ fontSize: 9, fontWeight: 600, border: "1px solid #333", background: "#222", color: "white", padding: "2px 8px", cursor: "pointer" }}>
                  {lesson.progress > 0 ? "Continue" : "Start"}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
      <BottomNav active="lessons" />
    </div>
  );
}

// ── Screen 5: Practice ───────────────────────────────────────────────

function PracticeScreen() {
  const [target, setTarget] = useState("A");
  const letters = Array.from({ length: 10 }, (_, i) => String.fromCharCode(65 + i));
  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ padding: "14px 16px", borderBottom: "1px solid #e0e0e0", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ fontSize: 13, fontWeight: 700 }}>Practice</div>
        <div style={{ border: "1px solid #ccc", padding: "4px 10px", fontSize: 11, fontFamily: "monospace" }}>0:00</div>
      </div>
      <div style={{ flex: 1, overflowY: "auto", padding: 14, display: "flex", flexDirection: "column", gap: 12 }}>
        {/* Camera box */}
        <div style={{
          border: "1px dashed #999", height: 140,
          display: "flex", flexDirection: "column",
          alignItems: "center", justifyContent: "center", gap: 8, background: "#f8f8f8"
        }}>
          <Box w={32} h={24} />
          <span style={{ fontSize: 10, color: "#888" }}>Position your hand in the frame</span>
        </div>
        {/* Buttons */}
        <div style={{ display: "flex", gap: 8 }}>
          <div style={{ flex: 1 }}><WBtn>Start Practice</WBtn></div>
          <WBtn variant="outline">Stop</WBtn>
        </div>
        {/* Target sign */}
        <div style={{ border: "1px solid #ccc", padding: 10, display: "flex", alignItems: "center", gap: 10 }}>
          <Box w={36} h={36} />
          <div>
            <div style={{ fontSize: 9, color: "#888" }}>Target Sign</div>
            <div style={{ fontSize: 24, fontWeight: 700, lineHeight: 1.1 }}>{target}</div>
          </div>
        </div>
        {/* Letter picker */}
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
          {letters.map(l => (
            <button
              key={l}
              onClick={() => setTarget(l)}
              style={{
                width: 28, height: 28, border: "1px solid #999",
                background: target === l ? "#222" : "#e8e8e8",
                color: target === l ? "white" : "black",
                fontSize: 11, fontWeight: 600, cursor: "pointer"
              }}
            >
              {l}
            </button>
          ))}
        </div>
        {/* Session Results */}
        <div style={{ border: "1px solid #ccc", padding: 10 }}>
          <div style={{ fontSize: 10, fontWeight: 600, marginBottom: 8 }}>Session Results</div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
            {["Predicted Sign", "Confidence", "Accuracy", "Feedback"].map(label => (
              <div key={label}>
                <div style={{ fontSize: 9, color: "#888" }}>{label}</div>
                <div style={{ fontSize: 11, color: "#ccc", marginTop: 2 }}>—</div>
              </div>
            ))}
          </div>
          <div style={{ fontSize: 9, color: "#aaa", marginTop: 8, fontStyle: "italic" }}>Not started</div>
        </div>
      </div>
      <BottomNav active="practice" />
    </div>
  );
}

// ── Frame wrapper ────────────────────────────────────────────────────

function Frame({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12, flexShrink: 0 }}>
      <div style={{
        width: 300, height: 620,
        background: "white",
        border: "1px solid #bbb",
        overflow: "hidden",
        fontFamily: "sans-serif",
      }}>
        {children}
      </div>
      <span style={{ fontSize: 11, fontWeight: 600, color: "#666", letterSpacing: "0.05em", textTransform: "uppercase" }}>
        {label}
      </span>
    </div>
  );
}

// ── Root ─────────────────────────────────────────────────────────────

export default function App() {
  return (
    <div style={{
      minHeight: "100vh", background: "#d8d8d8",
      display: "flex", alignItems: "flex-start",
      justifyContent: "flex-start",
      padding: 40, overflowX: "auto"
    }}>
      <div style={{ display: "flex", gap: 32, alignItems: "flex-start" }}>
        <Frame label="01 — Login"><LoginScreen /></Frame>
        <Frame label="02 — Register"><RegisterScreen /></Frame>
        <Frame label="03 — Dashboard"><DashboardScreen /></Frame>
        <Frame label="04 — Lessons"><LessonsScreen /></Frame>
        <Frame label="05 — Practice"><PracticeScreen /></Frame>
      </div>
    </div>
  );
}
