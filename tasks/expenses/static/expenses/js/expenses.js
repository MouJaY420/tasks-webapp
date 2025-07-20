// Device detection logic
function isMobileDevice() {
  return /Mobi|Android|iPhone|iPad|iPod|Windows Phone/i.test(navigator.userAgent);
}

const householdId = "{{ household.pk }}";
const socket = new WebSocket(
    `ws://${window.location.host}/ws/receipt/${householdId}/`
);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // For now, just reload:
    location.reload();
};

document.addEventListener("DOMContentLoaded", function () {
  const mobileUpload = document.getElementById("mobile-upload");
  const desktopQR = document.getElementById("desktop-qr");

  if (mobileUpload && desktopQR) {
    if (isMobileDevice()) {
      mobileUpload.classList.remove("d-none");
    } else {
      desktopQR.classList.remove("d-none");
    }
  }
});

  // Toggle chart button (optional if reused in both views)
const toggleBtn = document.getElementById("toggleChartBtn");
const collapseEl = document.getElementById("expenseChartContainer");

if (toggleBtn && collapseEl) {
    collapseEl.addEventListener("show.bs.collapse", () => {
        toggleBtn.textContent = "Hide Monthly Chart";
    });

    collapseEl.addEventListener("hide.bs.collapse", () => {
        toggleBtn.textContent = "Show Monthly Chart";
    });
}

  // If you're rendering a chart
if (typeof Chart !== "undefined" && typeof chart_labels !== "undefined" && typeof chart_data !== "undefined") {
    new Chart(document.getElementById("monthlyChart"), {
        type: "bar",
        data: {
            labels: chart_labels,
            datasets: [{
                label: chart_label || "Expenses",
                data: chart_data
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
};


