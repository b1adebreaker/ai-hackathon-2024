import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CanvasJSAngularChartsModule } from '@canvasjs/angular-charts';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-bad-emissions-graph',
  standalone: true,
  imports: [RouterModule, 
            CommonModule,
            CanvasJSAngularChartsModule],
  templateUrl: './bad-emissions-graph.component.html',
  styleUrl: './bad-emissions-graph.component.css'
})
export class BadEmissionsGraphComponent {

  chart: any;

  chartOptions = {
  animationEnabled: true,
  theme: "light2",
  title:{
    text: "Carbon Emissions and Sentiment"
  },
  axisY: {
    title: "Sentiment Score",
    includeZero: true
  },
  axisY2: {
    title: "Total Carbon Emissions",
    includeZero: true,
    labelFormatter: (e:any) => {
      var suffixes = ["", "K", "M", "B"];

      var order = Math.max(Math.floor(Math.log(e.value) / Math.log(1000)), 0);
      if(order > suffixes.length - 1)
      order = suffixes.length - 1;

      var suffix = suffixes[order];
      return (e.value / Math.pow(1000, order)) + suffix + " tCo2e";
    }
  },
  toolTip: {
    shared: true
  },
  legend: {
    cursor: "pointer",
    itemclick: function (e: any) {
      if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
      } else {
        e.dataSeries.visible = true;
      } 
      e.chart.render();
    }
  },
  data: [{ //import from good 
    type: "column",
    showInLegend: true,
    name: "Carbon Emissions",
    axisYType: "secondary",
    dataPoints: [
      { label: "2005", y: 420000000 },
      { label: "2006", y: 964600000 },
      { label: "2007", y: 962900000 }

    ]
    },{
    type: "spline",
    showInLegend: true,
    name: "Sentiment Score",
    dataPoints: [
      { label: "2005", y: 52 },
      { label: "2006", y: 68 },
      { label: "2007", y: 60 }
    ]
  }]
  }
}
