import Highcharts from "highcharts";
import { HighchartsReact } from "highcharts-react-official";

export default function PriceVolumeChart({ prices, ticker }) {
  if (!prices || prices.length === 0) return null;

  const sortedPrices = [...prices].sort(
    (a, b) => new Date(a.date) - new Date(b.date)
  );

  const closePrices = sortedPrices.map((p) => [
    new Date(p.date).getTime(),
    Number(p.price || p.close),
  ]);

  const volumes = sortedPrices.map((p) => [
    new Date(p.date).getTime(),
    Number(p.volume),
  ]);

  const priceOptions = {
    title: { text: `${ticker} Close Price` },
    xAxis: { type: "datetime" },
    yAxis: { title: { text: "Price" } },
    tooltip: { shared: true },
    series: [
      {
        name: "Close Price",
        type: "line",
        data: closePrices,
      },
    ],
  };

  const volumeOptions = {
    title: { text: `${ticker} Volume` },
    xAxis: { type: "datetime" },
    yAxis: { title: { text: "Volume" } },
    tooltip: { shared: true },
    series: [
      {
        name: "Volume",
        type: "column",
        data: volumes,
      },
    ],
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <div style={{ marginBottom: "2rem" }}>
        <HighchartsReact highcharts={Highcharts} options={priceOptions} />
      </div>

      <div>
        <HighchartsReact highcharts={Highcharts} options={volumeOptions} />
      </div>
    </div>
  );
}