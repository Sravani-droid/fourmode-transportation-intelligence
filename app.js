let masterData;
let primaryChart;
let secondaryChart;

fetch("transportation_master.json")
.then(res => res.json())
.then(data => {
  masterData = data;
  const page = document.body.dataset.page || "overview";
if(page === "overview") loadOverview();

if(page === "road") loadRoad();

if(page === "air") loadAir();

if(page === "rail") loadRail();

if(page === "maritime") loadMaritime();
});

function setText(id, value){
  const el = document.getElementById(id);
  if(el) el.innerText = value;
}

function setKPIs(items){
  document.getElementById("kpiGrid").innerHTML = items.map(item => `
    <div class="glass-card">
      <h3>${item.label}</h3>
      <h2>${item.value}</h2>
    </div>
  `).join("");
}

function setInsights(items){
  document.getElementById("insightList").innerHTML =
    items.map(i => `<li>${i}</li>`).join("");
}

function clearCharts(){
  if(primaryChart) primaryChart.destroy();
  if(secondaryChart) secondaryChart.destroy();
}

function colors(){
  return [
    "rgba(0,212,255,.80)",
    "rgba(96,165,250,.80)",
    "rgba(110,231,183,.80)",
    "rgba(168,85,247,.80)",
    "rgba(251,191,36,.80)",
    "rgba(239,68,68,.80)",
    "rgba(45,212,191,.80)",
    "rgba(244,114,182,.80)"
  ];
}

function borders(){
  return [
    "#67e8f9",
    "#93c5fd",
    "#6ee7b7",
    "#c4b5fd",
    "#fde68a",
    "#fca5a5",
    "#5eead4",
    "#f9a8d4"
  ];
}

function chartOptions(horizontal=false){
  return {
    indexAxis: horizontal ? "y" : "x",
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: "#ffffff",
          font: { size: 13, weight: "bold" }
        }
      }
    },
    scales: {
      x: {
        ticks: { color: "#ffffff", font: { size: 12, weight: "bold" } },
        grid: { color: "rgba(255,255,255,.10)" }
      },
      y: {
        ticks: { color: "#ffffff", font: { size: 12, weight: "bold" } },
        grid: { color: "rgba(255,255,255,.10)" }
      }
    }
  };
}

function doughnutOptions(){
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: "#ffffff",
          font: { size: 13, weight: "bold" }
        }
      }
    }
  };
}

function makeBarChart(id, labels, values, label, horizontal=false){
  return new Chart(document.getElementById(id), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label,
        data: values,
        backgroundColor: colors(),
        borderColor: borders(),
        borderWidth: 2,
        borderRadius: 14
      }]
    },
    options: chartOptions(horizontal)
  });
}

function makeDoughnutChart(id, labels, values){
  return new Chart(document.getElementById(id), {
    type: "doughnut",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors(),
        borderColor: "#ffffff",
        borderWidth: 2
      }]
    },
    options: doughnutOptions()
  });
}

function loadRoad(){
  clearCharts();

  setText("pageTitle", "Road Logistics Intelligence");
  setText("pageSubtitle", "Revenue, Routes, Idle Capacity & Carrier Optimization");
  setText("pageDescription", "Executive road transportation analytics covering revenue generation, fleet utilization, carrier performance, route optimization, and operational efficiency.");

  setKPIs([
    {label:"Total Revenue", value:"$298.6M"},
    {label:"Loads Moved", value:"85,410"},
    {label:"Idle Hours", value:"598,791"},
    {label:"Revenue / Mile", value:"$2.47"}
  ]);

  setText("primaryChartTitle", "Top Carrier Analysis");
  setText("primaryChartNote", "Carrier shipment performance comparison across major logistics providers.");
  setText("secondaryChartTitle", "Route Revenue Analysis");
  setText("secondaryChartNote", "Highest performing freight corridors by modeled revenue.");

  const carriers = masterData.road.carriers.highest_volume_carriers;
  primaryChart = makeBarChart(
    "primaryChart",
    carriers.map(x => x.carrier),
    carriers.map(x => x.shipments),
    "Shipments"
  );

  const routes = masterData.road.routes.top_revenue_routes.slice(0, 6);
  secondaryChart = makeBarChart(
    "secondaryChart",
    routes.map(x => `${x.origin_city} to ${x.destination_city}`),
    routes.map(x => +(x.total_revenue / 1_000_000).toFixed(1)),
    "Revenue ($M)",
    true
  );

  setInsights([
    "$298.6M total modeled transportation revenue.",
    "598,791 idle hours identified across operations.",
    "Top carriers maintain strong shipment consistency.",
    "Revenue concentration exists on a small number of high-performing corridors.",
    "Operational efficiency improvements remain the largest savings opportunity."
  ]);

  setText("aiRecommendation",
    "Road transportation remains the strongest regional delivery network within FourMode. Current analysis indicates excess idle capacity is the largest optimization opportunity. Reducing idle time by only 10% could recover nearly 60,000 productive operating hours. Carrier benchmarking suggests lower performing routes should be prioritized first."
  );
  setText("impactTitle", "Potential Savings Opportunity");
  setText("impactValue", "$5.2M");
}

function loadAir(){
  clearCharts();

  setText("pageTitle", "Air Cargo & Passenger Intelligence");
  setText("pageSubtitle", "Passenger Demand, Cargo Movement & Airline Concentration");
  setText("pageDescription", "Aviation analytics covering passenger demand, air cargo movement, airline concentration, and regional traffic patterns.");

  setKPIs([
    {label:"Passengers", value:"667.9M"},
    {label:"Cargo Tons", value:"7.36M"},
    {label:"Top Airline", value:"United"},
    {label:"Top Region", value:"Asia"}
  ]);

  setText("primaryChartTitle", "Top Cargo Airlines");
  setText("primaryChartNote", "Airline cargo leaders by total metric tons.");
  setText("secondaryChartTitle", "Cargo Distribution by Region");
  setText("secondaryChartNote", "Regional concentration of modeled air cargo movement.");

  primaryChart = makeBarChart(
    "primaryChart",
    masterData.air.top_airlines.slice(0, 7).map(x => x.operating_airline),
    masterData.air.top_airlines.slice(0, 7).map(x => Math.round(x.cargo_metric_tons)),
    "Cargo Metric Tons"
  );

  secondaryChart = makeDoughnutChart(
    "secondaryChart",
    masterData.air.regions.map(x => x.geo_region),
    masterData.air.regions.map(x => Math.round(x.cargo_metric_tons))
  );

  setInsights([
    "667.9M passengers modeled across airline activity.",
    "7.36M cargo metric tons analyzed.",
    "United Airlines leads both cargo and passenger volume.",
    "Asia and US dominate cargo movement.",
    "Air is best suited for urgent, high-value, time-sensitive shipments."
  ]);

  setText("aiRecommendation",
    "Air transportation provides the strongest speed advantage but should be reserved for urgent or high-value shipments. The data shows heavy concentration among a few major airlines and regions, meaning capacity risk should be monitored closely for Asia and US corridors."
  );
  setText("impactTitle", "Best Use Case");
  setText("impactValue", "Urgent Cargo");
}

function loadRail(){
  clearCharts();

  setText("pageTitle", "Rail Freight Growth Intelligence");
  setText("pageSubtitle", "Freight Volume, Ton-Miles & Long-Range Forecasting");
  setText("pageDescription", "Rail analytics focused on long-haul freight growth, bulk movement, capacity planning, and demand forecasting.");

  setKPIs([
    {label:"2015 Freight", value:"18.1M tons"},
    {label:"2045 Forecast", value:"26.9M tons"},
    {label:"Projected Growth", value:"+48.9%"},
    {label:"Best Use", value:"Bulk Freight"}
  ]);

  setText("primaryChartTitle", "Rail Growth Forecast");
  setText("primaryChartNote", "Projected rail freight growth from 2015 baseline to 2045 forecast.");
  setText("secondaryChartTitle", "Top Rail Origins");
  setText("secondaryChartNote", "Highest origin states by modeled freight tons.");

  primaryChart = makeBarChart(
    "primaryChart",
    ["2015 Tons", "2045 Projected Tons"],
    [masterData.rail.kpis.total_tons_2015, masterData.rail.kpis.total_tons_2045],
    "Tons"
  );

  secondaryChart = makeBarChart(
    "secondaryChart",
    masterData.rail.top_origins.slice(0, 8).map(x => "State " + x.dms_orig),
    masterData.rail.top_origins.slice(0, 8).map(x => Math.round(x.tons_2015)),
    "Tons"
  );

  setInsights([
    "18.1M rail freight tons modeled in 2015 baseline.",
    "26.9M tons projected by 2045.",
    "Rail is strongest for heavy, lower-urgency freight.",
    "Projected growth indicates rising long-haul capacity demand.",
    "Best suited for bulk commodities and interregional freight."
  ]);

  setText("aiRecommendation",
    "Rail should be prioritized for long-distance, heavy, lower-urgency freight. The projected growth from 2015 to 2045 indicates rail will remain critical for bulk movement and capacity planning."
  );
  setText("impactTitle", "Strategic Advantage");
  setText("impactValue", "Low-Cost Scale");
}

function loadMaritime(){
  clearCharts();

  setText("pageTitle", "Maritime Port & Trade Intelligence");
  setText("pageSubtitle", "Port Calls, Global Trade Flow & Cargo Mix");
  setText("pageDescription", "Maritime intelligence covering port activity, import-export flow, cargo composition, and international trade throughput.");

  setKPIs([
    {label:"Total Trade", value:"$60.8B"},
    {label:"Port Calls", value:"9.3M"},
    {label:"Top Port", value:"Singapore"},
    {label:"Top Cargo", value:"Dry Bulk"}
  ]);

  setText("primaryChartTitle", "Cargo Mix");
  setText("primaryChartNote", "Cargo composition across container, dry bulk, general cargo, RoRo, and tanker freight.");
  setText("secondaryChartTitle", "Top Ports by Activity");
  setText("secondaryChartNote", "Global ports ranked by total port calls.");

  const cargo = masterData.maritime.cargo_mix[0];

  primaryChart = makeDoughnutChart(
    "primaryChart",
    ["Container", "Dry Bulk", "General Cargo", "RoRo", "Tanker"],
    [cargo.container, cargo.dry_bulk, cargo.general_cargo, cargo.roro, cargo.tanker]
  );

  secondaryChart = makeBarChart(
    "secondaryChart",
    masterData.maritime.top_ports.slice(0, 8).map(x => x.portname),
    masterData.maritime.top_ports.slice(0, 8).map(x => x.portcalls),
    "Port Calls"
  );

  setInsights([
    "$60.8B total maritime trade activity modeled.",
    "9.3M port calls analyzed.",
    "Singapore leads global port activity.",
    "Dry bulk and tanker cargo dominate trade volume.",
    "Maritime is best for massive-volume, low-urgency global shipments."
  ]);

  setText("aiRecommendation",
    "Maritime should be used for large-volume, low-urgency global shipments. Port activity is highly concentrated around major trade hubs, so risk monitoring should focus on congestion, port delays, and cargo-type dependency."
  );
  setText("impactTitle", "Strategic Advantage");
  setText("impactValue", "Global Scale");
}
function loadOverview(){

  clearCharts();

  const overviewChart = document.getElementById("overviewChart");

  if(overviewChart){

    primaryChart = new Chart(overviewChart,{

      type:"bar",

      data:{

        labels:[
          "Road",
          "Air",
          "Rail",
          "Maritime"
        ],

        datasets:[{

          label:"Transportation Scale",

          data:[
            298.6,
            7.36,
            26.9,
            60.8
          ],

          backgroundColor:[
            "#38bdf8",
            "#60a5fa",
            "#6ee7b7",
            "#a855f7"
          ],

          borderColor:[
            "#7dd3fc",
            "#93c5fd",
            "#86efac",
            "#c084fc"
          ],

          borderWidth:2,
          borderRadius:12
        }]
      },

      options:{
        responsive:true,
        maintainAspectRatio:false,

        plugins:{
          legend:{
            labels:{
              color:"#ffffff",
              font:{
                size:14,
                weight:"bold"
              }
            }
          }
        },

        scales:{

          x:{
            ticks:{
              color:"#ffffff",
              font:{
                size:12,
                weight:"bold"
              }
            },

            grid:{
              color:"rgba(255,255,255,.08)"
            }
          },

          y:{
            ticks:{
              color:"#ffffff",
              font:{
                size:12,
                weight:"bold"
              }
            },

            grid:{
              color:"rgba(255,255,255,.08)"
            }
          }
        }
      }
    });
  }
}