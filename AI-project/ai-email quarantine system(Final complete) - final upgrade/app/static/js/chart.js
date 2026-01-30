document.addEventListener("DOMContentLoaded", function () {

  // Read mail statistics injected as JSON in the template.
  const mailStatsScript = document.getElementById("mail-stats");
  const mailStats = mailStatsScript
    ? JSON.parse(mailStatsScript.textContent)
    : { safe: 0, suspicious: 0, quarantined: 0 };

  // Common options for both charts (IMPORTANT)
  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false, 
    plugins: {
      legend: {position: "bottom"},
      tooltip: {enabled: true}
    }
  };

  // SPIKE CHART 
  const lineCanvas = document.getElementById("lineChart");
  if (lineCanvas) {
    new Chart(lineCanvas, {
      type: "line",
      data: {
        labels: ["Scan 1", "Scan 2", "Scan 3", "Scan 4", "Scan 5"],
        datasets: [{
          label: "Emails Detected",
          data: [
            mailStats.safe + 1,
            mailStats.safe - 2,
            mailStats.safe + mailStats.suspicious,
            mailStats.safe - 1,
            mailStats.safe
          ],
          borderColor: "#2563eb",
          backgroundColor: "rgba(37, 99, 235, 0.15)",
          fill: true,
          tension: 0.4,
          pointRadius: 4
        }]
      },
      options: {
        ...commonOptions,
        plugins: { legend: { display: false } },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { precision: 0 }
          }
        }
      }
    });
  }

  //  PIE CHART 
  const pieCanvas = document.getElementById("pieChart");
if (pieCanvas) {
  new Chart(pieCanvas, {
    type: "pie",
    data: {
      labels: ["Safe", "Suspicious", "Quarantined"],
      datasets: [{
        data: [
          mailStats.safe,
          mailStats.suspicious,
          mailStats.quarantined
        ],
        backgroundColor: ["#10b981", "#f59e0b", "#ef4444"],
        borderWidth: 1
      }]
    },
    options: {
      ...commonOptions,
      layout: {
        padding: 10
      }
    }
  });
}


  //  BAR CHART 
  const barCanvas = document.getElementById("barChart");
  if (barCanvas) {
    new Chart(barCanvas, {
      type: "bar",
      data: {
        labels: ["Safe", "Suspicious", "Quarantined"],
        datasets: [{
          label: "Email Count",
          data: [
            mailStats.safe,
            mailStats.suspicious,
            mailStats.quarantined
          ],
          backgroundColor: ["#10b981", "#f59e0b", "#ef4444"],
          borderRadius: 6
        }]
      },
      options: {
        ...commonOptions,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0
            }
          }
        }
      }
    });
  }

});


