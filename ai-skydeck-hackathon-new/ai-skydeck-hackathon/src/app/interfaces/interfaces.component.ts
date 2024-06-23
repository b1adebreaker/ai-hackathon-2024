import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface CompanyList {
  good_companies: string[];
  bad_companies: string[];
}

export interface CompanyData {
[year: number]: {
  report: string;
  video: string;
  scope_1: number;
  scope_2: number;
  scope_3: number;
  report_sentiment: number;
  video_sentiment: string;
}
}

// export interface CompanyYearData {
//   report: string;
//   video: string;
//   scope_1: number;
//   scope_2: number;
//   scope_3: number;
//   report_sentiment: number;
//   video_sentiment: number;
// }

@Component({
  selector: 'app-interfaces',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './interfaces.component.html',
  styleUrl: './interfaces.component.css'
})

export class InterfacesComponent {

}
