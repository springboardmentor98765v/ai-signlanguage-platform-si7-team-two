import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

// Mock data — swap for real data from Intern 4's Analytics API (Day 9)
const mockLessonsData = [
  { week: "Week 1", lessons: 3 },
  { week: "Week 2", lessons: 5 },
  { week: "Week 3", lessons: 4 },
  { week: "Week 4", lessons: 7 },
];

export default function LessonsCompletedChart({ data = mockLessonsData }) {
  return (
    <div className="chart-card">
      <p className="label">Lessons completed</p>
      <p className="chart-sub">Number of lessons you finished each week.</p>

      <div style={{ width: "100%", height: 240 }}>
        <ResponsiveContainer>
          <BarChart data={data} margin={{ top: 5, right: 10, left: -10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--line)" vertical={false} />
            <XAxis
              dataKey="week"
              tick={{ fontSize: 12, fill: "var(--muted)" }}
              axisLine={{ stroke: "var(--line)" }}
              tickLine={false}
            />
            <YAxis
              allowDecimals={false}
              tick={{ fontSize: 12, fill: "var(--muted)" }}
              axisLine={{ stroke: "var(--line)" }}
              tickLine={false}
              width={28}
            />
            <Tooltip
              formatter={(value) => [value, "Lessons"]}
              contentStyle={{
                fontSize: 12,
                borderRadius: 8,
                border: "1px solid var(--line)",
              }}
              cursor={{ fill: "var(--paper)" }}
            />
            <Bar dataKey="lessons" fill="var(--moss)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
