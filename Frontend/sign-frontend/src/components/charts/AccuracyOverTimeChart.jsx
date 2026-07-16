import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

// Mock data — swap for real data from Intern 4's Analytics API (Day 9)
const mockAccuracyData = [
  { day: "Mon", accuracy: 62 },
  { day: "Tue", accuracy: 68 },
  { day: "Wed", accuracy: 71 },
  { day: "Thu", accuracy: 75 },
  { day: "Fri", accuracy: 74 },
  { day: "Sat", accuracy: 81 },
  { day: "Sun", accuracy: 85 },
];

export default function AccuracyOverTimeChart({ data = mockAccuracyData }) {
  return (
    <div className="chart-card">
      <p className="label">Accuracy over time</p>
      <p className="chart-sub">Your sign recognition accuracy across the last 7 days.</p>

      <div style={{ width: "100%", height: 240 }}>
        <ResponsiveContainer>
          <LineChart data={data} margin={{ top: 5, right: 10, left: -10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--line)" />
            <XAxis
              dataKey="day"
              tick={{ fontSize: 12, fill: "var(--muted)" }}
              axisLine={{ stroke: "var(--line)" }}
              tickLine={false}
            />
            <YAxis
              domain={[0, 100]}
              tick={{ fontSize: 12, fill: "var(--muted)" }}
              axisLine={{ stroke: "var(--line)" }}
              tickLine={false}
              width={32}
            />
            <Tooltip
              formatter={(value) => [`${value}%`, "Accuracy"]}
              contentStyle={{
                fontSize: 12,
                borderRadius: 8,
                border: "1px solid var(--line)",
              }}
            />
            <Line
              type="monotone"
              dataKey="accuracy"
              stroke="var(--moss)"
              strokeWidth={2}
              dot={{ r: 3, fill: "var(--moss)" }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
