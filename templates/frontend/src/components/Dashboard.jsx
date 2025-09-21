import { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const COLORS = ["#10B981", "#EF4444", "#F59E0B"]; // green, red, amber

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/dashboard") // Flask API endpoint
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error("Error fetching dashboard data:", err));
  }, []);

  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-screen text-gray-600">
        Loading dashboard...
      </div>
    );
  }

  return (
    <section className="bg-gray-50 min-h-screen py-12 px-6">
      <div className="max-w-7xl mx-auto">
        {/* Title */}
        <h1 className="text-3xl font-extrabold text-gray-900 mb-8">
          Verification Reports
        </h1>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          {/* Pie Chart */}
          <div className="bg-white p-6 rounded-2xl shadow">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              Verification Breakdown
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={data.pieData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {data.pieData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Bar Chart */}
          <div className="bg-white p-6 rounded-2xl shadow">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              Verifications per Day
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3B82F6" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Results Table */}
        <div className="bg-white p-6 rounded-2xl shadow">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Recent Verifications
          </h2>
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-100 text-left">
                <th className="p-3 text-gray-700">ID</th>
                <th className="p-3 text-gray-700">News Snippet</th>
                <th className="p-3 text-gray-700">Status</th>
              </tr>
            </thead>
            <tbody>
              {data.recentResults.map((row) => (
                <tr key={row.id} className="border-b hover:bg-gray-50">
                  <td className="p-3">{row.id}</td>
                  <td className="p-3 text-gray-600">{row.text}</td>
                  <td
                    className={`p-3 font-medium ${
                      row.status === "Real"
                        ? "text-green-600"
                        : row.status === "Fake"
                        ? "text-red-600"
                        : "text-yellow-600"
                    }`}
                  >
                    {row.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
