import React, { useState, useEffect } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

function App() {
  // 1. Dashboard States
  const [distance, setDistance] = useState(5.0);
  const [hour, setHour] = useState(12);
  const [traffic, setTraffic] = useState(1.0);
  const [weather, setWeather] = useState("Clear");
  const [price, setPrice] = useState(0.0);
  
  // 2. State for the Chart History (Tracks past predictions)
  const [history, setHistory] = useState([]);

  // 3. Function to talk to the Python AI Server
  const fetchPrediction = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", {
        hour: parseInt(hour),
        weather: weather,
        distance: parseFloat(distance),
        traffic_multiplier: parseFloat(traffic),
      });

      const predictedPrice = response.data.predicted_price;
      setPrice(predictedPrice);

      // Add prediction to chart history
      setHistory((prev) => [
        ...prev.slice(-9), // Keep only the last 10 guesses
        { name: `${distance}mi`, Price: predictedPrice },
      ]);
    } catch (error) {
      console.error("Error communicating with AI server:", error);
    }
  };

  useEffect(() => {
    fetchPrediction();
  }, [distance, hour, traffic, weather]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center p-6 font-sans">
      {/* Header */}
      <header className="text-center my-8">
        <h1 className="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
          SURGE: AI Pricing Engine
        </h1>
        <p className="text-slate-400 mt-2">Real-time predictive taxi surge algorithm</p>
      </header>

      {/* Main Grid */}
      <div className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Left Side: Controls */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-6">
          <h2 className="text-xl font-bold border-b border-slate-800 pb-3">Environmental Parameters</h2>

          {/* Distance Slider */}
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-slate-400">Ride Distance</span>
              <span className="font-semibold text-indigo-400">{distance} miles</span>
            </div>
            <input
              type="range"
              min="1.0"
              max="20.0"
              step="0.5"
              value={distance}
              onChange={(e) => setDistance(parseFloat(e.target.value))}
              className="w-full accent-indigo-500 cursor-pointer"
            />
          </div>

          {/* Hour Slider */}
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-slate-400">Time of Day</span>
              <span className="font-semibold text-indigo-400">{hour}:00</span>
            </div>
            <input
              type="range"
              min="0"
              max="23"
              step="1"
              value={hour}
              onChange={(e) => setHour(parseInt(e.target.value))}
              className="w-full accent-indigo-500 cursor-pointer"
            />
          </div>

          {/* Traffic Slider */}
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-slate-400">Traffic Density</span>
              <span className="font-semibold text-indigo-400">{traffic}x (Multiplier)</span>
            </div>
            <input
              type="range"
              min="0.8"
              max="2.5"
              step="0.1"
              value={traffic}
              onChange={(e) => setTraffic(parseFloat(e.target.value))}
              className="w-full accent-indigo-500 cursor-pointer"
            />
          </div>

          {/* Weather Selector */}
          <div>
            <label className="block text-sm text-slate-400 mb-2">Weather Condition</label>
            <div className="grid grid-cols-3 gap-3">
              {["Clear", "Rain", "Snow"].map((type) => (
                <button
                  key={type}
                  onClick={() => setWeather(type)}
                  className={`py-2 px-4 rounded-lg font-semibold border transition-all ${
                    weather === type
                      ? "bg-indigo-600 border-indigo-500 text-white"
                      : "bg-slate-800 border-slate-700 hover:border-slate-600 text-slate-300"
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Side: AI Price Output & Graph */}
        <div className="space-y-6">
          {/* Output Card */}
          <div className="bg-gradient-to-br from-indigo-900/40 to-slate-900 border border-indigo-500/30 p-8 rounded-2xl flex flex-col items-center justify-center shadow-2xl relative overflow-hidden">
            <span className="text-sm tracking-wider uppercase text-indigo-400 font-bold mb-2">Predicted Ride Fare</span>
            <span className="text-6xl font-extrabold tracking-tight text-white mb-1">
              ${price.toFixed(2)}
            </span>
            <span className="text-xs text-slate-500">FastAPI Model Active</span>
          </div>

          {/* History Chart */}
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl h-64 flex flex-col">
            <h3 className="text-sm font-bold text-slate-400 mb-4">Price Trend Analysis</h3>
            <div className="flex-1 w-full h-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={history}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
                  <YAxis stroke="#64748b" fontSize={11} />
                  <Tooltip
                    contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", color: "#f8fafc" }}
                  />
                  <Line type="monotone" dataKey="Price" stroke="#6366f1" strokeWidth={3} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;