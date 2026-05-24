import { useState } from "react";

const API_URL = "https://pnclgqyuw1.execute-api.us-east-1.amazonaws.com";

export default function App() {
  const [ticker, setTicker] = useState("AAPL");
  const [prices, setPrices] = useState([]);
  const [message, setMessage] = useState("");

  async function collectPrices() {
    setMessage("Collecting prices...");

    const res = await fetch(`${API_URL}/prices/collect`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ticker }),
    });

    const data = await res.json();
    setMessage(data.message || "Done");
  }

  async function getPrices() {
    setMessage("Loading prices...");

    const res = await fetch(`${API_URL}/prices?ticker=${ticker}`);
    const data = await res.json();

    setPrices(data.prices || []);
    setMessage(`Loaded ${data.count} prices`);
  }

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Portfolio Risk Dashboard</h1>

      <input
        value={ticker}
        onChange={(e) => setTicker(e.target.value.toUpperCase())}
        placeholder="Ticker"
      />

      <button onClick={collectPrices}>Collect Prices</button>
      <button onClick={getPrices}>Get Prices</button>

      <p>{message}</p>

      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Date</th>
            <th>Open</th>
            <th>High</th>
            <th>Low</th>
            <th>Close / Price</th>
            <th>Volume</th>
          </tr>
        </thead>

        <tbody>
          {prices.map((price) => (
            <tr key={`${price.ticker}-${price.date}`}>
              <td>{price.date}</td>
              <td>{price.open}</td>
              <td>{price.high}</td>
              <td>{price.low}</td>
              <td>{price.price || price.close}</td>
              <td>{price.volume}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}