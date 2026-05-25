import { useState } from "react";
import PriceVolumeChart from "../components/PriceVolumeChart";
import CompanyOverviewCard from "../components/CompanyOverviewCard";

const API_URL = "https://pnclgqyuw1.execute-api.us-east-1.amazonaws.com";

export default function PricesPage() {
    const [ticker, setTicker] = useState("AAPL");
    const [prices, setPrices] = useState([]);
    const [message, setMessage] = useState("");
    const [overview, setOverview] = useState(null);

    async function collectPrices() {
        setMessage("Collecting prices...");

        const res = await fetch(`${API_URL}/prices/collect`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ticker }),
        });

        const data = await res.json();
        setMessage(data.message || "Done");
    }

    async function getPrices() {
        setMessage("Loading prices and company overview...");

        const [pricesRes, overviewRes] = await Promise.all([
            fetch(`${API_URL}/prices?ticker=${ticker}`),
            fetch(`${API_URL}/company/overview?ticker=${ticker}`),
        ]);

        const pricesData = await pricesRes.json();
        const overviewData = await overviewRes.json();

        setPrices(pricesData.prices || []);
        setOverview(overviewData);

        setMessage(`Loaded ${pricesData.count || 0} prices for ${ticker}`);
    }

    return (
        <>
            <h1>Stock Prices</h1>

            <input
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                placeholder="Ticker"
            />

            <button onClick={collectPrices}>Collect Prices</button>
            <button onClick={getPrices}>Get Prices</button>

            <p>{message}</p>
            <CompanyOverviewCard overview={overview} />
            <PriceVolumeChart prices={prices} ticker={ticker} />
        </>
    );
}