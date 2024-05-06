function plotData(plotId, data, xLabel, yLabel) {
  // Define axis attributes.
  const xtickVals = Array.from({length: data[0]["x"].length}, (_, i) => i * 4);
  const xaxis = {
    tickmode: 'array',
    tickvals: xtickVals,
    ticktext: data[0]["x"],
    tickangle: -45,
    range: [0.85, data[0]["x"].length+0.15],  // "0.85"/"0.15" are left/right padding on x-axis.
    title: xLabel,
    tickfont: {
      size: 18
    }
  };
  const yaxis = {
    title: yLabel,
    tickfont: {
      size: 18
    }
  }

  // Convert x-axis values to numeric for plotting instead of patch version strings.
  for (var i = 0; i < data.length; i++) {
    data[i]["x"] = xtickVals;
  }

  // Define plot configuration.
  const layout = {
    xaxis: xaxis,
    yaxis: yaxis,
    title: yaxis.title + " vs. " + xaxis.title,
    showlegend: true,
    font: {
      family: 'Lora',
      size: 18 // 30
    }
  };

  // Plot the data.
  Plotly.newPlot(plotId, data, layout);
}

function convertPatchVersionFormat(patches) {
  for (var i = 0; i < patches.length; i++) {
    patches[i] = patches[i].replace("_", ".");
  }
  return patches;
}

const championColors = {};

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * letters.length)];
  }
  
  return color;
}

function updateWinRatesPlot() {
  let x = patchesDATA;
  const y = winRatesDATA;

  // Clean patch versions to have decimals instead of underscores.
  x = convertPatchVersionFormat(x);

  // Create data dictionary for each selected champion.
  const data = [];
  const champions = document.getElementById("winRatesChampions").options;
  for (var i = 0; i < champions.length; i++) {
    if (champions[i].selected) {

      if (!(champions[i].value in championColors)) {
        championColors[champions[i].value] = getRandomColor();
      }

      // Set marker color to red if not data for that patch (i.e., -1).
      colors = []
      for (var j = 0; j < y[champions[i].value].length; j++) {
        if (y[champions[i].value][j] == "-1") {
          colors.push("red");
        } else {
          colors.push(championColors[champions[i].value]);
        }
      }

      data.push({
        x: x,
        y: y[champions[i].value],
        name: champions[i].value,
        mode: 'lines+markers',
        marker: {
          size: 8,
          color: colors
        },
        line: {
          color: championColors[champions[i].value]
        }
      });
    }
  }

  const xLabel = "Patch Version";
  const yLabel = "Win Rates";

  plotData("winRatesPlot", data, xLabel, yLabel);
}

function updateNerfsBuffsPlot() {
  let x = patchesDATA;
  const y = nerfsBuffsDATA;

  // Clean patch versions to have decimals instead of underscores.
  x = convertPatchVersionFormat(x);

  // Create data dictionary for each selected champion.
  const data = [];
  const champions = document.getElementById("nerfsBuffsChampions").options;
  for (var i = 0; i < champions.length; i++) {
    if (champions[i].selected) {

      if (!(champions[i].value in championColors)) {
        championColors[champions[i].value] = getRandomColor();
      }

      // Set marker color to red if not data for that patch (i.e., -1).
      colors = []
      for (var j = 0; j < y[champions[i].value].length; j++) {
        if (y[champions[i].value][j] == "-1") {
          colors.push("red");
        } else {
          colors.push(championColors[champions[i].value]);
        }
      }
      
      data.push({
        x: x,
        y: y[champions[i].value],
        name: champions[i].value,
        mode: "scatter",
        mode: 'lines+markers',
        marker: {
          size: 8,
          color: colors
        },
        line: {
          color: championColors[champions[i].value]
        }
      });
    }
  }

  const xLabel = "Patch Version";
  const yLabel = "Nerfs / Buffs Score";

  plotData("nerfsBuffsPlot", data, xLabel, yLabel);
}

function initChampions() {
  // TODO: Get champions from endpoint instead of hardcoded.

  const containers = document.getElementsByClassName("champions");
  for (var i = 0; i < containers.length; i++) {
    let options = ``;
    for (var j = 0; j < championsDATA.length; j++) {
      var selected = j == 0 ? "selected" : "";
      options += `<option value="`+ championsDATA[j] +`" `+ selected +`>`+ championsDATA[j] +`</option>`;
    }
    containers[i].innerHTML = options;
  }
}